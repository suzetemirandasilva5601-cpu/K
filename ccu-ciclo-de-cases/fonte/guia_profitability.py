"""Gera o Guia de tipo de case: Profitability (lucratividade).

Mesmo formato do guia de Market Entry do ciclo de cases (Carlito, vermelho CCU,
tabelas com cabeçalho vermelho). Uso:

    pip install reportlab
    python guia_profitability.py   # gera ../Guia_Tipo_de_Case_Profitability.pdf

As fontes Carlito (licença OFL) são baixadas para fonte/fonts/ se não existirem.
"""
import os
import urllib.request

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)
from reportlab.platypus.flowables import HRFlowable

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "..", "Guia_Tipo_de_Case_Profitability.pdf")
LOGO = os.path.join(AQUI, "logo_guia.png")
FONTES = os.path.join(AQUI, "fonts")

VERMELHO = HexColor("#c1272d")
TEXTO = HexColor("#1e293b")
CINZA = HexColor("#475569")
LINHA_CLARA = HexColor("#f8fafc")


def carregar_fontes():
    os.makedirs(FONTES, exist_ok=True)
    base = "https://github.com/google/fonts/raw/main/ofl/carlito/"
    for nome in ["Regular", "Bold", "Italic", "BoldItalic"]:
        arq = os.path.join(FONTES, f"Carlito-{nome}.ttf")
        if not os.path.exists(arq):
            urllib.request.urlretrieve(base + f"Carlito-{nome}.ttf", arq)
        pdfmetrics.registerFont(TTFont(f"Carlito-{nome}", arq))
    pdfmetrics.registerFontFamily("Carlito", normal="Carlito-Regular", bold="Carlito-Bold",
                                  italic="Carlito-Italic", boldItalic="Carlito-BoldItalic")


carregar_fontes()

S_TITULO = ParagraphStyle("t", fontName="Carlito-Bold", fontSize=19, leading=22, textColor=VERMELHO)
S_SUB = ParagraphStyle("s", fontName="Carlito-Italic", fontSize=9, leading=12, textColor=CINZA,
                       spaceBefore=2, spaceAfter=5)
S_CORPO = ParagraphStyle("c", fontName="Carlito-Regular", fontSize=9.5, leading=11.6, textColor=TEXTO)
S_BULLET = ParagraphStyle("b", parent=S_CORPO, leftIndent=15.5, bulletIndent=0, bulletFontSize=9.5)
S_SECAO = ParagraphStyle("h", fontName="Carlito-Bold", fontSize=10.5, leading=13, textColor=VERMELHO,
                         spaceBefore=9, spaceAfter=0)
S_NOTA = ParagraphStyle("n", fontName="Carlito-Italic", fontSize=8.5, leading=10.5, textColor=CINZA,
                        spaceAfter=3)
S_TAB = ParagraphStyle("tb", fontName="Carlito-Regular", fontSize=8, leading=9.8, textColor=TEXTO)
S_TAB_B = ParagraphStyle("tbb", parent=S_TAB, fontName="Carlito-Bold")
S_TAB_H = ParagraphStyle("th", parent=S_TAB, fontName="Carlito-Bold", textColor=white)
S_FINAL = ParagraphStyle("f", fontName="Carlito-BoldItalic", fontSize=9.5, leading=11.6,
                         textColor=VERMELHO, spaceBefore=2)

LARGURA = 612 - 2 * 42.5


def secao(texto):
    titulo = Paragraph(texto, S_SECAO)
    linha = HRFlowable(width="100%", thickness=0.75, color=VERMELHO, spaceBefore=1, spaceAfter=4)
    titulo.keepWithNext = linha.keepWithNext = True
    return [titulo, linha]


def bullets(itens):
    out = []
    for item in itens:
        if isinstance(item, tuple):
            item = f"<b>{item[0]}</b> {item[1]}"
        out.append(Paragraph(item, S_BULLET, bulletText="•"))
    return out


def tabela(cabecalho, linhas, larguras, primeira_negrito=True):
    dados = [[Paragraph(c, S_TAB_H) for c in cabecalho]]
    for linha in linhas:
        dados.append([Paragraph(c, S_TAB_B if (i == 0 and primeira_negrito) else S_TAB)
                      for i, c in enumerate(linha)])
    t = Table(dados, colWidths=[LARGURA * w for w in larguras], repeatRows=1)
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), VERMELHO),
        ("GRID", (0, 0), (-1, -1), 0.5, black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]
    for r in range(2, len(dados), 2):
        estilo.append(("BACKGROUND", (0, r), (-1, r), LINHA_CLARA))
    t.setStyle(TableStyle(estilo))
    return t


def cabecalho_rodape(canvas, doc):
    canvas.saveState()
    canvas.drawImage(LOGO, 51.5, 792 - 63.2, width=56.7, height=27.2, mask="auto")
    canvas.setFont("Carlito-Bold", 8.5)
    canvas.setFillColor(VERMELHO)
    canvas.drawString(212, 792 - 62, "Guia de tipo de case  ·  Ciclo de cases")
    canvas.setFont("Carlito-Regular", 7.5)
    canvas.setFillColor(CINZA)
    canvas.drawString(42.5, 792 - 753, "Clube de Consultoria Universitário  ·  Gestão de Pessoas")
    canvas.restoreState()


# ---------------------------------------------------------------- conteúdo
h = []
h.append(Paragraph("Profitability (Lucratividade)", S_TITULO))
h.append(Paragraph("Guia de tipo de case  ·  como atacar, as contas que sempre caem e os macetes", S_SUB))
h.append(Paragraph(
    "Este guia vale para qualquer setor. Ele é sobre o tipo de pergunta, não sobre o mercado da semana. "
    "Lucro em queda, margem apertada, custo que subiu ou um choque externo que ameaça o resultado são "
    "variações do mesmo case, e todas se resolvem com a mesma equação: lucro é receita menos custo.", S_CORPO))

h += secao("1. Como reconhecer que é este tipo de case")
h += bullets([
    "A pergunta fala de resultado: o lucro caiu, a margem apertou, como proteger o EBITDA, como voltar a ganhar dinheiro.",
    "O cliente já opera e o problema bate na conta do negócio atual. Pode nascer dentro (custo, preço, mix) ou "
    "chegar de fora (concorrente, regulação, crise de demanda). Se o cliente quer entrar em algo novo, o case é outro.",
    "Aparecem palavras como DRE, EBITDA, margem, custo fixo e variável, ticket médio, volume, ponto de equilíbrio.",
    "Às vezes vem disfarçado de decisão: como responder, qual opção escolher. Quando a escolha se resolve comparando "
    "o lucro de cada opção, o case continua sendo de lucratividade, só que com várias contas em vez de uma.",
])

h += secao("2. A estrutura que funciona, em quatro blocos")
h.append(Paragraph("Ataque sempre nesta ordem. Pular o bloco 1 e ir direto para ideias é o erro mais comum: "
                   "sem saber onde o lucro mexeu, a lista de soluções vira chute.", S_NOTA))
h.append(tabela(
    ["Bloco", "A pergunta", "O que olhar"],
    [["1. Onde está o problema", "É receita, custo ou os dois? Desde quando?",
      "Qual linha da DRE mexeu, quanto e desde quando, comparada ao histórico, à meta e aos concorrentes"],
     ["2. Por que aconteceu", "A causa é interna ou externa? Vai durar quanto?",
      "Receita: volume (unidades, clientes, frequência) × preço e mix. Custo: fixo, variável e único. "
      "Fora: mercado, concorrentes, regulação, choque e sua duração"],
     ["3. Quais são as opções", "O que o cliente pode fazer?",
      "Aumentar receita, reduzir custo ou mudar o modelo. Sempre mais de duas opções, com prós e contras "
      "financeiros e não financeiros"],
     ["4. A conta fecha e o que recomendar", "Qual opção deixa mais lucro no horizonte do problema?",
      "Resultado de cada opção período a período, custo único de implantação, comparação com não fazer nada, "
      "efeito na marca, nos clientes e nas pessoas, riscos"]],
    [0.33, 0.33, 0.34]))

h += secao("3. A árvore de lucro: abra até achar a linha que mexeu")
h += bullets([
    ("Lado da receita:", "receita = volume × preço. Volume se abre em unidades ou lojas × clientes por unidade × "
     "frequência. Preço inclui ticket médio, mix de produtos e descontos."),
    ("Lado do custo:", "separe o fixo (aluguel, overhead, SG&amp;A, equipe mínima) do variável (CMV, insumos, comissão, "
     "frete). O custo único, como investimento ou lançamento, fica em uma linha à parte."),
])
h.append(Paragraph(
    "<b>Macete central: compare cada linha com uma referência, seja o período anterior, o cenário sem o problema "
    "ou o concorrente. A linha que mais se moveu explica mais que todas as outras juntas. Ache essa linha antes de "
    "propor qualquer solução.</b>", S_CORPO))

h += secao("4. As contas que sempre caem")
h.append(tabela(
    ["Conta", "Fórmula", "Serve para"],
    [["Lucro operacional (EBITDA)", "receita − CMV − despesas operacionais", "Medir o resultado antes de juros, impostos e depreciação"],
     ["Margem", "lucro ÷ receita", "Comparar períodos e empresas de tamanhos diferentes"],
     ["Margem de contribuição unitária", "preço − custo variável unitário", "Saber quanto cada venda paga do custo fixo"],
     ["Ponto de equilíbrio", "custo fixo ÷ margem de contribuição unitária", "Saber o volume mínimo sem prejuízo"],
     ["Aplicar um choque", "valor atual × (1 ± variação %)", "Levar a queda ou alta para cada linha da DRE"],
     ["Resultado no horizonte", "soma do resultado de cada período", "Medir um problema que dura vários meses"],
     ["Custo único", "entra só no período em que acontece", "Não repetir investimento nos meses seguintes"],
     ["Perda contra a base", "resultado com o problema ÷ resultado sem o problema − 1", "Dizer o tamanho da perda em %"],
     ["Escala", "resultado por unidade × número de unidades", "Levar a conta da loja para a rede"]],
    [0.33, 0.33, 0.34]))

h += secao("5. Macetes que mudam a nota")
h += bullets([
    ("Escreva a DRE antes de calcular.", "Monte as linhas (receita, custo variável, custo fixo, custo único, "
     "resultado) e só depois preencha. O entrevistador acompanha o seu mapa e nenhum número se perde."),
    ("Separe fixo de variável.", "Quando a receita cai, parte do custo cai junto e o fixo continua lá. Errar essa "
     "separação é o que mais distorce a conta."),
    ("Respeite o horizonte.", "Se o problema tem prazo, calcule período a período e depois some. O custo único pesa "
     "só no primeiro período, e juntar tudo em um mês só esconde isso."),
    ("Compare com a alternativa.", "Lucro menor pode ser a melhor resposta se as outras opções são piores. Diga contra "
     "o que você compara: não fazer nada, fechar, ou outra opção."),
    ("Vá além do binário.", "Abrir ou fechar e cortar ou manter quase nunca esgotam as opções. Traga pelo menos uma "
     "terceira via que mude o modelo: canal, horário, mix, parceria."),
    ("Faça brainstorming com estrutura.", "Separe as ideias em aumentar receita e reduzir custo, e dentro delas em "
     "volume e preço, fixo e variável. Uma ideia criativa dentro de uma estrutura vale mais que dez soltas."),
    ("Interprete cada número.", "Depois de cada conta, diga o que ela significa para a decisão. Por exemplo: o "
     "resultado fica negativo no primeiro mês, mas o período fecha positivo. Número sem leitura não pontua."),
    ("Pense além do dinheiro.", "Marca, segurança, clientes, funcionários e reação dos concorrentes podem mudar a "
     "recomendação. Cite esses pontos e ligue cada um à decisão."),
    ("Arredonde com aviso.", "Arredondar facilita a conta de cabeça. Diga quando arredondou e carregue o mesmo "
     "número até o fim."),
])

h += secao("6. Armadilhas que derrubam a análise")
h += bullets([
    "Pular para soluções sem dizer se o problema está na receita ou no custo.",
    "Tratar todo custo como fixo, ou todo custo como variável.",
    "Calcular um único período quando o problema dura vários, ou repetir o custo único em todos os meses.",
    "Usar um dado só porque o entrevistador entregou. Nem toda informação do case entra na conta.",
    "Cortar custo sem olhar o efeito na receita. Reduzir equipe ou cardápio pode derrubar serviço e vendas.",
    "Esquecer a marca e os clientes quando a decisão é pública e vai ser vista fora da unidade analisada.",
    "Recomendação sem número, ou número sem recomendação. Os dois valem meio caminho.",
    "Riscos genéricos, como crise, câmbio ou concorrência, que não se ligam às contas do case.",
])

h.append(KeepTogether(secao("7. Roteiro de ataque nos 30 minutos") + [
    Paragraph("O case é conduzido pelo entrevistador: ele faz as perguntas e entrega os dados quando você pede.", S_NOTA),
    tabela(
        ["Quando", "O que fazer"],
        [["Minutos 0 a 3", "Repete a pergunta com suas palavras, confirma o objetivo (lucro, margem, prazo) e "
          "pergunta o que não ficou claro"],
         ["Minutos 3 a 8", "Pede um tempo, monta a estrutura em quatro blocos, apresenta antes de pedir dados e "
          "diz a hipótese inicial"],
         ["Minutos 8 a 20", "Pede a DRE e o efeito do problema, escreve as linhas, anuncia o plano da conta, "
          "calcula período a período e interpreta o resultado"],
         ["Minutos 20 a 27", "Lista opções e ideias de melhoria, separadas em receita e custo, com prós, contras "
          "e pontos não financeiros"],
         ["Minutos 27 a 30", "Fecha em até 1 minuto: recomendação, número que a sustenta, riscos ligados ao case "
          "e próximos passos"]],
        [0.5, 0.5])]))

h += secao("8. Checklist antes de fechar o case")
h += bullets([
    "Disse se o problema está na receita, no custo ou nos dois.",
    "Separou custo fixo, variável e único.",
    "Calculou o resultado de cada período e o total no horizonte do problema.",
    "Comparou o resultado com a base sem o problema e com as outras opções.",
    "Trouxe mais de duas opções, com prós e contras.",
    "Organizou as ideias de melhoria em receita e custo.",
    "Considerou marca, clientes e pessoas, e ligou cada ponto à decisão.",
    "A recomendação cabe em uma frase e tem o número que a sustenta.",
    "Os riscos e os próximos passos são específicos do case.",
])
h.append(Paragraph(
    "Regra final: em case de lucratividade, o entrevistador não está comprando a sua lista de ideias, está "
    "comprando o caminho da equação até a decisão. Mostre onde o lucro mexeu, quanto mexeu e o que fazer com isso.",
    S_FINAL))

# ---------------------------------------------------------------- montagem
doc = BaseDocTemplate(SAIDA, pagesize=letter, leftMargin=42.5, rightMargin=42.5,
                      topMargin=66, bottomMargin=52,
                      title="Guia de tipo de case: Profitability (Lucratividade)",
                      author="Clube de Consultoria Universitário")
frame = Frame(42.5, 52, LARGURA, 792 - 66 - 52, id="f", leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=cabecalho_rodape)])
doc.build(h)
print("gerado:", os.path.abspath(SAIDA))
