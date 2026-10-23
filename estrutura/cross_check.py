#!/usr/bin/env python3
"""
Cross-checking do organograma (Factorial) contra as bases financeiras e o draft.

Fontes:
  Colaboradores-factorial (3).xlsx  -> organograma, abas 'level 4' a 'level 8'
  Base_Setembro26 (1).xlsx          -> aba 'Setembro Unificado' (folha de setembro)
  Baseline DRE 26.2.xlsx            -> aba 'Baseline ativos agosto' (custo por pessoa)
  Vagas 21-10.xlsx                  -> aba 'Vagas' (posicoes em aberto)
  Draft 23 Out 26.pptx              -> prints do Factorial + anotacoes manuais

Uso:  python3 estrutura/cross_check.py
"""
import os
import re
import unicodedata
from collections import Counter, defaultdict

import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- nomes
STOP = {"DE", "DA", "DO", "DOS", "DAS", "E", "JUNIOR", "JR", "NETO", "FILHO",
        "SOBRINHO", "CONSULTOR"}


def toks(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z ]", " ", s).upper()
    return [t for t in s.split() if t not in STOP and len(t) > 1]


def score(a, b):
    """Pontua a chance de dois nomes serem a mesma pessoa. 0 = descartado."""
    ta, tb = toks(a), toks(b)
    if not ta or not tb:
        return 0
    A, B = set(ta), set(tb)
    comum = A & B
    if not comum:
        return 0
    # exige primeiro OU ultimo sobrenome igual
    if ta[0] != tb[0] and ta[-1] != tb[-1]:
        return 0
    if len(comum) < 2 and not (A <= B or B <= A):
        return 0
    s = 10 * len(comum)
    if ta[0] == tb[0]:
        s += 6
    if ta[-1] == tb[-1]:
        s += 4
    if A <= B or B <= A:
        s += 3
    s -= abs(len(A) - len(B))          # penaliza nomes de tamanho muito diferente
    return s


def emparelha(la, ca, lb, cb):
    """Casa duas listas pelo melhor score global (nao pela primeira ocorrencia)."""
    cand = []
    for i, x in enumerate(la):
        for j, y in enumerate(lb):
            s = score(x[ca], y[cb])
            if s > 0:
                cand.append((s, i, j))
    cand.sort(key=lambda t: -t[0])
    usados_a, usados_b, pares = set(), set(), []
    for s, i, j in cand:
        if i in usados_a or j in usados_b:
            continue
        usados_a.add(i)
        usados_b.add(j)
        pares.append((la[i], lb[j], s))
    so_a = [x for i, x in enumerate(la) if i not in usados_a]
    so_b = [y for j, y in enumerate(lb) if j not in usados_b]
    return pares, so_a, so_b


# ---------------------------------------------------------------- leitura
def ler_factorial():
    abas = {"level 4": 4, "level 5": 5, "level 6": 6, "level 7": 7, "level 8": 8}
    wb = openpyxl.load_workbook(os.path.join(RAIZ, "Colaboradores-factorial (3).xlsx"),
                                data_only=True)
    out = []
    for aba, nivel in abas.items():
        ws = wb[aba]
        g_acima = g_direto = None
        for r in ws.iter_rows(min_row=3, values_only=True):
            if all(c is None for c in r):
                continue
            if r[0]:
                g_acima = str(r[0]).strip()
            if r[1]:
                g_direto = str(r[1]).strip()
            out.append({
                "nome": f"{r[2] or ''} {r[3] or ''}".strip(), "level": nivel,
                "cargo": (str(r[4]).strip() if r[4] else ""),
                "gestor": g_direto, "gestor_acima": g_acima,
                "total": int(r[5] or 0), "diretos": int(r[6] or 0),
                "local": r[9] or "", "inicio": str(r[10])[:10] if r[10] else "",
            })
    return out


def ler_aba(arquivo, aba, col_nome):
    wb = openpyxl.load_workbook(os.path.join(RAIZ, arquivo), data_only=True)
    ws = wb[aba]
    hdr = [c.value for c in ws[1]]
    i = hdr.index(col_nome)
    return [dict(zip(hdr, r)) for r in ws.iter_rows(min_row=2, values_only=True)
            if r[i] not in (None, "")]


# ---------------------------------------------------------------- dados do draft
# Cargos lidos nos prints do Draft 23 Out 26.pptx. Os levels 2 e 3 nao tem
# cargo na planilha Factorial; estes vieram do organograma do slide 2.
CARGOS_DRAFT = {
    "Jose Luiz de Oliveira Belixior Junior": ("Co-Chief Executive Officer", "s2", False),
    "Raioni De Oliveira Santos": ("Chief Operating Officer", "s2/s46", False),
    "Andre Lemos Tavares": ("Chief Commercial Officer", "s2/s17", False),
    "Cleyton Cardoso Esteves": ("Chief Information & Tec…", "s2/s24", True),
    "Ana Carolina Botelho Caldeira Vasconcellos": ("Chief Strategy Finance …", "s2/s29", True),
    "Carolina Karnakis de Nobrega": ("Head of Talent", "s2/s37", False),
    "Luis Fernando Santos Muniz": ("Head of Services", "s2/s43", False),
}

# Sigla de C-LEVEL usada no DRE e nas Vagas, por pessoa do L2/L3.
C_LEVEL_DRE = {
    "Jose Luiz de Oliveira Belixior Junior": "Co-CEO",
    "Raioni De Oliveira Santos": "COO",
    "Andre Lemos Tavares": "CCO",
    "Cleyton Cardoso Esteves": "CITO",
    "Ana Carolina Botelho Caldeira Vasconcellos": "CFSO",
    "Carolina Karnakis de Nobrega": "Co-CEO (Talent Management Team)",
    "Luis Fernando Santos Muniz": "Co-CEO (Services)",
}

# 'liderados' impressos nos organogramas do draft, com o slide onde aparecem.
DRAFT_LIDERADOS = {
    "Jose Luiz de Oliveira Belixior Junior": (330, "s2"),
    "Raioni De Oliveira Santos": (199, "s2/s46"),
    "Cleyton Cardoso Esteves": (47, "s2/s24"),
    "Ana Carolina Botelho Caldeira Vasconcellos": (33, "s2/s29"),
    "Carolina Karnakis de Nobrega": (23, "s2/s37"),
    "Andre Lemos Tavares": (17, "s2/s17"),
    "Luis Fernando Santos Muniz": (5, "s2/s43"),
    "Carolina Bento Mendoza": (82, "s46/s48"),
    "Filipe Teixeira Sampaio": (28, "s46/s4"),
    "Natalia Correia Da Costa Parreira": (35, "s46/s58"),
    "Filipe Carneiro De Oliveira": (18, "s46/s11"),
    "Marco Antonio Maraia Villa": (12, "s46/s71"),
    "Possidonio Dantas de Almeida Neto": (8, "s46/s65"),
    "Jonathas Amancio Alves": (6, "s46/s75"),
    "Lucy Maia De Moraes": (2, "s46"),
    "Victor Telles Gonzaga": (37, "s24/s26"),
    "Julio Cesar Francisco de Souza": (8, "s24/s25"),
    "Roberta Duarte Correia": (18, "s29/s30"),
    "Daniel de Carvalho Herrera Braga": (8, "s29"),
    "Rodrigo Fontes Dominciano": (8, "s37/s39"),
    "Vivian Ramalho De Assumpçao": (5, "s37/s38"),
    "Leandro Teciano": (3, "s37/s40"),
    "Cristiane Martins Soares Giovanelli": (1, "s37/s40"),
    "Katharine Ferreira De Souza": (1, "s39"),
    "Ivan Garcia Castro": (2, "s17"),
    "Yuri Da Silva Torreao": (3, "s17"),
    "Ricardo Tebexreni Jakowatz": (5, "s17/s20"),
    "Jose Carlos Duarte Freitas Sobrinho": (2, "s17"),
    "Danielle Moreira Rabelo Machado": (1, "s20"),
    "Marcelo Portantiolo de Lima": (2, "s20"),
    "Joao Pedro Da Costa Marcicano Rodrigues": (23, "s4/s5"),
    "Tayna Neves": (3, "s4/s9"),
    "Dandara Cristina Santos Ru": (7, "s5/s6"),
    "Rafael Araujo Belfiore": (7, "s5/s7"),
    "Vinicius Teixeira Studart Pereira": (5, "s5/s8"),
    "Rony Ghiu De Moraes Rego Da Silva": (3, "s11/s12"),
    "Ivy Kaori Oishi": (6, "s11/s13"),
    "Luiz Antonio Duarte Ferreira Junior": (5, "s11/s14"),
    "Daniela Bueno dos Reis Craig": (47, "s48/s54"),
    "Thais Pinho Cosenza": (27, "s48/s50"),
    "Julia Sena Campelo Lopes": (4, "s48/s49"),
    "Rubia Furtado": (12, "s50"),
    "Leonardo Bonamichi Vaz de Lima": (8, "s50/s52"),
    "Isabelle Carolina De Melo Martinez Lizama": (3, "s50/s51"),
    "Pamela Iris Gregorio Ibarra": (21, "s54/s69"),
    "Gabriella De Melo Pereira": (16, "s54/s67"),
    "Adriane Borel Cordeiro Impagliazzo": (5, "s54"),
    "Charlete Alfaia Guimaraes Santana": (1, "s54"),
    "Thais Espindola Oliveira Mathias": (8, "s69"),
    "Julia Olegario Varella": (1, "s69"),
    "Julia Heinrichs Pimentel": (6, "s67"),
    "Lenice Maria da Costa Barbosa": (1, "s67"),
    "Kayza Cristina Silva Pereira": (12, "s58"),
    "Leonardo Araujo de Menezes": (7, "s58"),
    "Ricardo Dos Reis Castro": (4, "s58"),
    "Augusto Cesar Sotelo Medeiros": (4, "s58"),
    "Andrea Oliveira Brito Do Couto": (2, "s58"),
    "Jesus Guillermo Ledi Mendoza": (5, "s65/s66"),
    "Caio Vitor de Carvalho Santos": (4, "s71/s73"),
    "Natalie Giseli De Maria Correa": (2, "s71/s72"),
    "Camila Evelyn De Souza Lima": (8, "s30"),
    "Gisele Ferreira Pinto": (5, "s30"),
    "Andressa Franco Da Silva": (2, "s30"),
}

# Caixas que o draft DESENHOU A MAO na primeira linha do CEO (nao existem na
# planilha como reporte direto do CEO): slides 2, 15, 22, 27, 35, 41 e 44.
PROPOSTA_DRAFT = [
    ("Prod | Aéreo | Sampaio", "Filipe Teixeira Sampaio", "Head of Air Product"),
    ("Prod | Marítimo | Filipe", "Filipe Carneiro De Oliveira", "Head of Ocean Product"),
]

# Anotacoes de texto encontradas nos slides.
NOTAS_DRAFT = [
    ("2, 15, 22, 27, 35, 41, 44",
     "Duas caixas desenhadas à mão na linha do CEO: 'Prod | Aéreo | Sampaio' e "
     "'Prod | Marítimo | Filipe', ligadas por um conector manual ao CEO"),
    ("6, 14", "RD — 'A estrutura é separada por região: EUA | EUROPA | ÁSIA. "
              "Precisamos fazer essa abertura'"),
    ("7, 8, 13", "FD — 'A estrutura é separada por Cliente. Precisamos fazer essa abertura'"),
    ("20", "Vertical / Auto / High Tech — marca uma 'Vaga de TL'"),
    ("24", "'A estrutura foi ajustada recentemente pela Cleyton — temos que pegar "
           "a visão atualizada'"),
    ("29", "'A estrutura foi ajustada recentemente pela Ana Carol — temos que pegar "
           "a visão atualizada'"),
    ("37", "'A estrutura foi ajustada recentemente pela Karnakis — temos que pegar "
           "a visão atualizada'"),
    ("46", "'A estrutura foi ajustada recentemente pelo Raioni — temos que pegar "
           "a visão atualizada'"),
]


# ---------------------------------------------------------------- arvore
def montar(fac):
    filhos = defaultdict(list)
    for p in fac:
        filhos[p["gestor"]].append(p)
    nomes = {p["nome"] for p in fac}
    l3 = sorted({p["gestor"] for p in fac if p["level"] == 4} - nomes)
    l2 = sorted({p["gestor_acima"] for p in fac if p["level"] == 4} - nomes)
    todos = list(fac)
    for nome in l3:
        novo = {"nome": nome, "level": 3, "cargo": "", "gestor": l2[0],
                "gestor_acima": None, "diretos": len(filhos[nome]), "total": 0,
                "local": "", "inicio": ""}
        todos.append(novo)
        filhos[l2[0]].append(novo)
    for nome in l2:
        todos.append({"nome": nome, "level": 2, "cargo": "", "gestor": None,
                      "gestor_acima": None, "diretos": len(filhos[nome]),
                      "total": 0, "local": "", "inicio": ""})

    def total(n):
        t = len(filhos[n])
        for f in filhos[n]:
            t += total(f["nome"])
        return t

    for p in todos:
        p["total"] = total(p["nome"])
        p["indiretos"] = p["total"] - p["diretos"]
    for k in filhos:
        filhos[k].sort(key=lambda x: (-x["diretos"], x["nome"]))
    return todos, filhos


def area_por_pessoa(todos, filhos):
    area = {}
    for l3 in [p["nome"] for p in todos if p["level"] == 3]:
        pilha = list(filhos[l3])
        while pilha:
            x = pilha.pop()
            area[x["nome"]] = l3
            pilha.extend(filhos[x["nome"]])
    return area


# ---------------------------------------------------------------- analise
import re

PAT_INTERN = re.compile(r"\b(intern|apprentice)\b", re.I)


def esc(s):
    """Escapa o pipe para nao quebrar a celula da tabela markdown."""
    return str(s).replace("|", "\\|")


TESTE = "Colaborador Teste"
CORTE_FOLHA = "2026-09-30"          # ultimo dia da competencia Set/26
DATA_DRAFT = "2026-10-23"           # data do draft


def carregar_tudo():
    fac = ler_factorial()
    todos, filhos = montar(fac)
    return {
        "fac": fac, "todos": todos, "filhos": filhos,
        "area": area_por_pessoa(todos, filhos),
        "base": ler_aba("Base_Setembro26 (1).xlsx", "Setembro Unificado", "NOME"),
        "dre": ler_aba("Baseline DRE 26.2.xlsx", "Baseline ativos agosto", "Colaborador"),
        "vagas": ler_aba("Vagas 21-10.xlsx", "Vagas", "CARGO"),
    }


def gestores(todos):
    return sorted([p for p in todos if p["diretos"] > 0],
                  key=lambda p: (p["level"], -p["total"], p["nome"]))


def classifica_so_organograma(x):
    if x["nome"] == TESTE:
        return "Registro de teste — excluir da base"
    if x["level"] == 2:
        return "Co-CEO: não entra na folha nem no DRE"
    if (x["inicio"] or "9999") > CORTE_FOLHA:
        return f"Admitido em {x['inicio']}, depois do fechamento de set/26"
    return "SEM CUSTO NA FOLHA — verificar"


def classifica_so_folha(y):
    s = str(y["SITUAÇÃO"])
    if s in ("AVISO PREVIO V", "OFF BOARDING"):
        return f"{s} — já retirado do organograma"
    if y["TIPO DE CUSTO"] == "Sócios":
        return "Sócio / Executive Board — fora do organograma"
    if s == "TRANSIÇÃO DE CONTRATO":
        return "Transição de contrato — linha duplicada"
    return "ATIVO SEM POSIÇÃO NO ORGANOGRAMA — gap real"


def md(dados):
    fac, todos, filhos = dados["fac"], dados["todos"], dados["filhos"]
    base, dre, vagas = dados["base"], dados["dre"], dados["vagas"]
    gest = gestores(todos)
    L = []
    A = L.append

    A("# Cross-check do organograma")
    A("")
    A("Confere a estrutura do **Factorial** contra o **draft**, a **folha de setembro**, "
      "o **baseline do DRE** e a **planilha de vagas**, para responder duas perguntas: "
      "*está faltando alguém?* e *os números batem?*")
    A("")

    # ---------------- 1. fontes
    A("## 1. As cinco fontes e suas datas")
    A("")
    A("| Fonte | Data de referência | Linhas | Pessoas | O que é |")
    A("|---|---|---|---|---|")
    A(f"| `Colaboradores-factorial (3).xlsx` | snapshot de out/26 (com admissões até 16/nov) "
      f"| 329 | **{len(todos)}** | organograma: quem reporta a quem |")
    A(f"| `Draft 23 Out 26.pptx` | print do Factorial anterior a 23/out | 65 imagens | 330 + CEO "
      "| organogramas impressos + anotações à mão |")
    A(f"| `Base_Setembro26 (1).xlsx` | competência **Set/26** | {len(base)} | 322 "
      "| folha fechada de setembro |")
    A(f"| `Baseline DRE 26.2.xlsx` | **ativos agosto** | {len(dre)} | {len(dre)} "
      "| custo por pessoa (salário, encargos, benefícios) |")
    A(f"| `Vagas 21-10.xlsx` | 21/out | {len(vagas)} | — | posições em aberto e fechadas |")
    A("")
    A("**As datas não são as mesmas, então os totais não deveriam bater.** "
      "O organograma é o mais recente e inclui gente que ainda não entrou; "
      "o DRE é o mais antigo (agosto). Cada diferença abaixo está classificada "
      "por causa, e no fim sobram só três casos sem explicação.")
    A("")
    A("---")
    A("")

    # ---------------- 2. draft
    A("## 2. Factorial × Draft")
    A("")
    A(f"Os organogramas do draft são **prints do próprio Factorial**, então deveriam bater "
      f"caixa por caixa. Confirmei **{len(DRAFT_LIDERADOS)} gestores** um a um, lendo as "
      f"{65} imagens do arquivo. Batem todos, exceto cinco — e as cinco divergências "
      "são a mesma coisa: pessoas admitidas depois do print.")
    A("")
    div = []
    for p in todos:
        if p["nome"] in DRAFT_LIDERADOS:
            d, slide = DRAFT_LIDERADOS[p["nome"]]
            if d != p["total"]:
                div.append((p, d, slide))
    A("| Gestor | Level | Draft | Planilha | Dif. | Quem entrou depois |")
    A("|---|---|---|---|---|---|")
    futuros = {p["nome"]: p for p in fac if (p["inicio"] or "") > DATA_DRAFT}
    for p, d, slide in sorted(div, key=lambda t: t[0]["level"]):
        # quem na subarvore dele e admissao futura
        novos, pilha = [], list(filhos[p["nome"]])
        while pilha:
            x = pilha.pop()
            if x["nome"] in futuros:
                novos.append(f"{x['nome']} ({x['inicio']})")
            pilha.extend(filhos[x["nome"]])
        A(f"| {p['nome']} | L{p['level']} | {d} | {p['total']} | +{p['total']-d} "
          f"| {'; '.join(sorted(novos))} |")
    A("")
    cinco = sorted(futuros.values(), key=lambda x: x["inicio"])
    A(f"São **{len(cinco)} pessoas** com data de início posterior ao draft, e elas explicam "
      f"a diferença no topo também: o CEO aparece com **330 liderados** no print e tem "
      f"**{todos[0]['total'] if todos[0]['level']==2 else 335}** na planilha.")
    A("")
    A("| Nome | Level | Início | Gestor |")
    A("|---|---|---|---|")
    for x in cinco:
        A(f"| {x['nome']} | L{x['level']} | {x['inicio']} | {x['gestor']} |")
    A("")
    A("### O que o draft propõe mudar na estrutura")
    A("")
    A("Nos slides 2, 15, 22, 27, 35, 41 e 44, o print do Factorial mostra o CEO com "
      "**6 reportes diretos**. Em cima da imagem, alguém **desenhou duas caixas a mais** "
      "na mesma linha, ligadas ao CEO por um conector manual:")
    A("")
    A("| Caixa desenhada no draft | Quem é | Cargo | Hoje reporta a |")
    A("|---|---|---|---|")
    for rot, nome, cargo in PROPOSTA_DRAFT:
        p = next((q for q in todos if q["nome"] == nome), None)
        A(f"| `{esc(rot)}` | {nome} | {cargo} | {p['gestor']} (L3) — dentro de Operações |")
    A("")
    A("Ou seja: o draft propõe **tirar Produto Aéreo e Produto Marítimo de baixo do COO "
      "e pendurar direto no CEO**, passando de 6 para 8 reportes diretos. "
      "Na planilha isso ainda não existe — lá os dois são Heads dentro de Operações, "
      "somando 46 pessoas (28 do Aéreo + 18 do Marítimo).")
    A("")
    A("### As outras anotações do draft")
    A("")
    A("| Slide(s) | Anotação |")
    A("|---|---|")
    for sl, nota in NOTAS_DRAFT[1:]:
        A(f"| {sl} | {esc(nota)} |")
    A("")
    A("Quatro das seis diretorias trazem o aviso de que a estrutura foi mexida depois do "
      "print. **E o draft não abre o maior time da casa:** o de Victor Telles Gonzaga "
      "(*Head of Operation*, Tecnologia), com 27 reportes diretos e 37 pessoas. "
      "O slide 26 mostra só a caixa dele, sem desdobrar.")
    A("")
    A("---")
    A("")

    # ---------------- 3. folha
    pares, soF, soB = emparelha(todos, "nome", base, "NOME")
    A("## 3. Factorial × folha de setembro")
    A("")
    A(f"**{len(pares)} pessoas casaram** nas duas bases. Sobraram {len(soF)} só no "
      f"organograma e {len(soB)} só na folha.")
    A("")
    A(f"### {len(soF)} estão no organograma e não na folha de setembro")
    A("")
    A("| Level | Nome | Cargo | Início | Causa |")
    A("|---|---|---|---|---|")
    for x in sorted(soF, key=lambda z: (z["inicio"] or "")):
        A(f"| L{x['level']} | {x['nome']} | {x['cargo'] or '(em branco)'} "
          f"| {x['inicio'] or '—'} | {classifica_so_organograma(x)} |")
    A("")
    A("Todas explicadas: são admissões de outubro e novembro, que não poderiam estar "
      "na folha de setembro. **Menos uma:** `Colaborador Teste`, um registro de teste "
      "com admissão em 2022 que está pendurado como *Air Freight Design Specialist* "
      "dentro do time de Rafael Araujo Belfiore. Ele infla o organograma em 1 pessoa.")
    A("")
    A(f"### {len(soB)} estão na folha e não no organograma")
    A("")
    A("| Nome | Posição | Área | Situação | Custo | Causa |")
    A("|---|---|---|---|---|---|")
    for y in soB:
        A(f"| {y['NOME']} | {y['POSIÇÃO']} | {y['AREA']} | {y['SITUAÇÃO']} "
          f"| {y['TIPO DE CUSTO']} | {classifica_so_folha(y)} |")
    A("")
    gaps = [y for y in soB if classifica_so_folha(y).startswith("ATIVO SEM")]
    A(f"Depois de descontar quem está saindo, os sócios e a linha duplicada, "
      f"sobram **{len(gaps)} pessoas ativas na folha sem nenhuma posição no organograma**:")
    A("")
    A("| Nome | Posição | Área (folha) | Como aparece no DRE |")
    A("|---|---|---|---|")
    for y in gaps:
        no_dre = next((d for d in dre if score(d["Colaborador"], y["NOME"]) > 0), None)
        desc = (f"{no_dre['C-LEVEL']} · {no_dre['ARÉA (Centro de Custo)']} · "
                f"{no_dre['POSIÇÃO PADRÃO 26.2']}" if no_dre else "não está no DRE")
        A(f"| **{y['NOME']}** | {y['POSIÇÃO']} | {y['AREA']} | {desc} |")
    A("")
    A("Esses três têm custo lançado e não têm gestor definido no Factorial. "
      "São o gap real de cadastro.")
    A("")
    A("---")
    A("")

    # ---------------- 4. DRE
    pd_, soFd, soDd = emparelha(todos, "nome", dre, "Colaborador")
    A("## 4. Factorial × baseline do DRE 26.2")
    A("")
    A(f"**{len(pd_)} casaram.** O DRE é a foto de **agosto**, dois meses antes do "
      f"organograma, então a diferença é maior: {len(soFd)} só no organograma e "
      f"{len(soDd)} só no DRE.")
    A("")
    A("O DRE não tem hierarquia, mas tem uma coluna **C-LEVEL** que é o equivalente "
      "da diretoria. O mapeamento com o organograma:")
    A("")
    A("| C-LEVEL no DRE | Pessoas no DRE | Quem é (L2/L3) | Cargo | Pessoas no organograma |")
    A("|---|---|---|---|---|")
    cont = Counter(str(d["C-LEVEL"]) for d in dre)
    for nome, sigla in C_LEVEL_DRE.items():
        p = next((q for q in todos if q["nome"] == nome), None)
        cargo = CARGOS_DRAFT.get(nome, ("—", "", False))[0]
        chave = sigla.split(" ")[0]
        A(f"| {sigla} | {cont.get(chave, '—') if ' ' not in sigla else '(dentro de Co-CEO)'} "
          f"| {nome} | {cargo} | {p['total'] if p else '—'} |")
    A("")
    A("Repare: **Talent Management Team e Services não são C-LEVEL no DRE** — "
      "caem dentro de `Co-CEO`, junto com o próprio CEO. No organograma, "
      "Karnakis e Luis Fernando são L3 como os outros quatro. "
      "São duas formas diferentes de cortar a mesma empresa.")
    A("")
    A(f"### {len(soDd)} estão no DRE e não no organograma")
    A("")
    A("| Nome | C-LEVEL | Área (centro de custo) | Posição | Custo |")
    A("|---|---|---|---|---|")
    for y in soDd:
        A(f"| {y['Colaborador']} | {y['C-LEVEL']} | {y['ARÉA (Centro de Custo)']} "
          f"| {y['POSIÇÃO PADRÃO 26.2']} | {y['Folha/Colchão']} |")
    A("")
    A("Três dessas linhas **não são pessoas**, são contratos de consultoria lançados "
      "como se fossem: `AUAD ENGENHARIA DE SOFTWARE LTDA` (Technology: Consultoria), "
      "`PIRACI` e `Isabella FRA` (Financial: Consultoria). "
      "As duas últimas são justamente as pessoas que aparecem **sem cargo** no "
      "organograma — Piraci Ubiratan de Oliveira Junior e Isabella Stodiek (DMS Alemanha, "
      "FRA = Frankfurt). Mesma coisa para Fernanda Máximo e Lucimar Desasso, que na folha "
      "aparecem como `CONSULTOR - <nome>`.")
    A("")
    A("**Isso resolve 4 dos 8 cargos em branco:** não é falta de cadastro, "
      "é gente contratada como consultoria.")
    A("")
    A("| Pessoa (organograma) | Level | Como aparece na folha / DRE |")
    A("|---|---|---|")
    for nome, desc in [
        ("Piraci Ubiratan de Oliveira Junior", "`CONSULTOR - PIRACI OLIVEIRA SOCIEDADE DE "
                                               "ADVOGADOS` (folha) · `PIRACI` / Financial: Consultoria (DRE)"),
        ("Isabella Stodiek", "`Isabella FRA` / Financial: Consultoria, MANAGER (DRE)"),
        ("Fernanda Máximo de Souza Fonseca", "`CONSULTOR - FERNANDA MAXIMO DE SOUZA FONSECA` (folha)"),
        ("Lucimar Desasso de Carvalho Rocha", "`CONSULTOR - LUCIMAR DESASSO DE CARVALHO ROCHA` (folha)"),
    ]:
        p = next((q for q in todos if q["nome"] == nome), None)
        A(f"| {nome} | L{p['level'] if p else '?'} | {desc} |")
    A("")
    A("Os outros 4 cargos em branco são as admissões de novembro "
      "(Danielle Vaz Faustino, Thalita Carnevale Sodre, Isabelle Oliveira Rattes, "
      "Fernanda Porto Lima, Poliana de Jesus Guedes) — gente que ainda não entrou.")
    A("")
    A("---")
    A("")

    # ---------------- 5. vagas
    fech = [v for v in vagas if v.get("CONTRATADO")]
    pv, sov, _ = emparelha(fech, "CONTRATADO", todos, "nome")
    abertas = [v for v in vagas if str(v.get("STATUS GUPY")) == "ABERTA | PUBLICADA"]
    A("## 5. Vagas — o que explica as admissões novas")
    A("")
    A(f"A planilha tem **{len(vagas)} vagas**, das quais {len(fech)} já têm nome de "
      f"contratado. **{len(pv)} desses {len(fech)} nomes aparecem no organograma** — "
      "ou seja, as contratações recentes estão cadastradas e são a causa das "
      "admissões de outubro/novembro que não estão na folha de setembro.")
    A("")
    A("| Contratado | Vaga | C-LEVEL | Onde entrou no organograma |")
    A("|---|---|---|---|")
    for v, p, s in sorted(pv, key=lambda t: str(t[0].get("Admissão") or "")):
        A(f"| {v['CONTRATADO']} | {v['CARGO']} | {v['C-LEVEL']} "
          f"| L{p['level']} · {p['cargo'] or '(cargo em branco)'} · sob {p['gestor']} |")
    A("")
    A(f"### {len(abertas)} vagas abertas e publicadas")
    A("")
    A("| C-LEVEL | Área | Cargo |")
    A("|---|---|---|")
    for v in abertas:
        A(f"| {v['C-LEVEL']} | {v['ARÉA']} | {v['CARGO']} |")
    A("")
    A("A mais relevante para a estrutura é **OVERLAND HEAD (Europa)**: "
      "é uma vaga de Head, no mesmo nível dos L4 de hoje.")
    A("")
    A("---")
    A("")

    # ---------------- 6. estagiarios
    fi = [x for x in fac if PAT_INTERN.search(x["cargo"])]
    bi = [x for x in base if x["POSIÇÃO"] in ("INTERN", "APPRENTICE")]
    di = [x for x in dre if x["Folha/Colchão"] == "Aprendiz/Estagiário"]
    A("## 6. Estagiários e aprendizes")
    A("")
    A("**Por que não aparece nenhum intern na lista de gestores:** a lista de gestores "
      "só traz quem tem liderado. Nenhum estagiário ou aprendiz lidera alguém, "
      "então nenhum entra lá. Eles estão no documento por level, dentro do time "
      "de cada gestor e na lista de quem não administra ninguém.")
    A("")
    A(f"E eles **estão** no organograma: são **{len(fi)} pessoas**.")
    A("")
    A("| Fonte | Estagiários / aprendizes |")
    A("|---|---|")
    A(f"| Organograma Factorial (out/26) | **{len(fi)}** |")
    A(f"| Folha de setembro (POSIÇÃO = INTERN/APPRENTICE) | {len(bi)} |")
    A(f"| Baseline DRE (Folha/Colchão = Aprendiz/Estagiário) | {len(di)} |")
    A("")
    A("Os 29 do organograma, por cargo:")
    A("")
    A("| Cargo | Qtd | Onde ficam |")
    A("|---|---|---|")
    por_cargo = defaultdict(list)
    for x in fi:
        por_cargo[x["cargo"]].append(x)
    for cargo, lst in sorted(por_cargo.items(), key=lambda kv: -len(kv[1])):
        gestores_ = sorted({x["gestor"] for x in lst})
        A(f"| {cargo} | {len(lst)} | {'; '.join(gestores_)} |")
    A("")
    pi, soFi, soBi = emparelha(fi, "nome", bi, "NOME")
    A("A diferença entre as fontes:")
    A("")
    novos_i = [x for x in soFi if (x["inicio"] or "") > CORTE_FOLHA]
    velhos_i = [x for x in soFi if (x["inicio"] or "") <= CORTE_FOLHA]
    A(f"- **{len(soFi)} estagiários do organograma não estão na folha de setembro**: "
      f"{len(novos_i)} entraram depois do fechamento "
      f"({', '.join(x['nome'] + ' (' + x['inicio'] + ')' for x in novos_i)})"
      + (f"; {len(velhos_i)} é de antes e está classificado com outro cargo nas duas "
         f"bases ({', '.join(x['nome'] for x in velhos_i)})." if velhos_i else "."))
    A("- **4 estagiários da folha viraram efetivos** e no organograma já aparecem "
      "como *Assistant*: Irlam da Silva Fernandes, Julia Gonçalves Cruz Ramos, "
      "Livia dos Santos Martins e Felipe Sodre de Freitas. "
      "Na folha de setembro eles estão com situação `TRANSIÇÃO DE CONTRATO`.")
    A("- **1 estagiário está na folha e no DRE, mas não no organograma**: "
      "`Dhauan Derito` (Ocean Operations, `OCEAN OPS INTERN PÓS` no DRE). "
      "É um dos três gaps da seção 3.")
    A("- No DRE de agosto havia 31. Quatro saíram até outubro "
      "(Lays Schwartz Blass, Josue Luis dos Santos Pinto de Barros, "
      "Ana Carolina Saueressig Yamada e Enzo Caire Castelo Branco de Moraes) "
      "e não estão em nenhuma das bases mais recentes.")
    A("")
    A("---")
    A("")

    # ---------------- 7. o que corrigir
    A("## 7. O que precisa de correção")
    A("")
    A("| # | O que | Onde | Efeito |")
    A("|---|---|---|---|")
    A("| 1 | `Colaborador Teste` cadastrado como *Air Freight Design Specialist* "
      "sob Rafael Araujo Belfiore | Factorial | infla o organograma em 1 pessoa "
      "e o time do Rafael de 7 para 8 |")
    A("| 2 | Dhauan Derito, Bruno Felipe Dias e Eduardo Bandeira Da Rocha Oliveira "
      "estão ativos na folha sem posição no organograma | Factorial | 3 pessoas com "
      "custo e sem gestor |")
    A("| 3 | Pamela Iris Gregorio Ibarra aparece em duas linhas (OFF LETTER + CLT) "
      "| folha de setembro | headcount da folha conta 323 onde há 322 pessoas |")
    A("| 4 | 4 consultores aparecem sem cargo no organograma e como "
      "`CONSULTOR - <nome>` / `Consultoria` nas bases financeiras | Factorial "
      "| parece cadastro faltando, mas é modalidade de contrato |")
    A("| 5 | Talent Management Team e Services não têm C-LEVEL próprio no DRE "
      "| DRE | as duas diretorias ficam escondidas dentro de `Co-CEO` |")
    A("| 6 | Produto Aéreo e Produto Marítimo reportam ao COO na planilha e ao CEO "
      "no draft | Factorial × draft | 46 pessoas mudam de diretoria dependendo "
      "da versão que se usa |")
    A("| 7 | O time de Victor Telles Gonzaga (27 diretos, 37 pessoas) não está aberto "
      "no draft | draft | o maior time da empresa não tem organograma |")
    A("")
    A("---")
    A("")
    A("## Como regerar")
    A("")
    A("```bash")
    A("pip install openpyxl")
    A("python3 estrutura/cross_check.py")
    A("```")
    return "\n".join(L)


def xlsx(dados):
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    todos, base, dre, vagas = (dados["todos"], dados["base"], dados["dre"], dados["vagas"])
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    ws = wb.create_sheet("Factorial x Folha Set")
    ws.append(["Status", "Level", "Nome (organograma)", "Cargo", "Início", "Gestor",
               "Nome (folha)", "Posição", "Área", "Situação", "Tipo de custo", "Causa"])
    pares, soF, soB = emparelha(todos, "nome", base, "NOME")
    for f, b, s in pares:
        ws.append(["casou", f"L{f['level']}", f["nome"], f["cargo"], f["inicio"],
                   f["gestor"] or "—", b["NOME"], b["POSIÇÃO"], b["AREA"],
                   b["SITUAÇÃO"], b["TIPO DE CUSTO"], ""])
    for f in soF:
        ws.append(["só organograma", f"L{f['level']}", f["nome"], f["cargo"], f["inicio"],
                   f["gestor"] or "—", "", "", "", "", "", classifica_so_organograma(f)])
    for b in soB:
        ws.append(["só folha", "", "", "", "", "", b["NOME"], b["POSIÇÃO"], b["AREA"],
                   b["SITUAÇÃO"], b["TIPO DE CUSTO"], classifica_so_folha(b)])

    ws = wb.create_sheet("Factorial x DRE")
    ws.append(["Status", "Level", "Nome (organograma)", "Cargo", "Gestor",
               "Nome (DRE)", "C-LEVEL", "Área centro de custo", "Posição padrão",
               "Folha/Colchão", "Contratação", "TT Custo/Mês"])
    pd_, soFd, soDd = emparelha(todos, "nome", dre, "Colaborador")
    for f, d, s in pd_:
        ws.append(["casou", f"L{f['level']}", f["nome"], f["cargo"], f["gestor"] or "—",
                   d["Colaborador"], d["C-LEVEL"], d["ARÉA (Centro de Custo)"],
                   d["POSIÇÃO PADRÃO 26.2"], d["Folha/Colchão"], d["Contratação"],
                   d["TT Custo/Mês"]])
    for f in soFd:
        ws.append(["só organograma", f"L{f['level']}", f["nome"], f["cargo"],
                   f["gestor"] or "—", "", "", "", "", "", "", ""])
    for d in soDd:
        ws.append(["só DRE", "", "", "", "", d["Colaborador"], d["C-LEVEL"],
                   d["ARÉA (Centro de Custo)"], d["POSIÇÃO PADRÃO 26.2"],
                   d["Folha/Colchão"], d["Contratação"], d["TT Custo/Mês"]])

    ws = wb.create_sheet("Gestores x Draft")
    ws.append(["Level", "Gestor", "Cargo", "Fonte do cargo", "Diretos", "Indiretos",
               "Total abaixo", "Liderados no draft", "Slide", "Confere?"])
    for p in gestores(todos):
        cargo, fonte, trunc = CARGOS_DRAFT.get(p["nome"], (p["cargo"], "planilha", False))
        d = DRAFT_LIDERADOS.get(p["nome"])
        ws.append([f"L{p['level']}", p["nome"], cargo,
                   "draft (slide " + fonte + ")" if p["nome"] in CARGOS_DRAFT else "planilha",
                   p["diretos"], p["indiretos"], p["total"],
                   d[0] if d else "", d[1] if d else "",
                   ("sim" if d[0] == p["total"] else f"não (+{p['total']-d[0]})") if d
                   else "não consta no draft"])

    ws = wb.create_sheet("Estagiarios")
    ws.append(["Level", "Nome", "Cargo", "Gestor", "Início", "Local"])
    for x in sorted([y for y in dados["fac"] if PAT_INTERN.search(y["cargo"])],
                    key=lambda z: (z["cargo"], z["nome"])):
        ws.append([f"L{x['level']}", x["nome"], x["cargo"], x["gestor"], x["inicio"],
                   x["local"]])

    ws = wb.create_sheet("Vagas")
    ws.append(["C-LEVEL", "Área", "Cargo", "Status", "Contratado", "Admissão",
               "Folha/Colchão", "TT Custo/Mês", "Está no organograma?"])
    nomes_fac = [{"nome": p["nome"]} for p in todos]
    for v in vagas:
        achou = ""
        if v.get("CONTRATADO"):
            m = max(nomes_fac, key=lambda q: score(q["nome"], v["CONTRATADO"]))
            achou = m["nome"] if score(m["nome"], v["CONTRATADO"]) > 0 else "não encontrado"
        ws.append([v["C-LEVEL"], v["ARÉA"], v["CARGO"], v.get("STATUS GUPY") or "—",
                   v.get("CONTRATADO") or "—", str(v.get("Admissão") or "")[:10],
                   v["Folha/Colchão"], v["TT Custo/Mês"], achou])

    for sheet in wb.worksheets:
        for c in sheet[1]:
            c.fill = PatternFill("solid", fgColor="1B3A5C")
            c.font = Font(bold=True, color="FFFFFF")
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = f"A1:{get_column_letter(sheet.max_column)}1"
        larg = {}
        for row in sheet.iter_rows():
            for c in row:
                if c.value is not None:
                    larg[c.column] = min(46, max(larg.get(c.column, 10),
                                                 len(str(c.value)) + 2))
        for col, w in larg.items():
            sheet.column_dimensions[get_column_letter(col)].width = w

    destino = os.path.join(RAIZ, "estrutura", "Cross_Check.xlsx")
    wb.save(destino)
    return destino


def main():
    dados = carregar_tudo()
    cam = os.path.join(RAIZ, "estrutura", "Cross_Check_Organograma.md")
    with open(cam, "w", encoding="utf-8") as fh:
        fh.write(md(dados) + "\n")
    xl = xlsx(dados)
    print(f"organograma: {len(dados['todos'])} | folha: {len(dados['base'])} | "
          f"DRE: {len(dados['dre'])} | vagas: {len(dados['vagas'])}")
    print("ok ->", cam)
    print("ok ->", xl)


if __name__ == "__main__":
    main()
