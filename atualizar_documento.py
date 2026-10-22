# -*- coding: utf-8 -*-
"""
Atualiza DMS_Base_Setembro26_Visao_Organizacional.docx:

1. Remove todos os travessoes (em dash U+2014, en dash U+2013).
2. Corrige a numeracao duplicada de secoes criada pela mesclagem das analises.
3. Integra a analise de posicoes em aberto (Vagas 21-10.xlsx) correlacionada
   com as areas E com os cargos da base de setembro, incluindo um dicionario
   de equivalencia de nomenclatura entre as duas planilhas.

Edicao IN PLACE: preserva o conteudo e a formatacao existentes.

Correlacao em dois niveis:
  - AREA  : a planilha de vagas usa "Air Operations" e a base usa
            "AIR OPERATIONS"; alem disso "Healthcare" na base e
            "HEALTHCARE INDUSTRY". O dicionario MAP resolve isso.
  - CARGO : termos como "INLAND" NAO aparecem na coluna AREA da base, apenas
            em "CARGO DRE 2026.2" (ex.: AIR OPS ANALYST INLAND USA). A
            correlacao por cargo mostra quantas pessoas ja ocupam cada cargo
            e marca os cargos que ainda nao existem na estrutura.
"""
import re
from collections import Counter, defaultdict

import openpyxl
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT

DOCX = 'DMS_Base_Setembro26_Visao_Organizacional.docx'
BASE = 'Base_Setembro26 (1).xlsx'
VAGAS = 'Vagas 21-10.xlsx'

EM, EN = '\u2014', '\u2013'
AZUL = RGBColor(0x1F, 0x3B, 0x63)
CINZA = RGBColor(0x55, 0x55, 0x55)

# colunas da base
B_NOME, B_SIT, B_POS, B_CARGO, B_AREA, B_HEAD, B_CL, B_TOT = 4, 6, 10, 11, 12, 13, 14, 21
# colunas das vagas
V_CL, V_AREA, V_CARGO, V_TIPOCUSTO = 1, 2, 3, 5
V_CONTRATADO, V_STATUS, V_CONTR, V_CUSTO, V_MES, V_OCUP = 6, 7, 8, 12, 13, 15


def num(v):
    if v is None or v == '-':
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def brl(v):
    return 'R$ ' + '{:,.0f}'.format(v).replace(',', '.')


def pct(v, base):
    if not base:
        return 'n/a'
    return '{:.1f}%'.format(v / base * 100).replace('.', ',')


# ==================== DADOS ====================
ws = openpyxl.load_workbook(BASE, data_only=True)['Setembro Unificado']
TODOS = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[B_NOME]]
ATIVOS = [r for r in TODOS if str(r[B_SIT]).strip().upper() == 'ATIVO']
N_A = len(ATIVOS)
CUSTO_A = sum(num(r[B_TOT]) for r in ATIVOS)

base_hc = Counter(r[B_AREA] for r in ATIVOS)
base_cargo_hc = Counter(str(r[B_CARGO]).strip().upper() for r in ATIVOS if r[B_CARGO])
base_cargos = set(base_cargo_hc)

wv = openpyxl.load_workbook(VAGAS, data_only=True)['Vagas']
VG = [r for r in wv.iter_rows(min_row=2, values_only=True)
      if r[V_CARGO] and str(r[V_CARGO]).strip() not in ('', 'None')]

# dicionario de equivalencia de nomenclatura entre as duas planilhas
MAP = {
    'Air Operations': 'AIR OPERATIONS',
    'Air Product': 'AIR PRODUCT',
    'Ocean Operations': 'OCEAN OPERATIONS',
    'Ocean Product': 'OCEAN PRODUCT',
    'Technology': 'TECHNOLOGY',
    'Financial': 'FINANCIAL',
    'Talent Management Team': 'TALENT MANAGEMENT TEAM',
    'Services': 'SERVICES',
    'Quality & Operational Intelligence': 'QUALITY & OPERATIONAL INTELLIGENCE',
    'Healthcare': 'HEALTHCARE INDUSTRY',
    'Automotive': 'AUTOMOTIVE INDUSTRY',
    'Overland (Europa)': 'OVERLAND',
    'High-Tech': None,
    'Special Operations': None,
}


def area_base(orig):
    """Traduz a area da planilha de vagas para a nomenclatura da base."""
    o = str(orig).strip()
    if o in MAP:
        return MAP[o]
    up = o.upper()
    return up if up in base_hc else None


def eh_aumento(r):
    return 'Aumento' in str(r[V_OCUP])


# agregacao por area (chave na nomenclatura da base; None = area nova)
vg = defaultdict(lambda: {'n': 0, 'aum': 0, 'sub': 0, 'cost': 0.0,
                          'cl': Counter(), 'orig': set()})
for r in VG:
    ab = area_base(r[V_AREA])
    key = ab if ab else '%s (area nova)' % str(r[V_AREA]).strip()
    d = vg[key]
    d['n'] += 1
    d['cost'] += num(r[V_CUSTO])
    d['cl'][str(r[V_CL]).strip()] += 1
    d['orig'].add(str(r[V_AREA]).strip())
    if eh_aumento(r):
        d['aum'] += 1
    else:
        d['sub'] += 1

TOT_VAGAS = len(VG)
TOT_AUM = sum(d['aum'] for d in vg.values())
TOT_SUB = sum(d['sub'] for d in vg.values())
TOT_CUSTO_V = sum(d['cost'] for d in vg.values())
HC_PROJ = N_A + TOT_AUM

# correlacao por cargo
cargos_novos = []
cargos_exist = []
for r in VG:
    cg = str(r[V_CARGO]).strip().upper()
    (cargos_exist if cg in base_cargos else cargos_novos).append(r)
N_CG_EXIST = len(cargos_exist)
N_CG_NOVO = len(cargos_novos)

# ==================== 1. REMOCAO DE TRAVESSOES ====================
ESPECIFICAS = [
    ('DMS ' + EM + ' Base de Setembro/2026', 'DMS: Base de Setembro/2026'),
    ('Insights ' + EM + ' Proporção', 'Insights: Proporção'),
    ('custo mensal ' + EM + ' é o maior', 'custo mensal, sendo o maior'),
    ('78 pessoas ' + EM + ' span muito', '78 pessoas, span muito'),
    ('30' + EN + '100%', '30% a 100%'),
]


def limpa(texto, is_heading):
    for a, b in ESPECIFICAS:
        texto = texto.replace(a, b)
    texto = re.sub(r'(\d)\s*' + EN + r'\s*(\d)', r'\1 a \2', texto)
    if is_heading:
        texto = re.sub(r'\s*[' + EM + EN + r']\s*', ': ', texto)
    else:
        texto = re.sub(r'\s*[' + EM + EN + r']\s*', ', ', texto)
    return texto


doc = Document(DOCX)


def conta_dashes(d):
    t = 0
    for p in d.paragraphs:
        t += p.text.count(EM) + p.text.count(EN)
    for tb in d.tables:
        for row in tb.rows:
            for c in row.cells:
                t += c.text.count(EM) + c.text.count(EN)
    return t


antes = conta_dashes(doc)


def trata(p):
    is_h = p.style.name.startswith(('Heading', 'Title'))
    for run in p.runs:
        if EM in run.text or EN in run.text:
            run.text = limpa(run.text, is_h)
    if EM in p.text or EN in p.text:
        full = limpa(p.text, is_h)
        if p.runs:
            p.runs[0].text = full
            for run in p.runs[1:]:
                run.text = ''


for p in doc.paragraphs:
    trata(p)
for tb in doc.tables:
    for row in tb.rows:
        for c in row.cells:
            for p in c.paragraphs:
                trata(p)

print('Travessoes: %d antes -> %d depois' % (antes, conta_dashes(doc)))

# ==================== 2. RENUMERACAO ====================
h1s = [p for p in doc.paragraphs if p.style.name == 'Heading 1']
print('\nRenumerando %d secoes:' % len(h1s))
for i, p in enumerate(h1s, start=1):
    novo = '%d. %s' % (i, re.sub(r'^\s*\d+\.\s*', '', p.text).strip())
    if p.runs:
        p.runs[0].text = novo
        for run in p.runs[1:]:
            run.text = ''
    print('   %s' % novo)

idx_ins = next((i for i, p in enumerate(h1s, start=1) if 'Insights' in p.text), None)
if idx_ins:
    for p in doc.paragraphs:
        if p.style.name == 'Heading 2' and re.match(r'^\s*\d+\.\d+', p.text):
            novo = re.sub(r'^\s*\d+\.(\d+)',
                          lambda m: '%d.%s' % (idx_ins, m.group(1)), p.text)
            if p.runs:
                p.runs[0].text = novo
                for run in p.runs[1:]:
                    run.text = ''

# ==================== 3. NOVA SECAO ====================
novos = []


def add_h(txt, lvl):
    p = doc.add_heading(txt, level=lvl)
    for r in p.runs:
        r.font.color.rgb = AZUL
    novos.append(p._p)
    return p


def add_p(txt, style=None):
    p = doc.add_paragraph(txt, style=style) if style else doc.add_paragraph(txt)
    novos.append(p._p)
    return p


def add_nota(txt):
    p = doc.add_paragraph()
    r = p.add_run(txt)
    r.italic = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = CINZA
    novos.append(p._p)
    return p


def add_tab(cols, linhas, fonte=8.5):
    t = doc.add_table(rows=1, cols=len(cols))
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cols):
        cell = t.rows[0].cells[i]
        cell.text = ''
        run = cell.paragraphs[0].add_run(c)
        run.bold = True
        run.font.size = Pt(fonte)
    for ln in linhas:
        cells = t.add_row().cells
        for i, v in enumerate(ln):
            cells[i].text = ''
            run = cells[i].paragraphs[0].add_run(str(v))
            run.font.size = Pt(fonte)
    novos.append(t._tbl)
    return t


SEC = len(h1s) + 1

# ---------------------------------------------------------------------------
# Blocos operacionais pedidos pela area: EUA, Europa e Brasil.
# A classificacao e feita pelo CARGO, nao pela AREA, porque termos como
# INLAND, AMERICAS, EUROPA, WH, CC e EXPORT so existem em "CARGO DRE 2026.2".
# ---------------------------------------------------------------------------
BLOCOS = [
    'EUA / Inland Freight America',
    'EUA / Operacoes America',
    'EUA / Warehouses (MIA, Houston, NY)',
    'Europa / Inland Freight Europa',
    'Europa / Operacoes Europa',
    'Brasil / Customer Care',
    'Brasil / Exportacao',
]


def bloco(cargo):
    c = str(cargo).upper()
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


b_at = Counter()
b_head = defaultdict(Counter)
b_vg = Counter()
b_aum = Counter()
b_sub = Counter()
b_cst = defaultdict(float)
b_mes = defaultdict(Counter)
b_st = defaultdict(Counter)
for r in ATIVOS:
    b = bloco(r[B_CARGO])
    if b:
        b_at[b] += 1
        b_head[b][r[B_HEAD]] += 1
for r in VG:
    b = bloco(r[V_CARGO])
    if b:
        b_vg[b] += 1
        b_cst[b] += num(r[V_CUSTO])
        b_mes[b][str(r[13]).strip()] += 1
        s = str(r[V_STATUS]).upper()
        b_st[b]['publicada' if 'ABERTA' in s else
                ('fechada' if 'FECHADA' in s else 'sem status')] += 1
        if eh_aumento(r):
            b_aum[b] += 1
        else:
            b_sub[b] += 1

# Volume de referencia do CIS (embarques/mes, media abr a set/26), informado
# pela area. O CIS nao informa headcount por area, portanto o volume e
# atribuido ao bloco geografico e nao a pessoa.
CIS_AEREO = {'EUA': 970, 'Europa': 530,
             'Brasil / Customer Care': 2287, 'Brasil / Exportacao': 244}
CIS_MARIT = {'EUA': 139, 'Brasil / Exportacao': 55}
EUA_BLOCOS = [b for b in BLOCOS if b.startswith('EUA')]
EUR_BLOCOS = [b for b in BLOCOS if b.startswith('Europa')]
at_eua = sum(b_at[b] for b in EUA_BLOCOS)
at_eur = sum(b_at[b] for b in EUR_BLOCOS)
at_cc = b_at['Brasil / Customer Care']
at_ex = b_at['Brasil / Exportacao']

TOT_AT_OP = sum(b_at[b] for b in BLOCOS)
TOT_VG_OP = sum(b_vg[b] for b in BLOCOS)


def dono(b):
    return ' / '.join(str(h).title() for h, _ in b_head[b].most_common(2) if h)


def ocup(b):
    """% do quadro em aberto = vagas / (ativos + vagas)."""
    d = b_at[b] + b_vg[b]
    return pct(b_vg[b], d) if d else 'n/a'


add_h('%d. Vagas em Aberto x Ocupacao nas Operacoes' % SEC, 1)
add_p('Cruzamento entre a estrutura de Operacoes e as {tv} posicoes em aberto (base de vagas de '
      '21/10), bloco por bloco. Os blocos sao identificados pelo cargo e nao pela area, porque '
      'termos como INLAND, AMERICAS, EUROPA, WH, CC e EXPORT existem apenas na coluna '
      '"CARGO DRE 2026.2" da base de setembro. Dos {tv} cargos em aberto, {ce} ja existem na '
      'estrutura e {cn} sao cargos novos; ao cruzar as planilhas, CCO deve ser lido como CMO e '
      '"Healthcare" como "HEALTHCARE INDUSTRY".'.format(tv=TOT_VAGAS, ce=N_CG_EXIST, cn=N_CG_NOVO))

# ---- 11.1 panorama ----
add_h('%d.1 Ocupacao, vagas e volume por bloco' % SEC, 2)
add_p('Tres metricas por bloco: percentual do quadro em aberto, volume de embarques por ativo e '
      'estagio do processo. O volume vem do CIS, media de abril a setembro de 2026.')

linhas = []
for b in BLOCOS:
    if b.startswith('EUA'):
        vol = '%d (bloco EUA)' % CIS_AEREO['EUA']
        vpa = '%.0f' % ((CIS_AEREO['EUA'] + CIS_MARIT['EUA']) / at_eua) if at_eua else 'n/a'
    elif b.startswith('Europa'):
        vol = '%d (bloco Europa)' % CIS_AEREO['Europa']
        vpa = '%.0f' % (CIS_AEREO['Europa'] / at_eur) if at_eur else 'n/a'
    elif b == 'Brasil / Customer Care':
        vol = '%d' % CIS_AEREO[b]
        vpa = '%.0f' % (CIS_AEREO[b] / at_cc) if at_cc else 'n/a'
    else:
        vol = '%d' % CIS_AEREO[b]
        vpa = '%.0f' % ((CIS_AEREO[b] + CIS_MARIT[b]) / at_ex) if at_ex else 'n/a'
    linhas.append([b, b_at[b], b_vg[b], ocup(b), b_aum[b], b_sub[b],
                   vol, vpa, brl(b_cst[b]), dono(b)])
linhas.append(['TOTAL blocos de Operacoes', TOT_AT_OP, TOT_VG_OP,
               pct(TOT_VG_OP, TOT_AT_OP + TOT_VG_OP),
               sum(b_aum[b] for b in BLOCOS), sum(b_sub[b] for b in BLOCOS),
               '', '', brl(sum(b_cst[b] for b in BLOCOS)), ''])
add_tab(['Bloco', 'Ativos', 'Vagas', '% quadro aberto', 'Aumento', 'Subst.',
         'Embarques aereos/mes (CIS)', 'Embarques por ativo', 'Custo vagas', 'Dono'],
        linhas, fonte=7)

add_nota('O volume por ativo do bloco EUA inclui os {m} embarques maritimos de Miami e o de '
         'Exportacao inclui os {e} maritimos. Nova York nao aparece como escritorio no CIS e '
         'precisa ser confirmada com a Operacao. Houston cresce: media de {h} por mes no periodo, '
         'porem {hc} por mes entre julho e setembro, alta de {ha}.'.format(
             m=CIS_MARIT['EUA'], e=CIS_MARIT['Brasil / Exportacao'], h=94, hc=169,
             ha=pct(169 - 94, 94)))

# ---- 11.2 pontos de atencao ----
add_h('%d.2 Onde esta o maior ponto de atencao' % SEC, 2)
_top = sorted(BLOCOS, key=lambda b: -(b_vg[b] / (b_at[b] + b_vg[b]) if b_at[b] + b_vg[b] else 0))
_b1, _b2 = _top[0], _top[1]
add_p('Quadro mais vazio: {b1} com {o1} do quadro em aberto ({a1} ativos e {v1} vagas) e {b2} com '
      '{o2} ({a2} ativos e {v2} vagas). Sao os dois blocos onde a operacao roda com metade da '
      'equipe prevista.'.format(
          b1=_b1, o1=ocup(_b1), a1=b_at[_b1], v1=b_vg[_b1],
          b2=_b2, o2=ocup(_b2), a2=b_at[_b2], v2=b_vg[_b2]),
      style='List Bullet')
add_p('Maior volume por pessoa: Exportacao Brasil absorve cerca de {v} embarques por ativo ao mes '
      'com apenas {a} pessoas e {o} do quadro em aberto. Customer Care vem em seguida, com cerca '
      'de {vc} por ativo, porem com equipe de {ac} pessoas e somente {oc} em aberto.'.format(
          v='%.0f' % ((CIS_AEREO['Brasil / Exportacao'] + CIS_MARIT['Brasil / Exportacao']) / at_ex),
          a=at_ex, o=ocup('Brasil / Exportacao'),
          vc='%.0f' % (CIS_AEREO['Brasil / Customer Care'] / at_cc), ac=at_cc,
          oc=ocup('Brasil / Customer Care')),
      style='List Bullet')
add_p('Risco silencioso nos Warehouses: {a} pessoas cobrem tres pracas (MIA, Houston e NY) e o '
      'bloco nao tem nenhuma vaga aberta, mesmo com Houston crescendo {ha}. E o unico bloco de '
      'Operacoes sem reforco previsto.'.format(
          a=b_at['EUA / Warehouses (MIA, Houston, NY)'], ha=pct(169 - 94, 94)),
      style='List Bullet')
_sem_st = sum(b_st[b]['sem status'] for b in BLOCOS)
add_p('Vaga parada ha mais tempo: a unica posicao com ciclo iniciado em marco e PER DEP ANALYST, '
      'em Talent Management Team, cerca de 7 meses em aberto. Nos blocos de Operacoes nao ha vaga '
      'anterior a outubro, porem {s} das {t} vagas estao sem estagio de processo informado, o que '
      'impede medir o tempo real de cada uma.'.format(s=_sem_st, t=TOT_VG_OP),
      style='List Bullet')

# ---- 11.3 plano de acao ----
add_h('%d.3 Plano de acao para a reuniao de 30 minutos' % SEC, 2)
add_p('Uma linha por frente critica, com acao, responsavel e prazo de efeito.')
ACOES = [
    ['Europa / Inland Freight Europa', ocup('Europa / Inland Freight Europa'),
     'Reaproveitar finalistas de processos recentes e indicacao interna com bonus',
     dono('Europa / Inland Freight Europa') + ' + RH', '1 a 3 semanas'],
    ['EUA / Operacoes America', ocup('EUA / Operacoes America'),
     'Vaga pre-aprovada com faixa e budget definidos, processo enxuto e cobertura '
     'temporaria pelo Brasil no back-office',
     dono('EUA / Operacoes America') + ' + RH', 'Imediato'],
    ['Brasil / Exportacao', ocup('Brasil / Exportacao'),
     'Processo enxuto e busca de profissionais de contratos encerrados, verificando '
     'nao aliciamento',
     dono('Brasil / Exportacao') + ' + RH', 'Imediato a 4 semanas'],
    ['EUA / Inland Freight America', ocup('EUA / Inland Freight America'),
     'Indicacao interna com bonus; as tres vagas ja estao publicadas',
     dono('EUA / Inland Freight America') + ' + RH', '2 a 3 semanas'],
    ['EUA / Warehouses (MIA, Houston, NY)', ocup('EUA / Warehouses (MIA, Houston, NY)'),
     'Validar necessidade de abrir vaga e contratar temporarios ou agencia para as tres pracas',
     dono('EUA / Warehouses (MIA, Houston, NY)') + ' + RH', '1 a 2 semanas'],
    ['Europa / Operacoes Europa', ocup('Europa / Operacoes Europa'),
     'Processo enxuto com triagem em 48 horas e proposta em 24 horas',
     dono('Europa / Operacoes Europa') + ' + RH', 'Imediato'],
    ['Brasil / Customer Care', ocup('Brasil / Customer Care'),
     'Processo enxuto e acompanhamento do volume por ativo',
     dono('Brasil / Customer Care') + ' + RH', 'Imediato'],
    ['Talent Management Team (PER DEP ANALYST)', 'vaga mais antiga',
     'Headhunter, por passar de 45 dias em aberto', 'Carolina Karnakis + RH', '3 a 4 semanas'],
]
add_tab(['Frente critica', '% quadro aberto', 'Acao', 'Dono', 'Prazo de efeito'],
        ACOES, fonte=7.5)

# ---- 11.4 lacunas ----
add_h('%d.4 Lacunas a confirmar na reuniao' % SEC, 2)
add_p('Nova York nao aparece como escritorio no CIS. Confirmar com a Operacao se ha volume '
      'proprio e quantas pessoas do bloco de Warehouses atendem a praca.', style='List Bullet')
add_p('{s} das {t} vagas de Operacoes estao sem estagio de processo informado e a base traz '
      'apenas o mes de inicio do ciclo, nao a data de abertura. Sem isso nao e possivel medir '
      'dias em aberto por vaga, metrica necessaria para acionar headhunter acima de 45 dias.'.format(
          s=_sem_st, t=TOT_VG_OP), style='List Bullet')
add_p('O CIS mostra quem executou cada etapa, mas nao o headcount por area, e o Customer Care do '
      'Brasil atende embarques de Miami. O volume por ativo deve ser lido como ordem de grandeza '
      'por bloco, nao como produtividade individual.', style='List Bullet')
add_p('Das areas sub-dimensionadas fora de Operacoes, sete seguem sem qualquer vaga: AEROSPACE '
      'INDUSTRY, COLD CHAIN, ENERGY INDUSTRY, INDUSTRIES DEVELOPMENT, STRATEGY & FINANCE, '
      'OPERATIONAL EXCELLENCE e REVENUE MANAGEMENT, somando 26 pessoas.', style='List Bullet')

# ==================== 4. CORRECOES DE CONSISTENCIA ====================
# 4a. Normaliza percentuais para o padrao brasileiro (virgula decimal).
#     As tabelas herdadas usavam "33.1%" e as novas "33,1%" no mesmo documento.
conv = 0
for tb in doc.tables:
    for row in tb.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    novo = re.sub(r'(\d)\.(\d+%)', r'\1,\2', run.text)
                    if novo != run.text:
                        run.text = novo
                        conv += 1
print('\nPercentuais convertidos para virgula decimal: %d' % conv)

# 4b. Completa a tabela de heads: faltavam os registros sem head identificado,
#     por isso a coluna de time somava 309 em vez dos 311 ativos.
def norm_head(h):
    """Consolida as grafias variantes de Ana Carol Vasconcellos, como ja faz
    a tabela existente no documento. Sem isso as variantes entrariam como
    linhas novas e o total passaria de 311."""
    if h and 'VASCONCELLOS' in str(h).upper():
        return 'ANA CAROL VASCONCELLOS'
    return h or 'EM BRANCO'


head_hc = Counter(norm_head(r[B_HEAD]) for r in ATIVOS)
head_cost = defaultdict(float)
head_area = defaultdict(Counter)
head_cl = defaultdict(Counter)
for r in ATIVOS:
    k = norm_head(r[B_HEAD])
    head_cost[k] += num(r[B_TOT])
    head_area[k][r[B_AREA]] += 1
    head_cl[k][r[B_CL]] += 1

t_head = next((t for t in doc.tables
               if t.rows[0].cells[0].text.strip() == 'Head'), None)
if t_head is not None:
    presentes = {t_head.rows[i].cells[0].text.strip()
                 for i in range(1, len(t_head.rows))}
    soma_antes = sum(head_hc.get(n, 0) for n in presentes)
    faltantes = [k for k in head_hc if k not in presentes]
    for k in sorted(faltantes, key=lambda x: -head_hc[x]):
        cells = t_head.add_row().cells
        cl = ', '.join(str(c) for c, _ in head_cl[k].most_common() if c) or 'nao informado'
        areas = '; '.join('%s (%d)' % (a, c) for a, c in head_area[k].most_common())
        vals = [k, cl, head_hc[k],
                'R$ ' + '{:,.0f}'.format(head_cost[k]).replace(',', '.'), areas]
        for i, v in enumerate(vals):
            cells[i].text = ''
            run = cells[i].paragraphs[0].add_run(str(v))
            run.font.size = Pt(8)
    soma_depois = sum(head_hc.get(t_head.rows[i].cells[0].text.strip(), 0)
                      for i in range(1, len(t_head.rows)))
    print('Tabela de heads: soma %d -> %d (ativos=%d); linhas adicionadas: %s'
          % (soma_antes, soma_depois, N_A, faltantes or 'nenhuma'))

# 4c. Acentuacao: o conteudo novo foi escrito sem acentos e o documento
#     original usa acentuacao correta. Normaliza para o portugues correto.
#     Frases primeiro (resolve a ambiguidade entre a conjuncao "e" e o verbo
#     "e"), depois palavras isoladas com limite de palavra.
FRASES = [
    ('A leitura central e a distincao', 'A leitura central é a distinção'),
    ('e essencial', 'é essencial'),
    ('que expande a estrutura', 'que expande a estrutura'),
    ('E a unica area', 'É a única área'),
    ('e menor que o total', 'é menor que o total'),
    ('A coluna "HC atual no cargo"', 'A coluna "HC atual no cargo"'),
    ('Services e a maior aposta', 'Services é a maior aposta'),
    ('Trata-se da mesma estrutura', 'Trata-se da mesma estrutura'),
    ('a correlacao desses', 'a correlação desses'),
    ('tem de ser feita por cargo', 'tem de ser feita por cargo'),
    ('nao retorna resultado', 'não retorna resultado'),
    ('o que dificulta o cruzamento direto', 'o que dificulta o cruzamento direto'),
    ('Ha dois pontos de atencao', 'Há dois pontos de atenção'),
    ('as vezes com nome curto', 'às vezes com nome curto'),
    ('e o dicionario usado', 'é o dicionário usado'),
    ('O C-Level tambem muda de nome', 'O C-Level também muda de nome'),
    ('nao possui CCO', 'não possui CCO'),
    ('nao possuem CMO', 'não possuem CMO'),
    ('como mostra a tabela de equivalencia abaixo',
     'como mostra a tabela de equivalência abaixo'),
    ('os headcounts coincidem', 'os headcounts coincidem'),
    ('deve ser lido como CMO', 'deve ser lido como CMO'),
    ('ja existem na base', 'já existem na base'),
    ('sao cargos novos', 'são cargos novos'),
    ('que a empresa ainda nao possui', 'que a empresa ainda não possui'),
    ('o que indica criacao de competencias',
     'o que indica criação de competências'),
    ('nao possuem qualquer posicao em aberto', 'não possuem qualquer posição em aberto'),
    ('estas sao as que seguem', 'estas são as que seguem'),
    ('aumenta em vez de diluir', 'aumenta em vez de diluir'),
    ('A area sai de', 'A área sai de'),
    ('sua participacao no quadro', 'sua participação no quadro'),
    ('O plano de contratacao reforca', 'O plano de contratação reforça'),
    ('ja apontada como risco', 'já apontada como risco'),
    ('todas de aumento de quadro', 'todas de aumento de quadro'),
    ('que muda de patamar', 'que muda de patamar'),
    ('deixando de ser uma posicao isolada', 'deixando de ser uma posição isolada'),
    ('Healthcare merece atencao', 'Healthcare merece atenção'),
    ('porem todas de substituicao', 'porém todas de substituição'),
    ('o volume de reposicao equivale', 'o volume de reposição equivale'),
    ('esta sendo inteiramente trocada e nao reforcada',
     'está sendo inteiramente trocada e não reforçada'),
    ('O gargalo de capacidade apontado na secao',
     'O gargalo de capacidade apontado na seção'),
    ('seguem sem qualquer posicao em aberto', 'seguem sem qualquer posição em aberto'),
    ('reunem', 'reúnem'),
    ('o gargalo de execucao dessas verticais', 'o gargalo de execução dessas verticais'),
    ('nao esta enderecado no ciclo atual', 'não está endereçado no ciclo atual'),
    ('seguranca da informacao', 'segurança da informação'),
    ('engenharia de dados, remuneracao e multimodal',
     'engenharia de dados, remuneração e multimodal'),
    ('Somam-se a duas areas que nao existem', 'Somam-se a duas áreas que não existem'),
    ('o custo verdadeiramente incremental', 'o custo verdadeiramente incremental'),
    ('precisa ser lido junto da folha ja existente',
     'precisa ser lido junto da folha já existente'),
    ('Esta secao cruza o quadro atual', 'Esta seção cruza o quadro atual'),
    ('que apenas repoe uma saida', 'que apenas repõe uma saída'),
    ('nao altera o headcount projetado', 'não altera o headcount projetado'),
    ('Cada posicao em aberto com o cargo', 'Cada posição em aberto com o cargo'),
    ('o que permite localizar na base', 'o que permite localizar na base'),
    ('indica posicao que ainda nao existe', 'indica posição que ainda não existe'),
    ('A projecao e o crescimento consideram', 'A projeção e o crescimento consideram'),
    ('pois as substituicoes repoem posicoes ja existentes',
     'pois as substituições repõem posições já existentes'),
    ('Cruzando com a secao de areas sub-dimensionadas',
     'Cruzando com a seção de áreas sub-dimensionadas'),
    ('sem plano de reforco', 'sem plano de reforço'),
    ('Entre os cargos novos aparecem funcoes de estruturacao',
     'Entre os cargos novos aparecem funções de estruturação'),
    ('o que explica a diferenca entre', 'o que explica a diferença entre'),
    ('existem apenas na base de setembro', 'existem apenas na base de setembro'),
    ('a linha combinada', 'a linha combinada'),
    ('parte desse valor repoe custo', 'parte desse valor repõe custo'),
    ('nao representa despesa incremental', 'não representa despesa incremental'),
    ('As duas bases usam nomenclaturas diferentes',
     'As duas bases usam nomenclaturas diferentes'),
    ('A planilha de vagas grava a area em caixa mista',
     'A planilha de vagas grava a área em caixa mista'),
    # secao 11 enxuta
    ('a classificacao e feita pelo cargo', 'a classificação é feita pelo cargo'),
    ('nao e possivel medir', 'não é possível medir'),
    ('o volume e atribuido ao bloco', 'o volume é atribuído ao bloco'),
    ('E o unico bloco de Operacoes', 'É o único bloco de Operações'),
    ('Sao os dois blocos', 'São os dois blocos'),
    ('Tres metricas por bloco', 'Três métricas por bloco'),
    ('e a unica posicao com ciclo', 'é a única posição com ciclo'),
    ('ja existem na estrutura', 'já existem na estrutura'),
    ('sao cargos novos', 'são cargos novos'),
    ('Os blocos sao identificados', 'Os blocos são identificados'),
    ('nao tem nenhuma vaga aberta', 'não tem nenhuma vaga aberta'),
    ('nao aparece como escritorio no CIS', 'não aparece como escritório no CIS'),
    ('precisa ser confirmada com a Operacao', 'precisa ser confirmada com a Operação'),
    ('Confirmar com a Operacao se ha volume',
     'Confirmar com a Operação se há volume'),
    ('estao sem estagio de processo informado',
     'estão sem estágio de processo informado'),
    ('a base traz apenas o mes de inicio do ciclo',
     'a base traz apenas o mês de início do ciclo'),
    ('nao a data de abertura', 'não a data de abertura'),
    ('mas nao o headcount por area', 'mas não o headcount por área'),
    ('nao como produtividade individual', 'não como produtividade individual'),
    ('verificando nao aliciamento', 'verificando não aliciamento'),
    ('por passar de 45 dias em aberto', 'por passar de 45 dias em aberto'),
    ('roda com metade da equipe prevista', 'roda com metade da equipe prevista'),
    ('porem com equipe de', 'porém com equipe de'),
    ('porem', 'porém'),
    ('as tres vagas ja estao publicadas', 'as três vagas já estão publicadas'),
    ('tres pracas', 'três praças'),
    ('Onde esta o maior ponto', 'Onde está o maior ponto'),
    ('Vaga parada ha mais tempo', 'Vaga parada há mais tempo'),
    ('nao ha vaga anterior a outubro', 'não há vaga anterior a outubro'),
    ('em marco e PER DEP ANALYST', 'em março é PER DEP ANALYST'),
    ('Confirmar com a Operacao se ha volume proprio',
     'Confirmar com a Operação se há volume próprio'),
    ('Vaga pre-aprovada', 'Vaga pré-aprovada'),
    ('pre-aprovada', 'pré-aprovada'),
]
PALAVRAS = {
    'Posicoes': 'Posições', 'posicoes': 'posições',
    'Posicao': 'Posição', 'posicao': 'posição',
    'NAO': 'NÃO', 'Numeros': 'Números', 'numeros': 'números',
    'Ocupacao': 'Ocupação', 'ocupacao': 'ocupação',
    'Operacoes': 'Operações', 'operacoes': 'operações',
    'Operacao': 'Operação', 'operacao': 'operação',
    'Acao': 'Ação', 'acao': 'ação', 'Acoes': 'Ações', 'acoes': 'ações',
    'reuniao': 'reunião', 'Reuniao': 'Reunião',
    'atencao': 'atenção', 'Atencao': 'Atenção',
    'metricas': 'métricas', 'metrica': 'métrica',
    'estagio': 'estágio', 'Estagio': 'Estágio',
    'aereo': 'aéreo', 'aereos': 'aéreos',
    'maritimo': 'marítimo', 'maritimos': 'marítimos',
    'mes': 'mês', 'Mes': 'Mês',
    'inicio': 'início', 'Inicio': 'Início',
    'Exportacao': 'Exportação', 'exportacao': 'exportação',
    'pracas': 'praças', 'praca': 'praça',
    'unico': 'único', 'Unico': 'Único',
    'reforco': 'reforço', 'bonus': 'bônus',
    'temporaria': 'temporária', 'temporarios': 'temporários',
    'agencia': 'agência', 'necessaria': 'necessária',
    'possivel': 'possível', 'proprio': 'próprio',
    'marco': 'março', 'tres': 'três', 'Tres': 'Três',
    'atribuido': 'atribuído', 'classificacao': 'classificação',
    'Freight': 'Freight', 'critica': 'crítica', 'criticas': 'críticas',
    'responsavel': 'responsável', 'periodo': 'período',
    'media': 'média', 'Indicacao': 'Indicação', 'indicacao': 'indicação',
    'Possidonio': 'Possidônio', 'Natalia': 'Natália',
    'Areas': 'Áreas', 'areas': 'áreas', 'Area': 'Área', 'area': 'área',
    'Correlacao': 'Correlação', 'correlacao': 'correlação',
    'projecao': 'projeção', 'Projecao': 'Projeção',
    'Situacao': 'Situação', 'situacao': 'situação',
    'substituicao': 'substituição', 'Substituicao': 'Substituição',
    'Subst': 'Subst', 'secao': 'seção', 'Secao': 'Seção',
    'dicionario': 'dicionário', 'Dicionario': 'Dicionário',
    'equivalencia': 'equivalência', 'nomenclatura': 'nomenclatura',
    'cargos': 'cargos', 'Cresc': 'Cresc',
    'nao': 'não', 'sao': 'são', 'ja': 'já', 'alem': 'além',
    'tambem': 'também', 'porem': 'porém', 'unica': 'única',
    'proximo': 'próximo', 'numero': 'número', 'varios': 'vários',
    'Ha': 'Há', 'As': 'As',
}
ap = 0
for tb in doc.tables:
    for row in tb.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    t0 = run.text
                    for a, b in FRASES:
                        run.text = run.text.replace(a, b)
                    for a, b in PALAVRAS.items():
                        run.text = re.sub(r'\b%s\b' % re.escape(a), b, run.text)
                    if run.text != t0:
                        ap += 1
for p in doc.paragraphs:
    for run in p.runs:
        t0 = run.text
        for a, b in FRASES:
            run.text = run.text.replace(a, b)
        for a, b in PALAVRAS.items():
            run.text = re.sub(r'\b%s\b' % re.escape(a), b, run.text)
        if run.text != t0:
            ap += 1
print('Trechos com acentuacao corrigida: %d' % ap)

doc.save(DOCX)
print('\nDocumento salvo: %s' % DOCX)
print('Vagas %d | aumento %d | subst %d | custo %s | HC proj %d | cargo existente %d / novo %d'
      % (TOT_VAGAS, TOT_AUM, TOT_SUB, brl(TOT_CUSTO_V), HC_PROJ, N_CG_EXIST, N_CG_NOVO))
