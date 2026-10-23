#!/usr/bin/env python3
"""
Gera a hierarquia de gestao da DMS a partir de 'Colaboradores-factorial (3).xlsx'.

Saidas:
  estrutura/Hierarquia_Gestao_DMS.md    - visao visual (piramide, mermaid, arvores)
  estrutura/Hierarquia_DMS.xlsx         - base indentada + aba de gestores + resumo

Uso:  python3 estrutura/gerar_hierarquia.py
"""
import os
import re
import unicodedata
from collections import Counter, defaultdict

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, "Colaboradores-factorial (3).xlsx")
SAIDA = os.path.join(RAIZ, "estrutura")

# Abas do arquivo -> nivel hierarquico da pessoa listada na linha.
NIVEL_ABA = {"level 4": 4, "level 5": 5, "level 6": 6, "level 7": 7, "level 8": 8}

# L3 nao tem linha propria na planilha (so aparece como nome de gestor).
# As areas abaixo foram inferidas cruzando com o 'Draft 23 Out 26.pptx'.
AREAS_L3 = {
    "Ana Carolina Botelho Caldeira Vasconcellos": ("Finanças", "FIN"),
    "Andre Lemos Tavares": ("Comercial / Indústrias", "COM"),
    "Carolina Karnakis de Nobrega": ("Recursos Humanos", "RH"),
    "Cleyton Cardoso Esteves": ("Tecnologia", "TEC"),
    "Luis Fernando Santos Muniz": ("Serviços / Diligenciamento", "SER"),
    "Raioni De Oliveira Santos": ("Operações", "OPS"),
}
CEO = "Jose Luiz de Oliveira Belixior Junior"

# Faixa de senioridade a partir do titulo do cargo.
def faixa(cargo):
    c = (cargo or "").lower()
    if "head" in c or "director" in c or "manager" in c:
        return "Head / Manager"
    if "team leader" in c or "coordinator" in c or "lead " in c:
        return "Team Leader"
    if "specialist" in c or "architect" in c or "consultor" in c:
        return "Specialist"
    if "analyst" in c or "developer" in c or "analytiker" in c or "engineer" in c:
        return "Analyst"
    if "assistant" in c or "clerk" in c or "agent" in c:
        return "Assistant"
    if "intern" in c or "apprentice" in c:
        return "Intern / Aprendiz"
    if "executive" in c:
        return "Executive (comercial)"
    return "Cargo em branco"


PREP = {"de", "da", "do", "dos", "das", "e"}


def curto(nome, n=2):
    """Primeiro nome + sobrenomes, ignorando preposicoes."""
    p = [x for x in nome.split() if x.lower() not in PREP]
    return " ".join(p[:n]) if len(p) > n else " ".join(p)


def sigla(cargo):
    """Abrevia o cargo para caber nas caixas do diagrama."""
    if not cargo:
        return "cargo em branco"
    c = cargo
    for de, para in [
        ("Planning & Analysis", "FP&A"),
        ("Business Development", "BD"), ("Business Intelligence", "BI"),
        ("Operations", "Ops"), ("Operation", "Ops"),
        ("Operational", "Op."), ("Development", "Dev."),
        ("Customer Care", "Cust. Care"), ("Team Leader", "TL"),
        ("Senior", "Sr."), ("Intelligence", "Intel."),
        ("Human Resources", "RH"), ("Industry", "Ind."),
        ("Coordinator", "Coord."), ("Management", "Mgmt"),
        ("Specialist", "Spec."), ("Improvement", "Improv."),
        ("Certification", "Certif."), ("Department", "Dept."),
    ]:
        c = c.replace(de, para)
    return c.replace("&", "&amp;")


_ids = {}


def mid(nome):
    """Id curto, estavel e unico para no de mermaid."""
    if nome in _ids:
        return _ids[nome]
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    base = "n" + re.sub(r"[^A-Za-z0-9]", "", s)[:24]
    cand, i = base, 1
    while cand in _ids.values():
        i += 1
        cand = f"{base}{i}"
    _ids[nome] = cand
    return cand


# ----------------------------------------------------------------- leitura
def carregar():
    wb = openpyxl.load_workbook(ORIGEM, data_only=True)
    pessoas = []
    for ws in wb.worksheets:
        if ws.title not in NIVEL_ABA:
            continue
        linhas = list(ws.iter_rows(min_row=3, values_only=True))
        g_acima = g_direto = None
        for r in linhas:
            if all(c is None for c in r):
                continue
            if r[0]:
                g_acima = str(r[0]).strip()
            if r[1]:
                g_direto = str(r[1]).strip()
            nome = f"{r[2] or ''} {r[3] or ''}".strip()
            pessoas.append({
                "nome": nome,
                "nivel": NIVEL_ABA[ws.title],
                "cargo": (str(r[4]).strip() if r[4] else ""),
                "gestor": g_direto,
                "gestor_acima": g_acima,
                "total": int(r[5] or 0),
                "diretos": int(r[6] or 0),
                "entidade": r[7] or "",
                "genero": r[8] or "",
                "local": r[9] or "",
                "inicio": str(r[10])[:10] if r[10] else "",
            })
    return pessoas


def montar(pessoas):
    filhos = defaultdict(list)
    for p in pessoas:
        filhos[p["gestor"]].append(p)
    for k in filhos:
        filhos[k].sort(key=lambda x: (-x["total"], -x["diretos"], x["nome"]))
    return filhos


def tamanho(filhos, nome):
    t = len(filhos[nome])
    for f in filhos[nome]:
        t += tamanho(filhos, f["nome"])
    return t


# ----------------------------------------------------------------- markdown
def arvore_ascii(filhos, nome, nivel=0, linhas=None, so_gestores=True):
    linhas = linhas if linhas is not None else []
    diretos = filhos[nome]
    gestores = [p for p in diretos if p["diretos"] > 0]
    individuais = [p for p in diretos if p["diretos"] == 0]
    for g in gestores:
        pre = "    " * nivel + "+-- "
        dir_rot = "direto" if g["diretos"] == 1 else "diretos"
        linhas.append(
            f"{pre}**L{g['nivel']} {g['nome']}** · {sigla(g['cargo'])} "
            f"`{g['diretos']} {dir_rot} / {g['total']} total`"
        )
        arvore_ascii(filhos, g["nome"], nivel + 1, linhas, so_gestores)
    if individuais:
        pre = "    " * nivel + "+-- "
        cargos = Counter(sigla(p["cargo"]) or "cargo em branco" for p in individuais)
        desc = ", ".join(f"{c} ({n})" if n > 1 else c for c, n in cargos.most_common())
        n = len(individuais)
        rot = "1 pessoa que não lidera" if n == 1 else f"{n} pessoas que não lideram"
        linhas.append(f"{pre}_{rot}_ — {desc}")
    return linhas


ESTILOS = [
    '  classDef l3 fill:#1b3a5c,stroke:#0d1f31,color:#fff,font-weight:bold',
    '  classDef l4 fill:#2e6ca4,stroke:#1b3a5c,color:#fff',
    '  classDef l5 fill:#67a3d9,stroke:#2e6ca4,color:#06243d',
    '  classDef l6 fill:#aed2f0,stroke:#67a3d9,color:#06243d',
    '  classDef l7 fill:#dfeaf5,stroke:#aed2f0,color:#06243d',
    '  classDef eq fill:#f4f4f4,stroke:#bbb,color:#555,font-style:italic',
]


def conta_gestores(filhos, nome):
    n = 0
    for p in filhos[nome]:
        if p["diretos"] > 0:
            n += 1 + conta_gestores(filhos, p["nome"])
    return n


def mermaid(filhos, raiz, rotulo_raiz, classe_raiz="l3", so_filhos_gestores=False,
            profundidade=99):
    """Diagrama da cadeia de gestao a partir de `raiz` (so quem tem liderados)."""
    out = ["```mermaid", "flowchart LR"] + ESTILOS
    classes = defaultdict(list)
    out.append(f'  {mid(raiz)}["{rotulo_raiz}"]')
    classes[classe_raiz].append(mid(raiz))

    def rec(nome, prof):
        gest = [p for p in filhos[nome] if p["diretos"] > 0]
        ind = [p for p in filhos[nome] if p["diretos"] == 0]
        if prof <= 0:
            return
        for p in gest:
            nid = mid(p["nome"])
            out.append(
                f'  {nid}["L{p["nivel"]} · {curto(p["nome"])}<br/>{sigla(p["cargo"])}'
                f'<br/>{p["diretos"]} dir · {p["total"]} tot"]'
            )
            classes[f"l{min(p['nivel'], 7)}"].append(nid)
            out.append(f"  {mid(nome)} --> {nid}")
            rec(p["nome"], prof - 1)
        if ind and not so_filhos_gestores:
            eid = mid(nome) + "x"
            cargos = Counter(sigla(p["cargo"]) for p in ind)
            topo, qtd = cargos.most_common(1)[0]
            outros = len(cargos) - 1
            desc = (topo if outros == 0 else
                    f"{qtd}x {topo} +{outros} cargo" + ("s" if outros > 1 else ""))
            rot = "1 não lidera" if len(ind) == 1 else f"{len(ind)} não lideram"
            out.append(f'  {eid}("{rot}<br/>{desc}")')
            classes["eq"].append(eid)
            out.append(f"  {mid(nome)} -.-> {eid}")

    rec(raiz, profundidade)
    for cls, nos in classes.items():
        if nos:
            out.append(f"  class {','.join(sorted(set(nos)))} {cls}")
    out.append("```")
    return "\n".join(out)


def blocos_diretoria(filhos, l3, area):
    """Um diagrama por diretoria; se for grande, quebra em visao geral + ramos L4."""
    rot = f"L3 · {curto(l3, 3)}<br/><b>{area}</b><br/>{tamanho(filhos, l3)} pessoas"
    if conta_gestores(filhos, l3) <= 12:
        return [mermaid(filhos, l3, rot)]
    partes = ["**Visão geral da diretoria** — os Heads de primeira linha:", "",
              mermaid(filhos, l3, rot, so_filhos_gestores=False, profundidade=1), ""]
    for p in filhos[l3]:
        if conta_gestores(filhos, p["nome"]) == 0:
            continue
        rot4 = (f'L4 · {curto(p["nome"])}<br/><b>{sigla(p["cargo"])}</b>'
                f'<br/>{p["diretos"]} dir · {p["total"]} tot')
        partes += [f"**Ramo: {p['cargo']} — {p['nome']}** "
                   f"({p['total']} pessoas)", "",
                   mermaid(filhos, p["nome"], rot4, classe_raiz="l4"), ""]
    return partes


def gerar_md(pessoas, filhos):
    total = len(pessoas) + len(AREAS_L3) + 1
    por_nivel = Counter(p["nivel"] for p in pessoas)
    gest_nivel = {n: sum(1 for p in pessoas if p["nivel"] == n and p["diretos"] > 0)
                  for n in range(4, 9)}
    L = []
    A = L.append

    A("# Hierarquia de gestão — DMS")
    A("")
    A("Reconstruída a partir de **`Colaboradores-factorial (3).xlsx`** "
      "(abas `level 4` a `level 8`, 329 linhas). "
      "Os níveis 1 a 3 não têm linha própria na planilha: aparecem apenas como "
      "*nome do gestor*, então **não há cargo informado para eles**. "
      "O nome das diretorias abaixo foi inferido cruzando com o `Draft 23 Out 26.pptx`.")
    A("")
    A(f"**{total} pessoas** no total: 1 no topo (L2) + {len(AREAS_L3)} diretorias (L3) "
      f"+ {len(pessoas)} nas abas (L4–L8).")
    A("")
    A("---")
    A("")

    # ---------------- piramide
    gest_nivel[2] = 1
    gest_nivel[3] = sum(1 for l in AREAS_L3 if filhos[l])
    por_nivel[2] = 1
    por_nivel[3] = len(AREAS_L3)
    tot_gest = sum(gest_nivel.values())

    A("## 1. A pirâmide em uma tela")
    A("")
    A("```")
    A("  NÍVEL   PAPEL TÍPICO          VOLUME            PESSOAS  GESTORES  SÓ EXECUTA")
    A("  ───────────────────────────────────────────────────────────────────────────────")
    rot = {2: "CEO", 3: "Diretoria", 4: "Head / Team Leader",
           5: "TL / Especialista", 6: "Analista / TL",
           7: "Analista / Assistente", 8: "Analista / Assistente"}
    maxp = max(por_nivel[n] for n in range(2, 9))
    for n in range(2, 9):
        p, g = por_nivel[n], gest_nivel[n]
        barra = "█" * max(1, round(p / maxp * 16))
        A(f"  L{n}      {rot[n]:<21} {barra:<17} {p:>5}    {g:>5}      {p - g:>5}")
    A("  ───────────────────────────────────────────────────────────────────────────────")
    A(f"          TOTAL                                  {total:>5}    {tot_gest:>5}"
      f"      {total - tot_gest:>5}")
    A("```")
    A("")
    razao = f"{(total - tot_gest) / tot_gest:.1f}".replace(".", ",")
    A(f"Leitura rápida: **{tot_gest} gestores** e **{total - tot_gest} pessoas que só executam** "
      f"(1 gestor para cada {razao} liderados). "
      f"A gestão **termina no L7** — nenhum dos {por_nivel[8]} L8 lidera ninguém. "
      f"Dos {tot_gest} gestores, {gest_nivel[4] + gest_nivel[5]} estão em L4–L5 e "
      f"{gest_nivel[6] + gest_nivel[7]} em L6–L7, e esses {gest_nivel[6] + gest_nivel[7]} "
      "estão quase todos dentro de Operações Aéreo, a única área que desce até oito níveis.")
    A("")
    A("---")
    A("")

    # ---------------- topo
    A("## 2. Topo da casa (L2 → L3 → L4)")
    A("")
    A("```mermaid")
    A("flowchart TD")
    A('  classDef ceo fill:#0d1f31,stroke:#000,color:#fff,font-weight:bold')
    A('  classDef l3 fill:#1b3a5c,stroke:#0d1f31,color:#fff')
    A('  classDef l4 fill:#2e6ca4,stroke:#1b3a5c,color:#fff')
    A(f'  CEO["L2 · {curto(CEO,3)}<br/>CEO (cargo não informado)<br/>{total-1} liderados"]')
    A("  class CEO ceo")
    ids3, ids4 = [], []
    for l3, (area, _) in sorted(AREAS_L3.items(), key=lambda kv: -tamanho(filhos, kv[0])):
        A(f'  {mid(l3)}["L3 · {curto(l3,3)}<br/><b>{area}</b><br/>'
          f'{len(filhos[l3])} diretos · {tamanho(filhos,l3)} pessoas"]')
        A(f"  CEO --> {mid(l3)}")
        ids3.append(mid(l3))
        for p in filhos[l3]:
            A(f'  {mid(p["nome"])}["L4 · {curto(p["nome"])}<br/>{sigla(p["cargo"]) or "cargo em branco"}'
              f'<br/>{p["total"]} liderados"]')
            A(f"  {mid(l3)} --> {mid(p['nome'])}")
            ids4.append(mid(p["nome"]))
    A(f"  class {','.join(ids3)} l3")
    A(f"  class {','.join(sorted(set(ids4)))} l4")
    A("```")
    A("")

    # ---------------- tabela diretorias
    A("### As seis diretorias, por tamanho")
    A("")
    A("| # | Diretoria (L3) | Responsável | Diretos | Pessoas na área | % da empresa | Profundidade |")
    A("|---|---|---|---|---|---|---|")
    for i, (l3, (area, _)) in enumerate(
            sorted(AREAS_L3.items(), key=lambda kv: -tamanho(filhos, kv[0])), 1):
        tam = tamanho(filhos, l3)
        prof = max([p["nivel"] for p in pessoas if raiz_de(p, pessoas, filhos, l3)] or [3])
        A(f"| {i} | **{area}** | {l3} | {len(filhos[l3])} | {tam} | "
          f"{tam/ (total-1) * 100:.0f}% | até L{prof} |")
    A("")
    A("---")
    A("")

    # ---------------- por diretoria
    A("## 3. Cadeia de gestão, diretoria por diretoria")
    A("")
    A("Nas árvores: `X diretos / Y total` = liderados diretos e liderados somando "
      "todos os níveis abaixo. As linhas em itálico agrupam quem **não lidera ninguém**.")
    A("")
    for l3, (area, _) in sorted(AREAS_L3.items(), key=lambda kv: -tamanho(filhos, kv[0])):
        A(f"### {area} — {l3}")
        A("")
        A(f"`L3` · {len(filhos[l3])} liderados diretos · "
          f"**{tamanho(filhos,l3)} pessoas na área** · "
          f"{conta_gestores(filhos, l3)} gestores abaixo")
        A("")
        for bloco in blocos_diretoria(filhos, l3, area):
            A(bloco)
        A("")
        A("<details><summary>Árvore em texto (clique para abrir)</summary>")
        A("")
        A(f"**L3 {l3}** — {area}")
        A("")
        for ln in arvore_ascii(filhos, l3, 0):
            A(f"{ln}  ")
        A("")
        A("</details>")
        A("")
    A("---")
    A("")

    # ---------------- gestores
    A(f"## 4. Os {tot_gest} gestores, do maior para o menor time")
    A("")
    A("| Nível | Nome | Cargo | Diretos | Total abaixo | Diretoria |")
    A("|---|---|---|---|---|---|")
    A(f"| L2 | {CEO} | — (CEO) | {len(AREAS_L3)} | {total-1} | DMS |")
    for l3, (area, _) in sorted(AREAS_L3.items(), key=lambda kv: -tamanho(filhos, kv[0])):
        A(f"| L3 | {l3} | — | {len(filhos[l3])} | {tamanho(filhos,l3)} | {area} |")
    gest = sorted([p for p in pessoas if p["diretos"] > 0],
                  key=lambda p: (-p["total"], p["nivel"]))
    for p in gest:
        A(f"| L{p['nivel']} | {p['nome']} | {p['cargo']} | {p['diretos']} | "
          f"{p['total']} | {area_de(p, pessoas, filhos)} |")
    A("")
    A("---")
    A("")

    # ---------------- cargos por faixa
    A("## 5. Composição por faixa de cargo")
    A("")
    A("| Faixa | L4 | L5 | L6 | L7 | L8 | Total |")
    A("|---|---|---|---|---|---|---|")
    ordem = ["Head / Manager", "Team Leader", "Executive (comercial)", "Specialist",
             "Analyst", "Assistant", "Intern / Aprendiz", "Cargo em branco"]
    for f in ordem:
        linha = [sum(1 for p in pessoas if p["nivel"] == n and faixa(p["cargo"]) == f)
                 for n in range(4, 9)]
        if sum(linha) == 0:
            continue
        A(f"| {f} | " + " | ".join(str(x) for x in linha) + f" | **{sum(linha)}** |")
    A(f"| **Total** | " + " | ".join(str(por_nivel[n]) for n in range(4, 9))
      + f" | **{len(pessoas)}** |")
    A("")
    A("---")
    A("")

    # ---------------- achados
    A("## 6. O que salta aos olhos")
    A("")
    t_ops = tamanho(filhos, "Raioni De Oliveira Santos")
    A(f"1. **Operações concentra {t_ops / (total - 1) * 100:.0f}% da empresa** — "
      f"{t_ops} das {total - 1} pessoas abaixo do CEO, contra "
      f"{tamanho(filhos, 'Cleyton Cardoso Esteves')} em Tecnologia e "
      f"{tamanho(filhos, 'Ana Carolina Botelho Caldeira Vasconcellos')} em Finanças. "
      "É a única diretoria que desce até o L8.")
    A("2. **Sete níveis do CEO ao analista mais fundo, dentro de Operações Aéreo.** "
      "A cadeia é `CEO → Raioni → Carolina Mendoza → Daniela Craig → Pamela Ibarra → "
      "Thais Mathias → analista (L8)`: seis gestores empilhados sobre uma pessoa. "
      "Três delas (Pamela L6, Gabriella L6, Thais L7) carregam o **mesmo título** — "
      "*Air Freight Operations Team Leader* — e lideram umas às outras, "
      "o que indica que a senioridade real não está refletida no cargo.")
    spans = [p["diretos"] for p in pessoas if p["diretos"] > 0]
    maior = max(pessoas, key=lambda p: p["diretos"])
    media = f"{sum(spans) / len(spans):.1f}".replace(".", ",")
    A(f"3. **Um gestor com {maior['diretos']} liderados diretos:** {maior['nome']} "
      f"(*{maior['cargo']}*) — {maior['total']} no total, contra uma média de "
      f"{media} entre os gestores L4–L7. O cargo dele é *Head of Operation*, mas o time é "
      "todo de tecnologia (Developers, Data, Product Design) e ele reporta ao Cleyton — "
      "o título provavelmente está desatualizado na base.")
    solo = sorted([p for p in pessoas if p["diretos"] == 1], key=lambda x: x["nivel"])
    A(f"4. **{len(solo)} gestores com um único liderado** — "
      + "; ".join(f"{p['nome']} (L{p['nivel']}, {p['cargo'] or 'cargo em branco'})"
                  for p in solo)
      + ". São camadas de gestão que custam um nível inteiro para coordenar uma pessoa.")
    A("5. **Serviços / Diligenciamento (Luis Fernando) não tem nenhuma camada intermediária:** "
      "5 analistas reportando direto ao L3, e nenhum deles lidera ninguém. "
      "É a área que o draft trata na seção *Serviços (Diligenciamento)*.")
    brancos = sorted([p for p in pessoas if not p["cargo"]], key=lambda x: x["nivel"])
    futuros = [p for p in brancos if p["inicio"] > "2026-10-23"]
    A(f"6. **{len(brancos)} cargos em branco na planilha** — todas com data de início entre "
      f"{min(p['inicio'] for p in brancos)} e {max(p['inicio'] for p in brancos)}. "
      f"{len(futuros)} delas têm data de início **no futuro**, ou seja, são admissões "
      "ainda por entrar, e as outras 3 entraram em setembro sem função cadastrada:")
    A("")
    A("| Nível | Nome | Gestor | Início | Local |")
    A("|---|---|---|---|---|")
    for p in sorted([p for p in pessoas if not p["cargo"]], key=lambda x: x["nivel"]):
        A(f"| L{p['nivel']} | {p['nome']} | {p['gestor']} | {p['inicio']} | {p['local']} |")
    A("")
    chefia = ("team leader", "head", "manager", "coordinator")
    titulo_sem_time = [p for p in pessoas
                       if any(k in p["cargo"].lower() for k in chefia) and p["diretos"] == 0]
    time_sem_titulo = [p for p in pessoas
                       if p["diretos"] > 0
                       and not any(k in p["cargo"].lower() for k in chefia)]
    A(f"7. **Título e função não batem em {len(titulo_sem_time) + len(time_sem_titulo)} casos.** "
      f"{len(titulo_sem_time)} pessoas têm título de chefia e **nenhum liderado**: "
      + "; ".join(f"{p['nome']} (L{p['nivel']}, {p['cargo']})" for p in titulo_sem_time)
      + f". Na direção oposta, {len(time_sem_titulo)}: "
      + "; ".join(f"{p['nome']} (L{p['nivel']}, {p['cargo']}, "
                  f"{p['diretos']} liderado)" for p in time_sem_titulo)
      + ". Esse último caso é duplamente estranho: ela é de RH e o único liderado dela "
        "tem cargo de *Air Freight Design Specialist* — provavelmente um reporte "
        "mal cadastrado.")
    A("8. **Produtos aparecem dentro de Operações, não como diretoria.** "
      "*Head of Air Product* (Filipe Teixeira Sampaio, 28 pessoas) e *Head of Ocean Product* "
      "(Filipe Carneiro De Oliveira, 18) reportam ao Raioni. No draft, "
      "`Prod Aéreo | Sampaio` e `Prod Marítimo | Filipe` abrem como blocos próprios — "
      "vale alinhar se é a visão atual ou a visão desejada.")
    A("")
    A("---")
    A("")
    A("## 7. Onde a planilha e o draft divergem")
    A("")
    A("O `Draft 23 Out 26.pptx` tem 75 slides, mas os organogramas estão **como imagem** — "
      "não há texto extraível para comparar nome a nome. O que dá para cruzar são os títulos "
      "de seção e os bilhetes deixados nos slides:")
    A("")
    A("| Seção do draft | Equivalente na planilha | Observação do próprio draft |")
    A("|---|---|---|")
    A("| Produto Aéreo / Produto Marítimo (sl. 2–15) | L4 dentro de Operações | "
      "*\"A estrutura é separada por região — EUA / EUROPA / ÁSIA. Precisamos fazer essa abertura\"* |")
    A("| Indústria (sl. 16–21) | Comercial / Indústrias (André Lemos) | "
      "Aerospace, Energy, Automotivo, Healthcare batem com os 4 *Heads of Industry*; "
      "slide 20 marca **vaga de TL** |")
    A("| Tecnologia (sl. 23–26) | Tecnologia (Cleyton) | "
      "*\"A estrutura foi ajustada recentemente — temos que pegar a visão atualizada\"* |")
    A("| Finanças (sl. 28–34) | Finanças (Ana Carolina) | mesma ressalva de visão desatualizada |")
    A("| RH (sl. 36–40) | Recursos Humanos (Karnakis) | mesma ressalva |")
    A("| Serviços / Diligenciamento (sl. 42) | Luis Fernando (5 analistas) | — |")
    A("| Operações (sl. 45–75) | Operações (Raioni) | mesma ressalva; "
      "inclui Exportação, Customer Care, Marítimo, Aéreo EUA/MIA, "
      "Inteligência e Excelência Operacional, KAM e Capacity |")
    A("")
    A("Quatro das seis diretorias trazem o aviso de que **o organograma do draft está "
      "desatualizado em relação à estrutura real**. A planilha Factorial é a visão mais "
      "recente, e é ela que este documento reconstrói.")
    A("")
    A("---")
    A("")
    A("## Como regerar")
    A("")
    A("```bash")
    A("pip install openpyxl")
    A("python3 estrutura/gerar_hierarquia.py")
    A("```")
    A("")
    A("Gera este arquivo e `estrutura/Hierarquia_DMS.xlsx` "
      "(base indentada navegável, lista de gestores e resumo).")
    return "\n".join(L)


# cache simples para achar a diretoria de cada pessoa
_cache_area = {}


def _mapear_areas(pessoas, filhos):
    if _cache_area:
        return
    for l3, (area, _) in AREAS_L3.items():
        pilha = [p for p in filhos[l3]]
        while pilha:
            p = pilha.pop()
            _cache_area[p["nome"]] = area
            pilha.extend(filhos[p["nome"]])


def area_de(p, pessoas, filhos):
    _mapear_areas(pessoas, filhos)
    return _cache_area.get(p["nome"], "?")


def raiz_de(p, pessoas, filhos, l3):
    _mapear_areas(pessoas, filhos)
    return _cache_area.get(p["nome"]) == AREAS_L3[l3][0]


# ----------------------------------------------------------------- excel
def gerar_xlsx(pessoas, filhos):
    wb = openpyxl.Workbook()
    hdr_fill = PatternFill("solid", fgColor="1B3A5C")
    hdr_font = Font(bold=True, color="FFFFFF")
    cor_nivel = {2: "0D1F31", 3: "1B3A5C", 4: "2E6CA4", 5: "67A3D9",
                 6: "AED2F0", 7: "DFEAF5", 8: "F4F8FC"}
    txt_claro = {2, 3, 4}

    # ---- aba hierarquia indentada
    ws = wb.active
    ws.title = "Hierarquia"
    cols = ["Nível", "Estrutura (indentada)", "Nome completo", "Cargo", "Faixa",
            "Diretos", "Total abaixo", "Gestor direto", "Diretoria", "Local", "Início"]
    ws.append(cols)
    ws.append(["L2", CEO, CEO, "— (não informado na planilha)", "CEO",
               len(AREAS_L3), len(pessoas) + len(AREAS_L3), "", "DMS", "", ""])

    def escrever(nome, nivel):
        for p in filhos[nome]:
            ws.append([
                f"L{p['nivel']}",
                "    " * (p["nivel"] - 2) + p["nome"],
                p["nome"], p["cargo"] or "(em branco)", faixa(p["cargo"]),
                p["diretos"], p["total"], p["gestor"],
                area_de(p, pessoas, filhos), p["local"], p["inicio"],
            ])
            escrever(p["nome"], p["nivel"])

    for l3, (area, _) in sorted(AREAS_L3.items(), key=lambda kv: -tamanho(filhos, kv[0])):
        ws.append(["L3", "    " + l3, l3, "— (não informado na planilha)", "Diretoria",
                   len(filhos[l3]), tamanho(filhos, l3), CEO, area, "", ""])
        escrever(l3, 3)

    # ---- aba gestores
    ws2 = wb.create_sheet("Gestores")
    ws2.append(["Nível", "Nome", "Cargo", "Diretos", "Total abaixo", "Diretoria",
                "Lidera gestores?"])
    ws2.append(["L2", CEO, "—", len(AREAS_L3), len(pessoas) + len(AREAS_L3), "DMS", "Sim"])
    for l3, (area, _) in sorted(AREAS_L3.items(), key=lambda kv: -tamanho(filhos, kv[0])):
        tem = "Sim" if any(x["diretos"] > 0 for x in filhos[l3]) else "Não"
        ws2.append(["L3", l3, "—", len(filhos[l3]), tamanho(filhos, l3), area, tem])
    for p in sorted([x for x in pessoas if x["diretos"] > 0],
                    key=lambda x: (-x["total"], x["nivel"])):
        tem = "Sim" if any(x["diretos"] > 0 for x in filhos[p["nome"]]) else "Não"
        ws2.append([f"L{p['nivel']}", p["nome"], p["cargo"], p["diretos"], p["total"],
                    area_de(p, pessoas, filhos), tem])

    # ---- aba resumo
    ws3 = wb.create_sheet("Resumo")
    ws3.append(["Nível", "Pessoas", "Gestores", "Sem liderados", "Maior time (diretos)"])
    ws3.append(["L2", 1, 1, 0, len(AREAS_L3)])
    ws3.append(["L3", len(AREAS_L3), sum(1 for l in AREAS_L3 if filhos[l]),
                sum(1 for l in AREAS_L3 if not filhos[l]),
                max(len(filhos[l]) for l in AREAS_L3)])
    for n in range(4, 9):
        gr = [p for p in pessoas if p["nivel"] == n]
        g = [p for p in gr if p["diretos"] > 0]
        ws3.append([f"L{n}", len(gr), len(g), len(gr) - len(g),
                    max([p["diretos"] for p in g], default=0)])
    ws3.append([])
    ws3.append(["Diretoria", "Responsável (L3)", "Diretos", "Pessoas na área", "% empresa"])
    tot = len(pessoas) + len(AREAS_L3)
    for l3, (area, _) in sorted(AREAS_L3.items(), key=lambda kv: -tamanho(filhos, kv[0])):
        t = tamanho(filhos, l3)
        ws3.append([area, l3, len(filhos[l3]), t, round(t / tot * 100, 1)])
    ws3.append([])
    ws3.append(["Faixa de cargo", "Pessoas"])
    for f, n in Counter(faixa(p["cargo"]) for p in pessoas).most_common():
        ws3.append([f, n])

    # ---- formatacao
    for sheet in wb.worksheets:
        for c in sheet[1]:
            c.fill, c.font = hdr_fill, hdr_font
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = f"A1:{get_column_letter(sheet.max_column)}1"
        larguras = {}
        for row in sheet.iter_rows():
            for c in row:
                if c.value is not None:
                    larguras[c.column] = min(60, max(larguras.get(c.column, 9),
                                                     len(str(c.value)) + 2))
        for col, w in larguras.items():
            sheet.column_dimensions[get_column_letter(col)].width = w

    for row in ws.iter_rows(min_row=2):
        n = int(str(row[0].value)[1:])
        f = PatternFill("solid", fgColor=cor_nivel[n])
        row[0].fill = f
        row[0].font = Font(bold=True, color="FFFFFF" if n in txt_claro else "06243D")
        row[0].alignment = Alignment(horizontal="center")
        if n <= 4:
            row[1].font = Font(bold=True)
    for row in ws2.iter_rows(min_row=2):
        n = int(str(row[0].value)[1:])
        row[0].fill = PatternFill("solid", fgColor=cor_nivel[n])
        row[0].font = Font(bold=True, color="FFFFFF" if n in txt_claro else "06243D")
        row[0].alignment = Alignment(horizontal="center")

    destino = os.path.join(SAIDA, "Hierarquia_DMS.xlsx")
    wb.save(destino)
    return destino


def main():
    os.makedirs(SAIDA, exist_ok=True)
    pessoas = carregar()
    filhos = montar(pessoas)
    _mapear_areas(pessoas, filhos)

    md = gerar_md(pessoas, filhos)
    cam_md = os.path.join(SAIDA, "Hierarquia_Gestao_DMS.md")
    with open(cam_md, "w", encoding="utf-8") as fh:
        fh.write(md + "\n")
    cam_xl = gerar_xlsx(pessoas, filhos)

    print(f"{len(pessoas)} pessoas lidas (L4-L8) + {len(AREAS_L3)} L3 + 1 L2 "
          f"= {len(pessoas)+len(AREAS_L3)+1}")
    print("gestores:", sum(1 for p in pessoas if p["diretos"] > 0) + len(AREAS_L3) + 1)
    print("ok ->", cam_md)
    print("ok ->", cam_xl)


if __name__ == "__main__":
    main()
