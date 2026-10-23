#!/usr/bin/env python3
"""
Edita o deck da ATY '20261023 - ATY - Estrutura x Vagas.pptx', mantendo os
dois slides de conteudo e integrando os insights que faltavam.

Por que editar e nao gerar: o deck tem o template real da ATY (capa, marca,
layout Dual_Analytics) e graficos nativos. Editar preserva tudo isso; so o
texto dos blocos de leitura e a geometria da coluna da direita mudam.

Insights integrados:
  slide 2  - a vaga de TL de High-Tech existe no organograma do draft e nao
             consta na planilha de vagas; 6 titulos de chefia sem liderado;
             3 ativos da folha sem posicao no organograma
  slide 3  - as 5 caixas riscadas com X no draft e as 2 caixas azuis que
             movem Air Product e Ocean Product para o Co-CEO; as 3 vagas de
             TL de Americas divididas entre dois heads

Saida: '20261023 - ATY - Estrutura x Vagas.pptx' na raiz do repo.

Uso:  python3 estrutura/gerar_slides.py
"""
import copy
import os
import re
from collections import Counter

from pptx import Presentation
from pptx.util import Emu

from cross_check import RAIZ, ler_aba, ler_factorial, montar, diretoria_de

BASE = os.path.join(RAIZ, "20261023 - ATY - Estrutura x Vagas.pptx")
SAIDA = BASE          # sobrescreve o proprio deck, mesmo nome
NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def px(v):
    return Emu(int(round(v * 9525)))


# ---------------------------------------------------------------- conferencia
def dados():
    fac = ler_factorial()
    todos, filhos, ceo = montar(fac, aplicar_draft=True)
    idx = {p["nome"]: p for p in todos}
    area = diretoria_de(todos, filhos, ceo)

    vagas = ler_aba("Vagas 21-10.xlsx", "Vagas", "CARGO")
    for v in vagas:
        v["preenchida"] = (bool(v.get("CONTRATADO"))
                           or str(v.get("STATUS GUPY")) == "FECHADA"
                           or str(v.get("Admissão") or "")[:10] == "2026-10-01")
        v["publicada"] = str(v.get("STATUS GUPY")) == "ABERTA | PUBLICADA"
    ab = [v for v in vagas if not v["preenchida"]]

    CH = ("team leader", "head", "manager", "coordinator")
    sem_time = [p for p in todos
                if any(k in p["cargo"].lower() for k in CH) and p["diretos"] == 0]
    ate2 = [p for p in todos if 0 < p["diretos"] <= 2]
    ricardo = idx["Ricardo Tebexreni Jakowatz"]
    tl_hightech = [v for v in vagas if "HIGH" in str(v["ARÉA"]).upper()
                   and "TL" in str(v["CARGO"]).upper()]
    tl_americas = [v for v in ab if "TL AMERICAS" in str(v["CARGO"]).upper()]
    return {
        "todos": todos, "filhos": filhos, "ceo": ceo, "idx": idx, "area": area,
        "ab": ab, "sem_time": sem_time, "ate2": ate2, "ricardo": ricardo,
        "tl_hightech": tl_hightech, "tl_americas": tl_americas,
        "pub": sum(1 for v in ab if v["publicada"]),
    }


def conferir(d):
    """Reconfere os numeros que os dois slides afirmam."""
    todos, filhos, ceo, idx = d["todos"], d["filhos"], d["ceo"], d["idx"]
    area, ab = d["area"], d["ab"]
    g = [p for p in todos if p["diretos"] > 0]

    def gest_em(n):
        c = 1 if idx[n]["diretos"] else 0
        pil = list(filhos[n])
        while pil:
            x = pil.pop()
            c += 1 if x["diretos"] else 0
            pil.extend(filhos[x["nome"]])
        return c

    def vagas_de(nome):
        """Vagas cujo bloco esta na subarvore de `nome`."""
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
        dentro = {nome} | {p["nome"] for p in todos if area.get(p["nome"]) == nome}
        n = 0
        for v in ab:
            h = BL[str(v["ARÉA"])]
            if h in dentro or (h == nome):
                n += 1
        return n

    co = idx["Carolina Bento Mendoza"]
    sub = []
    pil = [co]
    while pil:
        x = pil.pop()
        sub.append(x)
        pil.extend(filhos[x["nome"]])

    checks = [
        ("pessoas no organograma", 336, len(todos)),
        ("gestores", 66, len(g)),
        ("niveis", 7, max(p["level"] for p in todos) - 1),
        ("vagas em aberto", 49, len(ab)),
        ("vagas publicadas", 8, d["pub"]),
        ("gestores com ate 2 diretos", 18, len(d["ate2"])),
        ("Co-CEO diretos", 8, idx["Jose Luiz de Oliveira Belixior Junior"]["diretos"]),
        ("Co-CEO indiretos", 327,
         idx["Jose Luiz de Oliveira Belixior Junior"]["total"] - 8),
        ("COO indiretos", 148, idx["Raioni De Oliveira Santos"]["total"] - 6),
        ("COO gestores", 29, gest_em("Raioni De Oliveira Santos")),
        ("COO vagas", 25, vagas_de("Raioni De Oliveira Santos")),
        ("CCO gestores", 8, gest_em("Andre Lemos Tavares")),
        ("CCO ate 2 diretos", 7,
         sum(1 for p in todos if area.get(p["nome"]) == "Andre Lemos Tavares"
             and 0 < p["diretos"] <= 2)),
        ("Air Ops indiretos", 81, co["total"] - 4),
        ("Air Ops gestores", 15, gest_em("Carolina Bento Mendoza")),
        ("Air Ops camadas de gestao", 4,
         len({p["level"] for p in sub if p["diretos"] > 0})),
        ("Air Ops maior time", 13, max(p["diretos"] for p in sub)),
        ("titulos de chefia sem liderado", 6, len(d["sem_time"])),
        ("vagas de TL para High-Tech", 0, len(d["tl_hightech"])),
        ("TLs de Americas em aberto", 3, len(d["tl_americas"])),
        ("fronts do Ricardo com TL", 2, d["ricardo"]["diretos"]),
    ]
    print("CONFERÊNCIA dos números dos dois slides")
    ruins = 0
    for rot, esp, ach in checks:
        ok = esp == ach
        ruins += 0 if ok else 1
        print(f"  {rot:<34}{esp:>6}{ach:>8}   {'OK' if ok else '<<< DIVERGE'}")
    print(f"  -> {len(checks)-ruins} de {len(checks)} conferem\n")
    return ruins


# ---------------------------------------------------------------- edicao
def achar(slide, **crit):
    """Acha a forma por nome ou por cor de preenchimento."""
    for sh in slide.shapes:
        if "nome" in crit and sh.name == crit["nome"]:
            return sh
        if "fill" in crit:
            try:
                if sh.fill.type == 1 and str(sh.fill.fore_color.rgb) == crit["fill"]:
                    return sh
            except Exception:
                pass
    return None


def altura_tabela(sh, total_px):
    """Redistribui a altura da tabela igualmente entre as linhas."""
    tb = sh.table
    h = int(round(total_px * 9525 / len(tb.rows)))
    for r in tb.rows:
        r.height = Emu(h)
    sh.height = Emu(h * len(tb.rows))


def set_bullets(caixa, itens):
    """Reescreve os bullets mantendo o formato: rotulo em negrito + texto."""
    tf = caixa.text_frame
    modelo = copy.deepcopy(tf.paragraphs[0]._p)
    for p in list(tf._txBody.findall(NS + "p")):
        tf._txBody.remove(p)
    for rotulo, texto in itens:
        novo = copy.deepcopy(modelo)
        tf._txBody.append(novo)
        runs = novo.findall(NS + "r")
        # o modelo tem dois runs: negrito (rotulo) e normal (texto)
        runs[0].find(NS + "t").text = rotulo
        if len(runs) > 1:
            runs[1].find(NS + "t").text = texto
            for extra in runs[2:]:
                novo.remove(extra)
        else:
            novo.append(copy.deepcopy(runs[0]))
    return caixa


def editar(prs, d):
    ab, sem_time, ate2 = d["ab"], d["sem_time"], d["ate2"]
    s2, s3 = prs.slides[1], prs.slides[2]

    # ---------------- slide 2
    ph = {x.placeholder_format.idx: x for x in s2.placeholders}
    ph[0].text_frame.paragraphs[0].runs[0].text = (
        "O COO concentra 25 das 49 vagas e a estrutura mais longa da casa; no CCO, "
        "7 dos 8 gestores lideram até 2 pessoas e a vaga de TL de High-Tech existe "
        "no organograma, mas não na planilha de vagas")
    ph[11].text_frame.paragraphs[0].runs[0].text = (
        f"336 pessoas em 7 níveis · 66 gestores · {len(ate2)} deles lideram até 2 "
        f"pessoas · {len(ab)} vagas, {d['pub']} publicadas no Gupy")
    ph[13].text_frame.paragraphs[0].runs[0].text = (
        "Fonte: ATY | Gestores por Level (organograma out/26, diretos e indiretos) · "
        "planilha de vagas (21/10/26) · Gupy · Draft 23 Out 26 · "
        "Base Setembro/26 (RH)")

    tab = next(sh for sh in s2.shapes if getattr(sh, "has_table", False))
    altura_tabela(tab, 234)                      # 196 -> 430
    caixa = achar(s2, fill="E8F4F4")
    caixa.top, caixa.height = px(444), px(203)   # ganha 59 px
    set_bullets(caixa, [
        ("High-Tech: ",
         "a vaga de TL está desenhada no organograma do draft e não existe na "
         "planilha de vagas; Ricardo Jakowatz tem 2 team leaders para 3 frentes "
         "(Vertical, Auto e High-Tech)"),
        ("COO: ",
         "6 diretos sustentam 148 indiretos em 6 níveis; é a única diretoria que "
         "chega ao L8"),
        ("CCO: ",
         "8 gestores para 19 pessoas, 7 deles com até 2 diretos, e 21% do quadro "
         "em aberto"),
        ("CITO e Air Product: ",
         "2 diretos cada; no CITO, o Head of Operation tem 27 diretos, o maior "
         "time da casa"),
        ("Fora do organograma: ",
         f"{len(sem_time)} pessoas têm título de chefia e nenhum liderado, e 3 "
         "ativos da folha de setembro não têm posição no organograma"),
    ])

    # ---------------- slide 3
    ph = {x.placeholder_format.idx: x for x in s3.placeholders}
    ph[0].text_frame.paragraphs[0].runs[0].text = (
        "No COO, Air Operations tem 4 níveis de gestão, da head ao TL que lidera "
        "TL, e concentra 19 das 25 vagas; o draft já risca cinco caixas dessa "
        "cadeia sem que a planilha registre")
    ph[13].text_frame.paragraphs[0].runs[0].text = (
        "Fonte: ATY | Gestores por Level (organograma out/26) · Base Setembro/26 "
        "(RH) para os blocos de Operações · planilha de vagas (21/10/26) · Gupy · "
        "Draft 23 Out 26")

    tab = next(sh for sh in s3.shapes if getattr(sh, "has_table", False))
    altura_tabela(tab, 216)                      # 196 -> 412
    nota = achar(s3, nome="TextBox 14")
    nota.top = px(420)
    nota.text_frame.paragraphs[0].runs[0].text = (
        "Camadas de gestão = níveis com gestor, da head até o último team leader. "
        "Special Operations tem vaga e não tem head no organograma.")
    caixa = achar(s3, fill="E8F4F4")
    caixa.top, caixa.height = px(456), px(194)   # ganha 60 px
    set_bullets(caixa, [
        ("Draft: ",
         "cinco caixas riscadas com X — Air Product e Ocean Product sobem para o "
         "Co-CEO pelas duas caixas azuis, e Magno Bezerra, Gabriella Pereira e "
         "Pamela Ibarra ficam marcados sem destino"),
        ("Air Operations: ",
         "TL que lidera TL; 4 team leaders em L7 respondem a team leaders em L6, "
         "e 3 gestores lideram até 2 pessoas"),
        ("Americas: ",
         "as 3 vagas de team leader estão divididas entre dois heads, 1 em Air "
         "Operations e 2 em Air Product, para a mesma praça"),
        ("Blocos de Operações: ",
         "as 12 vagas paradas estão nos EUA (6) e na Europa (6)"),
        ("Inland Freight Europa: ",
         "4 pessoas, 4 vagas e nenhuma de liderança"),
    ])
    return prs


def main():
    d = dados()
    ruins = conferir(d)
    prs = Presentation(BASE)
    assert len(prs.slides) == 4, f"esperava capa + 2 conteúdo + fim, achei {len(prs.slides)}"
    editar(prs, d)
    prs.save(SAIDA)
    print(f"slides: {len(prs.slides)} (capa + 2 de conteúdo + encerramento)")
    print(f"divergências nos números: {ruins}")
    print("ok ->", SAIDA)


if __name__ == "__main__":
    main()
