# -*- coding: utf-8 -*-
"""Documento de decisão do Board — Projeto Ásia (China). PDF executivo."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

SAIDA = 'DMS - Decisao do Board - Projeto Asia China.pdf'

AZUL = colors.HexColor('#005E9E')
AZULCLARO = colors.HexColor('#E5F0F8')
VERDE = colors.HexColor('#2E7D32')
VERDEF = colors.HexColor('#E8F5E9')
LARANJA = colors.HexColor('#C87000')
LARANJAF = colors.HexColor('#FDF0E4')
CINZA = colors.HexColor('#555555')
CINZACLARO = colors.HexColor('#F2F2F2')
BRANCO = colors.white

st = getSampleStyleSheet()
TIT = ParagraphStyle('t', parent=st['Title'], fontName='Helvetica-Bold', fontSize=19, textColor=AZUL, spaceAfter=2)
SUB = ParagraphStyle('s', parent=st['Normal'], fontName='Helvetica-Oblique', fontSize=10.5, textColor=CINZA, spaceAfter=10)
H1 = ParagraphStyle('h1', parent=st['Heading1'], fontName='Helvetica-Bold', fontSize=12.5, textColor=BRANCO, leftIndent=6, spaceBefore=6, spaceAfter=5)
BODY = ParagraphStyle('b', parent=st['Normal'], fontName='Helvetica', fontSize=9.3, textColor=colors.HexColor('#222222'), leading=13.5, spaceAfter=4, alignment=TA_LEFT)
BULL = ParagraphStyle('bu', parent=BODY, leftIndent=12, spaceAfter=3)
NOTE = ParagraphStyle('n', parent=BODY, fontSize=8.3, textColor=CINZA)

el = []


def faixa(txt, cor=AZUL):
    t = Table([[Paragraph(txt, H1)]], colWidths=[172 * mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), cor),
                           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    el.append(Spacer(1, 5)); el.append(t); el.append(Spacer(1, 4))


def p(t): el.append(Paragraph(t, BODY))
def b(t): el.append(Paragraph('• ' + t, BULL))
def nota(t): el.append(Paragraph('<i>' + t + '</i>', NOTE))
def sp(h=4): el.append(Spacer(1, h))


def tabela(dados, larg, destaque_col=None):
    t = Table(dados, colWidths=larg)
    cmd = [
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.4),
        ('TEXTCOLOR', (0, 0), (-1, 0), BRANCO),
        ('BACKGROUND', (0, 0), (-1, 0), AZUL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRANCO, CINZACLARO]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]
    t.setStyle(TableStyle(cmd))
    el.append(t); el.append(Spacer(1, 6))


def caixa(titulo, linhas, cor_borda, cor_fundo):
    conteudo = [[Paragraph('<b>' + titulo + '</b>', ParagraphStyle('ct', parent=BODY, textColor=cor_borda, fontSize=10))]]
    for ln in linhas:
        conteudo.append([Paragraph('• ' + ln, BODY)])
    t = Table(conteudo, colWidths=[168 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), cor_fundo),
        ('LINEABOVE', (0, 0), (-1, 0), 2, cor_borda),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    el.append(t); el.append(Spacer(1, 6))


# ===== CABECALHO =====
el.append(Paragraph('Projeto Ásia · China', TIT))
el.append(Paragraph('Documento de decisão do Board — investimento em presença local', SUB))
tabela([
    ['Campo', 'Conteúdo'],
    ['Deliberação', 'Aprovação de 1 posição de headcount da DMS na China, em parceria com a RS Logistics'],
    ['Natureza', 'Investimento em pessoa (não abertura de entidade) — reversível e de baixo compromisso'],
    ['Investimento anual', 'R$ 550-650 mil (salário + encargos, perfil sênior em Shanghai)'],
    ['Horizonte', '8 meses até a decisão de concentração (M3); M4 roda em paralelo'],
    ['Quem decide agora', 'Somente o headcount + mandato M1-M2 e o gatilho M4. M3 e M5 voltam ao board.'],
], [38 * mm, 134 * mm])

# ===== 1. DECISAO =====
faixa('1. A DECISÃO REQUERIDA')
p('O que se aprova nesta rodada é <b>o investimento em presença local</b> — não a '
  'migração de volume. A migração é consequência gradual do trabalho do profissional e '
  'volta ao board por gate.')
caixa('Aprovar nesta rodada', [
    '1 profissional da DMS posicionado na China, em parceria operacional com a RS Logistics',
    'Mandato inicial: atuar no bloco já comprovado (M1) e conduzir o piloto no armador-âncora (M2)',
    'Início de M4 em paralelo: consolidação própria de LCL ao atingir 20 CBM ou 5 embarques/semana',
], VERDE, VERDEF)
caixa('Condicionado a gate futuro (não se decide agora)', [
    'M3 — concentração parcial no âncora: só volta ao board com o resultado de M2 em mãos',
    'Exclusividade, SLA ou cláusula de reversibilidade: desenhadas apenas se M2 for aprovado',
    'M5 — multi-região: não entra em pauta antes de M3 provado e atribuído ao corredor Brasil',
], LARANJA, LARANJAF)

# ===== 2. CONTEXTO =====
faixa('2. CONTEXTO E RACIONAL')
p('A operação da China hoje depende de agentes parceiros para execução local, com volume '
  'fragmentado e baixo poder de negociação (diagnóstico de 16/10). A proposta posiciona '
  'uma pessoa da DMS dentro do mercado, usando a estrutura já montada da RS Logistics, '
  'para negociar direto com armadores — começando onde já há relação comprovada.')
p('<b>A alavancagem está concentrada, não pulverizada:</b>')
tabela([
    ['Bloco de negociação', 'Fatia do volume China', 'Papel'],
    ['Armador-âncora', '30,7%', 'Alvo final — única concentração capaz de mudar o jogo'],
    ['Bloco secundário comprovado', '16,3%', 'Ponto de partida de baixo risco (M1)'],
    ['Demais armadores dispersos', '53,0%', 'Cauda longa — não move a agulha'],
], [58 * mm, 44 * mm, 70 * mm])
nota('Concentração de cliente: top-5 clientes = 51,8% do volume China. A alavancagem '
     'depende também da permanência dessas contas.')

# ===== 3. CASO FINANCEIRO =====
faixa('3. CASO FINANCEIRO')
tabela([
    ['Indicador', 'Valor', 'Observação'],
    ['Profit OFF a agentes (12m)', 'R$ 2,04 mi', 'abr/25-mar/26 · universo teórico, não capturável de uma vez'],
    ['Concentração do pool', '69% em 2 agentes', 'maior oportunidade e maior risco de transição'],
    ['Custo do headcount', 'R$ 550-650 mil/ano', 'sênior em Shanghai (ERI SalaryExpert / Morgan McKinley)'],
    ['Captura para break-even', '~30% do pool', 'antes da taxa de estrutura da RS'],
], [46 * mm, 36 * mm, 90 * mm])
p('<b>Dois fluxos de valor distintos, não somar:</b> o ganho que banca o headcount vem '
  'da <b>margem de agente hoje paga a terceiros</b> pela execução local (comprovável). '
  'O ganho de <b>rate com armadores</b> (M2/M3) é hipótese — não houve movimentação de '
  'carga de teste ainda, por isso o piloto controlado antes de qualquer migração.')

# ===== 4. PLANO POR GATES =====
faixa('4. PLANO DE ATUAÇÃO — AVANÇO POR GATES')
p('Cada etapa só avança com resultado comprovado na anterior. Fornecedores atuais seguem '
  'como retaguarda ativa — nunca substituídos de uma vez. Horizonte de ~8 meses até M3.')
tabela([
    ['Módulo', 'O que é', 'Critério / gate'],
    ['Investimento', '1 profissional DMS via RS Logistics', 'APROVAR AGORA'],
    ['M1 · Expansão comprovada', 'Atua no bloco secundário já testado', '60 dias com rate e serviço na faixa'],
    ['M2 · Piloto no âncora', 'Negociação real e limitada, 15-20 emb.', 'GATE CRÍTICO · 4 métricas · go/no-go'],
    ['M3 · Concentração parcial', 'Migra fatia do âncora (nunca 100%)', 'Condicionado a M2 + aprovação do board'],
    ['M4 · LCL próprio (paralelo)', 'Consolidação própria', 'Gatilho: 20 CBM ou 5 emb./semana'],
    ['M5 · Multi-região', 'Expansão a outras regiões', 'Só após M3, atribuído ao Brasil'],
], [42 * mm, 70 * mm, 60 * mm])

# ===== 5. RISCOS =====
faixa('5. RISCOS E PONTOS DE ATENÇÃO')
b('<b>Taxa da RS não precificada:</b> o break-even de ~30% sobe conforme a taxa de '
  'estrutura cobrada pela RS Logistics for definida. É a principal variável em aberto.')
b('<b>Ganho de rate não comprovado:</b> o retorno de M2/M3 é hipótese até o piloto rodar '
  'com carga real — mitigado pelo próprio desenho em gates.')
b('<b>Transição dos 2 agentes (69%):</b> migrar rápido demais compromete o serviço que '
  'sustenta o volume atual. Retaguarda ativa mitiga.')
b('<b>Captura parcial:</b> parte dos R$ 2,04 mi é volume transacional (documentação, '
  'desembaraço), não negociável por 1 pessoa — a meta considera só a parcela "intelectual".')
b('<b>Ponto único de falha / exposição de informação:</b> cresce em M5; por isso exige '
  'governança e concordância formal das unidades antes de escalar.')

# ===== 6. RECOMENDACAO =====
faixa('6. RECOMENDAÇÃO', VERDE)
p('<b>Aprovar o investimento nesta rodada.</b> É uma aposta de baixa exposição e '
  'reversível: um headcount de R$ 550-650 mil/ano que se paga capturando ~30% de um pool '
  'de R$ 2,04 mi que hoje já sai para terceiros. O desenho em gates garante que nenhum '
  'avanço de volume — em especial no armador-âncora — ocorra sem resultado comprovado, e '
  'mantém os fornecedores atuais como retaguarda. Diferente de Hamburgo (abertura de '
  'filial), aqui não há CAPEX de entidade nem compromisso societário nesta fase.')
p('<b>Condicionar ao board:</b> fechar a taxa de estrutura da RS antes da contratação '
  '(para travar o break-even real) e trazer M3 de volta apenas com o resultado de M2 em mãos.')

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm,
                        topMargin=15 * mm, bottomMargin=15 * mm,
                        title='DMS - Decisao do Board - Projeto Asia')


def rod(c, d):
    c.saveState(); c.setFont('Helvetica', 7.3); c.setFillColor(CINZA)
    c.drawString(19 * mm, 9 * mm, 'DMS Cargo & Logistics · Projeto Ásia · documento de deliberação do Board')
    c.drawRightString(A4[0] - 19 * mm, 9 * mm, 'pág. %d' % d.page)
    c.restoreState()


doc.build(el, onFirstPage=rod, onLaterPages=rod)
print('PDF gerado:', SAIDA)
