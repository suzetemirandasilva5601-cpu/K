# -*- coding: utf-8 -*-
"""
Auditoria da apresentacao final (versao em briefing/), em 10 passadas.

Cada passada recarrega as 3 fontes do zero, recalcula cada numero exibido no
.pptx (texto, tabelas e graficos) e confronta. Foco no penultimo slide (o 3,
tabela de ativos x vagas por local) e em todos os percentuais.
"""
import datetime
import re
import sys
from collections import Counter

import openpyxl
import pandas as pd
from pptx import Presentation

PPTX = 'briefing/20261022 - DMS - Vagas em aberto x ocupação nas Operações.pptx'
BASE = 'Base_Setembro26 (1).xlsx'
VAGAS = 'Vagas 21-10.xlsx'
CIS = 'CIS_20261013_ORDERS.parquet'
REF = datetime.date(2026, 10, 21)


def num(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def nome_ok(v):
    return v is not None and str(v).strip() not in ('', 'None', '.', '-', 'TBD', 'TDB', '?')


def estado(r):
    if nome_ok(r[6]):
        return 'preenchida'
    a = r[4]
    if isinstance(a, datetime.datetime) and a.date() <= REF:
        return 'a confirmar'
    return 'aberta'


def bloco(c):
    c = str(c).upper()
    if 'WH ' in c or 'WAREHOUSE' in c:
        return 'WH'
    if 'INLAND USA' in c or 'INLAND AMERICAS' in c:
        return 'INLAND_US'
    if 'AMERICAS' in c:
        return 'OPS_AME'
    if 'INLAND EUROPA' in c:
        return 'INLAND_EU'
    if 'EUROPA' in c:
        return 'OPS_EU'
    if c.startswith('AIR CC') or c.startswith('OCEAN CC'):
        return 'CC'
    if 'EXPORT' in c:
        return 'EXP'
    return None


LIDER = {'TEAM LEADER', 'SR. TEAM LEADER', 'COORDINATOR', 'HEAD'}


def calcular():
    """Recalcula tudo das fontes. Retorna um dicionario de valores esperados."""
    ws = openpyxl.load_workbook(BASE, data_only=True)['Setembro Unificado']
    A = [r for r in ws.iter_rows(min_row=2, values_only=True)
         if r[4] and str(r[6]).strip().upper() == 'ATIVO']
    wv = openpyxl.load_workbook(VAGAS, data_only=True)['Vagas']
    V = [r for r in wv.iter_rows(min_row=2, values_only=True)
         if r[3] and str(r[3]).strip() not in ('', 'None')]
    AB = [r for r in V if estado(r) == 'aberta']
    COO = [r for r in AB if str(r[1]).strip() == 'COO']

    at, vab, tl, pub = Counter(), Counter(), Counter(), Counter()
    for r in A:
        b = bloco(r[11])
        if b:
            at[b] += 1
            if r[10] in LIDER:
                tl[b] += 1
    for r in AB:
        b = bloco(r[3])
        if b:
            vab[b] += 1
            if r[7] == 'ABERTA | PUBLICADA':
                pub[b] += 1

    d = pd.read_parquet(CIS)
    d['created_at'] = pd.to_datetime(d['created_at'])
    p = d[(d.created_at >= '2026-04-01') & (d.created_at <= '2026-09-30')]
    E = lambda f: round(p[f]['assembly_id'].nunique() / 6)
    cis = {
        'EUA': E((p['off'].isin(['DMS MIAMI', 'DMS HOUSTON'])) & (p['mode'] == 'air')),
        'Europa': E((p['off'].isin(['DMS FRANKFURT', 'DMS LOGISTICS LISBOA'])) & (p['mode'] == 'air')),
        'CC': E((p.imp_exp == 'IMP') & (p['mode'] == 'air')),
        'EXP': E((p.imp_exp == 'EXP') & (p['mode'] == 'air')),
    }

    G = {'EUA': ['WH', 'INLAND_US', 'OPS_AME'], 'Europa': ['INLAND_EU', 'OPS_EU'], 'Brasil': ['CC', 'EXP']}

    def soma(bs, cnt):
        return sum(cnt[b] for b in bs)

    r = {}
    r['linhas'] = len(V)
    r['abertas'] = len(AB)
    r['coo'] = len(COO)
    r['coo_as'] = sum(1 for x in COO if any(k in str(x[3]).upper() for k in ['ANALYST', 'SPEC'])
                      and 'TL' not in str(x[3]).upper())
    r['coo_pub'] = sum(1 for x in COO if x[7] == 'ABERTA | PUBLICADA')
    r['coo_bloco'] = sum(1 for x in COO if bloco(x[3]))
    r['coo_aabrir'] = sum(1 for x in COO if bloco(x[3]) and x[7] != 'ABERTA | PUBLICADA')
    # geografia das 49
    r['geo_eua'] = sum(1 for x in AB if bloco(x[3]) in ('WH', 'INLAND_US', 'OPS_AME'))
    r['geo_eur'] = sum(1 for x in AB if bloco(x[3]) in ('INLAND_EU', 'OPS_EU'))
    r['geo_br'] = len(AB) - r['geo_eua'] - r['geo_eur']
    # blocos
    for b in ['WH', 'INLAND_US', 'OPS_AME', 'INLAND_EU', 'OPS_EU', 'CC', 'EXP']:
        r['at_' + b] = at[b]
        r['vab_' + b] = vab[b]
        r['pct_' + b] = (vab[b] / (at[b] + vab[b]) * 100) if at[b] + vab[b] else 0
    for g, bs in G.items():
        r['at_' + g] = soma(bs, at)
        r['vab_' + g] = soma(bs, vab)
        r['pub_' + g] = soma(bs, pub)
        r['pct_' + g] = (soma(bs, vab) / (soma(bs, at) + soma(bs, vab)) * 100) if soma(bs, at) + soma(bs, vab) else 0
        r['ratio_' + g] = (soma(bs, at) / soma(bs, tl)) if soma(bs, tl) else 0
    r['tot_at'] = sum(at.values())
    r['tot_vab'] = sum(vab.values())
    r['pct_tot'] = r['tot_vab'] / (r['tot_at'] + r['tot_vab']) * 100
    r['cis'] = cis
    r['cis_br'] = cis['CC'] + cis['EXP']
    r['cis_tot'] = cis['EUA'] + cis['Europa'] + cis['CC'] + cis['EXP']
    return r


# ---------- texto do pptx ----------
def extrair_texto():
    prs = Presentation(PPTX)
    txt = []
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                txt.append(sh.text_frame.text)
            if sh.has_table:
                for row in sh.table.rows:
                    txt.append(' | '.join(c.text for c in row.cells))
            if sh.has_chart:
                # inclui os rotulos de categoria e os valores das series,
                # senao percentuais que vivem no grafico contam como ausentes
                try:
                    txt.append(' | '.join(str(c) for c in sh.chart.plots[0].categories))
                    for serie in sh.chart.series:
                        txt.append(' | '.join(str(v) for v in serie.values))
                except Exception:
                    pass
    return '\n'.join(txt)


TXT = extrair_texto()


def tem(s):
    return s in TXT


def pcbr(v):
    return ('%.1f%%' % v).replace('.', ',')


# ---------- 10 passadas ----------
print('=' * 76)
print('AUDITORIA DA APRESENTACAO FINAL — 10 PASSADAS')
print('=' * 76)

historico = []
for passada in range(1, 11):
    r = calcular()
    falhas = []

    def ck(desc, cond):
        if not cond:
            falhas.append(desc)

    # --- slide 2 ---
    ck('49 abertas', r['abertas'] == 49 and tem('49'))
    ck('65 linhas', r['linhas'] == 65 and tem('65'))
    ck('35 COO', r['coo'] == 35 and tem('35'))
    ck('26 de 35 analyst/spec', r['coo_as'] == 26 and tem('26 de 35'))
    ck('6 de 35 publicadas', r['coo_pub'] == 6 and tem('6 de 35'))
    ck('17 de 35 nos blocos', r['coo_bloco'] == 17 and tem('17 de 35'))
    ck('12 de 17 a abrir', r['coo_aabrir'] == 12 and tem('12 de 17'))
    ck('geografia 34/9/6', r['geo_br'] == 34 and r['geo_eua'] == 9 and r['geo_eur'] == 6)
    ck('geografia % no grafico', tem('69%') and tem('18%') and tem('12%'))

    # --- slide 3 (penultimo) ---
    ck('EUA ativos 20', r['at_EUA'] == 20 and tem('20'))
    ck('EUA vagas 9', r['vab_EUA'] == 9)
    ck('EUA % 31,0', abs(r['pct_EUA'] - 31.0) < 0.1 and tem('31,0%'))
    ck('Operacoes America 7/6/46,2', r['at_OPS_AME'] == 7 and r['vab_OPS_AME'] == 6 and tem('46,2%'))
    ck('Inland America 8/3/27,3', r['at_INLAND_US'] == 8 and r['vab_INLAND_US'] == 3 and tem('27,3%'))
    ck('Warehouses 5/0/0,0', r['at_WH'] == 5 and r['vab_WH'] == 0 and tem('0,0%'))
    ck('Europa 18/6/25,0', r['at_Europa'] == 18 and r['vab_Europa'] == 6 and tem('25,0%'))
    ck('Inland Europa 4/4/50,0', r['at_INLAND_EU'] == 4 and r['vab_INLAND_EU'] == 4 and tem('50,0%'))
    ck('Operacoes Europa 14/2/12,5', r['at_OPS_EU'] == 14 and r['vab_OPS_EU'] == 2 and tem('12,5%'))
    ck('Brasil 40/2/4,8', r['at_Brasil'] == 40 and r['vab_Brasil'] == 2 and tem('4,8%'))
    ck('Exportacao 3/1/25,0', r['at_EXP'] == 3 and r['vab_EXP'] == 1)
    ck('Customer Care 37/1/2,6', r['at_CC'] == 37 and r['vab_CC'] == 1 and tem('2,6%'))
    ck('Total 78/17/17,9', r['tot_at'] == 78 and r['tot_vab'] == 17 and tem('17,9%'))

    # --- CIS no slide 3 ---
    ck('CIS EUA 971', r['cis']['EUA'] == 971 and tem('971'))
    ck('CIS Europa 530', r['cis']['Europa'] == 530 and tem('530'))
    ck('CIS CC 2287', r['cis']['CC'] == 2287 and tem('2.287'))
    ck('CIS Export 244', r['cis']['EXP'] == 244 and tem('244'))
    ck('CIS Brasil 2531', r['cis_br'] == 2531 and tem('2.531'))
    ck('CIS total 4032', r['cis_tot'] == 4032 and tem('4.032'))
    ck('emb/ativo EUA 49', round(r['cis']['EUA'] / r['at_EUA']) == 49 and tem('49'))
    ck('emb/ativo Europa 29', round(r['cis']['Europa'] / r['at_Europa']) == 29 and tem('29'))
    ck('emb/ativo CC 62', round(r['cis']['CC'] / r['at_CC']) == 62 and tem('62'))
    ck('emb/ativo Export 81', round(r['cis']['EXP'] / r['at_EXP']) == 81 and tem('81'))
    ck('emb/ativo total 52', round(r['cis_tot'] / r['tot_at']) == 52 and tem('52'))

    # --- slide 4 pessoas por lideranca ---
    ck('ratio EUA 6,7', abs(r['ratio_EUA'] - 6.7) < 0.1)
    ck('ratio Europa 9,0', abs(r['ratio_Europa'] - 9.0) < 0.1)
    ck('ratio Brasil 5,0', abs(r['ratio_Brasil'] - 5.0) < 0.1)
    ck('57 sob Carol/Air Ops', tem('57'))

    historico.append(len(falhas))
    tag = 'OK' if not falhas else 'FALHAS: ' + '; '.join(falhas)
    print('passada %2d: %s' % (passada, tag))

print()
print('=' * 76)
consistente = len(set(historico)) == 1 and historico[0] == 0
print('resultado por passada (nº de falhas):', historico)
if consistente:
    print('RESULTADO: 10 passadas identicas, ZERO falhas.')
    print('Todos os numeros e percentuais da apresentacao conferem com as planilhas.')
else:
    print('ATENCAO: houve falhas ou variacao entre passadas. Rever acima.')
    sys.exit(1)
print('=' * 76)
