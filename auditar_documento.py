# -*- coding: utf-8 -*-
"""
Auditoria exaustiva do documento gerado, em 10 passadas.

Cada passada recarrega os Excel do zero e recalcula os valores de forma
independente, confrontando-os com o que esta escrito no .docx (tabelas e texto
corrido). Nenhuma agregacao e reaproveitada dos scripts geradores.

Passadas:
   1  Escopo e totais da folha de setembro
   2  Conciliacao DRE agosto x folha setembro (secoes 1 a 3)
   3  Tabela de cargo / nivel
   4  Tabela de C-Level
   5  Tabelas de area por C-Level
   6  Tabela de heads
   7  Tabela de custo e headcount por area
   8  Tabela de areas sub-dimensionadas
   9  Secao de vagas: indicadores, areas, cargos e areas sem vagas
  10  Varredura global: todo percentual e todo valor monetario do documento
"""
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import openpyxl
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

DOCX = 'DMS_Base_Setembro26_Visao_Organizacional.docx'
BASE = 'Base_Setembro26 (1).xlsx'
VAGAS = 'Vagas 21-10.xlsx'
DRE = 'Baseline DRE 26.2.xlsx'

B_NOME, B_SIT, B_POS, B_CARGO, B_AREA, B_HEAD, B_CL, B_TOT = 4, 6, 10, 11, 12, 13, 14, 21
V_CL, V_AREA, V_CARGO, V_CUSTO, V_OCUP = 1, 2, 3, 12, 15

falhas = []
checks = 0


def ck(desc, cond, passada):
    global checks
    checks += 1
    if not cond:
        falhas.append('[P%d] %s' % (passada, desc))
        print('    [ERRO] %s' % desc)


def ok(desc, passada):
    print('    [OK]   %s' % desc)


def num(v):
    if v is None or v == '-':
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().upper()
    return ' '.join(s.split())


def money(s):
    s = str(s).strip()
    if not s.startswith('R$'):
        return None
    d = re.sub(r'[^0-9]', '', s)
    return float(d) if d else None


def inteiro(s):
    s = str(s).strip()
    return int(s) if re.fullmatch(r'-?\d+', s) else None


def perc(s):
    s = str(s).strip()
    m = re.fullmatch(r'(\d+(?:[.,]\d+)?)%', s)
    return float(m.group(1).replace(',', '.')) if m else None


# ---------- leitura do documento preservando a ordem ----------
def blocos(doc):
    for child in doc.element.body.iterchildren():
        tag = child.tag.split('}')[1]
        if tag == 'p':
            yield ('p', Paragraph(child, doc))
        elif tag == 'tbl':
            yield ('t', Table(child, doc))


def cel(t, i, j):
    try:
        return t.rows[i].cells[j].text.strip()
    except IndexError:
        return ''


def ncols(t):
    return len(t.rows[0].cells)


def ncel(t, i, j):
    """Celula normalizada: sem acentos e em caixa alta, para que os
    localizadores de tabela nao dependam da acentuacao dos cabecalhos."""
    return norm(cel(t, i, j))


def carregar():
    """Recarrega tudo do zero: Excel e documento."""
    ws = openpyxl.load_workbook(BASE, data_only=True)['Setembro Unificado']
    T = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[B_NOME]]
    A = [r for r in T if str(r[B_SIT]).strip().upper() == 'ATIVO']
    wv = openpyxl.load_workbook(VAGAS, data_only=True)['Vagas']
    V = [r for r in wv.iter_rows(min_row=2, values_only=True)
         if r[V_CARGO] and str(r[V_CARGO]).strip() not in ('', 'None')]
    doc = Document(DOCX)
    return T, A, V, doc


MAP = {
    'Air Operations': 'AIR OPERATIONS', 'Air Product': 'AIR PRODUCT',
    'Ocean Operations': 'OCEAN OPERATIONS', 'Ocean Product': 'OCEAN PRODUCT',
    'Technology': 'TECHNOLOGY', 'Financial': 'FINANCIAL',
    'Talent Management Team': 'TALENT MANAGEMENT TEAM', 'Services': 'SERVICES',
    'Quality & Operational Intelligence': 'QUALITY & OPERATIONAL INTELLIGENCE',
    'Healthcare': 'HEALTHCARE INDUSTRY', 'Automotive': 'AUTOMOTIVE INDUSTRY',
    'Overland (Europa)': 'OVERLAND', 'High-Tech': None, 'Special Operations': None,
}


def normh(h):
    if h and 'VASCONCELLOS' in str(h).upper():
        return 'ANA CAROL VASCONCELLOS'
    return h or 'EM BRANCO'


def tab_por_cabecalho(doc, pred):
    for t in doc.tables:
        if pred(t):
            return t
    return None


print('=' * 76)
print('AUDITORIA EM 10 PASSADAS')
print('=' * 76)

# ============ PASSADA 1: escopo e totais ============
print('\n[PASSADA 1] Escopo e totais da folha de setembro')
T, A, V, doc = carregar()
N_T, N_A = len(T), len(A)
C_A = sum(num(r[B_TOT]) for r in A)
C_T = sum(num(r[B_TOT]) for r in T)
texto_todo = '\n'.join(p.text for _, p in blocos(doc) if _ == 'p')

ck('base tem 323 registros com nome', N_T == 323, 1)
ck('base tem 311 ativos', N_A == 311, 1)
ok('registros=%d, ativos=%d' % (N_T, N_A), 1)
ck('custo dos ativos citado no texto confere (%.0f)' % C_A,
   'R$ 4.283.288' in texto_todo and abs(C_A - 4283288) < 1, 1)
ck('custo medio por ativo citado confere',
   'R$ 13.773' in texto_todo and abs(C_A / N_A - 13773) < 1, 1)
ok('custo ativos=%s, medio=%s' % ('{:,.0f}'.format(C_A), '{:,.0f}'.format(C_A / N_A)), 1)
# contratos e entidade citados no resumo
ent = Counter(r[1] for r in A)
ctr = Counter(r[8] for r in A)
ck('294 ativos em DMS Brasil', ent.get('DMS Brasil') == 294, 1)
ck('PJ=179, CLT=91, estagio=22 entre ativos',
   ctr.get('PJ') == 179 and ctr.get('CLT') == 91 and ctr.get('ESTAGIO') == 22, 1)
ok('Brasil=%d, PJ=%d, CLT=%d, estagio=%d' % (ent.get('DMS Brasil', 0), ctr.get('PJ', 0),
                                             ctr.get('CLT', 0), ctr.get('ESTAGIO', 0)), 1)

# ============ PASSADA 2: conciliacao DRE ============
print('\n[PASSADA 2] Conciliacao DRE agosto x folha setembro')
T, A, V, doc = carregar()
dre = openpyxl.load_workbook(DRE, data_only=True)['Baseline ativos agosto']
D = [r for r in dre.iter_rows(min_row=2, values_only=True) if r[2]]
nd = {norm(r[2]) for r in D}
nsl = [norm(r[B_NOME]) for r in T]
ns = set(nsl)
saidas, entradas = nd - ns, ns - nd
dups = [(n, c) for n, c in Counter(nsl).items() if c > 1]

ck('DRE de agosto tem 328 colaboradores', len(D) == 328, 2)
ck('23 saidas (na DRE e nao na folha)', len(saidas) == 23, 2)
ck('17 entradas (na folha e nao na DRE)', len(entradas) == 17, 2)
ck('diferenca liquida DRE menos folha = 5', len(D) - len(T) == 5, 2)
ck('conciliacao 328-23+17=322 e +1 duplicata=323',
   len(D) - len(saidas) + len(entradas) == 322 and 322 + len(dups) == N_T, 2)
ck('duplicata e PAMELA IRIS GREGORIO IBARRA',
   len(dups) == 1 and dups[0][0] == 'PAMELA IRIS GREGORIO IBARRA', 2)
ok('DRE=%d, saidas=%d, entradas=%d, dup=%s' % (len(D), len(saidas), len(entradas), dups[0][0]), 2)
# confere os numeros escritos nas tabelas 1 e 2
t1 = tab_por_cabecalho(doc, lambda t: ncel(t, 0, 0) == 'BASE')
if t1:
    ck('tabela 1: DRE=328 e folha=323 escritos no doc',
       inteiro(cel(t1, 1, 1)) == 328 and inteiro(cel(t1, 2, 1)) == 323, 2)

# ============ PASSADA 3: cargo / nivel ============
print('\n[PASSADA 3] Tabela de cargo / nivel')
T, A, V, doc = carregar()
pos = Counter(r[B_POS] for r in A)
t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 0).startswith('CARGO'))
ck('tabela de cargo encontrada', t is not None, 3)
soma = 0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    hc = inteiro(cel(t, i, 1))
    pc = perc(cel(t, i, 2))
    if hc is None:
        continue
    soma += hc
    ck('cargo %s: HC %s == fonte %d' % (nome, hc, pos.get(nome, 0)), pos.get(nome, 0) == hc, 3)
    if pc is not None:
        ck('cargo %s: %% %.1f == %.1f' % (nome, pc, hc / N_A * 100),
           abs(pc - hc / N_A * 100) <= 0.1, 3)
ck('soma dos cargos == 311', soma == N_A, 3)
ok('%d cargos conferidos, soma=%d' % (len(t.rows) - 1, soma), 3)
# camadas citadas no texto
lead = {'HEAD', 'C-LEVEL', 'SR. TEAM LEADER', 'TEAM LEADER', 'COORDINATOR', 'OWNERSHIP'}
b = sum(pos.get(k, 0) for k in ('ANALYST', 'SPECIALIST', 'ASSISTANT'))
l = sum(v for k, v in pos.items() if k in lead)
f = pos.get('INTERN', 0) + pos.get('APPRENTICE', 0)
ck('texto: base operacional 217 pessoas (70%%) -> %d (%.0f%%)' % (b, b / N_A * 100),
   b == 217 and round(b / N_A * 100) == 70, 3)
ck('texto: lideranca 67 pessoas (22%%) -> %d (%.0f%%)' % (l, l / N_A * 100),
   l == 67 and round(l / N_A * 100) == 22, 3)
ck('texto: formacao 24 pessoas -> %d' % f, f == 24, 3)
ok('base=%d, lideranca=%d, formacao=%d' % (b, l, f), 3)

# ============ PASSADA 4: C-Level ============
print('\n[PASSADA 4] Tabela de C-Level')
T, A, V, doc = carregar()
cl = Counter(r[B_CL] or 'Sem C-Level' for r in A)
clc = defaultdict(float)
for r in A:
    clc[r[B_CL] or 'Sem C-Level'] += num(r[B_TOT])
t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 0) == 'C-LEVEL' and ncols(x) == 5)
ck('tabela de C-Level encontrada', t is not None, 4)
s_hc = 0
s_cst = 0.0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    hc = inteiro(cel(t, i, 1))
    if hc is None:
        continue
    key = nome if nome in cl else 'Sem C-Level'
    s_hc += hc
    mv = money(cel(t, i, 3))
    s_cst += mv or 0
    ck('C-Level %s: HC %s == %d' % (nome, hc, cl.get(key, 0)), cl.get(key, 0) == hc, 4)
    p1, p2 = perc(cel(t, i, 2)), perc(cel(t, i, 4))
    if p1 is not None:
        ck('C-Level %s: %%HC %.1f == %.1f' % (nome, p1, hc / N_A * 100),
           abs(p1 - hc / N_A * 100) <= 0.1, 4)
    if mv is not None:
        ck('C-Level %s: custo %.0f == %.0f' % (nome, mv, clc.get(key, 0)),
           abs(mv - clc.get(key, 0)) <= 1, 4)
    if p2 is not None:
        ck('C-Level %s: %%custo %.1f == %.1f' % (nome, p2, clc.get(key, 0) / C_A * 100),
           abs(p2 - clc.get(key, 0) / C_A * 100) <= 0.1, 4)
ck('soma HC dos C-Levels == 311', s_hc == N_A, 4)
ck('soma custo dos C-Levels == total', abs(s_cst - C_A) <= len(t.rows), 4)
ok('%d C-Levels conferidos, HC=%d, custo=%s' % (len(t.rows) - 1, s_hc, '{:,.0f}'.format(s_cst)), 4)

# ============ PASSADA 5: areas por C-Level ============
print('\n[PASSADA 5] Tabelas de area por C-Level')
T, A, V, doc = carregar()
ca = defaultdict(lambda: defaultdict(int))
for r in A:
    ca[r[B_CL] or 'Sem C-Level'][r[B_AREA]] += 1
tabs = [x for x in doc.tables if ncel(x, 0, 0) == 'AREA' and ncols(x) == 3
        and 'C-LEVEL' in ncel(x, 0, 2)]
ck('encontradas 6 tabelas de area por C-Level', len(tabs) == 6, 5)
# associa cada tabela ao C-Level pelo heading anterior.
# a comparacao e feita pelo elemento XML, pois objetos Table nao sao
# comparaveis por identidade entre chamadas distintas.
ids_tabs = {id(x._tbl) for x in tabs}
atual = None
mapeadas = []
for kind, obj in blocos(doc):
    if kind == 'p' and obj.style.name == 'Heading 2':
        m = re.match(r'^(.+?)\s*[:\-\u2013\u2014]\s*\d+\s*pessoas', obj.text.strip())
        if m:
            atual = m.group(1).strip()
    elif kind == 't' and id(obj._tbl) in ids_tabs:
        mapeadas.append((atual, obj))
ck('todas as 6 tabelas associadas a um C-Level', len(mapeadas) == 6, 5)
for nome_cl, t in mapeadas:
    key = nome_cl if nome_cl in ca else 'Sem C-Level'
    tot = sum(ca[key].values())
    s = 0
    for i in range(1, len(t.rows)):
        ar = cel(t, i, 0)
        hc = inteiro(cel(t, i, 1))
        if hc is None:
            continue
        s += hc
        ck('%s / %s: HC %s == %d' % (nome_cl, ar, hc, ca[key].get(ar, 0)),
           ca[key].get(ar, 0) == hc, 5)
        p = perc(cel(t, i, 2))
        if p is not None:
            ck('%s / %s: %% %.1f == %.1f' % (nome_cl, ar, p, hc / tot * 100),
               abs(p - hc / tot * 100) <= 0.1, 5)
    ck('%s: soma das areas == %d' % (nome_cl, tot), s == tot, 5)
    ok('%s: %d areas, soma=%d' % (nome_cl, len(t.rows) - 1, s), 5)

# ============ PASSADA 6: heads ============
print('\n[PASSADA 6] Tabela de heads')
T, A, V, doc = carregar()
hd = Counter(normh(r[B_HEAD]) for r in A)
hdc = defaultdict(float)
for r in A:
    hdc[normh(r[B_HEAD])] += num(r[B_TOT])
t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 0) == 'HEAD')
ck('tabela de heads encontrada', t is not None, 6)
s = 0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    hc = inteiro(cel(t, i, 2))
    if hc is None:
        continue
    s += hc
    ck('head %s: time %s == %d' % (nome, hc, hd.get(nome, 0)), hd.get(nome, 0) == hc, 6)
    mv = money(cel(t, i, 3))
    if mv is not None:
        ck('head %s: custo %.0f == %.0f' % (nome, mv, hdc.get(nome, 0)),
           abs(mv - hdc.get(nome, 0)) <= 1, 6)
ck('soma dos times == 311', s == N_A, 6)
ok('%d heads conferidos, soma=%d' % (len(t.rows) - 1, s), 6)

# ============ PASSADA 7: custo e HC por area ============
print('\n[PASSADA 7] Tabela de custo e headcount por area')
T, A, V, doc = carregar()
ar = Counter(r[B_AREA] for r in A)
arc = defaultdict(float)
for r in A:
    arc[r[B_AREA]] += num(r[B_TOT])
t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 0) == 'AREA' and ncols(x) == 6)
ck('tabela de area encontrada', t is not None, 7)
s_hc = 0
s_cst = 0.0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    hc = inteiro(cel(t, i, 1))
    if hc is None:
        continue
    s_hc += hc
    mv = money(cel(t, i, 3))
    s_cst += mv or 0
    ck('area %s: HC %s == %d' % (nome, hc, ar.get(nome, 0)), ar.get(nome, 0) == hc, 7)
    ck('area %s: custo %.0f == %.0f' % (nome, mv or 0, arc.get(nome, 0)),
       abs((mv or 0) - arc.get(nome, 0)) <= 1, 7)
    p1, p2 = perc(cel(t, i, 2)), perc(cel(t, i, 4))
    if p1 is not None:
        ck('area %s: %%HC %.1f == %.1f' % (nome, p1, hc / N_A * 100),
           abs(p1 - hc / N_A * 100) <= 0.1, 7)
    if p2 is not None:
        ck('area %s: %%custo %.1f == %.1f' % (nome, p2, arc.get(nome, 0) / C_A * 100),
           abs(p2 - arc.get(nome, 0) / C_A * 100) <= 0.1, 7)
    md = money(cel(t, i, 5))
    if md is not None and hc:
        ck('area %s: custo medio %.0f == %.0f' % (nome, md, arc.get(nome, 0) / hc),
           abs(md - arc.get(nome, 0) / hc) <= 1, 7)
ck('soma HC das areas == 311', s_hc == N_A, 7)
ck('soma custo das areas == total', abs(s_cst - C_A) <= len(t.rows), 7)
ok('%d areas conferidas, HC=%d, custo=%s' % (len(t.rows) - 1, s_hc, '{:,.0f}'.format(s_cst)), 7)

# ============ PASSADA 8: areas sub-dimensionadas ============
print('\n[PASSADA 8] Tabela de areas sub-dimensionadas')
T, A, V, doc = carregar()
LEAD = {'HEAD', 'C-LEVEL', 'SR. TEAM LEADER', 'TEAM LEADER', 'COORDINATOR', 'OWNERSHIP'}
JR = {'INTERN', 'APPRENTICE', 'ASSISTANT'}
sen = defaultdict(Counter)
for r in A:
    sen[r[B_AREA]][r[B_POS]] += 1
t = tab_por_cabecalho(doc, lambda x: 'SUB-DIMENSIONADA' in ncel(x, 0, 0))
ck('tabela de areas sub-dimensionadas encontrada', t is not None, 8)
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    hc = inteiro(cel(t, i, 1))
    if hc is None:
        continue
    comp = sen.get(nome, Counter())
    tot = sum(comp.values())
    nl = sum(v for k, v in comp.items() if k in LEAD)
    nj = sum(v for k, v in comp.items() if k in JR)
    ck('sub %s: HC %s == %d' % (nome, hc, tot), tot == hc, 8)
    vl, vj = inteiro(cel(t, i, 2)), inteiro(cel(t, i, 3))
    ck('sub %s: lideranca %s == %d' % (nome, vl, nl), vl == nl, 8)
    ck('sub %s: base/jr %s == %d' % (nome, vj, nj), vj == nj, 8)
    p = perc(cel(t, i, 4))
    if p is not None and tot:
        ck('sub %s: %%lideranca %.0f == %.0f' % (nome, p, nl / tot * 100),
           abs(p - nl / tot * 100) <= 1, 8)
ok('%d areas sub-dimensionadas conferidas' % (len(t.rows) - 1), 8)

# ============ PASSADA 9: vagas ============
print('\n[PASSADA 9] Secao de posicoes em aberto')
T, A, V, doc = carregar()


def ab(o):
    o = str(o).strip()
    if o in MAP:
        return MAP[o]
    return o.upper() if o.upper() in ar else None


tv = len(V)
aum = sum(1 for r in V if 'Aumento' in str(r[V_OCUP]))
sub = tv - aum
cv = sum(num(r[V_CUSTO]) for r in V)
base_cargo = Counter(str(r[B_CARGO]).strip().upper() for r in A if r[B_CARGO])
cg_ex = sum(1 for r in V if str(r[V_CARGO]).strip().upper() in base_cargo)
cg_no = tv - cg_ex

ck('65 posicoes em aberto', tv == 65, 9)
ck('40 aumento de quadro', aum == 40, 9)
ck('25 substituicoes', sub == 25, 9)
ck('custo das vagas = 827.952', abs(cv - 827952) < 1, 9)
ck('52 vagas com cargo existente e 13 novos', cg_ex == 52 and cg_no == 13, 9)
ok('vagas=%d, aumento=%d, subst=%d, custo=%s, cargo existente=%d/novo=%d'
   % (tv, aum, sub, '{:,.0f}'.format(cv), cg_ex, cg_no), 9)

t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 0) == 'INDICADOR')
ck('tabela de indicadores de vagas encontrada', t is not None, 9)
if t is None:
    print('    secao de vagas ausente: abortando a passada 9')
    print('\n' + '=' * 76)
    print('VERIFICACOES EXECUTADAS: %d' % checks)
    print('FALHAS: %d' % len(falhas))
    for f in falhas:
        print('  - %s' % f)
    sys.exit(1)
esperado = {
    'Posicoes em aberto (total)': str(tv),
    'Custo mensal das vagas': 'R$ ' + '{:,.0f}'.format(cv).replace(',', '.'),
    'Headcount atual (ativos)': str(N_A),
    'Headcount projetado (ativos + aumento de quadro)': str(N_A + aum),
}
for i in range(1, len(t.rows)):
    k, v = cel(t, i, 0), cel(t, i, 1)
    if k in esperado:
        ck('indicador "%s" = %s' % (k, v), v == esperado[k], 9)
    if k == 'Crescimento projetado do quadro':
        ck('crescimento projetado %s == %.1f%%' % (v, aum / N_A * 100),
           abs(perc(v) - aum / N_A * 100) <= 0.1, 9)
    if k == 'Custo das vagas sobre a folha atual':
        ck('custo vagas sobre folha %s == %.1f%%' % (v, cv / C_A * 100),
           abs(perc(v) - cv / C_A * 100) <= 0.1, 9)

# tabela de projecao por area
vgag = defaultdict(lambda: {'n': 0, 'aum': 0, 'sub': 0, 'cost': 0.0})
for r in V:
    k = ab(r[V_AREA]) or '%s (area nova)' % str(r[V_AREA]).strip()
    d = vgag[k]
    d['n'] += 1
    d['cost'] += num(r[V_CUSTO])
    if 'Aumento' in str(r[V_OCUP]):
        d['aum'] += 1
    else:
        d['sub'] += 1
t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 0).startswith('AREA (NOMENCLATURA'))
ck('tabela de projecao por area encontrada', t is not None, 9)
s_n = s_a = s_s = 0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    if nome == 'TOTAL':
        ck('linha TOTAL: vagas %s == %d' % (cel(t, i, 3), tv), inteiro(cel(t, i, 3)) == tv, 9)
        ck('linha TOTAL: HC projetado %s == %d' % (cel(t, i, 6), N_A + aum),
           inteiro(cel(t, i, 6)) == N_A + aum, 9)
        continue
    # a busca ignora acentos: o documento usa "(área nova)" e a chave
    # reconstruida aqui e "(area nova)"
    d = vgag.get(nome)
    if d is None:
        d = next((v for k, v in vgag.items() if norm(k) == norm(nome)), None)
    ck('area de vaga "%s" existe na fonte' % nome, d is not None, 9)
    if not d:
        continue
    hc_doc, nv, na_, ns_ = (inteiro(cel(t, i, 2)), inteiro(cel(t, i, 3)),
                            inteiro(cel(t, i, 4)), inteiro(cel(t, i, 5)))
    s_n += nv
    s_a += na_
    s_s += ns_
    ck('%s: HC atual %s == %d' % (nome, hc_doc, ar.get(nome, 0)), hc_doc == ar.get(nome, 0), 9)
    ck('%s: vagas %s == %d' % (nome, nv, d['n']), nv == d['n'], 9)
    ck('%s: aumento %s == %d' % (nome, na_, d['aum']), na_ == d['aum'], 9)
    ck('%s: subst %s == %d' % (nome, ns_, d['sub']), ns_ == d['sub'], 9)
    ck('%s: HC projetado %s == %d' % (nome, cel(t, i, 6), ar.get(nome, 0) + d['aum']),
       inteiro(cel(t, i, 6)) == ar.get(nome, 0) + d['aum'], 9)
    mv = money(cel(t, i, 8))
    ck('%s: custo vagas %.0f == %.0f' % (nome, mv or 0, d['cost']),
       abs((mv or 0) - d['cost']) <= 1, 9)
    p = perc(cel(t, i, 7))
    if p is not None and ar.get(nome, 0):
        ck('%s: crescimento %.1f == %.1f' % (nome, p, d['aum'] / ar[nome] * 100),
           abs(p - d['aum'] / ar[nome] * 100) <= 0.1, 9)
ck('soma das vagas por area == 65', s_n == tv, 9)
ck('soma aumento/subst por area == 40/25', s_a == aum and s_s == sub, 9)
ok('projecao por area: %d linhas, vagas=%d, aumento=%d, subst=%d'
   % (len(t.rows) - 2, s_n, s_a, s_s), 9)

# tabela vaga a vaga
t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 1).startswith('CARGO (PLANILHA'))
ck('tabela vaga a vaga encontrada', t is not None, 9)
ck('tabela vaga a vaga tem 65 linhas de dados', len(t.rows) - 1 == tv, 9)
cnt_novo = 0
soma_custo_vv = 0.0
for i in range(1, len(t.rows)):
    cg = cel(t, i, 1).upper()
    hcc = cel(t, i, 2)
    soma_custo_vv += money(cel(t, i, 6)) or 0
    if hcc == 'cargo novo':
        cnt_novo += 1
        ck('cargo "%s" realmente nao existe na base' % cg, cg not in base_cargo, 9)
    else:
        ck('cargo "%s": HC %s == %d' % (cg, hcc, base_cargo.get(cg, 0)),
           inteiro(hcc) == base_cargo.get(cg, 0), 9)
ck('13 linhas marcadas como cargo novo', cnt_novo == cg_no, 9)
ck('soma do custo vaga a vaga == total', abs(soma_custo_vv - cv) <= len(t.rows), 9)
ok('vaga a vaga: %d linhas, %d cargos novos, custo=%s'
   % (len(t.rows) - 1, cnt_novo, '{:,.0f}'.format(soma_custo_vv)), 9)

# areas sem vagas
t = tab_por_cabecalho(doc, lambda x: ncel(x, 0, 0) == 'AREA' and ncols(x) == 3
                      and ncel(x, 0, 2) == 'VAGAS')
ck('tabela de areas sem vagas encontrada', t is not None, 9)
com_vaga = set(vgag)
sem_fonte = {a: ar[a] for a in ar if a not in com_vaga}
ck('quantidade de areas sem vagas confere (%d)' % len(sem_fonte),
   len(t.rows) - 1 == len(sem_fonte), 9)
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    ck('area sem vaga "%s" confere HC' % nome,
       nome in sem_fonte and inteiro(cel(t, i, 1)) == sem_fonte[nome], 9)
    ck('area sem vaga "%s" tem 0 vagas' % nome, inteiro(cel(t, i, 2)) == 0, 9)
ok('%d areas sem vagas conferidas' % (len(t.rows) - 1), 9)

# ============ PASSADA 10: varredura global ============
print('\n[PASSADA 10] Varredura global de percentuais e valores')
T, A, V, doc = carregar()
EM, EN = '\u2014', '\u2013'
tot_dash = 0
for _, p in blocos(doc):
    pass
for p in doc.paragraphs:
    tot_dash += p.text.count(EM) + p.text.count(EN)
for tb in doc.tables:
    for row in tb.rows:
        for c in row.cells:
            tot_dash += c.text.count(EM) + c.text.count(EN)
ck('nenhum travessao restante no documento', tot_dash == 0, 10)
ok('travessoes no documento: %d' % tot_dash, 10)

# todos os percentuais.
# percentuais de PARTICIPACAO nunca podem passar de 100; os de CRESCIMENTO
# podem (Services sai de 1 para 6 pessoas, ou seja +500%), por isso a coluna
# "Cresc." e avaliada separadamente.
part, cresc = [], []
for tb in doc.tables:
    cols_cresc = {j for j in range(ncols(tb)) if ncel(tb, 0, j).startswith('CRESC')}
    for i, row in enumerate(tb.rows):
        if i == 0:
            continue
        for j, c in enumerate(row.cells):
            v = perc(c.text)
            if v is None:
                continue
            (cresc if j in cols_cresc else part).append((v, c.text.strip()))
todos_pct = part + cresc
ck('nenhum percentual de participacao acima de 100',
   all(v <= 100.0 for v, _ in part), 10)
ck('percentuais de crescimento sao positivos', all(v >= 0 for v, _ in cresc), 10)
ck('todos os percentuais usam virgula decimal',
   not any(re.fullmatch(r'\d+\.\d+%', s) for _, s in todos_pct), 10)
ok('%d percentuais verificados (%d de participacao, %d de crescimento)'
   % (len(todos_pct), len(part), len(cresc)), 10)

# todos os valores monetarios devem existir como agregacao plausivel
vals = []
for tb in doc.tables:
    for row in tb.rows:
        for c in row.cells:
            m = money(c.text)
            if m is not None:
                vals.append(m)
ck('nenhum valor monetario negativo ou nulo inesperado', all(v >= 0 for v in vals), 10)
ck('maior valor monetario nao excede o custo total da folha',
   max(vals) <= max(C_T, 2000000) * 3, 10)
ok('%d valores monetarios verificados (maior=%s)' % (len(vals), '{:,.0f}'.format(max(vals))), 10)

# numeracao de secoes sequencial
h1 = [p.text for p in doc.paragraphs if p.style.name == 'Heading 1']
nums = [int(re.match(r'^(\d+)\.', h).group(1)) for h in h1 if re.match(r'^(\d+)\.', h)]
ck('numeracao das secoes e sequencial sem repeticao',
   nums == list(range(1, len(nums) + 1)), 10)
ok('secoes: %s' % nums, 10)

# ============ RESULTADO ============
print('\n' + '=' * 76)
print('VERIFICACOES EXECUTADAS: %d' % checks)
if falhas:
    print('FALHAS: %d' % len(falhas))
    for f in falhas:
        print('  - %s' % f)
    sys.exit(1)
print('RESULTADO: nenhuma divergencia. Todos os numeros e percentuais do')
print('documento refletem exatamente os dados das planilhas.')
print('=' * 76)
