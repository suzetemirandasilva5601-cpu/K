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


def tabela(s, l, t, w, h, cabec, linhas, larguras, tam=8, destaques=()):
    gt = s.shapes.add_table(len(linhas) + 1, len(cabec), px(l), px(t), px(w), px(h))
    tb = gt.table
    tb.first_row = True
    for i, lg in enumerate(larguras):
        tb.columns[i].width = px(lg)
    alt = int(round(h * 9525 / (len(linhas) + 1)))
    for r in tb.rows:
        r.height = Emu(alt)
    for j, c in enumerate(cabec):
        cel = tb.cell(0, j)
        cel.fill.solid()
        cel.fill.fore_color.rgb = AZUL
        cel.margin_left = cel.margin_right = px(4)
        cel.margin_top = cel.margin_bottom = px(0)
        cel.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cel.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if 0 < j < 5 else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = c
        r.font.size = Pt(tam)
        r.font.bold = True
        r.font.name = "Arial"
        r.font.color.rgb = BRANCO
    for i, ln in enumerate(linhas, 1):
        forte = i - 1 in destaques
        total = str(ln[0]).startswith("Total")
        for j, v in enumerate(ln):
            cel = tb.cell(i, j)
            cel.fill.solid()
            cel.fill.fore_color.rgb = (FUNDO_LAR if forte else
                                       (FUNDO if total else
                                        (BRANCO if i % 2 else
                                         RGBColor(0xF7, 0xF7, 0xF7))))
            cel.margin_left = cel.margin_right = px(4)
            cel.margin_top = cel.margin_bottom = px(0)
            cel.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cel.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if 0 < j < 5 else PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(v)
            r.font.size = Pt(tam)
            r.font.bold = total or (j == 0 and forte)
            r.font.name = "Arial"
            r.font.color.rgb = TEXTO
    return tb


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
SETORES = [
    ("Air Operations", "Carolina Bento Mendoza", "Air Operations",
     "4 camadas de team leader: 4 TLs de L7 respondem a TLs de L6 com o título "
     "idêntico, e 14 das 19 vagas nunca foram abertas",
     "Colapsar para 2 camadas e criar Sr. Team Leader para separar a senioridade "
     "real; abrir primeiro as vagas de EUA e Europa"),
    ("Ocean Operations", "Natalia Correia Da Costa Parreira", "Ocean Operations",
     "Times desbalanceados: um TL com 12 diretos e outro com 2; as 3 vagas são "
     "reposição e nenhuma foi aberta",
     "Reequilibrar os dois times e abrir as 3 reposições, que já estão aprovadas "
     "como quadro"),
    ("Air Product", "Filipe Teixeira Sampaio", "Air Product",
     "2 diretos para 29 pessoas e 3 das 7 vagas são de chefia, incluindo 2 TL "
     "Americas que também existem em Air Operations",
     "Consolidar as 3 vagas de TL Americas num único dono antes de publicar, "
     "para não contratar o mesmo cargo duas vezes"),
    ("Ocean Product", "Filipe Carneiro De Oliveira", "Ocean Product",
     "Asia Trade & Market Intelligence é posição única, sem suplente, e as 2 "
     "vagas são reposição",
     "Definir cobertura para a praça Ásia e repor as 2 posições de design"),
    ("Quality & Op. Intel.", "Marco Antonio Maraia Villa",
     "Quality & Operational Intelligence",
     "6 diretos no head, dos quais 4 são especialistas sem camada; 1 analista em "
     "MIA reporta a São Paulo",
     "Agrupar os 3 Logistics Process Specialist sob o TL que já existe e passar o "
     "analista de MIA para a gestão local"),
    ("Overland", "Possidonio Dantas de Almeida Neto", "Overland (Europa)",
     "2 Warehouse TLs para 5 pessoas, um deles sem nenhum liderado, e o head "
     "comanda MIA, IAH e NY de São Paulo",
     "Um TL por praça e liderança local nos EUA; decidir se o Head de Europa "
     "pertence a Overland ou a Operações"),
    ("Operational Excellence", "Jonathas Amancio Alves", None,
     "6 Key Account Executives direto no head, sem nenhuma camada; o DRE de "
     "agosto tinha 10 KAM e 4 saíram sem reposição",
     "Confirmar o quadro-alvo de KAM antes de repor e avaliar uma camada de "
     "coordenação se voltar a 10"),
    ("Cold Chain", "Lucy Maia De Moraes", None,
     "Head com 2 liderados: é uma diretoria inteira para coordenar 2 pessoas",
     "Fundir com Air Product ou com Quality e manter Cold Chain como "
     "especialidade, não como área"),
    ("Special Operations", None, "Special Operations",
     "Tem 1 vaga na planilha e não tem head nem equipe no organograma",
     "Definir o dono da frente antes de abrir a vaga"),
]


def slide_operacoes(prs, d):
    s = prs.slides[2]
    limpar(s)
    idx, filhos, vol = d["idx"], d["filhos"], d["vol"]
    vivo = {p["nome"] for p in d["hoje"]}
    ab = d["ab"]

    def sub(n):
        out, pil = [], [idx[n]]
        while pil:
            x = pil.pop()
            if x["nome"] in vivo:
                out.append(x)
            pil.extend(filhos[x["nome"]])
        return out

    vagas = Counter()
    abrir = Counter()
    for v in ab:
        a = str(v["ARÉA"])
        vagas[a] += 1
        abrir[a] += 0 if v["pub"] else 1

    linhas, destaques = [], []
    tp = tg = tv = ta = 0
    for k, (rot, head, area, falha, rec) in enumerate(SETORES):
        if head:
            eq = sub(head)
            p = len(eq)
            g = sum(1 for x in eq if x["diretos"] > 0)
        else:
            p = g = 0
        v = vagas[area] if area else 0
        a = abrir[area] if area else 0
        tp += p
        tg += g
        tv += v
        ta += a
        if a >= 7 or (v and not p):
            destaques.append(k)
        linhas.append([rot, p or "—", g or "—", v or "—", a or "—", falha, rec])
    linhas.append(["Total Operações", tp, tg, tv, ta,
                   "8 heads, 2 deles com 2 liderados ou menos", ""])

    cabecalho(
        s, "Estrutura × Vagas | Operações (COO)",
        f"Os {len(filhos['Raioni De Oliveira Santos'])} setores do COO somam "
        f"{tp} pessoas e {tv} vagas, mas {ta} nunca foram abertas; a falha se "
        "repete em dois padrões — camada de chefia duplicada e vaga sem dono",
        f"COO: {tp + 1} pessoas · 8 heads diretos · {tv} vagas, {tv - ta} "
        f"publicadas · {br(sum(vol.values()))} embarques originados por mês "
        "(CIS, abr–set/26)",
        "Fonte: ATY | Colaboradores Factorial (organograma out/26, sem as 5 "
        "admissões de novembro) · planilha de vagas (21/10/26) · Gupy · "
        "Baseline DRE 26.2 · CIS ORDERS (13/10/26)")

    rotulo(s, 37, 152, 1207, "Diagnóstico por setor de Operações",
           "quadro atual, vagas em aberto, a falha identificada e o que mudar; "
           "em laranja, os setores que travam a fila")

    tabela(s, 36, 196, 1208, 330,
           ["Setor", "Pessoas", "Gestores", "Vagas", "A abrir",
            "Falha identificada", "Recomendação"],
           linhas, [168, 68, 72, 58, 64, 350, 428], tam=8,
           destaques=tuple(destaques))

    painel(s, 36, 540, 1208, 112, "As três mudanças que destravam mais", [
        ("1. Air Operations, de 4 camadas para 2:", "é o maior setor (83 pessoas, "
         "15 gestores) e o que concentra as vagas; separar Sr. Team Leader de "
         "Team Leader resolve a cadeia de TL sobre TL e libera 2 níveis"),
        ("2. Um dono para as vagas de chefia:", "as 3 de TL Americas estão "
         "divididas entre Air Operations e Air Product, e a de Head de Europa "
         "está dentro de Overland — definir o dono antes de publicar"),
        ("3. Liderança na praça que origina o volume:", f"EUA e Europa originam "
         f"{br(vol['EUA'] + vol['Europa'])} dos {br(sum(vol.values()))} embarques "
         "por mês com 15 pessoas; a Europa não tem head nem TL local e as 12 "
         "vagas paradas estão todas nas duas"),
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
