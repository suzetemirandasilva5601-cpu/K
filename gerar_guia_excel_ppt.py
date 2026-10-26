# -*- coding: utf-8 -*-
"""Gera um guia visual (PDF) de Excel e PowerPoint aplicado ao projeto DMS."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

SAIDA = 'DMS - Guia de Excel e PowerPoint para o projeto.pdf'

AZUL = colors.HexColor('#005E9E')
AZULCLARO = colors.HexColor('#E5F0F8')
LARANJA = colors.HexColor('#FF8E2E')
LARANJAF = colors.HexColor('#FDF0E4')
TEAL = colors.HexColor('#009796')
CINZA = colors.HexColor('#555555')
CINZACLARO = colors.HexColor('#F2F2F2')
CODBG = colors.HexColor('#F4F6F8')
BRANCO = colors.white

st = getSampleStyleSheet()
TIT = ParagraphStyle('t', parent=st['Title'], fontName='Helvetica-Bold', fontSize=20,
                     textColor=AZUL, spaceAfter=2)
SUB = ParagraphStyle('s', parent=st['Normal'], fontName='Helvetica-Oblique', fontSize=11,
                     textColor=CINZA, spaceAfter=12)
H1 = ParagraphStyle('h1', parent=st['Heading1'], fontName='Helvetica-Bold', fontSize=13,
                    textColor=BRANCO, spaceBefore=8, spaceAfter=6, leftIndent=6)
H2 = ParagraphStyle('h2', parent=st['Heading2'], fontName='Helvetica-Bold', fontSize=10.5,
                    textColor=AZUL, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle('b', parent=st['Normal'], fontName='Helvetica', fontSize=9,
                      textColor=colors.HexColor('#222222'), leading=13, spaceAfter=3)
CODE = ParagraphStyle('c', parent=st['Normal'], fontName='Courier', fontSize=8.5,
                      textColor=colors.HexColor('#0A2A43'), leading=12, backColor=CODBG,
                      borderPadding=5, spaceAfter=4, leftIndent=2)
NOTE = ParagraphStyle('n', parent=BODY, fontSize=8.5, textColor=CINZA, leftIndent=4)

el = []


def faixa(txt, cor=AZUL):
    t = Table([[Paragraph(txt, H1)]], colWidths=[172 * mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), cor),
                           ('TOPPADDING', (0, 0), (-1, -1), 3),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    el.append(Spacer(1, 4))
    el.append(t)
    el.append(Spacer(1, 4))


def h2(t): el.append(Paragraph(t, H2))
def p(t): el.append(Paragraph(t, BODY))
def code(t): el.append(Paragraph(t.replace(' ', '&nbsp;').replace(chr(10), '<br/>'), CODE))
def nota(t): el.append(Paragraph('<i>' + t + '</i>', NOTE))
def sp(h=4): el.append(Spacer(1, h))


def tabela(dados, larg):
    t = Table(dados, colWidths=larg)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.3),
        ('TEXTCOLOR', (0, 0), (-1, 0), BRANCO),
        ('BACKGROUND', (0, 0), (-1, 0), AZUL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRANCO, CINZACLARO]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]))
    el.append(t)
    el.append(Spacer(1, 6))


# ===== CAPA =====
el.append(Spacer(1, 30))
el.append(Paragraph('Guia de Excel e PowerPoint', TIT))
el.append(Paragraph('Fórmulas e técnicas aplicadas ao projeto DMS, do básico ao intermediário', SUB))
p('Este guia reúne o que você mais vai usar no projeto: contar e somar com condições, '
  'cruzar planilhas, classificar cargos por bloco, montar tabela dinâmica e editar os '
  'slides mantendo a identidade DMS. Os exemplos usam os dados reais do projeto '
  '(vagas, base de setembro e CIS).')
sp(6)
el.append(HRFlowable(width='100%', thickness=1, color=AZULCLARO))

# ===== EXCEL =====
faixa('EXCEL')

h2('1. Contar e somar com condições — o coração do projeto')
p('Foi assim que cheguei em "49 vagas", "17 nos blocos" e "40 ativos Brasil".')
code('=CONT.SE(intervalo; critério)            conta com 1 condição\n'
     '=CONT.SES(int1;crit1; int2;crit2; ...)   conta com VÁRIAS condições\n'
     '=SOMASE(intervalo; critério; soma)        soma com 1 condição\n'
     '=SOMASES(soma; int1;crit1; int2;crit2)    soma com várias condições')
p('<b>Exemplos no contexto DMS:</b>')
code('Vagas abertas do COO:\n'
     '=CONT.SES(C:C;"COO"; H:H;"<>FECHADA"; G:G;"")\n\n'
     'Custo dos ativos de Air Operations:\n'
     '=SOMASES(V:V; M:M;"AIR OPERATIONS"; G:G;"ATIVO")\n\n'
     '% em aberto de um bloco:\n'
     '=vagas/(ativos+vagas)      (formatar como %)')

h2('2. Procurar dados entre tabelas — cruzar base x vagas x DRE')
code('=PROCX(valor; coluna_busca; coluna_retorno)     moderno (M365)\n'
     '=PROCV(valor; tabela; nº_coluna; FALSO)          clássico\n'
     '=ÍNDICE(retorno; CORRESP(valor; busca; 0))       qualquer direção')
nota('Usei para checar se um nome das vagas já aparecia na base de setembro.')

h2('3. Criar coluna calculada — classificar cargo em bloco/geografia')
p('Para transformar "AIR OPS ANALYST INLAND USA" em "EUA":')
code('=SE(ÉNÚM(PROCURAR("INLAND USA";D2)); "EUA";\n'
     ' SE(ÉNÚM(PROCURAR("EUROPA";D2));    "Europa";\n'
     ' SE(ÉNÚM(PROCURAR("CC";D2));        "Brasil"; "Fora")))')
p('<b>Funções de texto úteis:</b>')
code('=PROCURAR("texto"; célula)    acha a posição de um trecho\n'
     '=ESQUERDA / =DIREITA / =EXT.TEXTO   recorta pedaços\n'
     '=MAIÚSCULA / =ARRUMAR          padroniza (ex: "ANACAROL")\n'
     '=SE.ERRO(fórmula; "-")        troca erro por valor limpo')

h2('4. Tabela Dinâmica — "vagas por área" e "por C-Level"')
tabela([
    ['Passo', 'O que fazer'],
    ['1', 'Selecionar os dados → Inserir → Tabela Dinâmica'],
    ['2', 'Linhas: ÁREA (ou C-LEVEL)'],
    ['3', 'Valores: CARGO, configurado como Contagem'],
    ['4', 'Filtros: SITUAÇÃO = ATIVO ou STATUS <> FECHADA'],
    ['5', '% do total: clique direito no valor → Mostrar Valores Como → % do Total Geral'],
    ['6', 'Segmentação de Dados: botões para filtrar por C-Level/geografia'],
    ['7', 'Quando a base mudar: clique direito → Atualizar'],
], [22 * mm, 150 * mm])
nota('Dica: transforme o intervalo em Tabela (Ctrl+T) antes; a dinâmica cresce sozinha '
     'ao adicionar linhas.')

h2('5. Limpeza de dados — o que faltou na base da DMS')
code('Remover Duplicatas (Dados→)     acha duplicata tipo "Pamela Iris"\n'
     'Formatação Condicional          pinta % em aberto > 40% de vermelho\n'
     'Texto para Colunas (Dados→)     separa "ABERTA | PUBLICADA" em 2\n'
     '=ÉCÉL.VAZIA / =SE.ERRO          trata head/C-level vazios')

h2('6. Atalhos que economizam tempo')
tabela([
    ['Atalho', 'Faz'],
    ['Ctrl+Shift+L', 'Liga/desliga filtros'],
    ['Alt + =', 'Soma automática'],
    ['Ctrl+T', 'Transforma em Tabela'],
    ['F4', 'Trava referência ($A$1) ao digitar fórmula'],
    ['Ctrl + Seta', 'Pula para o fim dos dados'],
], [40 * mm, 132 * mm])

# ===== POWERPOINT =====
faixa('POWERPOINT', TEAL)

h2('1. Editar um slide')
tabela([
    ['Ação', 'Como'],
    ['Mudar layout', 'Página Inicial → Layout'],
    ['Duplicar slide', 'Clique direito no slide → Duplicar (mantém o padrão)'],
    ['Reordenar', 'Arrastar no painel lateral'],
    ['Reutilizar do template', 'Novo Slide → Reutilizar Slides (puxa do template DMS)'],
], [45 * mm, 127 * mm])

h2('2. Tabelas (como a do penúltimo slide)')
tabela([
    ['Ação', 'Como'],
    ['Inserir', 'Inserir → Tabela'],
    ['Vincular ao Excel', 'Copiar no Excel → no PPT Colar Especial → Colar Vínculo'],
    ['Estilo', 'Aba Design da Tabela → bandas de cor e cabeçalho'],
    ['Alinhar números', 'Números à direita, percentuais centralizados'],
], [45 * mm, 127 * mm])
nota('Colar Vínculo faz a tabela do slide atualizar sozinha quando o Excel muda.')

h2('3. Gráficos (as barras dos slides 2 e 4)')
code('Inserir → Gráfico → Barras / Colunas\n'
     'Barra empilhada (vagas por nível): tipo "Coluna Empilhada"\n'
     'Clique direito → Adicionar Rótulos de Dados (nº em cima da barra)')

h2('4. Identidade visual consistente')
tabela([
    ['Recurso', 'Para que serve'],
    ['Slide Mestre (Exibir→)', 'Muda fonte/cor/logo de todos os slides de uma vez'],
    ['Conta-gotas de cor', 'Copia a cor exata da marca de qualquer elemento'],
    ['Pincel de Formatação', 'Ctrl+Shift+C copia formato / Ctrl+Shift+V aplica'],
], [55 * mm, 117 * mm])
p('<b>Cores da DMS usadas no deck:</b>')
pal = Table([['#005E9E', '#00ACEE', '#E5F0F8', '#FF8E2E', '#009796']],
            colWidths=[34 * mm] * 5)
pal.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, 0), AZUL), ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#00ACEE')),
    ('BACKGROUND', (2, 0), (2, 0), AZULCLARO), ('BACKGROUND', (3, 0), (3, 0), LARANJA),
    ('BACKGROUND', (4, 0), (4, 0), TEAL),
    ('TEXTCOLOR', (0, 0), (1, 0), BRANCO), ('TEXTCOLOR', (3, 0), (4, 0), BRANCO),
    ('TEXTCOLOR', (2, 0), (2, 0), AZUL),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
el.append(pal)
sp(6)

h2('5. Alinhamento (deixa profissional)')
code('Selecionar vários → Formatar → Alinhar (distribuir igual)\n'
     'Guias inteligentes: linhas vermelhas ao arrastar p/ encaixar\n'
     'Ctrl+D: duplica mantendo o espaçamento')

h2('6. Boas práticas que seguimos no deck')
p('• Título de ação: frase que entrega a conclusão, não só "Vagas".<br/>'
  '• Fonte dos dados no rodapé de todo slide com número.<br/>'
  '• Máximo ~6 linhas por bloco de texto.<br/>'
  '• Padrão brasileiro: vírgula decimal (17,9%) e ponto de milhar (R$ 4.283.288).')

# ===== TOP 5 =====
faixa('AS 5 QUE VOCÊ MAIS VAI USAR', LARANJA)
tabela([
    ['#', 'Recurso', 'Para quê'],
    ['1', '=CONT.SES', 'Contar vagas/ativos com múltiplos critérios'],
    ['2', 'Tabela Dinâmica + Contagem', 'Montar "por área" e "por C-level" sem fórmula'],
    ['3', '=SE aninhado com =PROCURAR', 'Classificar cargo em bloco/geografia'],
    ['4', '=PROCX / =PROCV', 'Cruzar base x vagas x DRE'],
    ['5', 'Colar Vínculo (Excel→PPT)', 'Tabela do slide que atualiza sozinha'],
], [10 * mm, 68 * mm, 94 * mm])

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm,
                        topMargin=15 * mm, bottomMargin=15 * mm,
                        title='DMS - Guia de Excel e PowerPoint')


def rodape(c, d):
    c.saveState()
    c.setFont('Helvetica', 7.5)
    c.setFillColor(CINZA)
    c.drawString(19 * mm, 9 * mm, 'DMS · Guia de Excel e PowerPoint para o projeto')
    c.drawRightString(A4[0] - 19 * mm, 9 * mm, 'pág. %d' % d.page)
    c.restoreState()


doc.build(el, onFirstPage=rodape, onLaterPages=rodape)
print('PDF gerado:', SAIDA)
