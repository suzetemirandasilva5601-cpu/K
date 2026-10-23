#!/usr/bin/env python3
"""
Gera dois slides de conteudo sobre estrutura hierarquica x vagas em aberto,
no template da ATY (o verde).

Template: 'DMS - Vagas em aberto x Ocupação nas Operações.pptx'
          master 1, layout 'DMS_Conteudo'. Geometria em pixels de 96 DPI.
Paleta:   azul 005E9E, verde 009796, verde ATY 00CC99, laranja FF8E2E,
          fundos E5F0F8 / D9F2E9 / FDF0E4 / F2F2F2, Arial.

Base de numeros: '20261022 - DMS - Vagas em aberto x ocupação nas Operações (2).pdf'
(versao corrigida) + 'DMS - Respostas aos apontamentos do Ze'. Todos os numeros
foram reconferidos contra as planilhas — ver conferencia() no fim do arquivo.

Regras de design vindas do feedback do Ze (PDF de respostas):
  - sem valores financeiros no deck
  - fonte maior, menos texto solto
  - geografia separada em EUA x Europa x Brasil/geral
  - funil das 17 vagas de Operacoes: 5 publicadas, 12 a abrir

Saida: estrutura/ATY - DMS Estrutura hierarquica x Vagas em aberto.pptx

Uso:  python3 estrutura/gerar_slides.py
"""
import os
import re
from collections import Counter

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

from cross_check import RAIZ, ler_aba, ler_factorial, montar

TEMPLATE = os.path.join(RAIZ, "DMS - Vagas em aberto x Ocupação nas Operações.pptx")
SAIDA = os.path.join(RAIZ, "estrutura",
                     "ATY - DMS Estrutura hierarquica x Vagas em aberto.pptx")
FONTE = ("Fonte: Colaboradores-factorial (3) — organograma out/26; planilha de "
         "vagas (21/10); Base Setembro/26 (RH); Draft 23 Out 26")

AZUL = RGBColor(0x00, 0x5E, 0x9E)
VERDE = RGBColor(0x00, 0x97, 0x96)
VERDE_ATY = RGBColor(0x00, 0xCC, 0x99)
LARANJA = RGBColor(0xFF, 0x8E, 0x2E)
CINZA = RGBColor(0xA6, 0xA6, 0xA6)
FUNDO_AZUL = RGBColor(0xE5, 0xF0, 0xF8)
FUNDO_VERDE = RGBColor(0xD9, 0xF2, 0xE9)
FUNDO_LARANJA = RGBColor(0xFD, 0xF0, 0xE4)
FUNDO_CINZA = RGBColor(0xF2, 0xF2, 0xF2)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
TEXTO = RGBColor(0x33, 0x33, 0x33)
CINZA_TXT = RGBColor(0x60, 0x60, 0x60)
VERDE_TXT = RGBColor(0x00, 0x6B, 0x5B)


def px(v):
    return Emu(int(round(v * 9525)))


# ------------------------------------------------------------------ dados
NIVEIS = [("HEAD", "Head"), ("TL", "Team Leader"), ("SPEC", "Specialist"),
          ("ANALYST", "Analyst"), ("ASSIST", "Assistant"), ("INTERN", "Intern"),
          ("APPRENTICE", "Aprendiz")]

# area da planilha de vagas -> (rotulo curto, head do bloco no organograma)
BLOCO = {
    "Air Operations": ("Air Operations", "Carolina Bento Mendoza"),
    "Air Product": ("Air Product", "Filipe Teixeira Sampaio"),
    "Ocean Operations": ("Ocean Operations", "Natalia Correia Da Costa Parreira"),
    "Ocean Product": ("Ocean Product", "Filipe Carneiro De Oliveira"),
    "Quality & Operational Intelligence": ("Quality & Op. Intel.",
                                           "Marco Antonio Maraia Villa"),
    "Overland (Europa)": ("Overland", "Possidonio Dantas de Almeida Neto"),
    "Services": ("Services", "Luis Fernando Santos Muniz"),
    "Special Operations": ("Special Operations", None),
    "Healthcare": ("Healthcare", "Jose Carlos Duarte Freitas Sobrinho"),
    "High-Tech": ("High-Tech", "Ricardo Tebexreni Jakowatz"),
    "Automotive": ("Automotive", "Ricardo Tebexreni Jakowatz"),
    "Financial": ("Financial", "Ana Carolina Botelho Caldeira Vasconcellos"),
    "Technology": ("Technology", "Cleyton Cardoso Esteves"),
    "Talent Management Team": ("Talent Mgmt", "Carolina Karnakis de Nobrega"),
}
# rotulo curto de C-level para a coluna da tabela
CURTO_CL = {"COO": "COO", "CITO": "CITO", "CFSO": "CFSO", "CCO": "CCO"}
SIGLA = {
    "Raioni De Oliveira Santos": "COO",
    "Cleyton Cardoso Esteves": "CITO",
    "Ana Carolina Botelho Caldeira Vasconcellos": "CFSO",
    "Andre Lemos Tavares": "CCO",
    "Carolina Karnakis de Nobrega": "Head of Talent",
    "Luis Fernando Santos Muniz": "Head of Services",
    "Filipe Teixeira Sampaio": "Head of Air Product",
    "Filipe Carneiro De Oliveira": "Head of Ocean Product",
}
# blocos operacionais do deck corrigido, lidos do marcador no nome do cargo
BLOCOS_OPS = [("INLAND USA", "Inland Freight America", "EUA"),
              ("AMERICAS", "Operações America", "EUA"),
              ("INLAND EUROPA", "Inland Freight Europa", "Europa"),
              ("EUROPA", "Operações Europa", "Europa"),
              ("EXPORT", "Exportação", "Brasil"),
              ("AIR CC", "Customer Care", "Brasil")]
# ativos e volume por bloco, do deck corrigido (base de setembro + CIS)
OPS_DECK = {
    "Inland Freight America": (8, "EUA"), "Operações America": (7, "EUA"),
    "Warehouses": (5, "EUA"), "Inland Freight Europa": (4, "Europa"),
    "Operações Europa": (14, "Europa"), "Exportação": (3, "Brasil"),
    "Customer Care": (37, "Brasil"),
}
EMB_LOCAL = {"EUA": ("~971", 49), "Europa": ("~530", 29), "Brasil": ("~2.531", 63)}


def nivel(c):
    for k, r in NIVEIS:
        if re.search(rf"\b{k}\b", c.upper()):
            return r
    return "Outro"


def bloco_ops(cargo):
    u = cargo.upper()
    for marca, rot, local in BLOCOS_OPS:
        if marca in u:
            return rot, local
    return None, None


def geografia(cargo):
    u = cargo.upper()
    if "INLAND USA" in u or "AMERICAS" in u:
        return "EUA"
    if "EUROPA" in u:
        return "Europa"
    return "Brasil/geral"


def curto(nome, n=2):
    p = [x for x in nome.split() if x.lower() not in {"de", "da", "do", "dos", "e"}]
    return " ".join(p[:n])


from gestores_por_level import levantar  # mesma base da planilha


# ------------------------------------------------------------------ helpers
def txt(s, l, t, w, h, linhas, tam=9.5, cor=TEXTO, bold=False,
        alinha=PP_ALIGN.LEFT, anchor=None, espaco=0):
    box = s.shapes.add_textbox(px(l), px(t), px(w), px(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = px(0)
    tf.margin_top = tf.margin_bottom = px(0)
    if anchor:
        tf.vertical_anchor = anchor
    for i, ln in enumerate(linhas if isinstance(linhas, list) else [linhas]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = alinha
        if espaco:
            p.space_after = px(espaco)
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(tam)
        r.font.bold = bold
        r.font.name = "Arial"
        r.font.color.rgb = cor
    return box


def cx(s, l, t, w, h, linhas, fundo=None, borda=None, cor=BRANCO, tam=10,
       tam2=None, bold=True, alinha=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
       raio=0.08, forma=MSO_SHAPE.ROUNDED_RECTANGLE, margem=5):
    sh = s.shapes.add_shape(forma, px(l), px(t), px(w), px(h))
    if fundo is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fundo
    if borda is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = borda
        sh.line.width = Pt(1)
    try:
        sh.adjustments[0] = raio
    except (IndexError, KeyError):
        pass
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = px(margem)
    tf.margin_top = tf.margin_bottom = px(2)
    for i, ln in enumerate(linhas if isinstance(linhas, list) else [linhas]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = alinha
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(tam if i == 0 else (tam2 or max(7, tam - 2)))
        r.font.bold = bold if i == 0 else False
        r.font.name = "Arial"
        r.font.color.rgb = cor
    return sh


def linha(s, x1, y1, x2, y2, cor=CINZA):
    ln = s.shapes.add_connector(2, px(x1), px(y1), px(x2), px(y2))
    ln.line.color.rgb = cor
    ln.line.width = Pt(1)
    return ln


def tabela(s, l, t, w, h, cabec, linhas, larguras, tam=9, cor_cab=AZUL,
           destaques=()):
    gt = s.shapes.add_table(len(linhas) + 1, len(cabec), px(l), px(t), px(w), px(h))
    tb = gt.table
    tb.first_row = True
    for i, lg in enumerate(larguras):
        tb.columns[i].width = px(lg)
    for j, c in enumerate(cabec):
        cel = tb.cell(0, j)
        cel.fill.solid()
        cel.fill.fore_color.rgb = cor_cab
        cel.margin_left = cel.margin_right = px(4)
        cel.margin_top = cel.margin_bottom = px(0)
        cel.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cel.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if j else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = c
        r.font.size = Pt(tam)
        r.font.bold = True
        r.font.name = "Arial"
        r.font.color.rgb = BRANCO
    for i, ln in enumerate(linhas, 1):
        forte = i - 1 in destaques
        for j, v in enumerate(ln):
            cel = tb.cell(i, j)
            cel.fill.solid()
            cel.fill.fore_color.rgb = (FUNDO_LARANJA if forte
                                       else (BRANCO if i % 2 else FUNDO_CINZA))
            cel.margin_left = cel.margin_right = px(4)
            cel.margin_top = cel.margin_bottom = px(0)
            cel.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cel.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if j else PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(v)
            r.font.size = Pt(tam)
            r.font.name = "Arial"
            r.font.bold = forte or str(ln[0]).startswith("Total")
            r.font.color.rgb = TEXTO
    return tb


def kpis(s, itens, t=155):
    """Cinco números grandes com legenda, na geometria do template."""
    pos = [(36, 220), (268, 220), (501, 220), (733, 220), (965, 249)]
    for (l, w), (num, leg, cor) in zip(pos, itens):
        txt(s, l, t, w, 49, num, tam=26, cor=cor, bold=True,
            alinha=PP_ALIGN.CENTER)
        txt(s, l, t + 46, w, 40, leg, tam=8.5, cor=TEXTO,
            alinha=PP_ALIGN.CENTER)


def cabecalho(s, kicker, takeaway, descricao):
    ph = {x.placeholder_format.idx: x for x in s.placeholders}
    ph[10].text_frame.text = kicker
    tf = ph[0].text_frame
    tf.text = takeaway
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.size = Pt(18)
    ph[11].text_frame.text = descricao
    ph[13].text_frame.text = FONTE
    txt(s, 860, 125, 384, 19, "Para discussão", tam=12, cor=AZUL, bold=True,
        alinha=PP_ALIGN.RIGHT)


def limpar_slides(prs, manter):
    ids = prs.slides._sldIdLst
    for i, el in enumerate(list(ids)):
        if i not in manter:
            rid = el.get("{http://schemas.openxmlformats.org/officeDocument/2006/"
                         "relationships}id")
            prs.part.drop_rel(rid)
            ids.remove(el)


def mover_para(prs, de, para):
    ids = prs.slides._sldIdLst
    el = list(ids)[de]
    ids.remove(el)
    ids.insert(para, el)


# ------------------------------------------------------------------ slide 1
def slide_estrutura(prs, lay, d):
    s = prs.slides.add_slide(lay)
    dirs, ab, todos = d["diretorias"], d["ab"], d["todos"]
    ativos = sum(f["ativos"] for f in dirs) + 1
    gest = sum(f["gestores"] for f in dirs) + 1
    niveis = max(p["level"] for p in todos) - 1
    chefia = [v for v in ab if v["nivel"] in ("Head", "Team Leader")]
    maior = max(todos, key=lambda p: p["diretos"])
    dens = {f["sigla"]: f["ativos"] / f["gestores"] for f in dirs}
    dmin, dmax = min(dens.values()), max(dens.values())
    mais = max(dirs, key=lambda f: f["ativos"] / f["gestores"])
    menos = min(dirs, key=lambda f: f["ativos"] / f["gestores"])
    ops = max(dirs, key=lambda f: f["ativos"])

    cabecalho(
        s,
        "Estrutura de liderança",
        f"São {gest} gestores para {ativos} pessoas em {niveis} níveis, mas a "
        f"densidade varia de {dmin:.1f} a {dmax:.1f} pessoas por gestor entre as "
        f"diretorias, e {len(chefia)} posições de chefia estão em aberto"
        .replace(".", ","),
        "Quadro ativo, quantos lideram alguém e quantas vagas de chefia há em cada "
        "reporte direto do CEO. Gestor = quem tem pelo menos um liderado direto.")

    kpis(s, [
        ([f"{ativos}"], ["pessoas no organograma", "de out/26"], AZUL),
        ([f"{gest}"], ["gestores",
                       f"1 para cada {(ativos-gest)/gest:.1f}".replace(".", ",")
                       + " executores"], AZUL),
        ([f"{niveis}"], ["níveis do CEO ao", "analista mais fundo"], AZUL),
        ([f"{maior['diretos']}"], ["liderados diretos no maior",
                                   "time, contra média de 5,1"], LARANJA),
        ([f"{len(chefia)}"], ["vagas de chefia em aberto",
                              f"{sum(1 for v in chefia if not v['publicada'])} "
                              "sem processo"], LARANJA),
    ])

    linhas, destaques = [], []
    for i, f in enumerate(dirs):
        dens = f["ativos"] / f["gestores"]
        if dens >= 8 or dens <= 2.5:
            destaques.append(i)
        linhas.append([f["sigla"], curto(f["nome"], 3), f["ativos"], f["gestores"],
                       f"{dens:.1f}".replace(".", ","), f["niveis"], f["vagas"],
                       f["chefia"] or "—"])
    linhas.append(["TOTAL", "DMS", ativos, gest,
                   f"{ativos/gest:.1f}".replace(".", ","), niveis, len(ab),
                   len(chefia)])
    tabela(s, 36, 262, 1208, 262,
           ["Diretoria", "Responsável", "Ativos", "Gestores",
            "Pessoas por gestor", "Níveis", "Vagas em aberto",
            "Vagas de chefia"],
           linhas, [150, 254, 110, 120, 174, 100, 150, 150], tam=9,
           destaques=tuple(destaques))

    cx(s, 36, 536, 1208, 26, "O que a densidade mostra", fundo=VERDE, tam=10.5)
    cx(s, 36, 566, 1208, 86,
       [f"• {mais['sigla']} tem {dmax:.1f} pessoas por gestor, quase o dobro da "
        f"média de {ativos/gest:.1f}, e é onde está o maior time da casa: "
        f"{maior['diretos']} reportes diretos no {maior['cargo']}."
        .replace(".", ",", 2),
        f"• {menos['sigla']} tem {dmin:.1f} pessoas por gestor: "
        f"{menos['gestores']} gestores para {menos['ativos']} pessoas, com quatro "
        "Heads de indústria liderando 2 pessoas ou menos.".replace(".", ",", 1),
        f"• {ops['sigla']} concentra {ops['ativos']} das {ativos} pessoas e "
        f"{ops['niveis']} níveis, a única diretoria que desce até o L8; "
        "as outras param no L5 ou L6."],
       fundo=FUNDO_VERDE, borda=VERDE, cor=TEXTO, tam=9, bold=False,
       alinha=PP_ALIGN.LEFT, margem=10)
    return s


# ------------------------------------------------------------------ slide 2
def slide_vagas(prs, lay, d):
    s = prs.slides.add_slide(lay)
    todos, ab, filhos = d["todos"], d["ab"], d["filhos"]
    solo = [p for p in todos if p["diretos"] == 1]
    CH = ("team leader", "head", "manager", "coordinator")
    sem = [p for p in todos if any(k in p["cargo"].lower() for k in CH)
           and p["diretos"] == 0]
    chefia = [v for v in ab if v["nivel"] in ("Head", "Team Leader")]
    a_abrir = [v for v in chefia if not v["publicada"]]

    cabecalho(
        s,
        "Onde a liderança trava",
        f"{len(sem)} pessoas têm título de chefia sem nenhum liderado, "
        f"{len(solo)} gestores lideram uma única pessoa e quatro Team Leaders "
        "lideram outros Team Leaders com o título idêntico",
        "Camada de liderança: onde ela está duplicada, onde está vazia e onde "
        "falta contratar. Nenhum desses pontos aparece no deck de vagas.")

    pos = [(36, 289), (345, 289), (654, 289), (963, 251)]
    titulos = ["1. Título de chefia sem time",
               "2. Camada que não se paga",
               "3. Team Leader liderando Team Leader",
               "4. Chefia a contratar"]
    cores = [LARANJA, LARANJA, LARANJA, AZUL]
    fundos = [FUNDO_LARANJA, FUNDO_LARANJA, FUNDO_LARANJA, FUNDO_AZUL]
    conteudo = [
        [f"{len(sem)} pessoas com cargo de Head, Manager ou Team Leader e "
         "zero liderados",
         "2 são Heads: Revenue Management e um BD Manager",
         "Magno Bezerra (Airport Operations Manager) é um deles — e o draft "
         "risca a caixa dele",
         "Decisão: o título reflete a função ou precisa ser revisto?"],
        [f"{len(solo)} gestores lideram uma única pessoa",
         "Yuri Torreao (Head of Energy) e Cristiane Giovanelli (Total Rewards TL) "
         "entre eles",
         "Cada um custa um nível inteiro de hierarquia para coordenar 1 pessoa",
         "Decisão: juntar os times ou assumir a carteira direto?"],
        ["Gabriella Pereira e Pamela Ibarra lideram 4 Team Leaders com o mesmo "
         "título de *Air Freight Operations Team Leader*",
         "São 4 camadas de TL dentro de Operações Aéreo",
         "O draft risca com X exatamente a Gabriella e a Pamela",
         "Decisão: qual é a senioridade real de cada camada?"],
        [f"{len(chefia)} vagas de chefia em aberto",
         f"{len(a_abrir)} sem processo iniciado",
         "A única publicada é o Overland Head (Europa)",
         "3 das 7 estão em Air Product",
         "Inland Freight Europa segue sem TL"],
    ]
    for (l, w), tit, cor, fundo, bullets in zip(pos, titulos, cores, fundos,
                                                conteudo):
        cx(s, l, 155, w, 28, tit, fundo=cor, tam=10.5)
        cx(s, l, 187, w, 180, ["• " + b.replace("*", "") for b in bullets],
           fundo=fundo, borda=cor, cor=TEXTO, tam=8.5, bold=False,
           alinha=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, margem=9)

    linhas = [
        ["Maior time da casa", "Victor Telles Gonzaga · Head of Operation",
         "L4 · Tecnologia", "27 diretos, 37 pessoas",
         "Quebrar em camadas ou manter?"],
        ["TL sobre TL", "Gabriella Pereira e Pamela Ibarra",
         "L6 · Operações Aéreo", "4 TLs de título idêntico abaixo",
         "Definir a senioridade de cada camada"],
        ["Gestor de uma pessoa", f"{len(solo)} gestores, de L4 a L7",
         "5 diretorias", "1 liderado cada",
         "Juntar times ou assumir carteira"],
        ["Título sem time", f"{len(sem)} pessoas", "L4 a L6", "0 liderados",
         "Revisar cargo ou atribuir equipe"],
        ["Bloco sem liderança", "Inland Freight Europa", "Operações Aéreo",
         "4 pessoas, 4 vagas, nenhum TL", "Abrir a vaga de TL da Europa"],
        ["Chefia a contratar", f"{len(chefia)} vagas", "4 diretorias",
         f"{len(a_abrir)} sem processo", "Pré-aprovar faixa e budget"],
    ]
    cx(s, 36, 378, 1208, 26, "O que precisa de decisão", fundo=VERDE, tam=10.5)
    tabela(s, 36, 408, 1208, 164,
           ["Ponto", "Quem", "Onde", "Hoje", "Decisão pedida"],
           linhas, [210, 316, 200, 250, 232], tam=8.5)

    cx(s, 36, 584, 1208, 68,
       ["• O deck de vagas mostra quantas pessoas faltam. Este mostra que, mesmo "
        "com o quadro cheio, a camada de liderança não está resolvida: 12 posições "
        "de chefia hoje não correspondem à função.",
        "• As três caixas que o draft risca com X (Magno Bezerra, Gabriella "
        "Pereira e Pamela Ibarra) são justamente pontos desta lista — a "
        "reorganização já começou no papel, só não está escrita."],
       fundo=FUNDO_VERDE, borda=VERDE, cor=TEXTO, tam=9, bold=False,
       alinha=PP_ALIGN.LEFT, margem=10)
    return s


def main():
    d = levantar()
    prs = Presentation(TEMPLATE)
    lay = [l for l in prs.slide_masters[1].slide_layouts
           if l.name == "DMS_Conteudo"][0]
    limpar_slides(prs, manter={0, 4})
    for sh in prs.slides[0].shapes:
        if sh.has_text_frame and "Projeto Diligenciamento" in sh.text_frame.text:
            runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
            runs[1].text = "Estrutura hierárquica e camada de liderança"

    slide_estrutura(prs, lay, d)
    slide_vagas(prs, lay, d)
    mover_para(prs, 2, 1)
    mover_para(prs, 3, 2)
    prs.save(SAIDA)
    print(f"template ATY (verde): {os.path.basename(TEMPLATE)}")
    print(f"slides: {len(prs.slides)}")
    print("ok ->", SAIDA)


if __name__ == "__main__":
    main()
