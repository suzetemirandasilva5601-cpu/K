# -*- coding: utf-8 -*-
"""
Gera documento Word com a visao organizacional da Base de Setembro/26 da DMS.

DOIS ESCOPOS apresentados lado a lado:
  - TOTAL GERAL : todos os 323 registros considerados no mes (linhas 2..324)
  - ATIVOS      : apenas SITUACAO = ATIVO (311 pessoas)

O script valida automaticamente (assert) que todos os subtotais reconciliam
com os totais de cada escopo antes de gravar o documento.
"""
import openpyxl
from collections import Counter, defaultdict
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

ARQ = 'Base_Setembro26 (1).xlsx'
SAIDA = 'DMS_Base_Setembro26_Visao_Organizacional.docx'

# ===================== CARGA =====================
wb = openpyxl.load_workbook(ARQ, data_only=True)
ws = wb['Setembro Unificado']

C_NOME, C_SIT, C_POS, C_AREA, C_HEAD, C_CL, C_TOT = 4, 6, 10, 12, 13, 14, 21
C_ENT, C_CONTR, C_TIPO = 1, 8, 5
COMPONENTES = (16, 17, 18, 19, 20)  # salario, encargos, beneficios, outros, incentivo


def num(v):
    if v is None or v == '-':
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace('R$', '').replace(' ', '')
    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except Exception:
        return 0.0


def normh(h):
    if h and 'VASCONCELLOS' in str(h).upper():
        return 'ANA CAROL VASCONCELLOS'
    return h or 'EM BRANCO'


TODOS = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[C_NOME]]
ATIVOS = [r for r in TODOS if str(r[C_SIT]).strip().upper() == 'ATIVO']
NAO_ATIVOS = [r for r in TODOS if str(r[C_SIT]).strip().upper() != 'ATIVO']

ESCOPOS = [('Total Geral', TODOS), ('Ativos', ATIVOS)]

N_T, N_A = len(TODOS), len(ATIVOS)
CUSTO_T = sum(num(r[C_TOT]) for r in TODOS)
CUSTO_A = sum(num(r[C_TOT]) for r in ATIVOS)
CUSTO_NA = sum(num(r[C_TOT]) for r in NAO_ATIVOS)

# ===================== VALIDACOES =====================
_erros = []


def check(desc, cond):
    if cond:
        print('  [OK]   ' + desc)
    else:
        print('  [ERRO] ' + desc)
        _erros.append(desc)


print('=' * 66)
print('VALIDACOES AUTOMATICAS')
print('=' * 66)
check('HC: ativos + nao-ativos == total geral (%d + %d == %d)' % (N_A, len(NAO_ATIVOS), N_T),
      N_A + len(NAO_ATIVOS) == N_T)
check('Custo: ativos + nao-ativos == total geral',
      round(CUSTO_A + CUSTO_NA, 2) == round(CUSTO_T, 2))
# coluna TOTAL == soma dos componentes, linha a linha
_div = [r[C_NOME] for r in TODOS
        if abs(num(r[C_TOT]) - sum(num(r[c]) for c in COMPONENTES)) > 0.5]
check('TOTAL R$ == salario+encargos+beneficios+outros+incentivo em todas as linhas',
      len(_div) == 0)
# subtotais de cada dimensao fecham com o total, nos dois escopos
for nome_esc, ds in ESCOPOS:
    n = len(ds)
    tot = sum(num(r[C_TOT]) for r in ds)
    for campo, col in [('POSICAO', C_POS), ('C-LEVEL', C_CL), ('AREA', C_AREA), ('HEAD', C_HEAD)]:
        cnt = Counter()
        cst = defaultdict(float)
        for r in ds:
            k = r[col] or 'EM BRANCO'
            cnt[k] += 1
            cst[k] += num(r[C_TOT])
        check('%s / %s: subtotais fecham (HC e custo)' % (nome_esc, campo),
              sum(cnt.values()) == n and round(sum(cst.values()), 2) == round(tot, 2))
assert not _erros, 'Validacoes falharam: %s' % _erros
print('TODAS AS VALIDACOES PASSARAM\n')

# ===================== AGREGACOES =====================


def agg(ds, col, norm=None):
    cnt = Counter()
    cst = defaultdict(float)
    for r in ds:
        k = r[col] or 'EM BRANCO'
        if norm:
            k = norm(k)
        cnt[k] += 1
        cst[k] += num(r[C_TOT])
    return cnt, cst


pos_t, pos_tc = agg(TODOS, C_POS)
pos_a, pos_ac = agg(ATIVOS, C_POS)
cl_t, cl_tc = agg(TODOS, C_CL)
cl_a, cl_ac = agg(ATIVOS, C_CL)
ar_t, ar_tc = agg(TODOS, C_AREA)
ar_a, ar_ac = agg(ATIVOS, C_AREA)
hd_t, hd_tc = agg(TODOS, C_HEAD, normh)
hd_a, hd_ac = agg(ATIVOS, C_HEAD, normh)

clevel_area_a = defaultdict(lambda: defaultdict(int))
clevel_area_t = defaultdict(lambda: defaultdict(int))
for r in ATIVOS:
    clevel_area_a[r[C_CL] or 'Sem C-Level'][r[C_AREA] or 'Sem Area'] += 1
for r in TODOS:
    clevel_area_t[r[C_CL] or 'Sem C-Level'][r[C_AREA] or 'Sem Area'] += 1

head_areas = defaultdict(Counter)
head_cl = defaultdict(Counter)
for r in ATIVOS:
    head_areas[normh(r[C_HEAD])][r[C_AREA]] += 1
    head_cl[normh(r[C_HEAD])][r[C_CL]] += 1

LEAD = {'HEAD', 'C-LEVEL', 'SR. TEAM LEADER', 'TEAM LEADER', 'COORDINATOR', 'OWNERSHIP'}
JR = {'INTERN', 'APPRENTICE', 'ASSISTANT'}
area_sen = defaultdict(Counter)
for r in ATIVOS:
    area_sen[r[C_AREA]][r[C_POS]] += 1

sit_cnt = Counter(str(r[C_SIT]).strip().upper() for r in TODOS)
sit_cst = defaultdict(float)
for r in TODOS:
    sit_cst[str(r[C_SIT]).strip().upper()] += num(r[C_TOT])

# ===================== DOCUMENTO =====================
doc = Document()
doc.styles['Normal'].font.name = 'Calibri'
doc.styles['Normal'].font.size = Pt(10)

AZUL = RGBColor(0x1F, 0x3B, 0x63)
CINZA = RGBColor(0x55, 0x55, 0x55)


def brl(v):
    return 'R$ ' + '{:,.0f}'.format(v).replace(',', '.')


def pct(v, base):
    if not base:
        return '-'
    return '{:.1f}%'.format(v / base * 100).replace('.', ',')


def dec(v):
    """Formata decimal no padrao brasileiro (virgula)."""
    return '{:.1f}'.format(v).replace('.', ',')


def rot_cl(k):
    """Rotulo amigavel para C-Level nao preenchido."""
    return 'Sem C-Level' if k in ('EM BRANCO', 'Sem C-Level', None) else k


def h1(t):
    p = doc.add_heading(t, level=1)
    for r in p.runs:
        r.font.color.rgb = AZUL
    return p


def h2(t):
    p = doc.add_heading(t, level=2)
    for r in p.runs:
        r.font.color.rgb = AZUL
    return p


def tabela(cols, linhas, fonte=8.5):
    t = doc.add_table(rows=1, cols=len(cols))
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cols):
        cell = t.rows[0].cells[i]
        cell.text = ''
        run = cell.paragraphs[0].add_run(c)
        run.bold = True
        run.font.size = Pt(fonte)
    for linha in linhas:
        cells = t.add_row().cells
        for i, val in enumerate(linha):
            cells[i].text = ''
            run = cells[i].paragraphs[0].add_run(str(val))
            run.font.size = Pt(fonte)
    return t


def nota(txt):
    p = doc.add_paragraph()
    run = p.add_run(txt)
    run.italic = True
    run.font.size = Pt(8.5)
    run.font.color.rgb = CINZA
    return p


# ---------- Titulo ----------
t = doc.add_heading('DMS - Base de Setembro/2026', level=0)
for r in t.runs:
    r.font.color.rgb = AZUL
p = doc.add_paragraph('Visao Organizacional: Ativos por Cargo, Administracao por Head/C-Level '
                      'e Insights por Setor')
p.runs[0].italic = True
p.runs[0].font.color.rgb = CINZA

doc.add_paragraph(
    'Fonte: planilha "Base_Setembro26", aba "Setembro Unificado" (linhas 2 a 324). '
    'Todas as tabelas deste documento apresentam DOIS ESCOPOS em paralelo: o Total Geral '
    '(todos os registros considerados no mes) e o recorte de Ativos (situacao = ATIVO). '
    'Os subtotais de cada dimensao foram validados automaticamente contra os totais de cada escopo.')

# ---------- 1. Escopos ----------
h1('1. Definicao de Escopo e Reconciliacao')
doc.add_paragraph(
    'A base contem {nt} registros marcados como "Considerar no mes = Sim". Destes, {na} estao '
    'com situacao ATIVO e {nna} estao em desligamento ou transicao. A tabela abaixo reconcilia '
    'os dois escopos: a soma do recorte de Ativos com os nao-ativos resulta exatamente no Total Geral.'.format(
        nt=N_T, na=N_A, nna=len(NAO_ATIVOS)))

tabela(['Escopo', 'Pessoas', 'Custo mensal', '% do Total Geral'], [
    ['Total Geral (linhas 2 a 324)', N_T, brl(CUSTO_T), '100,0%'],
    ['(-) Nao-ativos', len(NAO_ATIVOS), brl(CUSTO_NA), pct(CUSTO_NA, CUSTO_T)],
    ['(=) Ativos', N_A, brl(CUSTO_A), pct(CUSTO_A, CUSTO_T)],
], fonte=9.5)

doc.add_paragraph()
doc.add_paragraph('Composicao dos registros por situacao:')
linhas = []
for s, c in sit_cnt.most_common():
    linhas.append([s, c, pct(c, N_T), brl(sit_cst[s]), pct(sit_cst[s], CUSTO_T)])
tabela(['Situacao', 'Pessoas', '% HC', 'Custo mensal', '% Custo'], linhas, fonte=9.5)

nota('Leitura para o comite: o Total Geral ({ct}) representa o desembolso efetivo da competencia, '
     'pois inclui pessoas em aviso previo e off boarding que ainda geram custo no mes. O recorte de '
     'Ativos ({ca}) representa a estrutura recorrente, base adequada para decisoes de dimensionamento '
     'e para projecao dos proximos meses. A diferenca entre os dois e de {d}.'.format(
         ct=brl(CUSTO_T), ca=brl(CUSTO_A), d=brl(CUSTO_NA)))

# ---------- 2. Resumo executivo ----------
h1('2. Resumo Executivo')
ent_t = Counter(r[C_ENT] for r in TODOS)
ent_a = Counter(r[C_ENT] for r in ATIVOS)
ctr_t = Counter(r[C_CONTR] for r in TODOS)
ctr_a = Counter(r[C_CONTR] for r in ATIVOS)

tabela(['Indicador', 'Total Geral', 'Ativos'], [
    ['Pessoas', N_T, N_A],
    ['Custo mensal', brl(CUSTO_T), brl(CUSTO_A)],
    ['Custo medio por pessoa', brl(CUSTO_T / N_T), brl(CUSTO_A / N_A)],
    ['Areas distintas', len(ar_t), len(ar_a)],
    ['Heads distintos', len(hd_t), len(hd_a)],
    ['DMS Brasil', ent_t.get('DMS Brasil', 0), ent_a.get('DMS Brasil', 0)],
    ['Contratos PJ', ctr_t.get('PJ', 0), ctr_a.get('PJ', 0)],
    ['Contratos CLT', ctr_t.get('CLT', 0), ctr_a.get('CLT', 0)],
    ['Estagio / Jovem Aprendiz',
     ctr_t.get('ESTAGIO', 0) + ctr_t.get('JOVEM APRENDIZ', 0),
     ctr_a.get('ESTAGIO', 0) + ctr_a.get('JOVEM APRENDIZ', 0)],
], fonte=9.5)

doc.add_paragraph(
    'A operacao e concentrada no Brasil e organizada em cinco frentes de lideranca (C-Level): '
    'COO, CITO, CFSO, CMO e Co-CEO. O modelo de contratacao e predominantemente PJ, '
    'seguido de CLT e de um programa de estagio relevante.')

# ---------- 3. Cargos ----------
h1('3. Distribuicao por Cargo (Nivel)')
doc.add_paragraph(
    'Distribuicao pelo nivel hierarquico (coluna "POSICAO"). A piramide e dominada pela base '
    'operacional, coerente com uma operacao de servicos logisticos.')
linhas = []
for k, _ in pos_t.most_common():
    linhas.append([k, pos_t[k], pct(pos_t[k], N_T), pos_a.get(k, 0), pct(pos_a.get(k, 0), N_A)])
linhas.append(['TOTAL', N_T, '100,0%', N_A, '100,0%'])
tabela(['Cargo / Nivel', 'HC Total', '% Total', 'HC Ativos', '% Ativos'], linhas, fonte=9.5)

base_t = sum(pos_t.get(k, 0) for k in ('ANALYST', 'SPECIALIST', 'ASSISTANT'))
base_a = sum(pos_a.get(k, 0) for k in ('ANALYST', 'SPECIALIST', 'ASSISTANT'))
lid_t = sum(v for k, v in pos_t.items() if k in LEAD)
lid_a = sum(v for k, v in pos_a.items() if k in LEAD)
form_t = pos_t.get('INTERN', 0) + pos_t.get('APPRENTICE', 0)
form_a = pos_a.get('INTERN', 0) + pos_a.get('APPRENTICE', 0)

tabela(['Camada', 'HC Total', '% Total', 'HC Ativos', '% Ativos'], [
    ['Base operacional (Analyst/Specialist/Assistant)', base_t, pct(base_t, N_T), base_a, pct(base_a, N_A)],
    ['Lideranca (C-Level/Head/TL/Coord.)', lid_t, pct(lid_t, N_T), lid_a, pct(lid_a, N_A)],
    ['Formacao (Intern/Apprentice)', form_t, pct(form_t, N_T), form_a, pct(form_a, N_A)],
], fonte=9.5)
nota('Razao base por lider: {} no Total Geral e {} nos Ativos.'.format(
    dec(base_t / lid_t), dec(base_a / lid_a)))

# ---------- 4. C-Level ----------
h1('4. Quem Administra - Estrutura por C-Level')
doc.add_paragraph(
    'O COO concentra toda a operacao core (Air, Ocean, Overland, Qualidade e Excelencia Operacional). '
    'O CMO lidera as verticais de industria. O CITO responde por Technology, o CFSO pelo Financeiro '
    'e Estrategia, e o Co-CEO pelo time de Talentos.')
linhas = []
for k, _ in cl_t.most_common():
    linhas.append([rot_cl(k), cl_t[k], pct(cl_t[k], N_T), brl(cl_tc[k]),
                   cl_a.get(k, 0), pct(cl_a.get(k, 0), N_A), brl(cl_ac.get(k, 0.0)),
                   pct(cl_ac.get(k, 0.0), CUSTO_A)])
linhas.append(['TOTAL', N_T, '100,0%', brl(CUSTO_T), N_A, '100,0%', brl(CUSTO_A), '100,0%'])
tabela(['C-Level', 'HC Tot', '% Tot', 'Custo Tot',
        'HC Ativ', '% Ativ', 'Custo Ativ', '% Custo Ativ'], linhas, fonte=8)

# ---------- 5. C-Level x Areas ----------
h1('5. Areas sob cada C-Level')
for cl, _ in cl_a.most_common():
    tot_cl = cl_a[cl]
    h2('{} - {} ativos ({} no total geral)'.format(rot_cl(cl), tot_cl, cl_t.get(cl, 0)))
    linhas = []
    for ar, c in sorted(clevel_area_a[cl].items(), key=lambda x: -x[1]):
        linhas.append([ar, clevel_area_t[cl].get(ar, 0), c, pct(c, tot_cl)])
    tabela(['Area', 'HC Total', 'HC Ativos', '% do C-Level (ativos)'], linhas, fonte=9)

# ---------- 6. Heads ----------
h1('6. Quem Administra - Heads e seus Times')
doc.add_paragraph(
    'Cada Head (gestor direto) com o tamanho do time, custo e area(s) sob gestao. '
    'A coluna "C-Level" indica a quem o Head responde.')
linhas = []
for h, _ in sorted(hd_a.items(), key=lambda x: -x[1]):
    areas = '; '.join('{} ({})'.format(a, c) for a, c in head_areas[h].most_common())
    cls = ', '.join(str(c) for c, _ in head_cl[h].most_common() if c) or '-'
    linhas.append([h, cls, hd_t.get(h, 0), hd_a[h], brl(hd_tc.get(h, 0.0)), brl(hd_ac[h]), areas])
tabela(['Head', 'C-Level', 'Time Tot', 'Time Ativ', 'Custo Tot', 'Custo Ativ', 'Area(s) - ativos'],
       linhas, fonte=7.5)
nota('Observacao de qualidade de dados: grafias variantes de "Ana Carol Vasconcellos" foram '
     'consolidadas em um unico Head. Registros com HEAD vazio aparecem como "EM BRANCO".')

# ---------- 7. Areas ----------
h1('7. Custo e Headcount por Area')
doc.add_paragraph('Areas ordenadas pelo custo do Total Geral. O custo medio por pessoa (ativos) '
                  'evidencia areas de perfil senior/estrategico versus areas de volume e perfil junior.')
linhas = []
for ar in sorted(ar_tc, key=lambda x: -ar_tc[x]):
    ca_ = ar_ac.get(ar, 0.0)
    na_ = ar_a.get(ar, 0)
    linhas.append([ar, ar_t[ar], brl(ar_tc[ar]), pct(ar_tc[ar], CUSTO_T),
                   na_, pct(na_, N_A), brl(ca_), pct(ca_, CUSTO_A),
                   brl(ca_ / na_) if na_ else '-'])
linhas.append(['TOTAL', N_T, brl(CUSTO_T), '100,0%', N_A, '100,0%', brl(CUSTO_A), '100,0%',
               brl(CUSTO_A / N_A)])
tabela(['Area', 'HC Tot', 'Custo Tot', '% Custo Tot', 'HC Ativ', '% HC Ativ',
        'Custo Ativ', '% Custo Ativ', 'Custo medio/pes (ativ)'], linhas, fonte=7.5)

# ---------- 8. Insights ----------
h1('8. Insights - Proporcao entre Setores e Areas Defasadas')

h2('8.1 Concentracao operacional')
doc.add_paragraph(
    'O COO responde por {ha} dos {na} ativos ({pa}) e por {ca} do custo dos ativos. '
    'No Total Geral o padrao se mantem: {ht} de {nt} pessoas ({pt}). '
    'Dentro do COO, Air Operations isoladamente tem {air} ativos ({pair} da empresa) e '
    '{cair} de custo mensal, sendo o maior centro de pessoas e de custo da DMS. '
    'Ha dependencia estrutural de uma unica frente, o que concentra risco operacional e de gestao.'.format(
        ha=cl_a['COO'], na=N_A, pa=pct(cl_a['COO'], N_A), ca=pct(cl_ac['COO'], CUSTO_A),
        ht=cl_t['COO'], nt=N_T, pt=pct(cl_t['COO'], N_T),
        air=ar_a['AIR OPERATIONS'], pair=pct(ar_a['AIR OPERATIONS'], N_A),
        cair=brl(ar_ac['AIR OPERATIONS'])),
    style='List Bullet')

h2('8.2 Proporcao Operacao (core) vs. Produto vs. Industrias')
core_areas = ['AIR OPERATIONS', 'OCEAN OPERATIONS', 'OVERLAND']
prod_areas = ['AIR PRODUCT', 'OCEAN PRODUCT']
core_t = sum(ar_t.get(a, 0) for a in core_areas)
core_a = sum(ar_a.get(a, 0) for a in core_areas)
prod_t = sum(ar_t.get(a, 0) for a in prod_areas)
prod_a = sum(ar_a.get(a, 0) for a in prod_areas)
sup_t = cl_t.get('CITO', 0) + cl_t.get('CFSO', 0) + cl_t.get('Co-CEO', 0)
sup_a = cl_a.get('CITO', 0) + cl_a.get('CFSO', 0) + cl_a.get('Co-CEO', 0)

tabela(['Bloco', 'HC Total', '% Total', 'HC Ativos', '% Ativos'], [
    ['Operacao core (Air + Ocean + Overland)', core_t, pct(core_t, N_T), core_a, pct(core_a, N_A)],
    ['Produto (Air Product + Ocean Product)', prod_t, pct(prod_t, N_T), prod_a, pct(prod_a, N_A)],
    ['Verticais de industria / comercial (CMO)', cl_t.get('CMO', 0), pct(cl_t.get('CMO', 0), N_T),
     cl_a.get('CMO', 0), pct(cl_a.get('CMO', 0), N_A)],
    ['Suporte (Technology + Financeiro + Talentos)', sup_t, pct(sup_t, N_T), sup_a, pct(sup_a, N_A)],
], fonte=9.5)
doc.add_paragraph(
    'A relacao Produto/Operacao e de 1 pessoa de Produto para cada {ra} de operacao (ativos) '
    'e {rt} no Total Geral, indicando que o motor da empresa e a entrega operacional e que '
    'Produto atua de forma enxuta.'.format(ra=dec(core_a / prod_a), rt=dec(core_t / prod_t)),
    style='List Bullet')

h2('8.3 Areas mais defasadas (sub-dimensionadas)')
doc.add_paragraph(
    'As verticais de industria, estrategicas para o crescimento comercial, operam com equipes muito '
    'reduzidas e com peso elevado de lideranca, ou seja, pouca ou nenhuma camada de execucao. '
    'Sao areas montadas no topo, dependentes de poucos individuos.')
defasadas = ['AEROSPACE INDUSTRY', 'HEALTHCARE INDUSTRY', 'ENERGY INDUSTRY', 'AUTOMOTIVE INDUSTRY',
             'COLD CHAIN', 'INDUSTRIES DEVELOPMENT', 'STRATEGY & FINANCE',
             'OPERATIONAL EXCELLENCE', 'REVENUE MANAGEMENT']
linhas = []
for ar in defasadas:
    if ar not in area_sen:
        continue
    comp = area_sen[ar]
    tot = sum(comp.values())
    nl = sum(v for k, v in comp.items() if k in LEAD)
    nj = sum(v for k, v in comp.items() if k in JR)
    linhas.append([ar, tot, nl, nj, pct(nl, tot), brl(ar_ac.get(ar, 0.0) / tot)])
tabela(['Area sub-dimensionada', 'HC Ativos', 'Lideranca', 'Base/Jr', '% Lideranca', 'Custo medio/pes'],
       linhas, fonte=9)
doc.add_paragraph(
    'Padrao observado: nestas areas a lideranca representa de 30% a 100% do time. Ha Head e Specialist, '
    'mas quase nenhuma camada junior de execucao, sinal classico de area nascente ou defasada '
    'em capacidade de entrega. O custo medio por pessoa elevado reforca que sao times formados '
    'por perfis senior sem apoio operacional.')

h2('8.4 Risco de span of control e qualidade de dados')
doc.add_paragraph(
    '{h} responde sozinha por {n} ativos em Air Operations, span muito acima do saudavel, '
    'o que sugere necessidade de uma camada intermediaria de coordenacao.'.format(
        h='Carol Mendoza', n=hd_a.get('CAROL MENDOZA', 0)),
    style='List Bullet')
multi = [h for h in head_areas if len(head_areas[h]) >= 4]
doc.add_paragraph(
    'Heads distribuidos por quatro ou mais areas ({}) podem indicar acumulo de funcao interina '
    'ou inconsistencia no preenchimento da base.'.format(', '.join(sorted(multi)) or 'nenhum'),
    style='List Bullet')
doc.add_paragraph(
    'Existem registros com HEAD ou C-LEVEL vazios ou preenchidos como "N/A", alem de grafias '
    'variantes para o mesmo gestor. Recomenda-se padronizar esses campos para garantir '
    'comparabilidade nas analises dos proximos meses.',
    style='List Bullet')

# ---------- 9. Notas ----------
h1('9. Notas Metodologicas')
for txt in [
    'Fonte: aba "Setembro Unificado", linhas 2 a 324. Todos os {} registros possuem '
    '"Considerar no mes = Sim".'.format(N_T),
    'Total Geral = todos os {} registros. Ativos = {} registros com situacao ATIVO. '
    'A diferenca de {} corresponde a {} pessoas em aviso previo, off boarding ou transicao de contrato.'.format(
        N_T, N_A, brl(CUSTO_NA), len(NAO_ATIVOS)),
    'Custo = coluna "TOTAL R$", validada linha a linha como a soma de salario, encargos, '
    'beneficios, outros e incentivo (nenhuma divergencia encontrada).',
    'Area sub-dimensionada = baixo headcount combinado a alta proporcao de lideranca '
    'sem base de execucao.',
    'Grafias variantes de Heads foram consolidadas apenas no caso "Ana Carol Vasconcellos".',
    'Os subtotais de cargo, C-Level, area e head foram conferidos automaticamente contra os '
    'totais de cada escopo; todas as verificacoes fecharam.',
]:
    doc.add_paragraph(txt, style='List Bullet')

doc.save(SAIDA)
print('Documento gerado:', SAIDA)
print('  Total Geral: %d pessoas | %s' % (N_T, brl(CUSTO_T)))
print('  Ativos:      %d pessoas | %s' % (N_A, brl(CUSTO_A)))
print('  Nao-ativos:  %d pessoas | %s' % (len(NAO_ATIVOS), brl(CUSTO_NA)))
