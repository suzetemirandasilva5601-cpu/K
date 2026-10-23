#!/usr/bin/env python3
"""
Le 'Colaboradores-factorial (3).xlsx' e lista os gestores separados por level,
mostrando quem cada um administra.

Saidas:
  estrutura/Gestores_por_Level.md
  estrutura/Gestores_por_Level.xlsx

Como a planilha foi lida:
  - Cada aba ('level 4' a 'level 8') lista as pessoas DAQUELE level nas colunas
    Nome/Sobrenome/Funcao.
  - As colunas A e B sao 'Nivel de gerente N-2' e 'Nivel de gerente N-1'.
    Vem como celulas mescladas, entao o valor vale para todo o bloco abaixo.
  - A coluna B e o GESTOR DIRETO da pessoa da linha.
  - Os levels 1, 2 e 3 nao tem linha propria: aparecem apenas como nome de
    gestor nas colunas A e B, sem cargo informado.

Uso:  python3 estrutura/gestores_por_level.py
"""
import os
from collections import defaultdict

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from cross_check import CARGOS_DRAFT, C_LEVEL_DRE, DRAFT_LIDERADOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, "Colaboradores-factorial (3).xlsx")
SAIDA = os.path.join(RAIZ, "estrutura")

NIVEL_ABA = {"level 4": 4, "level 5": 5, "level 6": 6, "level 7": 7, "level 8": 8}
SEM_CARGO = "(cargo não informado na planilha)"


def cargo_refinado(p):
    """Cargo da planilha; para L2/L3 usa o cargo lido no draft."""
    if p["nome"] in CARGOS_DRAFT:
        cargo, slide, trunc = CARGOS_DRAFT[p["nome"]]
        return cargo, f"draft {slide}"
    return (p["cargo"], "planilha") if p["cargo"] else (SEM_CARGO, "—")


def plural(n, singular, plural_=None):
    return f"{n} {singular}" if n == 1 else f"{n} {plural_ or singular + 's'}"


def ler():
    """Retorna a lista de pessoas das abas level 4 a level 8."""
    wb = openpyxl.load_workbook(ORIGEM, data_only=True)
    pessoas = []
    for aba, nivel in NIVEL_ABA.items():
        ws = wb[aba]
        g_acima = g_direto = None
        for r in ws.iter_rows(min_row=3, values_only=True):
            if all(c is None for c in r):
                continue
            if r[0]:
                g_acima = str(r[0]).strip()
            if r[1]:
                g_direto = str(r[1]).strip()
            pessoas.append({
                "nome": f"{r[2] or ''} {r[3] or ''}".strip(),
                "level": nivel,
                "cargo": (str(r[4]).strip() if r[4] else ""),
                "gestor": g_direto,
                "gestor_acima": g_acima,
                "total": int(r[5] or 0),
                "diretos": int(r[6] or 0),
                "local": r[9] or "",
            })
    return pessoas


def organizar(pessoas):
    """Monta o indice gestor -> liderados e acrescenta os levels 2 e 3."""
    liderados = defaultdict(list)
    for p in pessoas:
        liderados[p["gestor"]].append(p)

    nomes = {p["nome"] for p in pessoas}
    # L3: citados como gestor de alguem do L4, mas sem linha propria.
    l3 = sorted({p["gestor"] for p in pessoas if p["level"] == 4} - nomes)
    # L2: citado na coluna A da aba level 4.
    l2 = sorted({p["gestor_acima"] for p in pessoas if p["level"] == 4} - nomes)

    for nome in l3:
        pessoas.append({
            "nome": nome, "level": 3, "cargo": "", "gestor": l2[0],
            "gestor_acima": None, "diretos": len(liderados[nome]),
            "total": 0, "local": "",
        })
        liderados[l2[0]].append(pessoas[-1])
    for nome in l2:
        pessoas.append({
            "nome": nome, "level": 2, "cargo": "", "gestor": None,
            "gestor_acima": None, "diretos": len(liderados[nome]),
            "total": 0, "local": "",
        })

    # total abaixo (todos os levels), calculado a partir da propria arvore
    def total(nome):
        t = len(liderados[nome])
        for f in liderados[nome]:
            t += total(f["nome"])
        return t

    for p in pessoas:
        p["total"] = total(p["nome"])
        p["indiretos"] = p["total"] - p["diretos"]

    for k in liderados:
        liderados[k].sort(key=lambda x: (-x["diretos"], x["nome"]))
    return liderados


def cargo_de(p):
    return p["cargo"] or SEM_CARGO


def gerar_md(pessoas, liderados):
    por_level = defaultdict(list)
    for p in pessoas:
        por_level[p["level"]].append(p)

    L = []
    A = L.append
    A("# Gestores por level — quem administra quem")
    A("")
    A("Fonte: **`Colaboradores-factorial (3).xlsx`**, abas `level 4` a `level 8`.")
    A("")
    A("**Como a planilha foi lida:** em cada aba, a pessoa da linha está no level "
      "da aba, e a **coluna B (`Nível de gerente N-1`) é o gestor direto dela**. "
      "Essas colunas vêm mescladas, então o nome vale para todo o bloco de linhas "
      "abaixo dele.")
    A("")
    A("**Os levels 2 e 3 não têm linha própria na planilha** — aparecem só como nome "
      "de gestor, sem cargo. Os cargos deles foram lidos nos organogramas do "
      "`Draft 23 Out 26.pptx` e estão marcados com a origem. "
      "Ver `Cross_Check_Organograma.md` para a conferência completa.")
    A("")

    # ---- topo da estrutura
    A("## O topo da estrutura, com cargo")
    A("")
    A("| Level | Nome | Cargo | Fonte do cargo | C-LEVEL no DRE | Diretos | Indiretos | Total |")
    A("|---|---|---|---|---|---|---|---|")
    for p in sorted([x for x in pessoas if x["level"] <= 3],
                    key=lambda x: (x["level"], -x["total"])):
        cargo, fonte = cargo_refinado(p)
        A(f"| L{p['level']} | **{p['nome']}** | {cargo} | {fonte} "
          f"| {C_LEVEL_DRE.get(p['nome'], '—')} | {p['diretos']} | {p['indiretos']} "
          f"| **{p['total']}** |")
    A("")
    A("Dois cargos vêm truncados no print do Factorial: *Chief Information & Tec…* "
      "(Cleyton) e *Chief Strategy Finance …* (Ana Carolina). No DRE eles aparecem "
      "pelas siglas **CITO** e **CFSO**.")
    A("")
    A("Note que o CEO é **Co-**Chief Executive Officer. A folha de setembro tem outras "
      "duas pessoas em `OWNERSHIP` que não estão no organograma: "
      "Fernando Esteves Arruda (EXECUTIVE BOARD) e Eduardo Reis de Almeida (OWNERSHIP).")
    A("")
    A("---")
    A("")

    # ---- indice
    A("## Quantos gestores em cada level")
    A("")
    A("| Level | Pessoas no level | Gestores | Administram juntos | Só executam |")
    A("|---|---|---|---|---|")
    for n in sorted(por_level):
        gr = por_level[n]
        g = [p for p in gr if p["diretos"] > 0]
        soma = sum(p["diretos"] for p in g)
        adm = f"{soma} pessoas do L{n+1}" if soma else "—"
        A(f"| **L{n}** | {len(gr)} | **{len(g)}** | {adm} | {len(gr) - len(g)} |")
    A(f"| **Total** | **{len(pessoas)}** | "
      f"**{sum(1 for p in pessoas if p['diretos'] > 0)}** | "
      f"{sum(p['diretos'] for p in pessoas)} | "
      f"{sum(1 for p in pessoas if p['diretos'] == 0)} |")
    A("")
    A("No L8 ninguém administra ninguém — é o fim da cadeia.")
    A("")
    A("---")
    A("")

    # ---- um bloco por level
    for n in sorted(por_level):
        gestores = [p for p in por_level[n] if p["diretos"] > 0]
        simples = [p for p in por_level[n] if p["diretos"] == 0]
        A(f"# LEVEL {n}")
        A("")
        if not gestores:
            A(f"**Nenhum gestor neste level.** As {len(simples)} pessoas do L{n} "
              "não administram ninguém.")
            A("")
            A("| Nome | Cargo | Gestor direto (L{}) |".format(n - 1))
            A("|---|---|---|")
            for p in sorted(simples, key=lambda x: x["nome"]):
                A(f"| {p['nome']} | {cargo_de(p)} | {p['gestor']} |")
            A("")
            continue

        A(f"**{plural(len(gestores), 'gestor', 'gestores')}** no L{n}, administrando "
          f"{plural(sum(p['diretos'] for p in gestores), 'pessoa')} diretamente.")
        if simples:
            A("")
            A(f"(as outras {len(simples)} pessoas do L{n} não administram ninguém — "
              "listadas no fim do bloco)")
        A("")
        A("| Gestor | Cargo | Diretos | Indiretos | Total abaixo | Confere com o draft? |")
        A("|---|---|---|---|---|---|")
        for p in gestores:
            cargo, _ = cargo_refinado(p)
            d = DRAFT_LIDERADOS.get(p["nome"])
            ok = ("—" if not d else
                  f"sim ({d[1]})" if d[0] == p["total"] else
                  f"draft {d[0]}, +{p['total']-d[0]} depois")
            A(f"| {p['nome']} | {cargo} | **{p['diretos']}** | {p['indiretos']} "
              f"| {p['total']} | {ok} |")
        A("")

        for p in gestores:
            cargo, fonte = cargo_refinado(p)
            A(f"### {p['nome']}  ·  L{n}")
            A("")
            A(f"{cargo}" + (f"  *(cargo lido no {fonte})*" if fonte.startswith("draft")
                            else "") + "  ")
            A(f"Administra **{plural(p['diretos'], 'pessoa')}** diretamente"
              + (f" e **{plural(p['indiretos'], 'pessoa')}** indiretamente, "
                 f"somando {p['total']}." if p["indiretos"] else
                 " — nenhum indireto: o time todo é de executores.")
              + (f"  \nReporta a: **{p['gestor']}** (L{n-1})" if p["gestor"] else
                 "  \nTopo da estrutura — não reporta a ninguém na planilha."))
            A("")
            A("| # | Administra | Cargo | Level | Esse também administra? |")
            A("|---|---|---|---|---|")
            for i, f in enumerate(liderados[p["nome"]], 1):
                adm = (f"sim — {plural(f['diretos'], 'pessoa')}"
                       if f["diretos"] > 0 else "não")
                A(f"| {i} | {f['nome']} | {cargo_de(f)} | L{f['level']} | {adm} |")
            A("")

        if simples:
            A(f"### L{n} — não administram ninguém ({len(simples)} pessoas)")
            A("")
            A(f"| Nome | Cargo | Gestor direto (L{n-1}) |")
            A("|---|---|---|")
            for p in sorted(simples, key=lambda x: x["nome"]):
                A(f"| {p['nome']} | {cargo_de(p)} | {p['gestor']} |")
            A("")
        A("---")
        A("")

    A("## Como regerar")
    A("")
    A("```bash")
    A("pip install openpyxl")
    A("python3 estrutura/gestores_por_level.py")
    A("```")
    return "\n".join(L)


def gerar_xlsx(pessoas, liderados):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    por_level = defaultdict(list)
    for p in pessoas:
        por_level[p["level"]].append(p)

    # ---- uma aba por level: gestor -> liderado
    for n in sorted(por_level):
        gestores = [p for p in por_level[n] if p["diretos"] > 0]
        if not gestores:
            continue
        ws = wb.create_sheet(f"L{n} gestores")
        ws.append([f"Gestor (L{n})", "Cargo do gestor", "Diretos", "Total abaixo",
                   "Administra", "Cargo de quem ele administra", "Level",
                   "Esse administra quantos?"])
        for p in gestores:
            for f in liderados[p["nome"]]:
                ws.append([p["nome"], cargo_de(p), p["diretos"], p["total"],
                           f["nome"], cargo_de(f), f"L{f['level']}", f["diretos"]])

    # ---- aba plana: cada pessoa e seu gestor
    ws = wb.create_sheet("Quem reporta a quem", 0)
    ws.append(["Level", "Nome", "Cargo", "Administra (diretos)", "Total abaixo",
               "Gestor direto", "Level do gestor", "Local"])
    for p in sorted(pessoas, key=lambda x: (x["level"], -x["diretos"], x["nome"])):
        ws.append([f"L{p['level']}", p["nome"], cargo_de(p), p["diretos"], p["total"],
                   p["gestor"] or "—", f"L{p['level']-1}" if p["gestor"] else "—",
                   p["local"]])

    # ---- aba resumo
    ws = wb.create_sheet("Resumo por level", 1)
    ws.append(["Level", "Pessoas", "Gestores", "Só executam", "Diretos administrados",
               "Maior time (diretos)"])
    for n in sorted(por_level):
        gr = por_level[n]
        g = [p for p in gr if p["diretos"] > 0]
        ws.append([f"L{n}", len(gr), len(g), len(gr) - len(g),
                   sum(p["diretos"] for p in g),
                   max([p["diretos"] for p in g], default=0)])

    # ---- formatacao
    cor = {2: "0D1F31", 3: "1B3A5C", 4: "2E6CA4", 5: "67A3D9",
           6: "AED2F0", 7: "DFEAF5", 8: "F4F8FC"}
    for sheet in wb.worksheets:
        for c in sheet[1]:
            c.fill = PatternFill("solid", fgColor="1B3A5C")
            c.font = Font(bold=True, color="FFFFFF")
            c.alignment = Alignment(horizontal="center", vertical="center",
                                    wrap_text=True)
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = f"A1:{get_column_letter(sheet.max_column)}1"
        larg = {}
        for row in sheet.iter_rows():
            for c in row:
                if c.value is not None:
                    larg[c.column] = min(48, max(larg.get(c.column, 10),
                                                 len(str(c.value)) + 2))
        for col, w in larg.items():
            sheet.column_dimensions[get_column_letter(col)].width = w
    ws = wb["Quem reporta a quem"]
    for row in ws.iter_rows(min_row=2):
        n = int(str(row[0].value)[1:])
        row[0].fill = PatternFill("solid", fgColor=cor[n])
        row[0].font = Font(bold=True, color="FFFFFF" if n <= 4 else "06243D")
        row[0].alignment = Alignment(horizontal="center")

    destino = os.path.join(SAIDA, "Gestores_por_Level.xlsx")
    wb.save(destino)
    return destino


def main():
    os.makedirs(SAIDA, exist_ok=True)
    pessoas = ler()
    lidos = len(pessoas)
    liderados = organizar(pessoas)

    md = os.path.join(SAIDA, "Gestores_por_Level.md")
    with open(md, "w", encoding="utf-8") as fh:
        fh.write(gerar_md(pessoas, liderados) + "\n")
    xl = gerar_xlsx(pessoas, liderados)

    print(f"{lidos} linhas lidas (L4-L8) + "
          f"{len(pessoas)-lidos} gestores de L2/L3 = {len(pessoas)} pessoas")
    for n in sorted({p['level'] for p in pessoas}):
        g = [p for p in pessoas if p["level"] == n and p["diretos"] > 0]
        print(f"  L{n}: {sum(1 for p in pessoas if p['level']==n):>3} pessoas, "
              f"{len(g):>2} gestores")
    print("ok ->", md)
    print("ok ->", xl)


if __name__ == "__main__":
    main()
