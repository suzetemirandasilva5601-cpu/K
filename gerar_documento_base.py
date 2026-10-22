# -*- coding: utf-8 -*-
"""
Gera documento Word com a visão da Base de Setembro/26 da DMS:
- Distribuição de ativos por cargo (nível/posição)
- Estrutura de administração: C-Level -> Head -> Área
- Custos por área e por C-Level
- Insights sobre proporção entre setores e áreas mais defasadas
"""
import openpyxl
from collections import Counter, defaultdict
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

ARQ = 'Base_Setembro26 (1).xlsx'
SAIDA = 'DMS_Base_Setembro26_Visao_Organizacional.docx'

# ---------------- Carga e preparação ----------------
wb = openpyxl.load_workbook(ARQ, data_only=True)
ws = wb['Setembro Unificado']
rows = list(ws.iter_rows(values_only=True))
header = rows[0]
idx = {h: i for i, h in enumerate(header)}
data = [r for r in rows[1:] if r[idx['NOME']]]
ativos = [r for r in data if str(r[idx['SITUAÇÃO']]).upper() == 'ATIVO']


def num(v):
    if v is None or v == '-':
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def normh(h):
    if h and 'VASCONCELLOS' in str(h).upper():
        return 'ANA CAROL VASCONCELLOS'
    return h or 'SEM HEAD'


def brl(v):
    return 'R$ {:,.0f}'.format(v).replace(',', '.')


TOTAL_CUSTO = sum(num(r[idx['TOTAL R$']]) for r in ativos)
N = len(ativos)

# ---------------- Agregações ----------------
pos_counter = Counter(r[idx['POSIÇÃO']] for r in ativos)
clevel_counter = Counter((r[idx['C-LEVEL']] or 'Sem C-Level') for r in ativos)

area_cnt = defaultdict(int)
area_cost = defaultdict(float)
for r in ativos:
    ar = r[idx['AREA']] or 'Sem Área'
    area_cnt[ar] += 1
    area_cost[ar] += num(r[idx['TOTAL R$']])

clevel_area = defaultdict(lambda: defaultdict(int))
clevel_cost = defaultdict(float)
for r in ativos:
    cl = r[idx['C-LEVEL']] or 'Sem C-Level'
    ar = r[idx['AREA']] or 'Sem Área'
    clevel_area[cl][ar] += 1
    clevel_cost[cl] += num(r[idx['TOTAL R$']])

heads = defaultdict(lambda: {'n': 0, 'cost': 0.0, 'areas': Counter(), 'cl': Counter()})
for r in ativos:
    h = normh(r[idx['HEAD']])
    heads[h]['n'] += 1
    heads[h]['cost'] += num(r[idx['TOTAL R$']])
    heads[h]['areas'][r[idx['AREA']]] += 1
    heads[h]['cl'][r[idx['C-LEVEL']]] += 1

# senioridade por área
LEAD = {'HEAD', 'C-LEVEL', 'SR. TEAM LEADER', 'TEAM LEADER', 'COORDINATOR', 'OWNERSHIP'}
JR = {'INTERN', 'APPRENTICE', 'ASSISTANT'}
area_sen = defaultdict(lambda: Counter())
for r in ativos:
    area_sen[r[idx['AREA']]][r[idx['POSIÇÃO']]] += 1

# ---------------- Documento ----------------
doc = Document()
# estilos base
normal = doc.styles['Normal']
normal.font.name = 'Calibri'
normal.font.size = Pt(10.5)

AZUL = RGBColor(0x1F, 0x3B, 0x63)
CINZA = RGBColor(0x55, 0x55, 0x55)


def h1(txt):
    p = doc.add_heading(txt, level=1)
    for run in p.runs:
        run.font.color.rgb = AZUL
    return p


def h2(txt):
    p = doc.add_heading(txt, level=2)
    for run in p.runs:
        run.font.color.rgb = AZUL
    return p


def tabela(cols, linhas, larguras=None):
    t = doc.add_table(rows=1, cols=len(cols))
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, c in enumerate(cols):
        hdr[i].text = ''
        run = hdr[i].paragraphs[0].add_run(c)
        run.bold = True
        run.font.size = Pt(9.5)
    for linha in linhas:
        cells = t.add_row().cells
        for i, val in enumerate(linha):
            cells[i].text = ''
            run = cells[i].paragraphs[0].add_run(str(val))
            run.font.size = Pt(9.5)
    return t


# ---- Capa / título ----
titulo = doc.add_heading('DMS — Base de Setembro/2026', level=0)
for run in titulo.runs:
    run.font.color.rgb = AZUL
sub = doc.add_paragraph('Visão Organizacional: Ativos por Cargo, Administração por Head/C-Level e Insights por Setor')
sub.runs[0].italic = True
sub.runs[0].font.color.rgb = CINZA
doc.add_paragraph('Documento gerado a partir da planilha "Base_Setembro26". '
                  'Escopo: colaboradores com situação ATIVO.')

# ---- 1. Resumo executivo ----
h1('1. Resumo Executivo')
entidades = Counter(r[idx['ENTIDADE']] for r in ativos)
contrato = Counter(r[idx['CONTRATO']] for r in ativos)
doc.add_paragraph(
    'A base de Setembro/26 contém {reg} registros considerados no mês; destes, '
    '{n} estão ATIVOS (os demais estão em aviso prévio, transição de contrato ou off boarding). '
    'O custo total mensal dos ativos é de {ct}, com custo médio de {cm} por pessoa.'.format(
        reg=len(data), n=N, ct=brl(TOTAL_CUSTO), cm=brl(TOTAL_CUSTO / N)))
doc.add_paragraph(
    'A operação é fortemente concentrada no Brasil ({br} de {n} ativos) e opera com cinco grandes '
    'frentes de liderança (C-Level): COO, CITO, CFSO, CMO e Co-CEO. '
    'A estrutura de contratação é predominantemente PJ ({pj}), seguida de CLT ({clt}) e estágio ({est}).'.format(
        br=entidades.get('DMS Brasil', 0), n=N,
        pj=contrato.get('PJ', 0), clt=contrato.get('CLT', 0), est=contrato.get('ESTAGIO', 0)))

# ---- 2. Distribuição por cargo / nível ----
h1('2. Distribuição de Ativos por Cargo (Nível)')
doc.add_paragraph(
    'Distribuição dos colaboradores ativos pelo nível hierárquico (coluna "POSIÇÃO"). '
    'A pirâmide é dominada pela base operacional (Analyst + Specialist + Assistant), '
    'o que é coerente com uma operação de serviços logísticos.')
linhas = []
for k, v in pos_counter.most_common():
    linhas.append([k, v, '{:.1f}%'.format(v / N * 100)])
tabela(['Cargo / Nível', 'Ativos', '% do total'], linhas)

base = pos_counter.get('ANALYST', 0) + pos_counter.get('SPECIALIST', 0) + pos_counter.get('ASSISTANT', 0)
lideranca = sum(v for k, v in pos_counter.items() if k in LEAD)
doc.add_paragraph(
    'Leitura: a base operacional (Analyst/Specialist/Assistant) soma {b} pessoas ({bp:.0f}%), '
    'enquanto a camada de liderança (Head, C-Level, Team Leaders e Coordenação) soma {l} pessoas ({lp:.0f}%). '
    'O programa de formação (Intern + Apprentice) representa {i} pessoas.'.format(
        b=base, bp=base / N * 100, l=lideranca, lp=lideranca / N * 100,
        i=pos_counter.get('INTERN', 0) + pos_counter.get('APPRENTICE', 0)))

# ---- 3. Administração: C-Level ----
h1('3. Quem Administra — Estrutura por C-Level')
doc.add_paragraph(
    'Distribuição dos ativos pelos cinco C-Levels. O COO concentra toda a operação core '
    '(Air/Ocean/Overland + Qualidade e Excelência Operacional), enquanto CMO lidera as '
    'verticais de indústria (Aerospace, Energy, Healthcare, Automotive, etc.).')
linhas = []
for cl, _ in clevel_counter.most_common():
    npeople = clevel_counter[cl]
    linhas.append([cl, npeople, '{:.1f}%'.format(npeople / N * 100),
                   brl(clevel_cost[cl]), '{:.1f}%'.format(clevel_cost[cl] / TOTAL_CUSTO * 100)])
tabela(['C-Level', 'Ativos', '% HC', 'Custo mensal', '% Custo'], linhas)

# ---- 4. C-Level -> Áreas ----
h1('4. Áreas sob cada C-Level')
for cl, _ in clevel_counter.most_common():
    tot = clevel_counter[cl]
    h2('{} — {} pessoas'.format(cl, tot))
    linhas = [[ar, c, '{:.1f}%'.format(c / tot * 100)]
              for ar, c in sorted(clevel_area[cl].items(), key=lambda x: -x[1])]
    tabela(['Área', 'Ativos', '% do C-Level'], linhas)

# ---- 5. Heads ----
h1('5. Quem Administra — Heads e seus Times')
doc.add_paragraph(
    'Mapeamento de cada Head (gestor direto) com o tamanho do seu time, área(s) e C-Level ao qual responde. '
    'Observação de qualidade de dados: grafias variantes de "Ana Carol Vasconcellos" foram consolidadas.')
linhas = []
for h, info in sorted(heads.items(), key=lambda x: -x[1]['n']):
    areas = '; '.join('{} ({})'.format(a, c) for a, c in info['areas'].most_common())
    cls = ', '.join(str(c) for c, _ in info['cl'].most_common() if c)
    linhas.append([h, cls or '—', info['n'], brl(info['cost']), areas])
tabela(['Head', 'C-Level', 'Time', 'Custo mensal', 'Área(s)'], linhas)

# ---- 6. Custo por área ----
h1('6. Custo e Headcount por Área')
doc.add_paragraph(
    'Áreas ordenadas por custo mensal. O custo médio por pessoa evidencia áreas com '
    'perfil mais sênior/estratégico (ex.: verticais de indústria e Overland) versus áreas '
    'de grande volume e perfil mais júnior (ex.: Technology e Financial).')
linhas = []
for ar in sorted(area_cost, key=lambda x: -area_cost[x]):
    c = area_cnt[ar]
    linhas.append([ar, c, '{:.1f}%'.format(c / N * 100), brl(area_cost[ar]),
                   '{:.1f}%'.format(area_cost[ar] / TOTAL_CUSTO * 100),
                   brl(area_cost[ar] / c)])
tabela(['Área', 'HC', '% HC', 'Custo mensal', '% Custo', 'Custo médio/pes'], linhas)

# ---- 7. Insights ----
h1('7. Insights — Proporção entre Setores e Áreas Defasadas')

h2('7.1 Concentração operacional')
doc.add_paragraph(
    'O COO responde por {coo} dos {n} ativos ({cp:.0f}%) e por {cc:.0f}% do custo. '
    'Dentro dele, Air Operations isoladamente tem {air} pessoas ({airp:.0f}% do total da empresa) e '
    '{airc} de custo mensal — é o maior centro de custo e de pessoas da DMS. '
    'Há dependência estrutural de uma única frente (Air), o que concentra risco operacional e de gestão.'.format(
        coo=clevel_counter['COO'], n=N, cp=clevel_counter['COO'] / N * 100,
        cc=clevel_cost['COO'] / TOTAL_CUSTO * 100,
        air=area_cnt['AIR OPERATIONS'], airp=area_cnt['AIR OPERATIONS'] / N * 100,
        airc=brl(area_cost['AIR OPERATIONS'])),
    style='List Bullet')

h2('7.2 Proporção Operação (core) vs. Produto vs. Indústrias (go-to-market)')
core = sum(area_cnt[a] for a in ['AIR OPERATIONS', 'OCEAN OPERATIONS', 'OVERLAND'])
produto = sum(area_cnt[a] for a in ['AIR PRODUCT', 'OCEAN PRODUCT'])
industrias = clevel_counter['CMO']
suporte = clevel_counter['CITO'] + clevel_counter['CFSO'] + clevel_counter['Co-CEO']
doc.add_paragraph(
    'Operação core (Air+Ocean+Overland): {core} pessoas ({cp:.0f}%). '
    'Produto (Air+Ocean Product): {prod} pessoas ({pp:.0f}%). '
    'Verticais de indústria/comercial (CMO): {ind} pessoas ({ip:.0f}%). '
    'Suporte (Tech+Financeiro+Talentos): {sup} pessoas ({sp:.0f}%).'.format(
        core=core, cp=core / N * 100, prod=produto, pp=produto / N * 100,
        ind=industrias, ip=industrias / N * 100, sup=suporte, sp=suporte / N * 100),
    style='List Bullet')
doc.add_paragraph(
    'A relação Produto/Operação é de ~1 para {r:.1f} pessoas de operação, indicando que o motor '
    'é a entrega operacional e que Produto atua enxuto.'.format(r=core / produto),
    style='List Bullet')

h2('7.3 Áreas mais defasadas (sub-dimensionadas)')
doc.add_paragraph(
    'As verticais de indústria, estratégicas para o crescimento comercial, estão com equipes muito reduzidas '
    'e com forte peso de liderança (quase sem base para executar). Isso sugere áreas "montadas no topo", '
    'dependentes de poucos indivíduos:')
defasadas = []
for ar in ['AEROSPACE INDUSTRY', 'HEALTHCARE INDUSTRY', 'ENERGY INDUSTRY', 'AUTOMOTIVE INDUSTRY',
           'COLD CHAIN', 'INDUSTRIES DEVELOPMENT', 'STRATEGY & FINANCE', 'OPERATIONAL EXCELLENCE',
           'REVENUE MANAGEMENT']:
    if ar in area_sen:
        comp = area_sen[ar]
        tot = sum(comp.values())
        nlead = sum(v for k, v in comp.items() if k in LEAD)
        njr = sum(v for k, v in comp.items() if k in JR)
        defasadas.append([ar, tot, nlead, njr, '{:.0f}%'.format(nlead / tot * 100)])
tabela(['Área sub-dimensionada', 'HC', 'Liderança', 'Base/Jr', '% Liderança'], defasadas)
doc.add_paragraph(
    'Padrão observado: em várias verticais de indústria a liderança representa 30–100% do time, '
    'ou seja, há Head/Specialist mas pouca ou nenhuma camada de execução júnior — sinal clássico '
    'de área nascente ou defasada em capacidade de entrega.')

h2('7.4 Risco de span of control e dados')
doc.add_paragraph(
    'Carol Mendoza (Air Operations) gere sozinha {n} pessoas — span muito acima do saudável, '
    'sugerindo necessidade de uma camada intermediária de coordenação.'.format(n=heads['CAROL MENDOZA']['n']),
    style='List Bullet')
doc.add_paragraph(
    'Alguns Heads (ex.: Jose Luiz, Raioni Santos) aparecem espalhados por múltiplas áreas e C-Levels, '
    'o que pode indicar acúmulo de função interina ou inconsistência de preenchimento da base.',
    style='List Bullet')
doc.add_paragraph(
    'Qualidade de dados: há variações de grafia para o mesmo Head e registros com HEAD/C-LEVEL em branco '
    'ou "N/A", que devem ser padronizados para análises futuras.',
    style='List Bullet')

# ---- Rodapé de notas ----
h1('8. Notas Metodológicas')
doc.add_paragraph('• Considerados apenas colaboradores ATIVOS (311 de 323 registros).', style='List Bullet')
doc.add_paragraph('• Custo = coluna "TOTAL R$" (salário + encargos + benefícios + outros + incentivo).', style='List Bullet')
doc.add_paragraph('• "Defasada/sub-dimensionada" = área com baixo headcount e alta proporção de liderança sem base de execução.', style='List Bullet')
doc.add_paragraph('• Variações de grafia de Heads foram consolidadas apenas para o caso "Ana Carol Vasconcellos".', style='List Bullet')

doc.save(SAIDA)
print('Documento gerado:', SAIDA)
print('Ativos:', N, '| Custo total:', brl(TOTAL_CUSTO))
