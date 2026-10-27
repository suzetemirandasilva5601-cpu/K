# -*- coding: utf-8 -*-
"""
Modelo financeiro do Projeto Asia (China) em Excel, com FORMULAS VIVAS.

O usuario muda as premissas (celulas amarelas) e tudo recalcula:
- Premissas editaveis (pool, custo, taxa RS, % captura)
- Resultado (captura liquida, resultado anual, break-even)
- Matriz de sensibilidade: % captura (linhas) x taxa RS (colunas), com
  formatacao condicional verde/vermelho no ponto de equilibrio.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.utils import get_column_letter

SAIDA = 'DMS - Modelo Financeiro Projeto Asia.xlsx'

AZUL = 'FF005E9E'
AZULCLARO = 'FFE5F0F8'
AMARELO = 'FFFFF2CC'      # celula editavel
CINZA = 'FFF2F2F2'
VERDE = 'FFC6EFCE'
VERMELHO = 'FFFFC7CE'
branco = Font(color='FFFFFFFF', bold=True, size=11)
titfont = Font(bold=True, size=14, color=AZUL)
bold = Font(bold=True)
ital = Font(italic=True, size=8, color='FF555555')
center = Alignment(horizontal='center', vertical='center')
left = Alignment(horizontal='left', vertical='center', wrap_text=True)
thin = Side(style='thin', color='FFBFBFBF')
bd = Border(left=thin, right=thin, top=thin, bottom=thin)
edit_fill = PatternFill('solid', fgColor=AMARELO)
az_fill = PatternFill('solid', fgColor=AZULCLARO)

wb = openpyxl.Workbook()

# ============ ABA 1: MODELO ============
sh = wb.active
sh.title = 'Modelo'
sh['A1'] = 'Projeto Asia (China) - Modelo Financeiro do Headcount'
sh['A1'].font = titfont
sh.merge_cells('A1:E1')
sh['A2'] = 'Celulas amarelas sao editaveis. Tudo recalcula automaticamente. Valores anuais em R$.'
sh['A2'].font = ital
sh.merge_cells('A2:E2')


def rotulo(cel, texto, b=True):
    sh[cel] = texto
    sh[cel].font = bold if b else Font()
    sh[cel].alignment = left


def valor(cel, v, fmt=None, editavel=False, formula=False):
    sh[cel] = v
    sh[cel].alignment = center
    sh[cel].border = bd
    if fmt:
        sh[cel].number_format = fmt
    if editavel:
        sh[cel].fill = edit_fill
        sh[cel].font = bold
    elif formula:
        sh[cel].fill = az_fill


# --- PREMISSAS ---
sh['A4'] = 'PREMISSAS (editaveis)'
sh['A4'].font = branco
sh['A4'].fill = PatternFill('solid', fgColor=AZUL)
sh.merge_cells('A4:C4')

premissas = [
    ('A5', 'B5', 'Pool Profit OFF a agentes (12m)', 2040000, 'R$ #,##0'),
    ('A6', 'B6', 'Parcela "intelectual" capturavel do pool (%)', 0.70, '0%'),
    ('A7', 'B7', 'Custo do headcount (salario + encargos)', 600000, 'R$ #,##0'),
    ('A8', 'B8', 'Taxa de estrutura da RS (% sobre captura)', 0.15, '0%'),
    ('A9', 'B9', '% de captura do pool capturavel (meta)', 0.30, '0%'),
]
for ar, br, txt, v, fmt in premissas:
    rotulo(ar, txt)
    valor(br, v, fmt, editavel=True)
sh['C6'] = 'parte do pool que 1 pessoa consegue negociar (resto e transacional)'
sh['C8'] = 'taxa que a RS cobra para hospedar o headcount (ponto em aberto)'
sh['C9'] = 'quanto do pool capturavel o profissional efetivamente traz'
for c in ('C6', 'C8', 'C9'):
    sh[c].font = ital
    sh[c].alignment = left

# --- RESULTADO ---
sh['A11'] = 'RESULTADO (calculado)'
sh['A11'].font = branco
sh['A11'].fill = PatternFill('solid', fgColor=AZUL)
sh.merge_cells('A11:C11')

calc = [
    ('A12', 'B12', 'Pool capturavel (R$)', '=B5*B6', 'R$ #,##0'),
    ('A13', 'B13', 'Captura bruta (R$)', '=B12*B9', 'R$ #,##0'),
    ('A14', 'B14', 'Taxa paga a RS (R$)', '=B13*B8', 'R$ #,##0'),
    ('A15', 'B15', 'Captura liquida (R$)', '=B13-B14', 'R$ #,##0'),
    ('A16', 'B16', 'Resultado anual (liquida - custo)', '=B15-B7', 'R$ #,##0'),
    ('A17', 'B17', 'Cobertura do custo (liquida / custo)', '=B15/B7', '0%'),
]
for ar, br, txt, f, fmt in calc:
    rotulo(ar, txt)
    valor(br, f, fmt, formula=True)

# break-even: % de captura que zera o resultado, dado taxa RS e custo
sh['A19'] = 'PONTO DE EQUILIBRIO'
sh['A19'].font = branco
sh['A19'].fill = PatternFill('solid', fgColor=AZUL)
sh.merge_cells('A19:C19')
rotulo('A20', '% de captura p/ break-even (dada taxa RS atual)')
# custo = pool_capturavel * x * (1 - taxaRS)  ->  x = custo / (pool_capt * (1-taxaRS))
valor('B20', '=B7/(B12*(1-B8))', '0,0%', formula=True)
sh['C20'] = 'abaixo disso o headcount da prejuizo no cenario de taxa RS informado'
sh['C20'].font = ital
sh['C20'].alignment = left

rotulo('A21', 'Status do cenario atual')
sh['B21'] = '=SE(B16>=0;"VIAVEL (resultado >= 0)";"ABAIXO DO BREAK-EVEN")'
sh['B21'].alignment = center
sh['B21'].border = bd
sh['B21'].font = bold
# cor condicional no status
sh.conditional_formatting.add('B21', CellIsRule(operator='containsText', formula=['"VIAVEL"'], fill=PatternFill('solid', fgColor=VERDE)))

for col, w in zip('ABC', (42, 18, 52)):
    sh.column_dimensions[col].width = w

# ============ ABA 2: SENSIBILIDADE ============
s2 = wb.create_sheet('Sensibilidade')
s2['A1'] = 'Sensibilidade: Resultado anual (R$) por % de captura x taxa da RS'
s2['A1'].font = titfont
s2.merge_cells('A1:H1')
s2['A2'] = 'Cada celula = captura liquida - custo. Verde = viavel (>=0), vermelho = prejuizo. Usa as premissas da aba Modelo (pool, parcela, custo).'
s2['A2'].font = ital
s2.merge_cells('A2:H2')

# eixos
taxas = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]   # colunas (taxa RS)
capturas = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]  # linhas

s2['A4'] = 'Captura \\ Taxa RS'
s2['A4'].font = branco
s2['A4'].fill = PatternFill('solid', fgColor=AZUL)
s2['A4'].alignment = center
s2['A4'].border = bd
for j, t in enumerate(taxas):
    c = s2.cell(row=4, column=2 + j, value=t)
    c.number_format = '0%'
    c.font = branco
    c.fill = PatternFill('solid', fgColor=AZUL)
    c.alignment = center
    c.border = bd

for i, cap in enumerate(capturas):
    r = 5 + i
    cl = s2.cell(row=r, column=1, value=cap)
    cl.number_format = '0%'
    cl.font = bold
    cl.fill = az_fill
    cl.alignment = center
    cl.border = bd
    for j, t in enumerate(taxas):
        col = 2 + j
        # resultado = poolcapt(Modelo!B12) * captura * (1 - taxa) - custo(Modelo!B7)
        cap_ref = '$A%d' % r
        taxa_ref = '%s$4' % get_column_letter(col)
        f = '=Modelo!$B$12*%s*(1-%s)-Modelo!$B$7' % (cap_ref, taxa_ref)
        cc = s2.cell(row=r, column=col, value=f)
        cc.number_format = 'R$ #,##0'
        cc.alignment = center
        cc.border = bd

# formatacao condicional: verde >=0, vermelho <0
rng = 'B5:%s%d' % (get_column_letter(1 + len(taxas)), 4 + len(capturas))
s2.conditional_formatting.add(rng, CellIsRule(operator='greaterThanOrEqual', formula=['0'], fill=PatternFill('solid', fgColor=VERDE)))
s2.conditional_formatting.add(rng, CellIsRule(operator='lessThan', formula=['0'], fill=PatternFill('solid', fgColor=VERMELHO)))

s2.column_dimensions['A'].width = 16
for j in range(len(taxas)):
    s2.column_dimensions[get_column_letter(2 + j)].width = 13

s2['A%d' % (6 + len(capturas))] = ('Leitura: o verde comeca por volta de 30% de captura; com a taxa da RS subindo, '
                                   'a fronteira do break-even desloca para a direita, exigindo capturar mais para o mesmo resultado.')
s2['A%d' % (6 + len(capturas))].font = ital
s2.merge_cells('A%d:H%d' % (6 + len(capturas), 6 + len(capturas)))

# ============ ABA 3: NOTAS ============
s3 = wb.create_sheet('Notas e Fontes')
notas = [
    'MODELO FINANCEIRO - PROJETO ASIA (CHINA)',
    '',
    'Objetivo: testar a viabilidade do headcount local sensibilizando as duas variaveis em aberto:',
    '  (1) a taxa de estrutura cobrada pela RS Logistics e (2) o % de captura que 1 pessoa consegue.',
    '',
    'Premissas e fontes:',
    '- Pool Profit OFF a agentes R$ 2,04 mi: apresentacao DMS +Asia (abr/25-mar/26), universo teorico.',
    '- Custo headcount R$ 550-650 mil (usado 600 mil de base): ERI SalaryExpert / Morgan McKinley 2025-26.',
    '- Parcela capturavel 70%: premissa de trabalho - parte do pool e transacional (doc/desembaraco),',
    '  nao substituivel por 1 pessoa. AJUSTAR quando o cliente detalhar a composicao do pool.',
    '- Taxa da RS: NAO INFORMADA pelo cliente - e a principal variavel em aberto. Default 15% ilustrativo.',
    '- % captura meta 30%: coerente com o break-even citado no deck para custo ~600k sem taxa RS.',
    '',
    'Como usar:',
    '- Aba Modelo: mude as celulas amarelas; o resultado e o break-even recalculam.',
    '- Aba Sensibilidade: ve o resultado anual para cada combinacao captura x taxa RS (verde = viavel).',
    '',
    'Ressalvas importantes:',
    '- Este modelo cobre apenas o ganho de MARGEM DE AGENTE (comprovavel). O ganho de rate com',
    '  armadores (M2/M3) NAO esta aqui - e hipotese ate o piloto rodar, e seria upside.',
    '- O pool nao e capturavel de uma vez; a captura e a meta de regime, nao o mes 1.',
    '- Nao inclui custo de transicao nem risco de perda de servico na migracao dos 2 agentes (69%).',
]
for i, n in enumerate(notas, 1):
    c = s3.cell(row=i, column=1, value=n)
    if i == 1:
        c.font = titfont
    elif n.endswith(':'):
        c.font = bold
    else:
        c.font = Font(size=9.5)
s3.column_dimensions['A'].width = 110

wb.save(SAIDA)
print('Excel gerado:', SAIDA)
