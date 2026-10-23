#!/usr/bin/env python3
"""
Gera dois slides de conteudo sobre estrutura hierarquica x vagas em aberto,
usando o template verde da DMS.

Template: 'DMS - Vagas em aberto x Ocupação nas Operações.pptx'
  master 1, layout 'DMS_Conteudo'
  azul 005E9E, verde 009796, laranja FF8E2E, texto 333333, Arial

Saida: estrutura/DMS - Estrutura hierarquica x Vagas em aberto.pptx

Uso:  python3 estrutura/gerar_slides.py
"""
import copy
import os
import re
from collections import Counter, defaultdict

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt


def px(v):
    """O template foi medido em pixels de 96 DPI (1 px = 9525 EMU).
    Tamanho de fonte continua em pontos."""
    return Emu(int(round(v * 9525)))

from cross_check import RAIZ, ler_aba, ler_factorial, montar

TEMPLATE = os.path.join(RAIZ, "DMS - Vagas em aberto x Ocupação nas Operações.pptx")
SAIDA = os.path.join(RAIZ, "estrutura",
                     "DMS - Estrutura hierarquica x Vagas em aberto.pptx")
FONTE = ("Fonte: Colaboradores-factorial (3) — organograma, out/26; "
         "Vagas 21/10; Base Setembro/26 (RH); Draft 23 Out 26")

AZUL = RGBColor(0x00, 0x5E, 0x9E)
VERDE = RGBColor(0x00, 0x97, 0x96)
LARANJA = RGBColor(0xFF, 0x8E, 0x2E)
CINZA_BARRA = RGBColor(0xA6, 0xA6, 0xA6)
FUNDO_AZUL = RGBColor(0xE5, 0xF0, 0xF8)
FUNDO_LARANJA = RGBColor(0xFD, 0xF0, 0xE4)
FUNDO_CINZA = RGBColor(0xF2, 0xF2, 0xF2)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
TEXTO = RGBColor(0x33, 0x33, 0x33)


# -------------------------------------------------------------- dados
NIVEIS = [("HEAD", "Head"), ("TL", "Team Leader"), ("SPEC", "Specialist"),
          ("ANALYST", "Analyst"), ("ASSIST", "Assistant"), ("INTERN", "Intern"),
          ("APPRENTICE", "Aprendiz")]
REGIOES = [("INLAND USA", "EUA"), ("INLAND EUROPA", "Europa"), ("EUROPA", "Europa"),
           ("AMERICAS", "Americas"), ("ASIA", "Ásia"), ("EXPORT", "Exportação")]

# Cada area da planilha de vagas ligada ao bloco do organograma.
BLOCO = {
    "Air Operations": ("Air Operations", "Carolina Bento Mendoza", "COO"),
    "Air Product": ("Air Product", "Filipe Teixeira Sampaio", "CEO*"),
    "Ocean Operations": ("Ocean Operations", "Natalia Correia Da Costa Parreira", "COO"),
    "Ocean Product": ("Ocean Product", "Filipe Carneiro De Oliveira", "CEO*"),
    "Quality & Operational Intelligence": ("Quality & Op. Intelligence",
                                           "Marco Antonio Maraia Villa", "COO"),
    "Overland (Europa)": ("Overland", "Possidonio Dantas de Almeida Neto", "COO"),
    "Services": ("Services", "Luis Fernando Santos Muniz", "CEO"),
    "Special Operations": ("Special Operations", "— sem bloco no organograma", "COO"),
    "Healthcare": ("Healthcare", "Jose Carlos Duarte Freitas Sobrinho", "CCO"),
    "High-Tech": ("High-Tech", "Ricardo Tebexreni Jakowatz", "CCO"),
    "Automotive": ("Automotive", "Ricardo Tebexreni Jakowatz", "CCO"),
    "Financial": ("Financial", "Ana Carolina Botelho Caldeira Vasconcellos", "CFSO"),
    "Technology": ("Technology", "Cleyton Cardoso Esteves", "CITO"),
    "Talent Management Team": ("Talent Management", "Carolina Karnakis de Nobrega",
                               "Head of Talent"),
}


def nivel(cargo):
    for k, r in NIVEIS:
        if re.search(rf"\b{k}\b", cargo.upper()):
            return r
    return "Outro"


def regiao(cargo):
    for k, r in REGIOES:
        if k in cargo.upper():
            return r
    return "sem região"


def br(n):
    return f"{n:,}".replace(",", ".")


def levantar():
    fac = ler_factorial()
    todos, filhos, ceo = montar(fac, aplicar_draft=True)
    idx = {p["nome"]: p for p in todos}

    vagas = ler_aba("Vagas 21-10.xlsx", "Vagas", "CARGO")
    for v in vagas:
        v["preenchida"] = (bool(v.get("CONTRATADO"))
                           or str(v.get("STATUS GUPY")) == "FECHADA"
                           or str(v.get("Admissão") or "")[:10] == "2026-10-01")
        v["nivel"] = nivel(str(v["CARGO"]))
        v["regiao"] = regiao(str(v["CARGO"]))
        v["publicada"] = str(v.get("STATUS GUPY")) == "ABERTA | PUBLICADA"
    abertas = [v for v in vagas if not v["preenchida"]]

    blocos = {}
    for v in abertas:
        rot, head, clv = BLOCO[str(v["ARÉA"])]
        b = blocos.setdefault(rot, {"head": head, "clevel": clv, "vagas": 0,
                                    "custo": 0, "lid": 0, "pub": 0, "ativos": 0})
        b["vagas"] += 1
        b["custo"] += v["TT Custo/Mês"]
        b["lid"] += 1 if v["nivel"] in ("Head", "Team Leader") else 0
        b["pub"] += 1 if v["publicada"] else 0
    # Automotive e High-Tech dividem o mesmo head: soma o quadro uma vez so
    usados = set()
    for rot, b in blocos.items():
        p = idx.get(b["head"])
        if p and b["head"] not in usados:
            b["ativos"] = p["total"] + 1
            usados.add(b["head"])
        elif p:
            b["ativos"] = 0
            b["head"] += " (quadro contado em outro bloco)"
    for rot, b in blocos.items():
        b["quadro"] = b["ativos"] + b["vagas"]
        b["pct"] = b["vagas"] / b["quadro"] if b["quadro"] else 0

    return {"todos": todos, "filhos": filhos, "ceo": ceo, "idx": idx,
            "vagas": vagas, "abertas": abertas, "blocos": blocos}


# -------------------------------------------------------------- helpers pptx
def txt(slide, l, t, w, h, linhas, tam=9.5, cor=TEXTO, bold=False,
        alinha=PP_ALIGN.LEFT, anchor=None):
    box = slide.shapes.add_textbox(px(l), px(t), px(w), px(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = px(0)
    tf.margin_top = tf.margin_bottom = px(0)
    if anchor:
        tf.vertical_anchor = anchor
    for i, ln in enumerate(linhas if isinstance(linhas, list) else [linhas]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = alinha
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(tam)
        r.font.bold = bold
        r.font.name = "Arial"
        r.font.color.rgb = cor
    return box


def barra(slide, l, t, w, rotulo, cor=AZUL, h=26):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px(l), px(t), px(w), px(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = cor
    sh.line.fill.background()
    sh.adjustments[0] = 0.12
    tf = sh.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = rotulo
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.name = "Arial"
    r.font.color.rgb = BRANCO
    return sh


def caixa(slide, l, t, w, h, bullets, fundo=FUNDO_AZUL, tam=9.5):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px(l), px(t), px(w), px(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fundo
    sh.line.fill.background()
    sh.adjustments[0] = 0.06
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = px(8)
    tf.margin_top = tf.margin_bottom = px(6)
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = "• " + b
        r.font.size = Pt(tam)
        r.font.name = "Arial"
        r.font.color.rgb = TEXTO
        p.space_after = px(2)
    return sh


def kpis(slide, itens, t=155):
    """Cinco blocos de numero grande + legenda, na geometria do template."""
    pos = [(36, 220), (268, 220), (501, 220), (733, 220), (965, 249)]
    for (l, w), (num, leg, cor) in zip(pos, itens):
        txt(slide, l, t, w, 49, num, tam=26, cor=cor, bold=True,
            alinha=PP_ALIGN.CENTER)
        txt(slide, l, t + 46, w, 40, leg, tam=8.5, cor=TEXTO,
            alinha=PP_ALIGN.CENTER)


def tabela(slide, l, t, w, h, cabec, linhas, larguras, tam=8.5):
    gt = slide.shapes.add_table(len(linhas) + 1, len(cabec), px(l), px(t), px(w), px(h))
    tb = gt.table
    tb.first_row = True
    for i, lg in enumerate(larguras):
        tb.columns[i].width = px(lg)
    for j, c in enumerate(cabec):
        cel = tb.cell(0, j)
        cel.fill.solid()
        cel.fill.fore_color.rgb = AZUL
        cel.margin_left = cel.margin_right = px(4)
        cel.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cel.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if j else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = c
        r.font.size = Pt(tam)
        r.font.bold = True
        r.font.name = "Arial"
        r.font.color.rgb = BRANCO
    for i, linha in enumerate(linhas, 1):
        for j, v in enumerate(linha):
            cel = tb.cell(i, j)
            cel.fill.solid()
            cel.fill.fore_color.rgb = BRANCO if i % 2 else FUNDO_CINZA
            cel.margin_left = cel.margin_right = px(4)
            cel.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cel.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if j else PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(v)
            r.font.size = Pt(tam)
            r.font.name = "Arial"
            r.font.bold = bool(linha[0] == "Total")
            r.font.color.rgb = TEXTO
    return tb


def cabecalho(slide, kicker, takeaway, descricao):
    ph = {s.placeholder_format.idx: s for s in slide.placeholders}
    ph[10].text_frame.text = kicker
    tf = ph[0].text_frame
    tf.text = takeaway
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.size = Pt(18)
    ph[11].text_frame.text = descricao
    ph[13].text_frame.text = FONTE
    txt(slide, 860, 125, 384, 19, "Para discussão", tam=12, cor=AZUL, bold=True,
        alinha=PP_ALIGN.RIGHT)


def limpar_slides(prs, manter):
    """Mantem apenas os indices informados, preservando a ordem."""
    ids = prs.slides._sldIdLst
    alvos = list(ids)
    for i, el in enumerate(alvos):
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


# -------------------------------------------------------------- slides
def slide_blocos(prs, lay, d):
    s = prs.slides.add_slide(lay)
    ab, bl = d["abertas"], d["blocos"]
    custo = sum(v["TT Custo/Mês"] for v in ab)
    coo = sum(1 for v in ab if v["C-LEVEL"] == "COO")
    lid = sum(1 for v in ab if v["nivel"] in ("Head", "Team Leader"))
    pub = sum(1 for v in ab if v["publicada"])
    # so blocos com quadro conhecido entram na disputa de "maior buraco"
    pior = max((kv for kv in bl.items() if kv[1]["ativos"]),
               key=lambda kv: kv[1]["pct"])

    cabecalho(
        s,
        "Estrutura e vagas em aberto, bloco a bloco",
        f"{len(ab)} vagas realmente em aberto custam R$ {br(custo)} por mês; "
        f"{coo/len(ab)*100:.0f}% estão sob o COO e {pior[0]} é o maior buraco "
        f"relativo, com {pior[1]['vagas']} vagas para {pior[1]['ativos']} pessoas",
        "Quadro ativo do organograma contra as posições em aberto, agrupado pelos "
        "mesmos blocos do organograma. Vagas de liderança são Head e Team Leader.")

    kpis(s, [
        ([f"{len(ab)}"], ["posições em aberto",
                          f"(de {len(d['vagas'])} registros na planilha)"], AZUL),
        ([f"R$ {br(custo)}"], ["custo mensal do quadro", "em aberto"], AZUL),
        ([f"{coo/len(ab)*100:.0f}%"], ["das vagas em aberto", "estão sob o COO"], AZUL),
        ([f"{lid}"], ["vagas de liderança",
                      f"({sum(1 for v in ab if v['nivel']=='Head')} Head e "
                      f"{sum(1 for v in ab if v['nivel']=='Team Leader')} "
                      f"Team Leaders)"], LARANJA),
        ([f"{pub} de {len(ab)}"], ["vagas publicadas no Gupy",
                                   f"— {len(ab)-pub} sem status de processo"], LARANJA),
    ])

    linhas = []
    for rot, b in sorted(bl.items(), key=lambda kv: -kv[1]["vagas"]):
        linhas.append([rot, b["clevel"], b["head"][:34],
                       b["ativos"] or "—", b["vagas"],
                       f"{b['pct']*100:.0f}%" if b["ativos"] else "—",
                       b["lid"] or "—", f"R$ {br(b['custo'])}"])
    linhas.append(["Total dos blocos com vaga", "", "",
                   sum(b["ativos"] for b in bl.values()), len(ab), "", lid,
                   f"R$ {br(custo)}"])
    tabela(s, 36, 258, 1178, 378,
           ["Bloco (área da vaga)", "C-level", "Head responsável", "Ativos",
            "Vagas", "% do quadro em aberto", "Vagas de liderança", "Custo/mês"],
           linhas, [196, 78, 250, 66, 62, 112, 110, 304], tam=8)
    txt(s, 36, 640, 1178, 20,
        "CEO* = Air Product e Ocean Product reportam ao CEO pelas caixas azuis do "
        "draft; na planilha Factorial ainda estão sob o COO. Automotive e High-Tech "
        "dividem o mesmo head, e o quadro é contado uma vez só.",
        tam=7.5, cor=RGBColor(0x60, 0x60, 0x60))
    return s


def slide_atencao(prs, lay, d):
    s = prs.slides.add_slide(lay)
    ab, bl = d["abertas"], d["blocos"]
    hc = bl["Healthcare"]
    ap = bl["Air Product"]
    reg = Counter(v["regiao"] for v in ab if v["regiao"] != "sem região")
    pub = sum(1 for v in ab if v["publicada"])
    colchao = sum(1 for v in ab if v["Folha/Colchão"] == "Colchão")

    cabecalho(
        s,
        "Vagas, pontos de atenção",
        "Healthcare tem mais vaga que gente, Air Product concentra 3 das 7 vagas "
        "de chefia e o draft já risca dois Team Leaders de Air Operations",
        "Blocos com maior proporção de quadro em aberto, camada de liderança "
        "descoberta e abertura por região das posições de operação")

    pos = [(36, 289), (345, 289), (654, 289), (963, 251)]
    titulos = ["1. Healthcare: mais vaga que gente",
               "2. Chefia em aberto, 3 em Air Product",
               "3. Abertura por região",
               "4. Fila sem processo"]
    cores = [LARANJA, LARANJA, LARANJA, CINZA_BARRA]
    fundos = [FUNDO_LARANJA, FUNDO_LARANJA, FUNDO_LARANJA, FUNDO_CINZA]
    conteudo = [
        [f"{hc['pct']*100:.0f}% do quadro em aberto, o maior de todos os blocos",
         f"{hc['ativos']} pessoas ativas e {hc['vagas']} vagas",
         "O Head tem só 2 liderados hoje",
         "Todas as 4 são BD Executive",
         f"R$ {br(hc['custo'])} por mês quando preenchidas",
         f"{hc['pub']} das {hc['vagas']} está publicada"],
        [f"{ap['lid']} das 7 vagas de liderança estão em Air Product",
         "1 Air RD TL e 2 Air Ops TL Americas",
         "O bloco tem 2 reportes diretos para 29 pessoas",
         "Overland Head (Europa) é a única publicada, R$ 31.833",
         "Financial e Technology têm 1 TL cada em aberto",
         "O draft marca 'Vaga de TL' em High-Tech, que não está na planilha"],
        [f"Americas {reg['Americas']}, Europa {reg['Europa']}, "
         f"EUA {reg['EUA']}, Ásia {reg['Ásia']}",
         f"{sum(reg.values())} das {len(ab)} vagas já trazem a região no cargo",
         "É exatamente a abertura que o draft pede nos slides 6 e 14",
         "Pamela Ibarra, riscada com X no draft, é a única TL sediada na Europa",
         "Gabriella Pereira, também riscada, lidera 9 pessoas no Rio"],
        [f"{len(ab)-pub} das {len(ab)} vagas sem status no Gupy",
         f"{pub} publicadas",
         f"{colchao} vaga em Colchão, fora da folha" if colchao == 1
         else f"{colchao} vagas em Colchão, fora da folha",
         "Special Operations não tem bloco no organograma",
         "3 vagas de Air Ops Intern sem data"],
    ]
    for (l, w), tit, cor, fundo, bullets in zip(pos, titulos, cores, fundos, conteudo):
        barra(s, l, 155, w, tit, cor=cor)
        caixa(s, l, 186, w, 209, bullets, fundo=fundo, tam=8.5)

    lideranca = [v for v in ab if v["nivel"] in ("Head", "Team Leader")]
    linhas = []
    for v in sorted(lideranca, key=lambda x: -x["TT Custo/Mês"]):
        rot, head, clv = BLOCO[str(v["ARÉA"])]
        linhas.append([v["CARGO"], v["nivel"], clv, rot, head[:30],
                       f"R$ {br(v['TT Custo/Mês'])}",
                       "publicada" if v["publicada"] else "sem status"])
    tabela(s, 36, 404, 1178, 176,
           ["Vaga de liderança em aberto", "Nível", "C-level", "Bloco",
            "Head responsável hoje", "Custo/mês", "Status no Gupy"],
           linhas, [268, 92, 78, 180, 230, 130, 200])

    barra(s, 36, 588, 1178, "Leitura", cor=VERDE, h=22)
    caixa(s, 36, 613, 1178, 42,
          ["Seis das sete vagas de chefia estão sem status de processo, "
           "então a camada de liderança é o gargalo que ninguém começou a resolver — "
           "e três delas ficam no mesmo bloco que o draft está reorganizando."],
          fundo=FUNDO_CINZA, tam=9)
    return s


def main():
    prs = Presentation(TEMPLATE)
    lay = [l for l in prs.slide_masters[1].slide_layouts
           if l.name == "DMS_Conteudo"][0]

    # capa (0) e encerramento (4); remove os 3 slides de conteudo antigos
    limpar_slides(prs, manter={0, 4})
    for sh in prs.slides[0].shapes:
        if sh.has_text_frame and "Projeto Diligenciamento" in sh.text_frame.text:
            runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
            runs[1].text = "Estrutura hierárquica x vagas em aberto"

    slide_blocos(prs, lay, DADOS)
    slide_atencao(prs, lay, DADOS)
    mover_para(prs, 2, 1)   # slide de blocos antes do encerramento
    mover_para(prs, 3, 2)   # slide de atencao depois dele

    prs.save(SAIDA)
    ab = DADOS["abertas"]
    print(f"{len(DADOS['vagas'])} registros -> {len(ab)} vagas em aberto")
    print(f"blocos mapeados: {len(DADOS['blocos'])}")
    print(f"slides: {len(prs.slides)} (capa + 2 conteúdo + encerramento)")
    print("ok ->", SAIDA)


if __name__ == "__main__":
    DADOS = levantar()
    main()
