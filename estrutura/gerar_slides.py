#!/usr/bin/env python3
"""
Refaz os dois slides de conteudo do deck da ATY com foco em ineficiencia:
  slide 2  visao geral — organograma por cargo (sem nomes) e onde falta gente
  slide 3  Operacoes — a cadeia por praca, cruzando vagas e volume do CIS

Base: '20261023 - ATY - Estrutura x Vagas.pptx' (template e paleta da ATY,
layout Dual_Analytics). Capa e encerramento preservados.

Fontes de numero:
  Colaboradores-factorial (3).xlsx  organograma; exclui as 5 admissoes com
                                    data futura, chegando aos 330 liderados
                                    que o draft imprime
  Vagas 21-10.xlsx                  vagas em aberto e status no Gupy
  CIS_20261013_ORDERS.parquet       embarques por praca de origem (campo off),
                                    media mensal de abr-set/26
  Draft 23 Out 26.pptx              vaga de TL de High-Tech e caixas riscadas

Uso:  python3 estrutura/gerar_slides.py
"""
import os
from collections import Counter

import pandas as pd
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

from cross_check import RAIZ, ler_aba, ler_factorial, montar

DECK = os.path.join(RAIZ, "20261023 - ATY - Estrutura x Vagas.pptx")
CIS = os.path.join(RAIZ, "CIS_20261013_ORDERS.parquet")
HOJE = "2026-10-23"
TESTE = "Colaborador Teste"

# paleta da ATY (theme1 do proprio deck)
AZUL = RGBColor(0x1D, 0x36, 0x8E)
VERDE = RGBColor(0x00, 0x97, 0x96)
LARANJA = RGBColor(0xFF, 0x8E, 0x2E)
CLARO = RGBColor(0x43, 0xCF, 0xF6)
FUNDO = RGBColor(0xE8, 0xF4, 0xF4)
FUNDO_LAR = RGBColor(0xFD, 0xF0, 0xE4)
CINZA = RGBColor(0xBF, 0xBF, 0xBF)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
TEXTO = RGBColor(0x26, 0x26, 0x26)
CINZA_TXT = RGBColor(0x7F, 0x7F, 0x7F)


def px(v):
    return Emu(int(round(v * 9525)))


def br(n):
    """Milhar com ponto, como em pt-BR."""
    return f"{int(n):,}".replace(",", ".")


def praca(local):
    l = str(local)
    if "América" in l:
        return "EUA"
    if "Portugal" in l or "Alemanha" in l:
        return "Europa"
    return "Brasil"


def praca_vaga(v):
    u, a = str(v["CARGO"]).upper(), str(v["ARÉA"]).upper()
    if "INLAND USA" in u or "AMERICAS" in u:
        return "EUA"
    if "EUROPA" in u or "EUROPA" in a:
        return "Europa"
    return "Brasil"


def levantar():
    fac = ler_factorial()
    todos, filhos, ceo = montar(fac, aplicar_draft=False)
    idx = {p["nome"]: p for p in todos}
    # quadro de hoje: fora as admissoes com data futura
    futuros = {p["nome"] for p in todos if (p["inicio"] or "") > HOJE}
    hoje = [p for p in todos if p["nome"] not in futuros]

    vagas = ler_aba("Vagas 21-10.xlsx", "Vagas", "CARGO")
    for v in vagas:
        v["preenchida"] = (bool(v.get("CONTRATADO"))
                           or str(v.get("STATUS GUPY")) == "FECHADA"
                           or str(v.get("Admissão") or "")[:10] == "2026-10-01")
        v["pub"] = str(v.get("STATUS GUPY")) == "ABERTA | PUBLICADA"
        v["praca"] = praca_vaga(v)
    ab = [v for v in vagas if not v["preenchida"]]

    # volume do CIS por praca de origem
    df = pd.read_parquet(CIS)
    d = pd.to_datetime(df["data_competencia"], errors="coerce", utc=True)
    df["mes"] = d.dt.tz_localize(None).dt.to_period("M")
    jan = df[(df["mes"] >= pd.Period("2026-04"))
             & (df["mes"] <= pd.Period("2026-09"))].copy()

    def grupo(o):
        u = str(o).upper()
        if "MIAMI" in u or "HOUSTON" in u:
            return "EUA"
        if "FRANKFURT" in u or "LISBOA" in u:
            return "Europa"
        if "DMS BRASIL" in u:
            return "Brasil"
        return "Agentes"

    jan["g"] = jan["off"].map(grupo)
    vol = {k: round(v / 6) for k, v in jan["g"].value_counts().items()}
    agentes = jan[jan["g"] == "Agentes"]["off"].nunique()

    # diretorias (convencao do deck: Air/Ocean Product seguem no COO)
    SIG = {"Raioni De Oliveira Santos": "COO",
           "Cleyton Cardoso Esteves": "CITO",
           "Ana Carolina Botelho Caldeira Vasconcellos": "CFSO",
           "Andre Lemos Tavares": "CCO",
           "Carolina Karnakis de Nobrega": "Head of Talent",
           "Luis Fernando Santos Muniz": "Head of Services"}
    BL = {"Air Operations": "Carolina Bento Mendoza",
          "Air Product": "Filipe Teixeira Sampaio",
          "Ocean Operations": "Natalia Correia Da Costa Parreira",
          "Ocean Product": "Filipe Carneiro De Oliveira",
          "Quality & Operational Intelligence": "Marco Antonio Maraia Villa",
          "Overland (Europa)": "Possidonio Dantas de Almeida Neto",
          "Services": "Luis Fernando Santos Muniz",
          "Special Operations": "Raioni De Oliveira Santos",
          "Healthcare": "Jose Carlos Duarte Freitas Sobrinho",
          "High-Tech": "Ricardo Tebexreni Jakowatz",
          "Automotive": "Ricardo Tebexreni Jakowatz",
          "Financial": "Ana Carolina Botelho Caldeira Vasconcellos",
          "Technology": "Cleyton Cardoso Esteves",
          "Talent Management Team": "Carolina Karnakis de Nobrega"}

    def l3_de(n):
        p = idx.get(n)
        while p and p["level"] > 3:
            p = idx.get(p["gestor"])
        return p["nome"] if p else "Raioni De Oliveira Santos"

    vagas_l3 = Counter(l3_de(BL[str(v["ARÉA"])]) for v in ab)
    vivo = {p["nome"] for p in hoje}

    def tam(n):
        c = 0
        pil = list(filhos[n])
        while pil:
            x = pil.pop()
            c += 1 if x["nome"] in vivo else 0
            pil.extend(filhos[x["nome"]])
        return c + (1 if n in vivo else 0)

    diretorias = []
    for nome, sig in SIG.items():
        diretorias.append({"sigla": sig, "nome": nome, "pessoas": tam(nome),
                           "diretos": idx[nome]["diretos"],
                           "vagas": vagas_l3[nome]})
    diretorias.sort(key=lambda x: -x["pessoas"])

    # pracas
    pess = Counter(praca(p["local"]) for p in hoje)
    gest = Counter(praca(p["local"]) for p in hoje if p["diretos"] > 0)
    vp = Counter(v["praca"] for v in ab)
    va = Counter(v["praca"] for v in ab if not v["pub"])

    return {"todos": todos, "hoje": hoje, "filhos": filhos, "ceo": ceo,
            "idx": idx, "ab": ab, "vol": vol, "agentes": agentes,
            "diretorias": diretorias, "pess": pess, "gest": gest,
            "vp": vp, "va": va, "futuros": futuros, "tam": tam}


# ------------------------------------------------------------------ desenho
def cx(s, l, t, w, h, linhas, fundo=None, borda=None, cor=BRANCO, tam=10,
       tam2=None, alinha=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margem=6,
       tracejado=False):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px(l), px(t), px(w), px(h))
    if fundo is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fundo
    if borda is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = borda
        sh.line.width = Pt(1.5 if tracejado else 1)
        if tracejado:
            sh.line.dash_style = 4            # MSO_LINE_DASH_STYLE.DASH
    try:
        sh.adjustments[0] = 0.08
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
        r.font.size = Pt(tam if i == 0 else (tam2 or tam - 1.5))
        r.font.bold = (i == 0)
        r.font.name = "Arial"
        r.font.color.rgb = cor
    return sh


def txt(s, l, t, w, h, linhas, tam=9.5, cor=TEXTO, bold=False,
        alinha=PP_ALIGN.LEFT, espaco=0):
    box = s.shapes.add_textbox(px(l), px(t), px(w), px(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = px(0)
    tf.margin_top = tf.margin_bottom = px(0)
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


def rotulo(s, l, t, w, titulo, sub):
    txt(s, l, t, w, 38, [titulo], tam=10.5, cor=TEXTO, bold=True)
    txt(s, l, t + 15, w, 20, [sub], tam=10, cor=TEXTO)


def linha(s, x1, y1, x2, y2, cor=CINZA):
    ln = s.shapes.add_connector(2, px(x1), px(y1), px(x2), px(y2))
    ln.line.color.rgb = cor
    ln.line.width = Pt(1)
    return ln


def painel(s, l, t, w, h, titulo, itens, cor=VERDE, fundo=FUNDO):
    cx(s, l, t, w, 24, titulo, fundo=cor, tam=10)
    caixa = cx(s, l, t + 27, w, h - 27, [""], fundo=fundo, borda=cor,
               cor=TEXTO, alinha=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, margem=10)
    tf = caixa.text_frame
    tf.paragraphs[0].runs[0].text = ""
    for i, (rot, texto) in enumerate(itens):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = px(5)
        for pedaco in list(p.runs):
            pedaco.text = ""
        r1 = p.add_run()
        r1.text = f"{rot} "
        r1.font.bold = True
        r2 = p.add_run()
        r2.text = texto
        for r in (r1, r2):
            r.font.size = Pt(9)
            r.font.name = "Arial"
            r.font.color.rgb = TEXTO
    return caixa


def limpar(slide):
    """Remove tudo que nao e placeholder (graficos, tabelas, caixas, linhas)."""
    for sh in list(slide.shapes):
        if sh.shape_type != 14:
            sh._element.getparent().remove(sh._element)


def cabecalho(slide, kicker, takeaway, metricas, fonte):
    ph = {x.placeholder_format.idx: x for x in slide.placeholders}
    for idx_, texto in ((10, kicker), (0, takeaway), (11, metricas), (13, fonte)):
        tf = ph[idx_].text_frame
        if tf.paragraphs[0].runs:
            tf.paragraphs[0].runs[0].text = texto
            for extra in tf.paragraphs[0].runs[1:]:
                extra.text = ""
        else:
            tf.text = texto


# ------------------------------------------------------------------ slide 2
def slide_geral(prs, d):
    s = prs.slides[1]
    limpar(s)
    dirs, ab = d["diretorias"], d["ab"]
    pessoas = len(d["hoje"])
    abrir = sum(1 for v in ab if not v["pub"])

    cabecalho(
        s, "Estrutura × Vagas | Visão geral",
        f"O Co-CEO tem {br(pessoas - 1)} liderados em 6 diretorias e {len(ab)} vagas "
        f"em aberto, mas {abrir} delas nunca foram abertas — e duas posições de "
        "chefia existem só no organograma, sem vaga na planilha",
        f"{pessoas} pessoas · 66 gestores · {len(ab)} vagas, "
        f"{len(ab)-abrir} publicadas no Gupy · 2 posições de chefia sem vaga",
        "Fonte: ATY | Colaboradores Factorial (organograma out/26, sem as 5 "
        "admissões de novembro) · planilha de vagas (21/10/26) · Gupy · "
        "Draft 23 Out 26")

    # organograma por cargo
    rotulo(s, 37, 152, 1207, "Organograma por cargo",
           "cada caixa é um cargo, com o quadro atual e as vagas em aberto; "
           "em laranja, o que falta")
    cx(s, 510, 196, 260, 40,
       ["Co-CEO", f"{br(pessoas-1)} liderados · {len(ab)} vagas"],
       fundo=AZUL, tam=11, tam2=8.5)
    larg, passo, x0 = 180, 201, 37
    linha(s, 640, 236, 640, 248)
    linha(s, x0 + larg / 2, 248, x0 + 5 * passo + larg / 2, 248)
    for i, f in enumerate(dirs):
        x = x0 + i * passo
        linha(s, x + larg / 2, 248, x + larg / 2, 260)
        vg = f"{f['vagas']} vaga" + ("s" if f["vagas"] != 1 else "")
        cx(s, x, 260, larg, 52,
           [f["sigla"], f"{f['pessoas']} pessoas · {vg}"],
           fundo=VERDE if f["vagas"] else CINZA, tam=9.5, tam2=8)

    # as duas lacunas de chefia
    ix_coo = [i for i, f in enumerate(dirs) if f["sigla"] == "COO"][0]
    ix_cco = [i for i, f in enumerate(dirs) if f["sigla"] == "CCO"][0]
    for ix, rot, sub in ((ix_coo, "VAGA · Head de Europa",
                          "publicada no Gupy · AMS, FRA, LIS"),
                         (ix_cco, "VAGA · TL de High-Tech",
                          "está no draft, não está na planilha")):
        x = x0 + ix * passo
        linha(s, x + larg / 2, 312, x + larg / 2, 324, cor=LARANJA)
        cx(s, x, 324, larg, 46, [rot, sub], fundo=FUNDO_LAR, borda=LARANJA,
           cor=TEXTO, tam=8.5, tam2=7.5, tracejado=True)

    painel(s, 36, 396, 596, 256, "Onde falta gente", [
        ("Europa:", "5 pessoas e 7 vagas — mais vaga que gente. Nenhum head: "
                    "a vaga de Head de Europa está publicada e as outras 6 "
                    "ainda não foram abertas"),
        ("EUA:", "10 pessoas e 9 vagas, 6 delas ainda a abrir. O Head of "
                 "Overland comanda de São Paulo"),
        ("High-Tech:", "o draft desenha uma vaga de TL que não existe na "
                       "planilha; são 2 team leaders para 3 frentes "
                       "(Vertical, Auto e High-Tech)"),
        ("Brasil:", f"321 das {pessoas} pessoas e 33 vagas, 29 sem processo"),
    ], cor=LARANJA, fundo=FUNDO_LAR)

    painel(s, 648, 396, 596, 256, "Onde dá para preencher lacuna sem contratar", [
        ("6 cargos de chefia sem equipe:", "Head Of Revenue Management, "
         "BD Manager, BI & Data Science TL, Airport Operations Manager, "
         "Warehouse TL e Air Freight CC TL — nenhum deles lidera ninguém hoje"),
        ("18 gestores lideram até 2 pessoas:", "7 deles no CCO, que tem 8 "
         "gestores para 19 pessoas"),
        ("4 camadas de team leader em Air Operations:", "team leaders "
         "respondendo a team leaders com o mesmo título"),
        ("Especialistas já na praça:", "a Europa tem 1 team leader sediada em "
         "Portugal liderando 13 pessoas, das quais 11 estão no Brasil"),
    ], cor=VERDE, fundo=FUNDO)
    return s


# ------------------------------------------------------------------ slide 3
def slide_operacoes(prs, d):
    s = prs.slides[2]
    limpar(s)
    vol, pess, gest, vp, va = d["vol"], d["pess"], d["gest"], d["vp"], d["va"]
    idx, filhos, tam = d["idx"], d["filhos"], d["tam"]
    total_vol = sum(vol.values())
    fora = vol["EUA"] + vol["Europa"]

    cabecalho(
        s, "Estrutura × Vagas | Operações por praça",
        f"EUA e Europa originam {br(fora)} dos {br(total_vol)} embarques por mês com "
        f"15 pessoas e 16 vagas em aberto; 12 dessas vagas nunca foram abertas "
        "e a Europa não tem head",
        f"Embarques originados por mês (média abr–set/26, CIS) · "
        f"{d['agentes']} agentes terceiros originam {br(vol['Agentes'])} · "
        "praça = entidade no organograma e escritório de origem no CIS",
        "Fonte: ATY | CIS ORDERS (13/10/26, campo off, média mensal abr–set/26) · "
        "Colaboradores Factorial (organograma out/26) · planilha de vagas "
        "(21/10/26) · Gupy")

    # cadeia do COO por praca
    rotulo(s, 37, 152, 1207, "A cadeia de Operações, por praça",
           "cargo, quadro atual, vagas em aberto e embarques originados por mês")
    cx(s, 540, 194, 200, 36, ["COO", f"{tam('Raioni De Oliveira Santos')} pessoas"],
       fundo=AZUL, tam=11, tam2=8.5)
    linha(s, 640, 230, 640, 242)
    linha(s, 186, 242, 1094, 242)

    blocos = [
        ("Head of Air Operations", "Customer Care e Exportação · Brasil",
         pess["Brasil"], vp["Brasil"], va["Brasil"], vol["Brasil"], VERDE),
        ("Air Freight Lead Coordinator", f"Agentes OFF · {d['agentes']} terceiros",
         51, 0, 0, vol["Agentes"], VERDE),
        ("Head of Overland", "EUA · MIA, IAH, NY",
         pess["EUA"], vp["EUA"], va["EUA"], vol["EUA"], LARANJA),
        ("VAGA · Head de Europa", "Europa · AMS, FRA, LIS",
         pess["Europa"], vp["Europa"], va["Europa"], vol["Europa"], LARANJA),
    ]
    larg, passo = 272, 290
    for i, (cargo, onde, p, v, a, vl, cor) in enumerate(blocos):
        x = 36 + i * passo
        linha(s, x + larg / 2, 242, x + larg / 2, 254, cor=cor)
        vaga = "vaga publicada" if cargo.startswith("VAGA") else (
            f"{v} vagas · {a} a abrir" if v else "sem vaga")
        cx(s, x, 254, larg, 62, [cargo, onde, f"{p} pessoas · {vaga}"],
           fundo=cor, tam=9.5, tam2=7.5,
           borda=LARANJA if cargo.startswith("VAGA") else None,
           tracejado=cargo.startswith("VAGA"))
        cx(s, x, 320, larg, 26, f"{br(vl)} embarques/mês", fundo=FUNDO,
           borda=cor, cor=TEXTO, tam=9)

    painel(s, 36, 372, 596, 280, "A conta por praça", [
        ("EUA · 10 pessoas, 9 vagas:", f"{br(vol['EUA'])} embarques/mês originados, "
         f"{round(vol['EUA']/pess['EUA'])} por pessoa. 1 gestor local, e são "
         "2 Warehouse Team Leaders — um deles sem nenhum liderado"),
        ("Europa · 5 pessoas, 7 vagas:", f"{br(vol['Europa'])} embarques/mês, "
         f"{round(vol['Europa']/pess['Europa'])} por pessoa. Sem head; "
         "a única TL está em Portugal e reporta ao Brasil"),
        ("Agentes OFF ·", f"{d['agentes']} agentes terceiros originam "
         f"{br(vol['Agentes'])} embarques/mês, "
         f"{round(vol['Agentes']/total_vol*100)}% do total, coordenados por 51 "
         "pessoas no Brasil"),
        ("Brasil ·", f"{br(vol['Brasil'])} embarques/mês originados, mas a equipe "
         "processa o lado destino de todos os embarques"),
    ], cor=AZUL, fundo=FUNDO)

    painel(s, 648, 372, 596, 280, "As ineficiências da cadeia", [
        ("Europa sem dono:", "58% do quadro europeu está em aberto e a praça "
         f"que origina {br(vol['Europa'])} embarques/mês não tem head nem team "
         "leader local"),
        ("Fila travada fora do Brasil:", "as 12 vagas que nunca foram abertas "
         "estão todas em EUA (6) e Europa (6) — o gargalo é a abertura interna"),
        ("Gestão à distância:", "13 das 15 pessoas de EUA e Europa têm gestor "
         "no Brasil; o Head of Overland responde por MIA, IAH e NY de São Paulo"),
        ("Camada que se repete:", "Air Operations tem 4 níveis de team leader; "
         "o draft risca 3 caixas dessa cadeia sem indicar destino"),
    ], cor=LARANJA, fundo=FUNDO_LAR)
    return s


def main():
    d = levantar()
    prs = Presentation(DECK)
    assert len(prs.slides) == 4
    slide_geral(prs, d)
    slide_operacoes(prs, d)
    prs.save(DECK)

    print(f"organograma: {len(d['todos'])} linhas, {len(d['hoje'])} hoje "
          f"({len(d['futuros'])} admissões futuras fora)")
    print(f"pessoas por praça: {dict(d['pess'])}")
    print(f"vagas por praça:   {dict(d['vp'])} | a abrir {dict(d['va'])}")
    print(f"embarques/mês CIS: {d['vol']} | {d['agentes']} agentes terceiros")
    print(f"slides: {len(prs.slides)} (capa + 2 de conteúdo + encerramento)")
    print("ok ->", DECK)


if __name__ == "__main__":
    main()
