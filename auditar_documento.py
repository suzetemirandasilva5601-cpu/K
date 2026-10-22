# -*- coding: utf-8 -*-
"""
Auditoria independente do documento gerado.

Le os numeros DE VOLTA das tabelas do arquivo .docx e confronta cada valor
com a planilha de origem. Nao reutiliza nenhuma agregacao do script gerador:
recalcula tudo a partir do Excel.
"""
import re
import openpyxl
from docx import Document
from collections import Counter, defaultdict

XLSX = 'Base_Setembro26 (1).xlsx'
DOCX = 'DMS_Base_Setembro26_Visao_Organizacional.docx'


def num(v):
    if v is None or v == '-':
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


# ---------- fonte ----------
ws = openpyxl.load_workbook(XLSX, data_only=True)['Setembro Unificado']
T = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[4]]
A = [r for r in T if str(r[6]).strip().upper() == 'ATIVO']
N_T, N_A = len(T), len(A)
C_T = sum(num(r[21]) for r in T)
C_A = sum(num(r[21]) for r in A)


def cnt(ds, col):
    c = Counter()
    for r in ds:
        c[r[col] or 'EM BRANCO'] += 1
    return c


def cst(ds, col):
    c = defaultdict(float)
    for r in ds:
        c[r[col] or 'EM BRANCO'] += num(r[21])
    return c


pos_t, pos_a = cnt(T, 10), cnt(A, 10)
ar_t, ar_a = cnt(T, 12), cnt(A, 12)
cl_t, cl_a = cnt(T, 14), cnt(A, 14)
arc_t, arc_a = cst(T, 12), cst(A, 12)
clc_t, clc_a = cst(T, 14), cst(A, 14)


def normh(h):
    if h and 'VASCONCELLOS' in str(h).upper():
        return 'ANA CAROL VASCONCELLOS'
    return h or 'EM BRANCO'


hd_t, hd_a = Counter(), Counter()
for r in T:
    hd_t[normh(r[13])] += 1
for r in A:
    hd_a[normh(r[13])] += 1

# ---------- documento ----------
doc = Document(DOCX)
erros = []


def cel(t, i, j):
    try:
        return t.rows[i].cells[j].text.strip()
    except IndexError:
        return ''


def ncols(t):
    return len(t.rows[0].cells)


def money(s):
    s = s.strip()
    if not s.startswith('R$'):
        return None
    return float(re.sub(r'[^0-9]', '', s))


def inteiro(s):
    s = s.strip()
    return int(s) if re.fullmatch(r'-?\d+', s) else None


def find(pred):
    for t in doc.tables:
        if pred(t):
            return t
    return None


def ck(desc, cond):
    print(('  [OK]   ' if cond else '  [ERRO] ') + desc)
    if not cond:
        erros.append(desc)


print('=' * 68)
print('AUDITORIA DO DOCUMENTO GERADO (%d tabelas)' % len(doc.tables))
print('=' * 68)

# ---- 1. reconciliacao de escopos ----
print('\n[1] Tabela de reconciliacao de escopos')
t = find(lambda x: cel(x, 0, 0) == 'Escopo')
v_tot, v_na, v_at = money(cel(t, 1, 2)), money(cel(t, 2, 2)), money(cel(t, 3, 2))
ck('HC total no doc (%s) == fonte (%d)' % (cel(t, 1, 1), N_T), inteiro(cel(t, 1, 1)) == N_T)
ck('HC ativos no doc (%s) == fonte (%d)' % (cel(t, 3, 1), N_A), inteiro(cel(t, 3, 1)) == N_A)
ck('HC nao-ativos no doc (%s) == fonte (%d)' % (cel(t, 2, 1), N_T - N_A),
   inteiro(cel(t, 2, 1)) == N_T - N_A)
ck('Custo total no doc (%s) == fonte (%.0f)' % (cel(t, 1, 2), C_T), abs(v_tot - round(C_T)) <= 1)
ck('Custo ativos no doc (%s) == fonte (%.0f)' % (cel(t, 3, 2), C_A), abs(v_at - round(C_A)) <= 1)
ck('Reconciliacao interna: ativos + nao-ativos == total', abs((v_at + v_na) - v_tot) <= 1)

# ---- 2. cargos ----
print('\n[2] Tabela de Cargo / Nivel')
t = find(lambda x: cel(x, 0, 0).startswith('Cargo'))
s_t = s_a = 0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    ht, ha = inteiro(cel(t, i, 1)), inteiro(cel(t, i, 3))
    if nome == 'TOTAL':
        ck('linha TOTAL: HC total == %d' % N_T, ht == N_T)
        ck('linha TOTAL: HC ativos == %d' % N_A, ha == N_A)
        continue
    s_t += ht
    s_a += ha
    if pos_t.get(nome, 0) != ht:
        erros.append('cargo %s HC total doc=%s fonte=%s' % (nome, ht, pos_t.get(nome, 0)))
    if pos_a.get(nome, 0) != ha:
        erros.append('cargo %s HC ativos doc=%s fonte=%s' % (nome, ha, pos_a.get(nome, 0)))
ck('todas as %d linhas de cargo batem com a fonte' % (len(t.rows) - 2),
   not [e for e in erros if e.startswith('cargo ')])
ck('soma das linhas == total (%d / %d)' % (s_t, s_a), s_t == N_T and s_a == N_A)

# ---- 3. C-Level ----
print('\n[3] Tabela de C-Level')
t = find(lambda x: cel(x, 0, 0) == 'C-Level' and ncols(x) >= 8)
s_t = s_a = 0
sc_t = sc_a = 0.0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    ht, ha = inteiro(cel(t, i, 1)), inteiro(cel(t, i, 4))
    if nome == 'TOTAL':
        ck('linha TOTAL: HC total == %d' % N_T, ht == N_T)
        ck('linha TOTAL: HC ativos == %d' % N_A, ha == N_A)
        continue
    s_t += ht
    s_a += ha
    sc_t += money(cel(t, i, 3)) or 0
    sc_a += money(cel(t, i, 6)) or 0
    # o documento rotula C-Level vazio como "Sem C-Level"; na fonte e "EM BRANCO"
    key = 'EM BRANCO' if nome == 'Sem C-Level' else nome
    if cl_t.get(key, 0) != ht:
        erros.append('clevel %s HC total doc=%s fonte=%s' % (nome, ht, cl_t.get(key, 0)))
    if cl_a.get(key, 0) != ha:
        erros.append('clevel %s HC ativos doc=%s fonte=%s' % (nome, ha, cl_a.get(key, 0)))
ck('todas as linhas de C-Level batem com a fonte',
   not [e for e in erros if e.startswith('clevel ')])
ck('soma HC == total (%d / %d)' % (s_t, s_a), s_t == N_T and s_a == N_A)
ck('soma custo total R$ %.0f ~= fonte R$ %.0f' % (sc_t, C_T), abs(sc_t - C_T) <= len(t.rows))
ck('soma custo ativos R$ %.0f ~= fonte R$ %.0f' % (sc_a, C_A), abs(sc_a - C_A) <= len(t.rows))

# ---- 4. areas ----
print('\n[4] Tabela de Areas')
t = find(lambda x: cel(x, 0, 0) == 'Area' and ncols(x) >= 9)
s_t = s_a = 0
sc_t = sc_a = 0.0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    if nome == 'TOTAL':
        ck('linha TOTAL: HC total == %d' % N_T, inteiro(cel(t, i, 1)) == N_T)
        continue
    ht, ha = inteiro(cel(t, i, 1)), inteiro(cel(t, i, 4))
    s_t += ht
    s_a += ha
    sc_t += money(cel(t, i, 2)) or 0
    sc_a += money(cel(t, i, 6)) or 0
    if ar_t.get(nome, 0) != ht:
        erros.append('area %s HC total doc=%s fonte=%s' % (nome, ht, ar_t.get(nome, 0)))
    if ar_a.get(nome, 0) != ha:
        erros.append('area %s HC ativos doc=%s fonte=%s' % (nome, ha, ar_a.get(nome, 0)))
    mt = money(cel(t, i, 2))
    if mt is not None and abs(mt - round(arc_t.get(nome, 0))) > 1:
        erros.append('area %s custo total doc=%s fonte=%.0f' % (nome, mt, arc_t.get(nome, 0)))
ck('todas as %d areas batem com a fonte (HC e custo)' % (len(t.rows) - 2),
   not [e for e in erros if e.startswith('area ')])
ck('soma HC == total (%d / %d)' % (s_t, s_a), s_t == N_T and s_a == N_A)
ck('soma custo total R$ %.0f ~= fonte R$ %.0f' % (sc_t, C_T), abs(sc_t - C_T) <= len(t.rows))
ck('soma custo ativos R$ %.0f ~= fonte R$ %.0f' % (sc_a, C_A), abs(sc_a - C_A) <= len(t.rows))

# ---- 5. heads ----
print('\n[5] Tabela de Heads')
t = find(lambda x: cel(x, 0, 0) == 'Head')
s_t = s_a = 0
for i in range(1, len(t.rows)):
    nome = cel(t, i, 0)
    ht, ha = inteiro(cel(t, i, 2)), inteiro(cel(t, i, 3))
    s_t += ht
    s_a += ha
    if hd_t.get(nome, 0) != ht:
        erros.append('head %s time total doc=%s fonte=%s' % (nome, ht, hd_t.get(nome, 0)))
    if hd_a.get(nome, 0) != ha:
        erros.append('head %s time ativos doc=%s fonte=%s' % (nome, ha, hd_a.get(nome, 0)))
ck('todos os %d heads batem com a fonte' % (len(t.rows) - 1),
   not [e for e in erros if e.startswith('head ')])
ck('soma dos times == total de ativos (%d)' % N_A, s_a == N_A)

# ---- 6. percentuais ----
print('\n[6] Consistencia de percentuais')
pcts = []
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            txt = c.text.strip()
            if re.fullmatch(r'\d+,\d%', txt):
                pcts.append(float(txt.replace(',', '.').rstrip('%')))
ck('nenhum percentual acima de 100%% (%d percentuais verificados)' % len(pcts),
   all(p <= 100.0 for p in pcts))
ck('formatacao decimal brasileira (virgula) em todos os percentuais',
   not any(re.fullmatch(r'\d+\.\d%', c.text.strip())
           for t in doc.tables for row in t.rows for c in row.cells))

# ---- resultado ----
print('\n' + '=' * 68)
if erros:
    print('FALHAS ENCONTRADAS (%d):' % len(erros))
    for e in erros:
        print('  - ' + e)
    raise SystemExit(1)
print('RESULTADO: todos os numeros do documento conferem com a planilha de origem.')
print('=' * 68)
