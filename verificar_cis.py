# -*- coding: utf-8 -*-
"""
Verificacao em 5 passadas do numero medio de embarques por local no CIS.

Cada passada recarrega o parquet do zero e usa um caminho de calculo
diferente (pandas groupby, filtro linha a linha, pivot, contagem por mes
e depois media, e agregacao via pyarrow puro). Se as cinco convergirem,
o numero esta correto.

Definicao de embarque: assembly_id distinto, datado por created_at.
Janela: abril a setembro de 2026 (6 meses).
"""
import sys
from collections import defaultdict

import pandas as pd
import pyarrow.parquet as pq

ARQ = 'CIS_20261013_ORDERS.parquet'
INI, FIM = '2026-04-01', '2026-09-30'
MESES = 6

# valores informados pela area, a conferir
ESPERADO = {
    ('DMS MIAMI', 'air'): 878,
    ('DMS MIAMI', 'sea'): 139,
    ('DMS HOUSTON', 'air'): 94,
    ('DMS FRANKFURT', 'air'): 351,
    ('DMS LOGISTICS LISBOA', 'air'): 179,
}
ESPERADO_FLUXO = {
    ('IMP', 'air'): 2287,   # importacao aerea, Customer Care
    ('EXP', 'air'): 244,    # exportacao aerea
    ('EXP', 'sea'): 55,     # exportacao maritima
}


def base():
    d = pd.read_parquet(ARQ)
    d['created_at'] = pd.to_datetime(d['created_at'])
    return d[(d.created_at >= INI) & (d.created_at <= FIM)]


# ---------------- passada 1: groupby nunique ----------------
def p1():
    p = base()
    g = p.groupby(['off', 'mode'])['assembly_id'].nunique() / MESES
    loc = {k: float(g.get(k, 0)) for k in ESPERADO}
    gf = p.groupby(['imp_exp', 'mode'])['assembly_id'].nunique() / MESES
    flx = {k: float(gf.get(k, 0)) for k in ESPERADO_FLUXO}
    return loc, flx


# ---------------- passada 2: filtro booleano por chave ----------------
def p2():
    p = base()
    loc = {}
    for (o, m) in ESPERADO:
        loc[(o, m)] = p[(p['off'] == o) & (p['mode'] == m)]['assembly_id'].nunique() / MESES
    flx = {}
    for (f, m) in ESPERADO_FLUXO:
        flx[(f, m)] = p[(p.imp_exp == f) & (p['mode'] == m)]['assembly_id'].nunique() / MESES
    return loc, flx


# ---------------- passada 3: pivot_table ----------------
def p3():
    p = base()
    pt = pd.pivot_table(p, index='off', columns='mode', values='assembly_id',
                        aggfunc=pd.Series.nunique, fill_value=0) / MESES
    loc = {(o, m): float(pt.loc[o, m]) if o in pt.index and m in pt.columns else 0.0
           for (o, m) in ESPERADO}
    pf = pd.pivot_table(p, index='imp_exp', columns='mode', values='assembly_id',
                        aggfunc=pd.Series.nunique, fill_value=0) / MESES
    flx = {(f, m): float(pf.loc[f, m]) if f in pf.index and m in pf.columns else 0.0
           for (f, m) in ESPERADO_FLUXO}
    return loc, flx


# ---------------- passada 4: conjuntos por mes, depois media ----------------
def p4():
    p = base().copy()
    p['ym'] = p.created_at.dt.to_period('M')
    loc = {}
    for (o, m) in ESPERADO:
        q = p[(p['off'] == o) & (p['mode'] == m)]
        por_mes = q.groupby('ym')['assembly_id'].nunique()
        # soma dos distintos de cada mes dividida pelos 6 meses da janela
        loc[(o, m)] = por_mes.sum() / MESES
    flx = {}
    for (f, m) in ESPERADO_FLUXO:
        q = p[(p.imp_exp == f) & (p['mode'] == m)]
        flx[(f, m)] = q.groupby('ym')['assembly_id'].nunique().sum() / MESES
    return loc, flx


# ---------------- passada 5: pyarrow puro, sets em python ----------------
def p5():
    t = pq.read_table(ARQ, columns=['off', 'mode', 'imp_exp', 'created_at', 'assembly_id'])
    off = t.column('off').to_pylist()
    mod = t.column('mode').to_pylist()
    ie = t.column('imp_exp').to_pylist()
    dt = t.column('created_at').to_pylist()
    asm = t.column('assembly_id').to_pylist()
    ini = pd.Timestamp(INI).date()
    fim = pd.Timestamp(FIM).date()
    sl = defaultdict(set)
    sf = defaultdict(set)
    for i in range(len(asm)):
        d = dt[i]
        if d is None or d < ini or d > fim:
            continue
        sl[(off[i], mod[i])].add(asm[i])
        sf[(ie[i], mod[i])].add(asm[i])
    loc = {k: len(sl.get(k, ())) / MESES for k in ESPERADO}
    flx = {k: len(sf.get(k, ())) / MESES for k in ESPERADO_FLUXO}
    return loc, flx


PASSADAS = [('groupby nunique', p1), ('filtro booleano', p2), ('pivot_table', p3),
            ('conjuntos por mes', p4), ('pyarrow + sets', p5)]

print('=' * 84)
print('VERIFICACAO DO CIS EM 5 PASSADAS')
print('embarque = assembly_id distinto | data = created_at | janela abr-set/26')
print('=' * 84)

res = []
for nome, fn in PASSADAS:
    loc, flx = fn()
    res.append((nome, loc, flx))
    print('\n[%s]' % nome)
    for k in ESPERADO:
        print('   %-24s %-4s %8.1f' % (k[0], k[1], loc[k]))
    for k in ESPERADO_FLUXO:
        print('   %-24s %-4s %8.1f' % (k[0], k[1], flx[k]))

print('\n' + '=' * 84)
print('CONVERGENCIA ENTRE AS 5 PASSADAS')
print('=' * 84)
falhas = []
for k in list(ESPERADO) + list(ESPERADO_FLUXO):
    vals = []
    for nome, loc, flx in res:
        vals.append(round((loc if k in loc else flx)[k], 2))
    igual = len(set(vals)) == 1
    esp = ESPERADO.get(k, ESPERADO_FLUXO.get(k))
    real = vals[0]
    conf = abs(real - esp) <= 1
    print('%-24s %-4s informado %6d | real %8.1f | 5 passadas %s | %s'
          % (k[0], k[1], esp, real,
             'identicas' if igual else 'DIVERGEM %s' % set(vals),
             'CONFERE' if conf else 'DIVERGE'))
    if not igual or not conf:
        falhas.append(k)

# somatorios e Houston
print('\n' + '=' * 84)
print('SOMATORIOS E RECORTES')
print('=' * 84)
p = base()
eua_air = p[(p['off'].isin(['DMS MIAMI', 'DMS HOUSTON'])) & (p['mode'] == 'air')]['assembly_id'].nunique() / MESES
eur_air = p[(p['off'].isin(['DMS FRANKFURT', 'DMS LOGISTICS LISBOA'])) & (p['mode'] == 'air')]['assembly_id'].nunique() / MESES
print('EUA aereo (Miami + Houston):      informado ~970 | real %.0f | %s'
      % (eua_air, 'CONFERE' if abs(eua_air - 970) <= 5 else 'DIVERGE'))
print('Europa aereo (Frankfurt + Lisboa):informado ~530 | real %.0f | %s'
      % (eur_air, 'CONFERE' if abs(eur_air - 530) <= 5 else 'DIVERGE'))
h = p[(p['off'] == 'DMS HOUSTON') & (p['mode'] == 'air')]
hjs = h[h.created_at >= '2026-07-01']['assembly_id'].nunique() / 3
haj = h[h.created_at < '2026-07-01']['assembly_id'].nunique() / 3
print('Houston jul-set:                  informado ~169 | real %.0f | %s'
      % (hjs, 'CONFERE' if abs(hjs - 169) <= 3 else 'DIVERGE'))
print('Houston abr-jun (derivado):                      real %.0f' % haj)
escritorios = sorted({o for o in pd.read_parquet(ARQ, columns=['off'])['off'].dropna().unique()
                      if 'DMS' in str(o).upper()})
print('\nEscritorios DMS no CIS: %s' % escritorios)
print('Nova York como escritorio proprio: %s'
      % ('NAO existe' if not any('YORK' in e.upper() or e.upper().endswith(' NY')
                                 for e in escritorios) else 'existe'))

print('\n' + '=' * 84)
if falhas:
    print('FALHAS: %s' % falhas)
    sys.exit(1)
print('RESULTADO: as 5 passadas convergem e todos os volumes por local')
print('conferem com os numeros informados pela area.')
print('=' * 84)
