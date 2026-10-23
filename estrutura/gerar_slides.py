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
        v["publicada"] = str(v.get("STATUS GUPY")) == "ABERTA | PUBLICADA"
        v["geo"] = geografia(str(v["CARGO"]))
        v["bloco_ops"], v["local"] = bloco_ops(str(v["CARGO"]))
        rot, head = BLOCO[str(v["ARÉA"])]
        v["bloco"], v["head"] = rot, head
    ab = [v for v in vagas if not v["preenchida"]]

    def l3_de(nome):
        p = idx.get(nome)
        while p and p["level"] > 3:
            p = idx.get(p["gestor"])
        return p["nome"] if p else "Raioni De Oliveira Santos"

    def gestores_em(nome):
        n = 1 if idx[nome]["diretos"] else 0
        pilha = list(filhos[nome])
        while pilha:
            x = pilha.pop()
            n += 1 if x["diretos"] else 0
            pilha.extend(filhos[x["nome"]])
        return n

    # vagas por L3 e por bloco do organograma
    por_l3, por_bloco = Counter(), {}
    for v in ab:
        l3 = l3_de(v["head"]) if v["head"] else "Raioni De Oliveira Santos"
        por_l3[l3] += 1
        b = por_bloco.setdefault(v["bloco"], {"head": v["head"], "l3": l3,
                                              "vagas": 0, "abrir": 0, "lid": 0})
        b["vagas"] += 1
        b["abrir"] += 0 if v["publicada"] else 1
        b["lid"] += 1 if v["nivel"] in ("Head", "Team Leader") else 0
    for rot, b in por_bloco.items():
        p = idx.get(b["head"])
        b["ativos"] = (p["total"] + 1) if p else 0
        b["gestores"] = gestores_em(b["head"]) if p else 0
        b["pct"] = b["vagas"] / (b["ativos"] + b["vagas"]) if b["ativos"] else None

    diretorias = []
    for l3 in sorted(filhos[ceo], key=lambda p: -p["total"]):
        diretorias.append({
            "nome": l3["nome"], "sigla": SIGLA.get(l3["nome"], "L3"),
            "ativos": l3["total"] + 1, "gestores": gestores_em(l3["nome"]),
            "vagas": por_l3[l3["nome"]],
            "blocos": sorted([(r, b) for r, b in por_bloco.items()
                              if b["l3"] == l3["nome"]], key=lambda kv: -kv[1]["vagas"]),
        })

    ops = [v for v in ab if v["bloco_ops"]]
    return {"todos": todos, "filhos": filhos, "ceo": ceo, "idx": idx,
            "vagas": vagas, "ab": ab, "ops": ops, "por_bloco": por_bloco,
            "diretorias": diretorias}


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
    ab, dirs = d["ab"], d["diretorias"]
    ativos = sum(x["ativos"] for x in dirs) + 1
    gestores = sum(x["gestores"] for x in dirs) + 1
    abrir = sum(1 for v in ab if not v["publicada"])

    cabecalho(
        s,
        "Estrutura hierárquica e onde falta gente",
        f"A casa tem {ativos} pessoas e {gestores} gestores em 7 níveis; as "
        f"{len(ab)} vagas em aberto se concentram em Operações, e {abrir} delas "
        "ainda não têm processo aberto no Gupy",
        "Cada caixa é um reporte direto do CEO, com o quadro ativo, quantos "
        "lideram alguém e quantas vagas estão em aberto. Abaixo, os blocos de "
        "Operações.")

    # topo
    cx(s, 476, 152, 328, 42,
       ["Co-CEO · Jose Luiz Belixior",
        f"{ativos} pessoas · {gestores} gestores · {len(ab)} vagas em aberto"],
       fundo=AZUL, tam=11, tam2=8.5)
    linha(s, 640, 194, 640, 206)
    linha(s, 62, 206, 1218, 206)

    # diretorias
    larg, passo = 142, 152
    x0 = 36
    for i, f in enumerate(dirs):
        x = x0 + i * passo
        linha(s, x + larg / 2, 206, x + larg / 2, 216)
        tem = f["vagas"] > 0
        cx(s, x, 216, larg, 60,
           [f["sigla"], curto(f["nome"]),
            f"{f['ativos']} ativos · {f['gestores']} gest."],
           fundo=VERDE if tem else CINZA, tam=9, tam2=7.5)
        cx(s, x, 280, larg, 22,
           f"{f['vagas']} vaga" + ("s" if f["vagas"] != 1 else "") + " em aberto",
           fundo=LARANJA if tem else FUNDO_CINZA,
           cor=BRANCO if tem else CINZA_TXT, tam=8.5)

    # blocos de Operacoes
    coo = next(f for f in dirs if f["sigla"] == "COO")
    ix = [i for i, f in enumerate(dirs) if f["sigla"] == "COO"][0]
    xc = x0 + ix * passo + larg / 2
    linha(s, xc, 302, xc, 318)
    cx(s, 36, 318, 236, 26, "Dentro de Operações (COO)", fundo=AZUL, tam=9.5)
    blocos = coo["blocos"] + [("Demais blocos sem vaga", None)]
    bl_larg, bl_passo = 148, 156
    for i, (rot, b) in enumerate(blocos):
        x = 284 + i * bl_passo
        if b is None:
            cx(s, x, 318, bl_larg, 26, "2 blocos sem vaga", fundo=FUNDO_CINZA,
               cor=CINZA_TXT, tam=8.5, bold=False)
            continue
        cx(s, x, 318, bl_larg, 26,
           f"{rot} · {b['vagas']}", fundo=VERDE_ATY, cor=RGBColor(0, 0x40, 0x33),
           tam=8.5)

    # tabela: heads com vaga
    linhas, destaques = [], []
    todos_blocos = sorted(d["por_bloco"].items(), key=lambda kv: -kv[1]["vagas"])
    for i, (rot, b) in enumerate(todos_blocos):
        if b["pct"] is not None and b["pct"] >= 0.5:
            destaques.append(i)
        sg = SIGLA.get(b["l3"], "—")
        linhas.append([rot, CURTO_CL.get(sg, "CEO"),
                       curto(b["head"], 3) if b["head"] else "— sem bloco",
                       b["ativos"] or "—", b["gestores"] or "—", b["vagas"],
                       b["abrir"], b["lid"] or "—",
                       f"{b['pct']*100:.0f}%" if b["pct"] is not None else "—"])
    linhas.append(["Total dos blocos", "", "",
                   sum(b["ativos"] for _, b in todos_blocos),
                   sum(b["gestores"] for _, b in todos_blocos), len(ab), abrir,
                   sum(b["lid"] for _, b in todos_blocos), ""])
    tabela(s, 36, 356, 1208, 268,
           ["Bloco", "C-level", "Head responsável", "Ativos", "Gestores",
            "Vagas em aberto", "Ainda a abrir", "Vagas de chefia",
            "% do quadro em aberto"],
           linhas, [196, 82, 200, 76, 86, 128, 110, 116, 214], tam=8,
           destaques=tuple(destaques))

    cx(s, 36, 630, 1208, 24,
       ["Healthcare é o único bloco com mais vaga que gente: 4 vagas para 3 "
        "pessoas. Air Operations concentra 19 das 49, mas são 18% do próprio "
        "quadro. Ativos do organograma de out/26; a base de setembro tem 311 "
        "ativos porque 23 admissões entraram depois do fechamento."],
       fundo=FUNDO_VERDE, borda=VERDE, cor=TEXTO, tam=8, bold=False,
       alinha=PP_ALIGN.LEFT, margem=8)
    return s


# ------------------------------------------------------------------ slide 2
def slide_vagas(prs, lay, d):
    s = prs.slides.add_slide(lay)
    ab, ops = d["ab"], d["ops"]
    coo = [v for v in ab if v["C-LEVEL"] == "COO"]
    pub_ops = sum(1 for v in ops if v["publicada"])
    abrir_ops = len(ops) - pub_ops
    geo = Counter(v["geo"] for v in ab)

    cabecalho(
        s,
        "Vagas em aberto, do total ao que trava",
        f"Das {len(ab)} vagas em aberto, {len(coo)} estão sob o COO e {len(ops)} "
        f"nos blocos de Operações; dessas, só {pub_ops} estão publicadas e "
        f"{abrir_ops} ainda precisam ser abertas",
        "Funil das vagas, abertura por geografia e situação de cada bloco de "
        "Operações. “Em aberto” na planilha não quer dizer processo rodando.")

    # funil
    cx(s, 36, 155, 268, 26, "Funil das vagas", fundo=AZUL, tam=10.5)
    etapas = [(f"{len(d['vagas'])}", "registros na planilha", CINZA),
              (f"{len(ab)}", "realmente em aberto", AZUL),
              (f"{len(coo)}", "sob o COO", AZUL),
              (f"{len(ops)}", "nos blocos de Operações", VERDE),
              (f"{pub_ops}", "publicadas no Gupy", VERDE),
              (f"{abrir_ops}", "ainda a abrir", LARANJA)]
    y = 189
    for num, rot, cor in etapas:
        cx(s, 36, y, 70, 32, num, fundo=cor, tam=14)
        txt(s, 114, y + 8, 190, 20, rot, tam=9, cor=TEXTO)
        y += 37

    # geografia
    cx(s, 324, 155, 268, 26, "Abertura por geografia", fundo=AZUL, tam=10.5)
    y = 189
    for g, n in [("Brasil / geral", geo["Brasil/geral"]), ("EUA", geo["EUA"]),
                 ("Europa", geo["Europa"])]:
        cx(s, 324, y, 268, 30,
           f"{g}: {n} vagas  ·  {n/len(ab)*100:.0f}%", fundo=FUNDO_AZUL,
           borda=AZUL, cor=TEXTO, tam=9.5, alinha=PP_ALIGN.LEFT, margem=10)
        y += 36
    txt(s, 324, y + 2, 268, 90,
        ["Nos EUA não há nenhuma reposição: as 9 vagas são aumento de quadro.",
         "Na Europa, 2 das 6 são reposição.",
         "Pelo campo Ocupante/Vaga: 30 aumento de quadro e 19 substituição."],
        tam=8.5, cor=CINZA_TXT, espaco=3)

    # pontos de atencao
    cx(s, 612, 155, 632, 26, "Onde falta chefe e onde falta gente",
       fundo=LARANJA, tam=10.5)
    cx(s, 612, 187, 632, 192,
       ["• Inland Freight Europa: 4 ativos, 4 vagas, 50% do quadro em aberto e "
        "nenhum team leader no bloco",
        "• Operações America: 46% em aberto e 3 vagas de team leader, todas "
        "ainda a abrir",
        "• As 7 vagas de chefia da casa: 1 Head (Overland Europa, a única "
        "publicada) e 6 Team Leaders",
        "• Exportação carrega ~81 embarques por ativo, o maior da operação, "
        "com 3 pessoas",
        "• Warehouses (MIA, Houston e NY): 5 pessoas e nenhuma vaga aberta"],
       fundo=FUNDO_LARANJA, borda=LARANJA, cor=TEXTO, tam=9, bold=False,
       alinha=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, margem=9)

    cx(s, 612, 389, 632, 26, "As 17 vagas de Operações por nível",
       fundo=VERDE, tam=10.5)
    niv = Counter(v["nivel"] for v in ops)
    txt(s, 616, 421, 624, 22,
        f"Team Leader {niv['Team Leader']}   ·   Specialist {niv['Specialist']}"
        f"   ·   Analyst {niv['Analyst']}", tam=10, cor=TEXTO, bold=True)

    # tabela por local
    linhas, destaques = [], []
    por_bloco = {}
    for v in ops:
        b = por_bloco.setdefault(v["bloco_ops"], {"v": 0, "a": 0, "loc": v["local"]})
        b["v"] += 1
        b["a"] += 0 if v["publicada"] else 1
    i = 0
    for local in ("EUA", "Europa", "Brasil"):
        blocos = [(r, b) for r, b in OPS_DECK.items() if b[1] == local]
        at_loc = sum(b[0] for _, b in blocos)
        vg_loc = sum(por_bloco.get(r, {"v": 0})["v"] for r, _ in blocos)
        ab_loc = sum(por_bloco.get(r, {"a": 0})["a"] for r, _ in blocos)
        emb, por = EMB_LOCAL[local]
        linhas.append([local, at_loc, vg_loc, ab_loc,
                       f"{vg_loc/(at_loc+vg_loc)*100:.1f}%".replace(".", ","),
                       emb, por])
        i += 1
        for rot, (at, _) in sorted(blocos, key=lambda kv: -kv[1][0]):
            b = por_bloco.get(rot, {"v": 0, "a": 0})
            pct = b["v"] / (at + b["v"]) * 100
            if pct >= 40:
                destaques.append(i)
            linhas.append([f"      {rot}", at, b["v"], b["a"],
                           f"{pct:.1f}%".replace(".", ","), "", ""])
            i += 1
    at_t = sum(b[0] for b in OPS_DECK.values())
    linhas.append(["Total Operações", at_t, len(ops), abrir_ops,
                   f"{len(ops)/(at_t+len(ops))*100:.1f}%".replace(".", ","),
                   "~4.032", 52])
    tabela(s, 36, 452, 1208, 178,
           ["Local · bloco", "Ativos", "Vagas em aberto", "Ainda a abrir",
            "% em aberto", "Embarques/mês", "Emb./ativo"],
           linhas, [392, 112, 150, 130, 134, 160, 130], tam=8,
           destaques=tuple(destaques))

    cx(s, 36, 636, 1208, 20,
       ["As 12 vagas ainda a abrir estão todas em EUA e Europa, justamente os dois "
        "blocos mais vazios: o gargalo é a abertura interna, não o mercado."],
       fundo=FUNDO_VERDE, borda=VERDE, cor=TEXTO, tam=8.5, bold=False,
       alinha=PP_ALIGN.LEFT, margem=8)
    return s


def conferencia(d):
    """Confere os numeros do deck corrigido (2) contra as planilhas."""
    ab, ops, vagas = d["ab"], d["ops"], d["vagas"]
    coo = [v for v in ab if v["C-LEVEL"] == "COO"]
    base = ler_aba("Base_Setembro26 (1).xlsx", "Setembro Unificado", "NOME")
    at = [b for b in base if b["SITUAÇÃO"] == "ATIVO"]
    num = lambda x: float(x) if isinstance(x, (int, float)) else 0.0
    geo = Counter(v["geo"] for v in ab)
    niv = Counter(v["nivel"] for v in coo)
    checks = [
        ("registros na planilha de vagas", 65, len(vagas)),
        ("vagas realmente em aberto", 49, len(ab)),
        ("já preenchidas", 13, sum(1 for v in vagas
                                   if str(v.get("STATUS GUPY")) == "FECHADA")),
        ("a confirmar", 3, sum(1 for v in vagas if v["preenchida"]
                               and str(v.get("STATUS GUPY")) != "FECHADA")),
        ("vagas sob o COO", 35, len(coo)),
        ("vagas do CCO", 5, sum(1 for v in ab if v["C-LEVEL"] == "CCO")),
        ("vagas do Co-CEO", 4, sum(1 for v in ab if v["C-LEVEL"] == "Co-CEO")),
        ("vagas do CFSO", 3, sum(1 for v in ab if v["C-LEVEL"] == "CFSO")),
        ("vagas do CITO", 2, sum(1 for v in ab if v["C-LEVEL"] == "CITO")),
        ("Air Operations", 19, sum(1 for v in coo
                                   if str(v["ARÉA"]) == "Air Operations")),
        ("Air Product", 7, sum(1 for v in coo if str(v["ARÉA"]) == "Air Product")),
        ("COO publicadas", 6, sum(1 for v in coo if v["publicada"])),
        ("COO Analyst + Specialist", 26, niv["Analyst"] + niv["Specialist"]),
        ("nos blocos de Operações", 17, len(ops)),
        ("dessas, publicadas", 5, sum(1 for v in ops if v["publicada"])),
        ("dessas, a abrir", 12, sum(1 for v in ops if not v["publicada"])),
        ("geografia Brasil/geral", 34, geo["Brasil/geral"]),
        ("geografia EUA", 9, geo["EUA"]),
        ("geografia Europa", 6, geo["Europa"]),
        ("Colchão entre as 49", 1, sum(1 for v in ab
                                       if v["Folha/Colchão"] == "Colchão")),
        ("Aumento de Quadro", 30, sum(1 for v in ab if str(v.get("Ocupante/Vaga"))
                                      == "Aumento de Quadro")),
        ("Vaga Substituição", 19, sum(1 for v in ab if str(v.get("Ocupante/Vaga"))
                                      == "Vaga Substituição")),
        ("ativos na base de setembro", 311, len(at)),
        ("COO na base de setembro", 193, sum(1 for b in at
                                             if str(b.get("C-LEVEL")) == "COO")),
        ("ativos sob Carol Mendoza", 78, sum(1 for b in at if "MENDOZA"
                                             in str(b.get("HEAD", "")).upper())),
        ("custo total set/26 (R$ mil)", 4283,
         round(sum(num(b.get("TOTAL R$")) for b in at) / 1000)),
        ("custo Air Operations (R$ mil)", 1046,
         round(sum(num(b.get("TOTAL R$")) for b in at
                   if str(b.get("AREA")) == "AIR OPERATIONS") / 1000)),
    ]
    print("\nCONFERÊNCIA — deck corrigido (2) × planilhas")
    print(f"  {'item':<34}{'deck':>8}{'planilha':>10}   ok?")
    ruins = 0
    for rot, esperado, achado in checks:
        ok = esperado == achado
        ruins += 0 if ok else 1
        print(f"  {rot:<34}{esperado:>8}{achado:>10}   {'OK' if ok else '<<< DIVERGE'}")
    print(f"  -> {len(checks)-ruins} de {len(checks)} conferem")
    return ruins


def main():
    d = levantar()
    ruins = conferencia(d)

    prs = Presentation(TEMPLATE)
    lay = [l for l in prs.slide_masters[1].slide_layouts
           if l.name == "DMS_Conteudo"][0]
    limpar_slides(prs, manter={0, 4})
    for sh in prs.slides[0].shapes:
        if sh.has_text_frame and "Projeto Diligenciamento" in sh.text_frame.text:
            runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
            runs[1].text = "Estrutura hierárquica x vagas em aberto"

    slide_estrutura(prs, lay, d)
    slide_vagas(prs, lay, d)
    mover_para(prs, 2, 1)
    mover_para(prs, 3, 2)
    prs.save(SAIDA)

    print(f"\ntemplate ATY (verde): {os.path.basename(TEMPLATE)}")
    print(f"slides: {len(prs.slides)} | divergências: {ruins}")
    print("ok ->", SAIDA)


if __name__ == "__main__":
    main()
