# -*- coding: utf-8 -*-
"""
Gera um PDF consolidando todas as respostas aos apontamentos do Ze sobre o
deck de vagas x ocupacao. Documento de discussao, uma pagina de abertura e
blocos tematicos.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

SAIDA = 'DMS - Respostas aos apontamentos do Ze - Vagas x Ocupacao.pdf'

AZUL = colors.HexColor('#005E9E')
AZULCLARO = colors.HexColor('#E5F0F8')
LARANJA = colors.HexColor('#FF8E2E')
CINZA = colors.HexColor('#555555')
CINZACLARO = colors.HexColor('#F2F2F2')
BRANCO = colors.white

styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold',
                    fontSize=14, textColor=AZUL, spaceBefore=10, spaceAfter=4)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold',
                    fontSize=11, textColor=AZUL, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica',
                      fontSize=9.5, textColor=colors.HexColor('#222222'),
                      leading=14, spaceAfter=4, alignment=TA_LEFT)
BULL = ParagraphStyle('Bull', parent=BODY, leftIndent=12, bulletIndent=2, spaceAfter=3)
NOTA = ParagraphStyle('Nota', parent=BODY, fontSize=8.5, textColor=CINZA,
                      leftIndent=6)
TITULO = ParagraphStyle('Titulo', parent=styles['Title'], fontName='Helvetica-Bold',
                        fontSize=20, textColor=AZUL, spaceAfter=2)
SUB = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Oblique',
                     fontSize=11, textColor=CINZA, spaceAfter=14)

el = []


def h1(t): el.append(Paragraph(t, H1))
def h2(t): el.append(Paragraph(t, H2))
def p(t): el.append(Paragraph(t, BODY))
def b(t): el.append(Paragraph('• ' + t, BULL))
def nota(t): el.append(Paragraph(t, NOTA))
def sp(h=4): el.append(Spacer(1, h))
def regua():
    el.append(Spacer(1, 3))
    el.append(HRFlowable(width='100%', thickness=0.6, color=AZULCLARO))
    el.append(Spacer(1, 3))


def tabela(dados, larguras, cab=True, destaques=None):
    t = Table(dados, colWidths=larguras)
    cmd = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#D0D7DE')),
    ]
    if cab:
        cmd += [('BACKGROUND', (0, 0), (-1, 0), AZUL),
                ('TEXTCOLOR', (0, 0), (-1, 0), BRANCO),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRANCO, CINZACLARO])]
    for (r, c, cor) in (destaques or []):
        cmd.append(('TEXTCOLOR', (c, r), (c, r), cor))
        cmd.append(('FONTNAME', (c, r), (c, r), 'Helvetica-Bold'))
    t.setStyle(TableStyle(cmd))
    el.append(t)
    el.append(Spacer(1, 6))


# ============================ CAPA ============================
el.append(Spacer(1, 60))
el.append(Paragraph('DMS · Vagas em aberto x Ocupação', TITULO))
el.append(Paragraph('Respostas aos apontamentos para discussão', SUB))
p('Este documento consolida os comentários do Zé sobre o deck de vagas x ocupação '
  'nas Operações e as respostas de cada um, separando o que é ajuste direto, o que '
  'depende de alinhamento de conceito e o que responde às perguntas abertas. '
  'Os números vêm da planilha de vagas (21/10), da base de setembro e do CIS.')
sp(8)
tabela([
    ['Referência', 'Número'],
    ['Linhas na planilha de vagas', '65'],
    ['Vagas realmente em aberto', '49'],
    ['Já preenchidas', '13'],
    ['A confirmar', '3'],
    ['Vagas em aberto nos blocos de Operações', '17'],
    ['Dessas, publicadas (processo rodando)', '5'],
    ['Dessas, ainda a abrir (sem status)', '12'],
], [320, 120], destaques=[(7, 1, LARANJA)])
nota('Observação: os rótulos de "crescer x repor" dos gráficos dependem de duas '
     'definições a confirmar com o Zé (ver bloco 3). Até lá, os números de total '
     'estão corretos, mas a quebra pode mudar.')

el.append(Spacer(1, 10))

# ============================ 1. DESIGN ============================
h1('1. Ajustes de design (podem ser feitos de imediato)')
b('<b>Remover os dois textos de baixo.</b> Concordo, competiam com os gráficos e não '
  'agregavam. Saem.')
b('<b>Ampliar os gráficos e a fonte.</b> Com os textos fora, sobra espaço para os três '
  'gráficos crescerem e a fonte subir.')
b('<b>Tirar os valores financeiros.</b> O foco é quadro e ocupação; os R$ saem do deck '
  'e ficam como apoio na fala.')
b('<b>Separar o gráfico da direita em USA x Europa x Geral.</b> Fica mais acionável, é '
  'como a operação é pensada por praça. Refaço com esse corte.')

regua()

# ============================ 2. 17 VAGAS ============================
h1('2. "Temos 17 vagas, mas tem as que precisam ser abertas, são essas mesmo?"')
p('São essas 17, sim, mas "em aberto" na planilha não quer dizer "sendo trabalhada". '
  'Só <b>5 estão publicadas</b> (processo rodando no Gupy). As outras <b>12 ainda '
  'precisam ser abertas</b>.')
tabela([
    ['Situação das 17 vagas de Operações', 'Qtd'],
    ['Publicadas (processo em andamento)', '5'],
    ['Sem status (precisam ser abertas)', '12'],
], [320, 120], destaques=[(2, 1, LARANJA)])
p('<b>O ponto que amarra:</b> as 12 não abertas estão concentradas nos dois blocos '
  'mais críticos. As 6 de Operações America e as 6 de Europa (Inland e Operações) '
  'estão todas sem processo iniciado. A frente mais urgente é a que menos andou, o '
  'gargalo é a abertura interna, não o mercado.')
h2('As 5 já publicadas')
b('EUA Inland: 3× AIR OPS ANALYST INLAND USA')
b('Brasil Customer Care: AIR CC SPEC · Brasil Exportação: AIR OPS ANALYST EXPORT')
h2('As 12 a abrir')
b('EUA Operações America (6): 3× AIR OPS TL AMERICAS, AIR OPS ANALYST AMERICAS, '
  '2× AIR OPS SPEC AMERICAS')
b('Europa Inland (4): 2× AIR OPS SPEC INLAND EUROPA, AIR OPS ANALYST INLAND EUROPA, '
  'AIR RD ANALYST INLAND EUROPA')
b('Europa Operações (2): 2× AIR OPS ANALYST EUROPA')

regua()

# ============================ 3. CONCEITOS A ALINHAR ============================
h1('3. Definições a alinhar antes de fechar os gráficos')
h2('3.1 "Colchão são vagas para crescer e demais são reposição"')
p('O conceito está certo, mas na planilha são <b>dois campos diferentes</b> e vale '
  'confirmar qual usar:')
b('<b>Folha/Colchão:</b> entre as 49 abertas, só 1 é Colchão. Se "crescer = Colchão", '
  'teríamos 1 vaga de crescimento, o que não bate com a realidade.')
b('<b>Ocupante/Vaga:</b> esse separa de verdade Aumento de Quadro (30) de Vaga '
  'Substituição (19). É o campo correto para crescer x repor.')
h2('3.2 "Temos 14 vagas de reposição"')
p('Pelo campo Ocupante/Vaga são <b>19 substituições no total</b> da empresa, e apenas '
  '<b>2 dentro dos blocos de Operações</b> (ambas de Europa Inland). O número 14 '
  'provavelmente vem de outra régua. Preciso que o Zé confirme: reposição é tudo que '
  'é "Vaga Substituição" (19), ou exclui estágios e outros cortes?')
nota('Enquanto isso não fecha, os totais estão corretos, mas a divisão crescer x repor '
     'nos gráficos fica travada.')

regua()

# ============================ 4. PERGUNTAS ============================
h1('4. Respostas às demais perguntas')
h2('4.1 Quais vagas são de USA / Europa?')
p('As 49 vagas abertas por geografia (lendo o marcador no cargo):')
tabela([
    ['Geografia', 'Vagas abertas', 'Das quais reposição'],
    ['Geral / Brasil', '34', '17'],
    ['USA', '9', '0'],
    ['Europa', '6', '2'],
], [200, 120, 150])
p('Nenhuma reposição nos EUA, lá é tudo aumento de quadro. As duas reposições de '
  'Europa são as AIR OPS/RD ANALYST INLAND EUROPA.')
h2('4.2 Os que estão em Warehouse, conseguimos saber quais são?')
p('Sim, os 5 estão identificados, todos em DMS América (EUA), área Overland, sob '
  'Possidônio Dantas:')
tabela([
    ['Nome', 'Cargo', 'Nível'],
    ['Jesus Guillermo Ledi Mendoza', 'WH TL', 'Team Leader'],
    ['Marcelo de Jesus Cedeño Diaz', 'WH Clerk Analyst', 'Analyst'],
    ['Daniel Marcelino Cedeño Rodríguez', 'WH Clerk Analyst', 'Analyst'],
    ['Jorge Correa Varela', 'WH Clerk Assist', 'Assistant'],
    ['Luis Carlos Coronado Barrera', 'WH Clerk Assist', 'Assistant'],
], [230, 130, 110])
nota('A base só diz "EUA", não separa MIA, Houston e NY. A quebra por praça precisa '
     'ser confirmada com a Operação, mesmo ponto do slide 4 sobre Nova York.')

regua()

# ============================ 5. PENDENTE ============================
h1('5. O que ainda não foi trabalhado (pendências)')
b('<b>As 12 vagas não abertas</b> dos blocos de Operações, concentradas em Europa e '
  'Americas. É o destaque novo a entrar no deck, como um funil 17 → 5 publicadas → '
  '12 a abrir.')
b('<b>Régua de reposição</b> (14, 15 ou 19) e <b>conceito de Colchão x aumento de '
  'quadro</b> (bloco 3). Travam os rótulos dos gráficos.')
b('<b>As 3 vagas "a confirmar"</b> (estágios com admissão já ocorrida e sem ocupante). '
  'Confirmar se já foram preenchidas.')
b('<b>Quebra por praça dos warehouses</b> (MIA / Houston / NY) e <b>Nova York</b>, que '
  'não aparece no CIS. Confirmar com a Operação.')

regua()

# ============================ 6. PROPOSTA ============================
h1('6. Proposta de encaminhamento')
p('<b>Faço já:</b> remover os dois textos, ampliar gráficos e fonte, tirar os valores '
  'financeiros, refazer o gráfico da direita em USA/Europa/Geral e adicionar o funil '
  'das 17 (5 publicadas, 12 a abrir).')
p('<b>Travado até confirmação do Zé:</b> a régua de reposição e o conceito de crescer '
  'x repor (Colchão ou aumento de quadro). Com as duas respostas, fecho os rótulos dos '
  'gráficos e finalizo o deck.')

doc = SimpleDocTemplate(SAIDA, pagesize=A4,
                        leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=16 * mm, bottomMargin=16 * mm,
                        title='DMS - Respostas aos apontamentos do Ze')


def rodape(canvas, docu):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(CINZA)
    canvas.drawString(18 * mm, 10 * mm,
                      'DMS · Vagas x Ocupação · documento para discussão')
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, 'pág. %d' % docu.page)
    canvas.restoreState()


doc.build(el, onFirstPage=rodape, onLaterPages=rodape)
print('PDF gerado:', SAIDA)
