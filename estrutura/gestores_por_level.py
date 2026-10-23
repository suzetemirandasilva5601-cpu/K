#!/usr/bin/env python3
"""
Consolida numa planilha unica e enxuta a estrutura de gestores da DMS,
integrando o que havia nas duas versoes anteriores ('Gestores_por_Level (1)'
e a versao com cross-check) e cruzando com a planilha de vagas.

Saidas:
  estrutura/Gestores_por_Level.xlsx   5 abas: Resumo, Gestores, Estrutura,
                                      Vagas por bloco, Divergencias
  estrutura/Gestores_por_Level.md     leitura em texto, por level

Simplificacoes em relacao as versoes anteriores:
  - uma aba 'Gestores' com filtro de level substitui as 6 abas 'Lx gestores'
  - 'Estrutura' com 8 colunas em vez de 15
  - 'Divergencias' traz so o que divergiu; quem casou nas duas bases sai
  - cargos do L2/L3 ja preenchidos com o que foi lido no draft

Uso:  python3 estrutura/gestores_por_level.py
"""
import os
import re
from collections import Counter, defaultdict

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from cross_check import (CARGOS_DRAFT, C_LEVEL_DRE, MOVIDOS_PARA_CEO, RAIZ,
                         RISCADOS, SEM_CARGO, diretoria_de, divergencias,
                         ler_aba, ler_factorial, montar)

SAIDA = os.path.join(RAIZ, "estrutura")
CHEFIA = ("team leader", "head", "manager", "coordinator")
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
# area da planilha de vagas -> head do bloco no organograma
BLOCO = {
    "Air Operations": "Carolina Bento Mendoza",
    "Air Product": "Filipe Teixeira Sampaio",
    "Ocean Operations": "Natalia Correia Da Costa Parreira",
    "Ocean Product": "Filipe Carneiro De Oliveira",
    "Quality & Operational Intelligence": "Marco Antonio Maraia Villa",
    "Overland (Europa)": "Possidonio Dantas de Almeida Neto",
    "Services": "Luis Fernando Santos Muniz",
    "Special Operations": None,
    "Healthcare": "Jose Carlos Duarte Freitas Sobrinho",
    "High-Tech": "Ricardo Tebexreni Jakowatz",
    "Automotive": "Ricardo Tebexreni Jakowatz",
    "Financial": "Ana Carolina Botelho Caldeira Vasconcellos",
    "Technology": "Cleyton Cardoso Esteves",
    "Talent Management Team": "Carolina Karnakis de Nobrega",
}
NIVEIS = [("HEAD", "Head"), ("TL", "Team Leader"), ("SPEC", "Specialist"),
          ("ANALYST", "Analyst"), ("ASSIST", "Assistant"), ("INTERN", "Intern"),
          ("APPRENTICE", "Aprendiz")]

AZUL = "1B3A5C"
VERDE = "009796"
LARANJA = "FF8E2E"
COR_LEVEL = {2: "0D1F31", 3: "1B3A5C", 4: "2E6CA4", 5: "67A3D9",
             6: "AED2F0", 7: "DFEAF5", 8: "F4F8FC"}


def nivel_vaga(c):
    for k, r in NIVEIS:
        if re.search(rf"\b{k}\b", c.upper()):
            return r
    return "Outro"


def cargo_de(p):
    if p["nome"] in CARGOS_DRAFT:
        cargo, slide = CARGOS_DRAFT[p["nome"]]
        return cargo, f"draft {slide}"
    return (p["cargo"], "planilha") if p["cargo"] else (SEM_CARGO, "—")


def levantar():
    fac = ler_factorial()
    todos, filhos, ceo = montar(fac, aplicar_draft=True)
    idx = {p["nome"]: p for p in todos}
    area = diretoria_de(todos, filhos, ceo)

    vagas = ler_aba("Vagas 21-10.xlsx", "Vagas", "CARGO")
    for v in vagas:
        v["preenchida"] = (bool(v.get("CONTRATADO"))
                           or str(v.get("STATUS GUPY")) == "FECHADA"
                           or str(v.get("Admissão") or "")[:10] == "2026-10-01")
        v["nivel"] = nivel_vaga(str(v["CARGO"]))
        v["publicada"] = str(v.get("STATUS GUPY")) == "ABERTA | PUBLICADA"
        v["head"] = BLOCO[str(v["ARÉA"])]
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

    por_l3 = defaultdict(lambda: {"vagas": 0, "chefia": 0})
    for v in ab:
        l3 = l3_de(v["head"]) if v["head"] else "Raioni De Oliveira Santos"
        por_l3[l3]["vagas"] += 1
        por_l3[l3]["chefia"] += 1 if v["nivel"] in ("Head", "Team Leader") else 0

    diretorias = []
    for l3 in sorted(filhos[ceo], key=lambda p: -p["total"]):
        # diretoria_de ja inclui o proprio L3; nao somar de novo
        sub = [p for p in todos if area.get(p["nome"]) == l3["nome"]]
        diretorias.append({
            "nome": l3["nome"], "sigla": SIGLA.get(l3["nome"], "L3"),
            "ativos": len(sub), "gestores": gestores_em(l3["nome"]),
            "niveis": max(p["level"] for p in sub) - l3["level"] + 1,
            "vagas": por_l3[l3["nome"]]["vagas"],
            "chefia": por_l3[l3["nome"]]["chefia"],
        })

    base = ler_aba("Base_Setembro26 (1).xlsx", "Setembro Unificado", "NOME")
    dre = ler_aba("Baseline DRE 26.2.xlsx", "Baseline ativos agosto", "Colaborador")
    return {"todos": todos, "filhos": filhos, "ceo": ceo, "idx": idx,
            "area": area, "vagas": vagas, "ab": ab, "diretorias": diretorias,
            "div": divergencias(todos, base, dre), "gestores_em": gestores_em,
            "l3_de": l3_de}


# ------------------------------------------------------------------ excel
def estilo(wb, abas_level=()):
    for ws in wb.worksheets:
        for c in ws[1]:
            c.fill = PatternFill("solid", fgColor=AZUL)
            c.font = Font(bold=True, color="FFFFFF", size=10)
            c.alignment = Alignment(horizontal="center", vertical="center",
                                    wrap_text=True)
        ws.row_dimensions[1].height = 30
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
        larg = {}
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None:
                    larg[c.column] = min(44, max(larg.get(c.column, 9),
                                                 len(str(c.value)) + 2))
        for col, w in larg.items():
            ws.column_dimensions[get_column_letter(col)].width = w
    for nome in abas_level:
        ws = wb[nome]
        for row in ws.iter_rows(min_row=2):
            v = str(row[0].value or "")
            if v.startswith("L") and v[1:].isdigit():
                n = int(v[1:])
                row[0].fill = PatternFill("solid", fgColor=COR_LEVEL.get(n, "FFFFFF"))
                row[0].font = Font(bold=True, size=10,
                                   color="FFFFFF" if n <= 4 else "06243D")
                row[0].alignment = Alignment(horizontal="center")


def gerar_xlsx(d):
    todos, filhos, ceo, area = d["todos"], d["filhos"], d["ceo"], d["area"]
    ab, dirs = d["ab"], d["diretorias"]
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # ---------- 1. Resumo
    ws = wb.create_sheet("Resumo")
    ws.append(["Diretoria (reporte direto do CEO)", "Responsável", "Ativos",
               "Gestores", "Pessoas por gestor", "Níveis", "Vagas em aberto",
               "Vagas de chefia"])
    for f in dirs:
        ws.append([f["sigla"], f["nome"], f["ativos"], f["gestores"],
                   round(f["ativos"] / f["gestores"], 1), f["niveis"],
                   f["vagas"], f["chefia"] or ""])
    tot_a = sum(f["ativos"] for f in dirs) + 1
    tot_g = sum(f["gestores"] for f in dirs) + 1
    ws.append(["TOTAL", "DMS", tot_a, tot_g, round(tot_a / tot_g, 1),
               max(p["level"] for p in todos) - 1, len(ab),
               sum(f["chefia"] for f in dirs)])
    ws.append([])
    ws.append(["Level", "Pessoas", "Gestores", "Só executam", "Maior time"])
    for n in sorted({p["level"] for p in todos}):
        gr = [p for p in todos if p["level"] == n]
        g = [p for p in gr if p["diretos"] > 0]
        ws.append([f"L{n}", len(gr), len(g), len(gr) - len(g),
                   max([p["diretos"] for p in g], default=0)])

    # ---------- 2. Gestores (substitui as 6 abas por level)
    ws = wb.create_sheet("Gestores")
    ws.append(["Level", "Gestor", "Cargo", "Diretoria", "Diretos", "Indiretos",
               "Total abaixo", "Reporta a", "Lidera outros gestores?",
               "Marcado no draft"])
    for p in sorted([x for x in todos if x["diretos"] > 0],
                    key=lambda x: (x["level"], -x["total"], x["nome"])):
        marca = ""
        if p["nome"] in MOVIDOS_PARA_CEO:
            marca = "caixa azul: passou a reportar ao CEO"
        if p["nome"] in RISCADOS:
            sl, _, obs = RISCADOS[p["nome"]]
            marca = (marca + " | " if marca else "") + f"X no slide {sl}: {obs}"
        ws.append([f"L{p['level']}", p["nome"], cargo_de(p)[0],
                   SIGLA.get(area.get(p["nome"], p["nome"]), "DMS"),
                   p["diretos"], p["indiretos"], p["total"], p["gestor"] or "—",
                   "Sim" if any(f["diretos"] for f in filhos[p["nome"]]) else "Não",
                   marca])

    # ---------- 3. Estrutura (todas as pessoas, enxuta)
    ws = wb.create_sheet("Estrutura")
    ws.append(["Level", "Nome", "Cargo", "Gestor direto", "Diretos",
               "Total abaixo", "Diretoria", "Local"])
    for p in sorted(todos, key=lambda x: (x["level"], -x["diretos"], x["nome"])):
        ws.append([f"L{p['level']}", p["nome"], cargo_de(p)[0], p["gestor"] or "—",
                   p["diretos"], p["total"],
                   SIGLA.get(area.get(p["nome"], p["nome"]), "DMS"), p["local"]])

    # ---------- 4. Vagas por bloco
    ws = wb.create_sheet("Vagas por bloco")
    ws.append(["Bloco (área da vaga)", "C-level", "Head responsável",
               "Cargo como está na planilha", "Qtd", "Nível", "Situação",
               "Aumento ou reposição", "Folha ou colchão"])
    agr = Counter()
    meta = {}
    for v in ab:
        k = (str(v["ARÉA"]), str(v["CARGO"]), v["publicada"],
             str(v.get("Ocupante/Vaga")), str(v["Folha/Colchão"]))
        agr[k] += 1
        meta[k] = v
    for (ar, cargo, pub, ocu, fc), n in sorted(
            agr.items(), key=lambda kv: (-sum(x for k, x in agr.items()
                                              if k[0] == kv[0][0]), kv[0][0],
                                         -kv[1], kv[0][1])):
        v = meta[(ar, cargo, pub, ocu, fc)]
        head = v["head"]
        ws.append([ar, v["C-LEVEL"], head or "— sem bloco no organograma", cargo,
                   n, v["nivel"], "Publicada no Gupy" if pub else "Ainda a abrir",
                   ocu, fc])

    # ---------- 5. Divergencias (so o que divergiu)
    ws = wb.create_sheet("Divergencias")
    ws.append(["Base comparada", "Situação", "Level", "Nome", "Cargo / posição",
               "Gestor ou área", "Causa"])
    for r in d["div"]:
        ws.append([r["base"], r["tipo"], r["level"],
                   r["nome_org"] or r["nome_base"],
                   r["cargo_org"] or f"{r['info1']} · {r['info3']}",
                   r["gestor"] or r["info2"], r["causa"]])

    estilo(wb, abas_level=("Gestores", "Estrutura"))
    ws = wb["Divergencias"]
    for row in ws.iter_rows(min_row=2):
        if "gap real" in str(row[6].value) or "teste" in str(row[6].value):
            for c in row:
                c.fill = PatternFill("solid", fgColor="FDE2E2")
            row[6].font = Font(bold=True, color="9C0006", size=10)
    for nome, cor in (("Resumo", VERDE), ("Vagas por bloco", LARANJA)):
        for c in wb[nome][1]:
            c.fill = PatternFill("solid", fgColor=cor)

    destino = os.path.join(SAIDA, "Gestores_por_Level.xlsx")
    wb.save(destino)
    return destino, wb


# ------------------------------------------------------------------ markdown
def gerar_md(d):
    todos, filhos, ceo, area = d["todos"], d["filhos"], d["ceo"], d["area"]
    ab, dirs = d["ab"], d["diretorias"]
    L = []
    A = L.append
    A("# Gestores da DMS — estrutura, liderança e vagas")
    A("")
    A("Planilha única: **`Gestores_por_Level.xlsx`**, 5 abas.")
    A("")
    A("| Aba | O que tem |")
    A("|---|---|")
    A("| `Resumo` | uma linha por diretoria: ativos, gestores, pessoas por gestor, "
      "níveis, vagas e vagas de chefia; abaixo, o corte por level |")
    A("| `Gestores` | os 66 gestores, com filtro de level — substitui as seis abas "
      "`Lx gestores` da versão anterior |")
    A("| `Estrutura` | as 336 pessoas com gestor direto, em 8 colunas |")
    A("| `Vagas por bloco` | as 49 vagas como estão escritas na planilha de vagas, "
      "ligadas ao head do bloco |")
    A("| `Divergencias` | só o que divergiu entre organograma, folha e DRE |")
    A("")
    A("---")
    A("")
    A("## A estrutura em uma tabela")
    A("")
    A("| Diretoria | Responsável | Ativos | Gestores | Pessoas por gestor | Níveis "
      "| Vagas | Vagas de chefia |")
    A("|---|---|---|---|---|---|---|---|")
    for f in dirs:
        A(f"| {f['sigla']} | {f['nome']} | {f['ativos']} | {f['gestores']} "
          f"| {f['ativos']/f['gestores']:.1f} | {f['niveis']} | {f['vagas']} "
          f"| {f['chefia'] or '—'} |")
    ta = sum(f["ativos"] for f in dirs) + 1
    tg = sum(f["gestores"] for f in dirs) + 1
    A(f"| **TOTAL** | DMS | **{ta}** | **{tg}** | **{ta/tg:.1f}** "
      f"| {max(p['level'] for p in todos)-1} | **{len(ab)}** "
      f"| **{sum(f['chefia'] for f in dirs)}** |")
    A("")
    A("---")
    A("")
    A("## Pontos da camada de liderança")
    A("")
    solo = [p for p in todos if p["diretos"] == 1]
    sem = [p for p in todos if any(k in p["cargo"].lower() for k in CHEFIA)
           and p["diretos"] == 0]
    maior = max(todos, key=lambda p: p["diretos"])
    A(f"1. **Um gestor com {maior['diretos']} liderados diretos** — {maior['nome']} "
      f"(*{maior['cargo']}*), contra média de 5,1 na casa.")
    A(f"2. **{len(solo)} gestores com um único liderado**: "
      + "; ".join(f"{p['nome']} (L{p['level']})" for p in solo) + ".")
    A(f"3. **{len(sem)} pessoas com título de chefia e nenhum liderado**: "
      + "; ".join(f"{p['nome']} ({p['cargo']})" for p in sem) + ".")
    A("4. **Quatro Team Leaders lideram outros Team Leaders com o título idêntico** "
      "em Operações Aéreo: Gabriella De Melo Pereira e Pamela Iris Gregorio Ibarra "
      "lideram Julia Heinrichs, Lenice Barbosa, Thais Mathias e Julia Varella, "
      "todos *Air Freight Operations Team Leader*. O draft risca com X justamente "
      "a Gabriella e a Pamela.")
    chefia = [v for v in ab if v["nivel"] in ("Head", "Team Leader")]
    A(f"5. **{len(chefia)} vagas de chefia em aberto**, "
      f"{sum(1 for v in chefia if not v['publicada'])} sem processo iniciado.")
    A("")
    A("---")
    A("")
    A("## As 49 vagas como aparecem na planilha")
    A("")
    A("| Bloco | Cargo na planilha | Qtd | Situação | Aumento ou reposição |")
    A("|---|---|---|---|---|")
    agr = Counter((str(v["ARÉA"]), str(v["CARGO"]), v["publicada"],
                   str(v.get("Ocupante/Vaga"))) for v in ab)
    tot_area = Counter(str(v["ARÉA"]) for v in ab)
    for (ar, cargo, pub, ocu), n in sorted(
            agr.items(), key=lambda kv: (-tot_area[kv[0][0]], kv[0][0], -kv[1])):
        A(f"| {ar} | `{cargo}` | {n} | "
          f"{'Publicada' if pub else 'Ainda a abrir'} | {ocu} |")
    A("")
    A("---")
    A("")
    A("## Divergências que sobraram")
    A("")
    gaps = [r for r in d["div"] if "gap real" in r["causa"]]
    A(f"Depois de descontar data de corte, aviso prévio, sócios, consultorias e "
      f"linha duplicada, restam **{len({r['nome_base'] for r in gaps})} pessoas "
      "com custo lançado e sem posição no organograma**. Detalhe na aba "
      "`Divergencias`.")
    A("")
    A("## Como regerar")
    A("")
    A("```bash")
    A("pip install openpyxl")
    A("python3 estrutura/gestores_por_level.py")
    A("```")
    return "\n".join(L)


def main():
    d = levantar()
    md = os.path.join(SAIDA, "Gestores_por_Level.md")
    with open(md, "w", encoding="utf-8") as fh:
        fh.write(gerar_md(d) + "\n")
    xl, wb = gerar_xlsx(d)
    print(f"{len(d['todos'])} pessoas | "
          f"{sum(1 for p in d['todos'] if p['diretos']>0)} gestores | "
          f"{len(d['ab'])} vagas em aberto")
    print("abas:", [ws.title + f" ({ws.max_row-1})" for ws in wb.worksheets])
    print(f"divergências: {len(d['div'])} linhas (sem as que casaram)")
    print("ok ->", md)
    print("ok ->", xl)


if __name__ == "__main__":
    main()
