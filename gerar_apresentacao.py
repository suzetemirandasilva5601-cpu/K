# -*- coding: utf-8 -*-
"""
Gera a apresentacao "Vagas em aberto x ocupacao nas Operacoes".

Parte do proprio template DMS para herdar arte, tema, fontes e layouts:
  slide 1 : capa (Blank_Analytics, arte original, texto trocado)
  slide 2 : onde estao as vagas, com foco no COO
  slide 3 : pontos de atencao
  slide 4 : plano de acao
  slide 5 : encerramento (arte original do divisor do template)

Todos os numeros vem das tres fontes e foram conferidos:
  Base_Setembro26 (ativos), Vagas 21-10 (vagas), CIS ORDERS (volumes).
"""
import copy
import datetime
import shutil
from collections import Counter, defaultdict

import openpyxl
import pandas as pd
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

TEMPLATE = '20261020 - ATY - Diligenciamento Fase 1 - Estrutura e Job Description vZé - Template DMS (1).pptx'
SAIDA = 'DMS - Vagas em aberto x Ocupação nas Operações.pptx'
BASE = 'Base_Setembro26 (1).xlsx'
VAGAS = 'Vagas 21-10.xlsx'
CIS = 'CIS_20261013_ORDERS.parquet'

# paleta extraida do template
AZUL = RGBColor(0x00, 0x5E, 0x9E)
AZUL_CLARO = RGBColor(0x00, 0xAC, 0xEE)
AZUL_FUNDO = RGBColor(0xE5, 0xF0, 0xF8)
LARANJA = RGBColor(0xFF, 0x8E, 0x2E)
LARANJA_FUNDO = RGBColor(0xFD, 0xF0, 0xE4)
TEAL = RGBColor(0x00, 0x97, 0x96)
CINZA_TXT = RGBColor(0x33, 0x33, 0x33)
CINZA_CLARO = RGBColor(0xF2, 0xF2, 0xF2)
CINZA_MEDIO = RGBColor(0xA6, 0xA6, 0xA6)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)

FONTE = 'Fonte: Base Setembro/26 (RH); Vagas 21/10; CIS ORDERS.parquet (13/10/2026)'

# ============================ DADOS ============================
REF = datetime.date(2026, 10, 21)
B_POS, B_CARGO, B_HEAD, B_AREA, B_CL, B_TOT = 10, 11, 12, 13, 14, 21
V_CL, V_AREA, V_CARGO, V_CONTRATADO, V_STATUS, V_CUSTO, V_OCUP = 1, 2, 3, 6, 7, 12, 15


def num(v):
    if v is None or v == '-':
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def cheio(v):
    return v is not None and str(v).strip() not in ('', 'None', '.', '-', 'TBD', 'TDB', '?')


def estado(r):
    if cheio(r[V_CONTRATADO]):
        return 'preenchida'
    a = r[4]
    if isinstance(a, datetime.datetime) and a.date() <= REF:
        return 'a confirmar'
    return 'aberta'


ws = openpyxl.load_workbook(BASE, data_only=True)['Setembro Unificado']
ATIVOS = [r for r in ws.iter_rows(min_row=2, values_only=True)
          if r[4] and str(r[6]).strip().upper() == 'ATIVO']
wv = openpyxl.load_workbook(VAGAS, data_only=True)['Vagas']
TODAS = [r for r in wv.iter_rows(min_row=2, values_only=True)
         if r[V_CARGO] and str(r[V_CARGO]).strip() not in ('', 'None')]
AB = [r for r in TODAS if estado(r) == 'aberta']
PREENCH = [r for r in TODAS if estado(r) == 'preenchida']
CONFIRMAR = [r for r in TODAS if estado(r) == 'a confirmar']

N_AB = len(AB)
CUSTO_AB = sum(num(r[V_CUSTO]) for r in AB)
COO_AB = [r for r in AB if str(r[V_CL]).strip() == 'COO']
N_COO = len(COO_AB)
CUSTO_COO = sum(num(r[V_CUSTO]) for r in COO_AB)
AT_COO = [r for r in ATIVOS if r[B_CL] == 'COO']

cl_cnt = Counter(str(r[V_CL]).strip() for r in AB)
coo_area = Counter(str(r[V_AREA]).strip() for r in COO_AB)


def nivel(c):
    c = str(c).upper()
    if ' TL' in c or 'TEAM LEADER' in c:
        return 'Team Leader'
    if 'HEAD' in c:
        return 'Head'
    if 'SPEC' in c:
        return 'Specialist'
    if 'ANALYST' in c:
        return 'Analyst'
    if 'ASSIST' in c:
        return 'Assistant'
    if 'INTERN' in c:
        return 'Intern'
    return 'Outro'


coo_nivel = Counter(nivel(r[V_CARGO]) for r in COO_AB)
coo_aum = sum(1 for r in COO_AB if 'Aumento' in str(r[V_OCUP]))
coo_pub = sum(1 for r in COO_AB if 'ABERTA' in str(r[V_STATUS]).upper())

# blocos operacionais
BLOCOS = ['EUA / Inland Freight America', 'EUA / Operações America',
          'EUA / Warehouses (MIA, Houston, NY)', 'Europa / Inland Freight Europa',
          'Europa / Operações Europa', 'Brasil / Customer Care', 'Brasil / Exportação']


def bloco(c):
    c = str(c).upper()
    if 'WH ' in c or 'WAREHOUSE' in c:
        return 'EUA / Warehouses (MIA, Houston, NY)'
    if 'INLAND USA' in c or 'INLAND AMERICAS' in c:
        return 'EUA / Inland Freight America'
    if 'AMERICAS' in c:
        return 'EUA / Operações America'
    if 'INLAND EUROPA' in c:
        return 'Europa / Inland Freight Europa'
    if 'EUROPA' in c:
        return 'Europa / Operações Europa'
    if c.startswith('AIR CC') or c.startswith('OCEAN CC'):
        return 'Brasil / Customer Care'
    if 'EXPORT' in c:
        return 'Brasil / Exportação'
    return None


LIDER = {'TEAM LEADER', 'SR. TEAM LEADER', 'COORDINATOR', 'HEAD'}
b_at, b_tl, b_ab, b_lid, b_semst = Counter(), Counter(), Counter(), Counter(), Counter()
for r in ATIVOS:
    b = bloco(r[B_CARGO])
    if b:
        b_at[b] += 1
        if r[B_POS] in LIDER:
            b_tl[b] += 1
for r in AB:
    b = bloco(r[V_CARGO])
    if b:
        b_ab[b] += 1
        cg = str(r[V_CARGO]).upper()
        if ' TL' in cg or 'HEAD' in cg:
            b_lid[b] += 1
        if 'ABERTA' not in str(r[V_STATUS]).upper():
            b_semst[b] += 1

TOT_AT_OP = sum(b_at[b] for b in BLOCOS)
TOT_AB_OP = sum(b_ab[b] for b in BLOCOS)
TOT_SEMST = sum(b_semst[b] for b in BLOCOS)

# CIS
d = pd.read_parquet(CIS)
d['created_at'] = pd.to_datetime(d['created_at'])
p = d[(d.created_at >= '2026-04-01') & (d.created_at <= '2026-09-30')]
E = lambda f: p[f]['assembly_id'].nunique() / 6
EUA_AIR = round(E((p['off'].isin(['DMS MIAMI', 'DMS HOUSTON'])) & (p['mode'] == 'air')))
MIA_SEA = round(E((p['off'] == 'DMS MIAMI') & (p['mode'] == 'sea')))
EUR_AIR = round(E((p['off'].isin(['DMS FRANKFURT', 'DMS LOGISTICS LISBOA'])) & (p['mode'] == 'air')))
CC_AIR = round(E((p.imp_exp == 'IMP') & (p['mode'] == 'air')))
EX_AIR = round(E((p.imp_exp == 'EXP') & (p['mode'] == 'air')))
EX_SEA = round(E((p.imp_exp == 'EXP') & (p['mode'] == 'sea')))
h = p[(p['off'] == 'DMS HOUSTON') & (p['mode'] == 'air')]
HOU_JS = round(h[h.created_at >= '2026-07-01']['assembly_id'].nunique() / 3)
HOU_AJ = round(h[h.created_at < '2026-07-01']['assembly_id'].nunique() / 3)

at_eua = sum(b_at[b] for b in BLOCOS if b.startswith('EUA'))
at_eur = sum(b_at[b] for b in BLOCOS if b.startswith('Europa'))
VPA_EUA = round((EUA_AIR + MIA_SEA) / at_eua)
VPA_EUR = round(EUR_AIR / at_eur)
VPA_CC = round(CC_AIR / b_at['Brasil / Customer Care'])
VPA_EX = round((EX_AIR + EX_SEA) / b_at['Brasil / Exportação'])


def pc(v, t):
    return ('%.1f%%' % (v / t * 100)).replace('.', ',') if t else '-'


def brl(v):
    return 'R$ ' + '{:,.0f}'.format(v).replace(',', '.')


def ocup(b):
    den = b_at[b] + b_ab[b]
    return pc(b_ab[b], den) if den else '-'


# ============================ MONTAGEM ============================
shutil.copy(TEMPLATE, SAIDA)
prs = Presentation(SAIDA)


def limpa(slide, manter_placeholders=True):
    """Remove shapes de conteudo, preservando placeholders e arte."""
    for sh in list(slide.shapes):
        if manter_placeholders and sh.is_placeholder:
            continue
        if sh.shape_type == 13:        # PICTURE: arte do template
            continue
        if sh.name == 'Disclaimer_Box':
            continue
        sh._element.getparent().remove(sh._element)


def ph(slide, nome_contem):
    for sh in slide.placeholders:
        if nome_contem.lower() in sh.name.lower():
            return sh
    return None


def set_ph(slide, nome, texto):
    sh = ph(slide, nome)
    if sh is None:
        return
    tf = sh.text_frame
    tf.clear()
    tf.paragraphs[0].text = texto


def titulo(slide, texto):
    sh = slide.shapes.title
    if sh is None:
        sh = ph(slide, 'Titel') or ph(slide, 'Title')
    tf = sh.text_frame
    tf.clear()
    par = tf.paragraphs[0]
    par.text = texto
    for r in par.runs:
        r.font.size = Pt(18)
    return sh


def caixa(slide, x, y, w, h, titulo_txt, linhas, cor_cab, cor_fundo,
          fonte_tit=11.5, fonte_txt=9.5, bullets=True):
    """Par de retangulos arredondados no padrao do template."""
    cab = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(0.28))
    cab.fill.solid()
    cab.fill.fore_color.rgb = cor_cab
    cab.line.fill.background()
    cab.shadow.inherit = False
    tf = cab.text_frame
    tf.clear()
    tf.margin_top = Pt(1)
    tf.margin_bottom = Pt(1)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    par = tf.paragraphs[0]
    par.alignment = PP_ALIGN.CENTER
    r = par.add_run()
    r.text = titulo_txt
    r.font.size = Pt(fonte_tit)
    r.font.bold = True
    r.font.name = 'Arial'
    r.font.color.rgb = BRANCO

    corpo = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Inches(x), Inches(y + 0.32), Inches(w), Inches(h))
    corpo.fill.solid()
    corpo.fill.fore_color.rgb = cor_fundo
    corpo.line.fill.background()
    corpo.shadow.inherit = False
    tf = corpo.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Pt(8)
    tf.margin_right = Pt(8)
    tf.margin_top = Pt(6)
    for i, txt in enumerate(linhas):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = par.add_run()
        r.text = ('• ' if bullets else '') + txt
        r.font.size = Pt(fonte_txt)
        r.font.name = 'Arial'
        r.font.color.rgb = CINZA_TXT
        par.space_after = Pt(4)
    return cab, corpo


def numerao(slide, x, y, w, valor, rotulo, cor=AZUL):
    """Numero grande com rotulo, para destaque."""
    cx = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(0.52))
    tf = cx.text_frame
    tf.clear()
    tf.word_wrap = True
    par = tf.paragraphs[0]
    par.alignment = PP_ALIGN.CENTER
    r = par.add_run()
    r.text = valor
    r.font.size = Pt(26)
    r.font.bold = True
    r.font.name = 'Arial'
    r.font.color.rgb = cor
    cx2 = slide.shapes.add_textbox(Inches(x), Inches(y + 0.48), Inches(w), Inches(0.42))
    tf2 = cx2.text_frame
    tf2.clear()
    tf2.word_wrap = True
    par2 = tf2.paragraphs[0]
    par2.alignment = PP_ALIGN.CENTER
    r2 = par2.add_run()
    r2.text = rotulo
    r2.font.size = Pt(8.5)
    r2.font.name = 'Arial'
    r2.font.color.rgb = CINZA_TXT


# ---------------- slide 1: capa ----------------
s1 = prs.slides[0]
for sh in s1.shapes:
    if sh.has_text_frame and sh.text_frame.text.strip():
        tf = sh.text_frame
        linhas = [('Projeto Diligenciamento', 24, 'Montserrat SemiBold'),
                  ('Vagas em aberto x ocupação nas Operações', 16, 'Montserrat'),
                  ('Outubro de 2026', 11, 'Montserrat')]
        tf.clear()
        for i, (txt, sz, fnt) in enumerate(linhas):
            par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = par.add_run()
            r.text = txt
            r.font.size = Pt(sz)
            r.font.name = fnt
            r.font.color.rgb = BRANCO
        break

# ---------------- slide 2: onde estao as vagas ----------------
s2 = prs.slides[1]
limpa(s2)
set_ph(s2, 'Textplatzhalter 6', 'Operações, vagas em aberto')
set_ph(s2, 'Text Placeholder 2', 'Operações, vagas em aberto')
titulo(s2, 'Das %d vagas realmente em aberto, %d estão sob o COO, e Air Operations '
            'concentra %d delas' % (N_AB, N_COO, coo_area['Air Operations']))
set_ph(s2, 'Text Placeholder 3',
       'Distribuição das posições em aberto por C-Level e, dentro do COO, por área e por nível')
set_ph(s2, 'Text Placeholder 4', FONTE)

# faixa de numeros
numerao(s2, 0.38, 1.62, 2.30, str(N_AB), 'posições em aberto\n(de 65 registros na planilha)')
numerao(s2, 2.80, 1.62, 2.30, '%s' % pc(N_COO, N_AB), 'das vagas em aberto\nestão sob o COO')
numerao(s2, 5.22, 1.62, 2.30, brl(CUSTO_COO).replace('R$ ', 'R$ '),
        'custo mensal das vagas\ndo COO (%s do total)' % pc(CUSTO_COO, CUSTO_AB))
numerao(s2, 7.64, 1.62, 2.30, '%d' % coo_aum, 'das %d vagas do COO são\naumento de quadro' % N_COO)
numerao(s2, 10.06, 1.62, 2.60, '%d de %d' % (coo_pub, N_COO),
        'vagas do COO estão\npublicadas', LARANJA)

caixa(s2, 0.38, 2.78, 4.10, 2.10, 'Vagas em aberto por C-Level',
      ['%s: %d vagas (%s)' % (k, v, pc(v, N_AB)) for k, v in cl_cnt.most_common()]
      + ['Total: %d vagas, %s por mês' % (N_AB, brl(CUSTO_AB))],
      AZUL, AZUL_FUNDO)

caixa(s2, 4.62, 2.78, 4.10, 2.10, 'Vagas do COO por área',
      ['%s: %d' % (k.replace('Quality & Operational Intelligence', 'Quality & Op. Intelligence'), v)
       for k, v in coo_area.most_common()],
      AZUL, AZUL_FUNDO)

caixa(s2, 8.86, 2.78, 3.80, 2.10, 'Vagas do COO por nível',
      ['%s: %d' % (k, v) for k, v in coo_nivel.most_common()],
      AZUL, AZUL_FUNDO)

caixa(s2, 0.38, 5.26, 12.28, 1.22, 'Leitura',
      ['A planilha tem 65 registros, mas %d já estão preenchidas e %d dependem de confirmação. '
       'Trabalhar com 65 superestima a necessidade de contratação em um terço.'
       % (len(PREENCH), len(CONFIRMAR)),
       'A fila de contratação é essencialmente operacional: %s das vagas em aberto respondem ao COO '
       'e %d das %d são de Analyst ou Specialist, ou seja, capacidade de execução.'
       % (pc(N_COO, N_AB), coo_nivel['Analyst'] + coo_nivel['Specialist'], N_COO),
       'Apenas %d das %d vagas do COO estão publicadas, o que indica que o gargalo está antes do '
       'mercado, na abertura e aprovação do processo.' % (coo_pub, N_COO)],
      TEAL, CINZA_CLARO, fonte_txt=9)

# ---------------- slide 3: pontos de atencao ----------------
s3 = prs.slides[2]
limpa(s3)
set_ph(s3, 'Textplatzhalter 6', 'Operações, pontos de atenção')
set_ph(s3, 'Text Placeholder 2', 'Operações, pontos de atenção')
titulo(s3, 'Europa opera sem team leader, a liderança de Americas está descoberta e '
            'Exportação carrega o maior volume por pessoa')
set_ph(s3, 'Text Placeholder 3',
       'Quadro em aberto, camada de liderança e volume de embarques por ativo, bloco a bloco')
set_ph(s3, 'Text Placeholder 4', FONTE)

b_eur = 'Europa / Inland Freight Europa'
b_ame = 'EUA / Operações America'
b_wh = 'EUA / Warehouses (MIA, Houston, NY)'
b_exp = 'Brasil / Exportação'
b_cc = 'Brasil / Customer Care'

caixa(s3, 0.38, 1.62, 3.02, 2.18, '1. Europa sem liderança',
      ['%s do quadro em aberto, o maior entre os blocos' % ocup(b_eur),
       '%d ativos e %d vagas em aberto' % (b_at[b_eur], b_ab[b_eur]),
       'Nenhum team leader no bloco',
       '%d embarques por ativo ao mês' % VPA_EUR,
       'Risco de a operação europeia ficar sem referência técnica'],
      LARANJA, LARANJA_FUNDO, fonte_txt=9)

caixa(s3, 3.60, 1.62, 3.02, 2.18, '2. Americas sem team leader',
      ['%s do quadro em aberto' % ocup(b_ame),
       '%d ativos e %d vagas em aberto' % (b_at[b_ame], b_ab[b_ame]),
       '%d das vagas abertas são de team leader' % b_lid[b_ame],
       'Apenas %d posição de liderança hoje' % b_tl[b_ame],
       'Maior custo de vagas entre os blocos'],
      LARANJA, LARANJA_FUNDO, fonte_txt=9)

caixa(s3, 6.82, 1.62, 3.02, 2.18, '3. Exportação sobrecarregada',
      ['%d embarques por ativo ao mês, o maior da operação' % VPA_EX,
       'Apenas %d pessoas no bloco' % b_at[b_exp],
       '%s do quadro em aberto' % ocup(b_exp),
       'Customer Care absorve %d por ativo, porém com %d pessoas'
       % (VPA_CC, b_at[b_cc]),
       'Dependência crítica de poucas pessoas'],
      LARANJA, LARANJA_FUNDO, fonte_txt=9)

caixa(s3, 10.04, 1.62, 2.62, 2.18, '4. Warehouses sem reforço',
      ['%d pessoas para três praças' % b_at[b_wh],
       'MIA, Houston e NY',
       'Nenhuma vaga aberta',
       'Houston saiu de %d para %d embarques por mês' % (HOU_AJ, HOU_JS),
       'Único bloco sem reforço previsto'],
      CINZA_MEDIO, CINZA_CLARO, fonte_txt=9)

# tabela resumo dos blocos
rows = [['Bloco', 'Ativos', 'TL+', 'Vagas', '% em aberto', 'Embarques por ativo']]
for b in sorted(BLOCOS, key=lambda x: -(b_ab[x] / (b_at[x] + b_ab[x]) if b_at[x] + b_ab[x] else 0)):
    vpa = (VPA_EUA if b.startswith('EUA') else VPA_EUR if b.startswith('Europa')
           else VPA_CC if b == b_cc else VPA_EX)
    rows.append([b.replace('EUA / ', '').replace('Europa / ', '').replace('Brasil / ', ''),
                 str(b_at[b]), str(b_tl[b]), str(b_ab[b]), ocup(b), str(vpa)])
rows.append(['Total Operações', str(TOT_AT_OP), str(sum(b_tl[b] for b in BLOCOS)),
             str(TOT_AB_OP), pc(TOT_AB_OP, TOT_AT_OP + TOT_AB_OP), ''])

gt = s3.shapes.add_table(len(rows), 6, Inches(0.38), Inches(4.26),
                         Inches(12.28), Inches(2.34)).table
larg = [3.90, 1.25, 1.05, 1.25, 1.85, 2.98]
for j, w in enumerate(larg):
    gt.columns[j].width = Inches(w)
for i, linha in enumerate(rows):
    gt.rows[i].height = Inches(0.26)
    for j, val in enumerate(linha):
        c = gt.cell(i, j)
        c.text = ''
        c.margin_left = Pt(5)
        c.margin_right = Pt(3)
        c.margin_top = Pt(1)
        c.margin_bottom = Pt(1)
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        par = c.text_frame.paragraphs[0]
        if j > 0:
            par.alignment = PP_ALIGN.CENTER
        r = par.add_run()
        r.text = val
        r.font.size = Pt(8.5)
        r.font.name = 'Arial'
        ultima = (i == len(rows) - 1)
        r.font.bold = (i == 0 or ultima)
        r.font.color.rgb = BRANCO if i == 0 else CINZA_TXT
        c.fill.solid()
        if i == 0:
            c.fill.fore_color.rgb = AZUL
        elif ultima:
            c.fill.fore_color.rgb = AZUL_FUNDO
        else:
            c.fill.fore_color.rgb = BRANCO if i % 2 else CINZA_CLARO

cx = s3.shapes.add_textbox(Inches(0.38), Inches(6.68), Inches(12.28), Inches(0.30))
tf = cx.text_frame
tf.clear()
tf.word_wrap = True
r = tf.paragraphs[0].add_run()
r.text = ('TL+ reúne team leaders, senior team leaders, coordinators e heads. Volume por ativo é '
          'ordem de grandeza por bloco: o CIS mostra quem executou cada etapa, não o headcount, e o '
          'Customer Care do Brasil atende embarques de Miami.')
r.font.size = Pt(7.5)
r.font.name = 'Arial'
r.font.color.rgb = CINZA_MEDIO

# ---------------- slide 4: plano de acao ----------------
s4 = prs.slides[4]
limpa(s4)
set_ph(s4, 'Textplatzhalter 6', 'Operações, plano de ação')
set_ph(s4, 'Text Placeholder 2', 'Operações, plano de ação')
titulo(s4, 'Cada frente crítica sai da agenda de 30 minutos com ação, dono e prazo definidos')
set_ph(s4, 'Text Placeholder 3',
       'Prioridade pela combinação de quadro em aberto, camada de liderança e volume por pessoa')
set_ph(s4, 'Text Placeholder 4', FONTE)

ACOES = [
    [b_eur, 'Reaproveitar finalistas de processos recentes e indicação interna com bônus',
     'Carol Mendoza + RH', '1 a 3 semanas'],
    [b_ame, 'Vaga pré-aprovada com faixa e budget definidos, processo enxuto e cobertura '
            'temporária pelo Brasil no back-office',
     'Carol Mendoza e Filipe Sampaio + RH', 'Imediato'],
    ['EUA / Inland Freight America', 'Indicação interna com bônus, as três vagas já estão publicadas',
     'Carol Mendoza e Filipe Sampaio + RH', '2 a 3 semanas'],
    [b_exp, 'Processo enxuto e profissionais vindos de contratos encerrados, verificando não aliciamento',
     'Carol Mendoza + RH', 'Imediato a 4 semanas'],
    ['Europa / Operações Europa', 'Processo enxuto: triagem em 48 horas e proposta em 24 horas',
     'Carol Mendoza e Filipe Sampaio + RH', 'Imediato'],
    [b_cc, 'Processo enxuto e acompanhamento do volume por ativo',
     'Carol Mendoza e Natália Costa + RH', 'Imediato'],
    [b_wh, 'Validar necessidade de abrir vaga e contratar temporários ou agência para as três praças',
     'Possidônio Dantas + RH', '1 a 2 semanas'],
]
rows = [['Frente crítica', '% em aberto', 'Ação', 'Dono', 'Prazo de efeito']]
for a in ACOES:
    rows.append([a[0], ocup(a[0]), a[1], a[2], a[3]])

at_tb = s4.shapes.add_table(len(rows), 5, Inches(0.38), Inches(1.68),
                            Inches(12.28), Inches(3.40)).table
for j, w in enumerate([2.70, 1.15, 4.63, 2.40, 1.40]):
    at_tb.columns[j].width = Inches(w)
for i, linha in enumerate(rows):
    at_tb.rows[i].height = Inches(0.42)
    for j, val in enumerate(linha):
        c = at_tb.cell(i, j)
        c.text = ''
        c.margin_left = Pt(5)
        c.margin_right = Pt(4)
        c.margin_top = Pt(2)
        c.margin_bottom = Pt(2)
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        par = c.text_frame.paragraphs[0]
        c.text_frame.word_wrap = True
        if j == 1 or j == 4:
            par.alignment = PP_ALIGN.CENTER
        r = par.add_run()
        r.text = val
        r.font.size = Pt(8.5)
        r.font.name = 'Arial'
        r.font.bold = (i == 0)
        r.font.color.rgb = BRANCO if i == 0 else CINZA_TXT
        c.fill.solid()
        if i == 0:
            c.fill.fore_color.rgb = AZUL
        else:
            c.fill.fore_color.rgb = BRANCO if i % 2 else CINZA_CLARO

caixa(s4, 0.38, 5.28, 6.05, 1.30, 'Pendências para fechar na reunião',
      ['%d das %d vagas de Operações estão sem estágio de processo informado: definir quem '
       'atualiza e com que frequência' % (TOT_SEMST, TOT_AB_OP),
       'Confirmar o estado das %d linhas com admissão ocorrida e sem ocupante' % len(CONFIRMAR),
       'Nova York não aparece como escritorio no CIS: confirmar volume proprio'],
      AZUL, AZUL_FUNDO, fonte_txt=8.5)

caixa(s4, 6.61, 5.28, 6.05, 1.30, 'O que destrava mais rápido',
      ['Pré-aprovação de faixa e budget resolve o gargalo de publicação: hoje só %d das %d vagas '
       'do COO estão publicadas' % (coo_pub, N_COO),
       'As %d vagas de team leader e head são as de maior impacto, pois destravam a gestão dos times'
       % sum(b_lid[b] for b in BLOCOS),
       'Cobertura temporária pelo Brasil alivia EUA e Europa no back-office'],
      TEAL, CINZA_CLARO, fonte_txt=8.5)

# ---------------- slide 5: encerramento ----------------
# move o divisor artistico do template (slide 4) para o fim
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
sldIdLst.remove(ids[3])
sldIdLst.append(ids[3])

prs.save(SAIDA)
print('Apresentacao gerada: %s' % SAIDA)
print('  slides: %d' % len(Presentation(SAIDA).slides))
print('  vagas em aberto: %d (COO %d, %s)' % (N_AB, N_COO, pc(N_COO, N_AB)))
print('  operações: %d ativos, %d vagas abertas (%s)'
      % (TOT_AT_OP, TOT_AB_OP, pc(TOT_AB_OP, TOT_AT_OP + TOT_AB_OP)))
print('  CIS: EUA %d, Europa %d, CC %d, Exp %d' % (EUA_AIR, EUR_AIR, CC_AIR, EX_AIR))
