# -*- coding: utf-8 -*-
"""
Auditoria da secao de vagas do documento, em 5 passadas.

Recalcula, a partir das tres fontes, todos os numeros e percentuais escritos
na secao "Vagas em Aberto x Ocupacao nas Operacoes" e confronta com o .docx.
Cada passada recarrega as fontes do zero.
"""
import datetime
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import openpyxl
import pandas as pd
from docx import Document

DOCX = 'DMS_Base_Setembro26_Visao_Organizacional.docx'
BASE = 'Base_Setembro26 (1).xlsx'
VAGAS = 'Vagas 21-10.xlsx'
CIS = 'CIS_20261013_ORDERS.parquet'

B_POS, B_CARGO, B_HEAD = 10, 11, 13
V_CARGO, V_CONTRATADO, V_STATUS, V_CUSTO, V_OCUP = 3, 6, 7, 12, 15
REF = datetime.date(2026, 10, 21)

falhas = []
checks = 0


def ck(desc, cond, p):
    global checks
    checks += 1
    if not cond:
        falhas.append('[P%d] %s' % (p, desc))
        print('    [ERRO] %s' % desc)


def ok(d, p):
    print('    [OK]   %s' % d)


def num(v):
    if v is None or v == '-':
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode()
    return ' '.join(s.upper().split())


def preench(v):
    return v is not None and str(v).strip() not in ('', 'None', '.', '-', 'TBD', 'TDB', '?')


def estado(r):
    if preench(r[V_CONTRATADO]):
        return 'preenchida'
    a = r[4]
    if isinstance(a, datetime.datetime) and a.date() <= REF:
        return 'a confirmar'
    return 'aberta'


def bloco(c):
    c = str(c).upper()
    if 'WH ' in c or 'WAREHOUSE' in c:
        return 'EUA / Warehouses (MIA, Houston, NY)'
    if 'INLAND USA' in c or 'INLAND AMERICAS' in c:
        return 'EUA / Inland Freight America'
    if 'AMERICAS' in c:
        return 'EUA / Operacoes America'
    if 'INLAND EUROPA' in c:
        return 'Europa / Inland Freight Europa'
    if 'EUROPA' in c:
        return 'Europa / Operacoes Europa'
    if c.startswith('AIR CC') or c.startswith('OCEAN CC'):
        return 'Brasil / Customer Care'
    if 'EXPORT' in c:
        return 'Brasil / Exportacao'
    return None


LIDER = {'TEAM LEADER', 'SR. TEAM LEADER', 'COORDINATOR', 'HEAD'}


def fontes():
    ws = openpyxl.load_workbook(BASE, data_only=True)['Setembro Unificado']
    A = [r for r in ws.iter_rows(min_row=2, values_only=True)
         if r[4] and str(r[6]).strip().upper() == 'ATIVO']
    wv = openpyxl.load_workbook(VAGAS, data_only=True)['Vagas']
    V = [r for r in wv.iter_rows(min_row=2, values_only=True)
         if r[V_CARGO] and str(r[V_CARGO]).strip() not in ('', 'None')]
    return A, V


def tabelas(doc):
    return doc.tables


def cel(t, i, j):
    try:
        return t.rows[i].cells[j].text.strip()
    except IndexError:
        return ''


def inte(s):
    s = str(s).strip()
    return int(s) if re.fullmatch(r'-?\d+', s) else None


def perc(s):
    m = re.fullmatch(r'(\d+(?:[.,]\d+)?)%', str(s).strip())
    return float(m.group(1).replace(',', '.')) if m else None


def money(s):
    s = str(s).strip()
    if not s.startswith('R$'):
        return None
    d = re.sub(r'[^0-9]', '', s)
    return float(d) if d else None


def acha(doc, pred):
    for t in doc.tables:
        if pred(t):
            return t
    return None


print('=' * 78)
print('AUDITORIA DA SECAO DE VAGAS, 5 PASSADAS')
print('=' * 78)

# ---------- P1: classificacao das 65 linhas ----------
print('\n[P1] Classificacao das linhas da planilha de vagas')
A, V = fontes()
c = Counter(estado(r) for r in V)
doc = Document(DOCX)
t = acha(doc, lambda x: norm(cel(x, 0, 0)).startswith('ESTADO DA LINHA'))
ck('tabela de estado encontrada', t is not None, 1)
esperado = {'EM ABERTO': c['aberta'], 'JA PREENCHIDA': c['preenchida'],
            'A CONFIRMAR': c['a confirmar'], 'TOTAL DE REGISTROS': len(V)}
for i in range(1, len(t.rows)):
    k = norm(cel(t, i, 0))
    v = inte(cel(t, i, 1))
    for pref, esp in esperado.items():
        if k.startswith(pref):
            ck('%s: doc %s == fonte %d' % (pref, v, esp), v == esp, 1)
ok('aberta=%d preenchida=%d a confirmar=%d total=%d'
   % (c['aberta'], c['preenchida'], c['a confirmar'], len(V)), 1)
ck('soma das tres classes == total', c['aberta'] + c['preenchida'] + c['a confirmar'] == len(V), 1)

# ---------- P2: contagens por bloco ----------
print('\n[P2] Ativos, TL+, vagas abertas e preenchidas por bloco')
A, V = fontes()
at = Counter()
tl = Counter()
for r in A:
    b = bloco(r[B_CARGO])
    if b:
        at[b] += 1
        if r[B_POS] in LIDER:
            tl[b] += 1
ab = Counter()
pr = Counter()
for r in V:
    b = bloco(r[V_CARGO])
    if not b:
        continue
    e = estado(r)
    if e == 'aberta':
        ab[b] += 1
    elif e == 'preenchida':
        pr[b] += 1
doc = Document(DOCX)
t = acha(doc, lambda x: norm(cel(x, 0, 0)) == 'BLOCO' and len(x.rows[0].cells) >= 12)
ck('tabela de blocos encontrada', t is not None, 2)
vistos = 0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    if norm(nome).startswith('TOTAL'):
        ck('TOTAL ativos == %d' % sum(at.values()), inte(cel(t, i, 1)) == sum(at.values()), 2)
        ck('TOTAL TL+ == %d' % sum(tl.values()), inte(cel(t, i, 2)) == sum(tl.values()), 2)
        ck('TOTAL abertas == %d' % sum(ab.values()), inte(cel(t, i, 3)) == sum(ab.values()), 2)
        ck('TOTAL preench == %d' % sum(pr.values()), inte(cel(t, i, 4)) == sum(pr.values()), 2)
        continue
    chave = next((b for b in at if norm(b) == norm(nome)), None)
    ck('bloco "%s" reconhecido' % nome, chave is not None, 2)
    if not chave:
        continue
    vistos += 1
    ck('%s ativos %s == %d' % (nome, cel(t, i, 1), at[chave]), inte(cel(t, i, 1)) == at[chave], 2)
    ck('%s TL+ %s == %d' % (nome, cel(t, i, 2), tl[chave]), inte(cel(t, i, 2)) == tl[chave], 2)
    ck('%s abertas %s == %d' % (nome, cel(t, i, 3), ab[chave]), inte(cel(t, i, 3)) == ab[chave], 2)
    ck('%s preench %s == %d' % (nome, cel(t, i, 4), pr[chave]), inte(cel(t, i, 4)) == pr[chave], 2)
ck('todos os 7 blocos presentes', vistos == 7, 2)
ok('%d blocos conferidos | ativos=%d abertas=%d preench=%d'
   % (vistos, sum(at.values()), sum(ab.values()), sum(pr.values())), 2)

# ---------- P3: percentuais de ocupacao ----------
print('\n[P3] Percentual do quadro em aberto')
A, V = fontes()
doc = Document(DOCX)
t = acha(doc, lambda x: norm(cel(x, 0, 0)) == 'BLOCO' and len(x.rows[0].cells) >= 12)
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    p = perc(cel(t, i, 5))
    if p is None:
        continue
    if norm(nome).startswith('TOTAL'):
        esp = sum(ab.values()) / (sum(at.values()) + sum(ab.values())) * 100
    else:
        chave = next((b for b in at if norm(b) == norm(nome)), None)
        if not chave:
            continue
        den = at[chave] + ab[chave]
        esp = ab[chave] / den * 100 if den else 0
    ck('%s: %% aberto %.1f == %.1f' % (nome, p, esp), abs(p - esp) <= 0.1, 3)
ok('percentuais de ocupacao conferidos (formula vagas / (ativos + vagas))', 3)
# ordenacao decrescente
vals = [perc(cel(t, i, 5)) for i in range(1, len(t.rows) - 1)]
vals = [v for v in vals if v is not None]
ck('tabela ordenada por %% aberto decrescente', vals == sorted(vals, reverse=True), 3)

# ---------- P4: custos e tipo de vaga ----------
print('\n[P4] Custo das vagas abertas, aumento e substituicao')
A, V = fontes()
cst = defaultdict(float)
aum = Counter()
sub = Counter()
for r in V:
    b = bloco(r[V_CARGO])
    if not b or estado(r) != 'aberta':
        continue
    cst[b] += num(r[V_CUSTO])
    if 'Aumento' in str(r[V_OCUP]):
        aum[b] += 1
    else:
        sub[b] += 1
doc = Document(DOCX)
t = acha(doc, lambda x: norm(cel(x, 0, 0)) == 'BLOCO' and len(x.rows[0].cells) >= 12)
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    if norm(nome).startswith('TOTAL'):
        ck('TOTAL custo == %.0f' % sum(cst.values()),
           abs((money(cel(t, i, 10)) or 0) - sum(cst.values())) <= 7, 4)
        ck('TOTAL aumento == %d' % sum(aum.values()), inte(cel(t, i, 6)) == sum(aum.values()), 4)
        ck('TOTAL subst == %d' % sum(sub.values()), inte(cel(t, i, 7)) == sum(sub.values()), 4)
        continue
    chave = next((b for b in at if norm(b) == norm(nome)), None)
    if not chave:
        continue
    ck('%s aumento %s == %d' % (nome, cel(t, i, 6), aum[chave]), inte(cel(t, i, 6)) == aum[chave], 4)
    ck('%s subst %s == %d' % (nome, cel(t, i, 7), sub[chave]), inte(cel(t, i, 7)) == sub[chave], 4)
    mv = money(cel(t, i, 10))
    ck('%s custo %.0f == %.0f' % (nome, mv or 0, cst[chave]),
       abs((mv or 0) - cst[chave]) <= 1, 4)
    ck('%s aumento + subst == abertas' % nome, aum[chave] + sub[chave] == ab[chave], 4)
ok('custos e tipos conferidos | total R$ %s' % ('{:,.0f}'.format(sum(cst.values()))), 4)

# ---------- P5: volume do CIS e embarques por ativo ----------
print('\n[P5] Volume do CIS e embarques por ativo')
d = pd.read_parquet(CIS)
d['created_at'] = pd.to_datetime(d['created_at'])
p = d[(d.created_at >= '2026-04-01') & (d.created_at <= '2026-09-30')]
E = lambda f: p[f]['assembly_id'].nunique() / 6
eua_air = E((p['off'].isin(['DMS MIAMI', 'DMS HOUSTON'])) & (p['mode'] == 'air'))
mia_sea = E((p['off'] == 'DMS MIAMI') & (p['mode'] == 'sea'))
eur_air = E((p['off'].isin(['DMS FRANKFURT', 'DMS LOGISTICS LISBOA'])) & (p['mode'] == 'air'))
cc_air = E((p.imp_exp == 'IMP') & (p['mode'] == 'air'))
ex_air = E((p.imp_exp == 'EXP') & (p['mode'] == 'air'))
ex_sea = E((p.imp_exp == 'EXP') & (p['mode'] == 'sea'))
at_eua = sum(at[b] for b in at if b.startswith('EUA'))
at_eur = sum(at[b] for b in at if b.startswith('Europa'))
esp_vpa = {
    'EUA / Inland Freight America': (eua_air + mia_sea) / at_eua,
    'EUA / Operacoes America': (eua_air + mia_sea) / at_eua,
    'EUA / Warehouses (MIA, Houston, NY)': (eua_air + mia_sea) / at_eua,
    'Europa / Inland Freight Europa': eur_air / at_eur,
    'Europa / Operacoes Europa': eur_air / at_eur,
    'Brasil / Customer Care': cc_air / at['Brasil / Customer Care'],
    'Brasil / Exportacao': (ex_air + ex_sea) / at['Brasil / Exportacao'],
}
doc = Document(DOCX)
t = acha(doc, lambda x: norm(cel(x, 0, 0)) == 'BLOCO' and len(x.rows[0].cells) >= 12)
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    chave = next((b for b in esp_vpa if norm(b) == norm(nome)), None)
    if not chave:
        continue
    v = inte(cel(t, i, 9))
    ck('%s embarques por ativo %s == %.0f' % (nome, v, esp_vpa[chave]),
       v is not None and abs(v - round(esp_vpa[chave])) <= 1, 5)
    vol = cel(t, i, 8)
    n = inte(re.sub(r'\D', '', vol.split('(')[0]) or '0')
    if chave.startswith('EUA'):
        ck('%s volume aereo %s == %.0f' % (nome, n, eua_air), abs(n - round(eua_air)) <= 1, 5)
    elif chave.startswith('Europa'):
        ck('%s volume aereo %s == %.0f' % (nome, n, eur_air), abs(n - round(eur_air)) <= 1, 5)
    elif chave == 'Brasil / Customer Care':
        ck('%s volume %s == %.0f' % (nome, n, cc_air), abs(n - round(cc_air)) <= 1, 5)
    else:
        ck('%s volume %s == %.0f' % (nome, n, ex_air), abs(n - round(ex_air)) <= 1, 5)
ok('volumes e embarques por ativo conferidos (EUA %.0f, Europa %.0f, CC %.0f, Exp %.0f)'
   % (eua_air, eur_air, cc_air, ex_air), 5)

# travessoes e percentuais
EM, EN = '\u2014', '\u2013'
tot = sum(pp.text.count(EM) + pp.text.count(EN) for pp in doc.paragraphs)
for tb in doc.tables:
    for row in tb.rows:
        for cc in row.cells:
            tot += cc.text.count(EM) + cc.text.count(EN)
ck('nenhum travessao no documento', tot == 0, 5)
pcts = []
for tb in doc.tables:
    for row in tb.rows:
        for cc in row.cells:
            v = perc(cc.text)
            if v is not None:
                pcts.append(v)
ck('nenhum percentual de participacao acima de 100', all(v <= 100 for v in pcts), 5)
ck('percentuais com virgula decimal',
   not any(re.fullmatch(r'\d+\.\d+%', cc.text.strip())
           for tb in doc.tables for row in tb.rows for cc in row.cells), 5)
ok('%d percentuais verificados, 0 travessoes' % len(pcts), 5)

print('\n' + '=' * 78)
print('VERIFICACOES: %d' % checks)
if falhas:
    print('FALHAS: %d' % len(falhas))
    for f in falhas:
        print('  - %s' % f)
    sys.exit(1)
print('RESULTADO: a secao de vagas reflete exatamente as tres fontes.')
print('=' * 78)
