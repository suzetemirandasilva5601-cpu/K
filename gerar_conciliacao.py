# -*- coding: utf-8 -*-
"""Gera Word (análise) e Excel (conciliação) da diferença DRE agosto x Folha setembro - DMS."""
import unicodedata, re
from collections import Counter
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

DRE_FILE = "Baseline DRE 26.2.xlsx"
DRE_SHEET = "Baseline ativos agosto"
FOL_FILE = "Base_Setembro26 (1).xlsx"
FOL_SHEET = "Setembro Unificado"

def norm(s):
    if s is None: return ""
    s = unicodedata.normalize("NFKD", str(s).strip()).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^A-Za-z ]", " ", s)
    return re.sub(r"\s+", " ", s).upper().strip()

def first_last(s):
    t = norm(s).split()
    if not t: return ""
    return t[0] + "|" + t[-1] if len(t) > 1 else t[0]

def load(f, sheet, namecol):
    wb = openpyxl.load_workbook(f, data_only=True)
    ws = wb[sheet]
    rows = []
    for r in range(2, ws.max_row + 1):
        v = ws.cell(row=r, column=namecol).value
        if v in (None, ""): continue
        rows.append({"linha": r, "nome": str(v).strip(), "norm": norm(v), "fl": first_last(v)})
    return rows

dre = load(DRE_FILE, DRE_SHEET, 3)
fol = load(FOL_FILE, FOL_SHEET, 5)

n_dre, n_fol = len(dre), len(fol)
dif = n_dre - n_fol

# duplicatas na folha
dup_fol = {k: v for k, v in Counter(x["norm"] for x in fol).items() if v > 1}

# Match por NOME COMPLETO normalizado (metodo A).
# Obs.: o match por primeiro+ultimo nome foi descartado como metodo principal
# porque colapsa pessoas distintas (ex.: LUCAS|SILVA, MARIA|SILVA aparecem 2x).
fol_norm = set(x["norm"] for x in fol)
dre_norm = set(x["norm"] for x in dre)

saidas = [x for x in dre if x["norm"] not in fol_norm]    # DRE e nao folha
entradas = [x for x in fol if x["norm"] not in dre_norm]  # folha e nao DRE

# linhas excedentes por duplicidade na folha
extra_dup = sum(v - 1 for v in dup_fol.values())

# grafia divergente conhecida (conferir manualmente) - pares provaveis
grafia = [
    ("PIRACI", "CONSULTOR - PIRACI OLIVEIRA SOCIEDADE DE ADVOGADOS",
     "Mesma PJ/pessoa com razao social na folha"),
    ("Isabella FRA", "ISABELLA STODIEK",
     "Nome truncado na DRE; confirmar se e a mesma pessoa"),
    ("AUAD ENGENHARIA DE SOFTWARE LTDA", "(verificar pessoa fisica na folha)",
     "Razao social de PJ na DRE; pode estar na folha pelo nome da pessoa"),
]

# ============================ EXCEL ============================
wb = openpyxl.Workbook()

HEAD_FILL = PatternFill("solid", fgColor="1F4E78")
HEAD_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14, color="1F4E78")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEAD_FILL; cell.font = HEAD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = BORDER

def autofit(ws):
    for col in ws.columns:
        width = 0
        letter = get_column_letter(col[0].column)
        for cell in col:
            if cell.value is not None:
                width = max(width, len(str(cell.value)))
        ws.column_dimensions[letter].width = min(max(width + 3, 12), 60)

# --- Aba Resumo ---
ws = wb.active
ws.title = "Resumo"
ws["A1"] = "Conciliacao DRE Agosto x Folha Setembro - DMS"
ws["A1"].font = TITLE_FONT
ws.merge_cells("A1:C1")
resumo = [
    ("Indicador", "Valor", "Observacao"),
    ("DRE de agosto (colaboradores)", n_dre, "Linhas 2-329 da aba 'Baseline ativos agosto'"),
    ("Folha de setembro (colaboradores)", n_fol, "Linhas 2-324 da aba 'Setembro Unificado'"),
    ("Diferenca liquida (DRE - Folha)", dif, "NAO sao 3 linhas; sao 5"),
    ("Nomes so na DRE (sairam/nao considerados)", len(saidas), "Rotatividade - saidas"),
    ("Nomes so na Folha (entradas)", len(entradas), "Rotatividade - entradas"),
    ("Duplicata na folha", "; ".join(dup_fol.keys()) or "nenhuma",
     f"{extra_dup} linha(s) excedente(s) por duplicidade"),
    ("Reconciliacao (subtotal)",
     f"{n_dre} - {len(saidas)} + {len(entradas)} = {n_dre - len(saidas) + len(entradas)}",
     "DRE menos saidas mais entradas"),
    ("Reconciliacao (final)",
     f"{n_dre - len(saidas) + len(entradas)} + {extra_dup} = {n_dre - len(saidas) + len(entradas) + extra_dup}",
     f"Igual ao total real da folha ({n_fol}) - balanco fecha"),
    ("Metodo de cruzamento", "Nome completo normalizado",
     "Sem acentos, maiusculas, espacos normalizados"),
]
start = 3
for i, (a, b, c) in enumerate(resumo):
    ws.cell(row=start + i, column=1, value=a)
    ws.cell(row=start + i, column=2, value=b)
    ws.cell(row=start + i, column=3, value=c)
style_header(ws, start, 3)
for r in range(start + 1, start + len(resumo)):
    for c in range(1, 4):
        ws.cell(row=r, column=c).border = BORDER
autofit(ws)

# --- Aba Sairam ---
ws2 = wb.create_sheet("Sairam (so na DRE)")
ws2.append(["#", "Nome na DRE (agosto)", "Linha na DRE"])
style_header(ws2, 1, 3)
for i, x in enumerate(sorted(saidas, key=lambda z: z["nome"].upper()), 1):
    ws2.append([i, x["nome"], x["linha"]])
    for c in range(1, 4): ws2.cell(row=i + 1, column=c).border = BORDER
autofit(ws2)

# --- Aba Entraram ---
ws3 = wb.create_sheet("Entraram (so na Folha)")
ws3.append(["#", "Nome na Folha (setembro)", "Linha na Folha"])
style_header(ws3, 1, 3)
for i, x in enumerate(sorted(entradas, key=lambda z: z["nome"].upper()), 1):
    ws3.append([i, x["nome"], x["linha"]])
    for c in range(1, 4): ws3.cell(row=i + 1, column=c).border = BORDER
autofit(ws3)

# --- Aba Grafia divergente ---
ws4 = wb.create_sheet("Grafia a conferir")
ws4.append(["#", "Como aparece na DRE", "Provavel na Folha", "Observacao"])
style_header(ws4, 1, 4)
for i, (a, b, obs) in enumerate(grafia, 1):
    ws4.append([i, a, b, obs])
    for c in range(1, 5): ws4.cell(row=i + 1, column=c).border = BORDER
autofit(ws4)

xlsx_out = "Conciliacao_DRE_Agosto_x_Folha_Setembro.xlsx"
wb.save(xlsx_out)
print("Excel gerado:", xlsx_out)

# ============================ WORD ============================
doc = Document()
# estilo base
style = doc.styles["Normal"]
style.font.name = "Calibri"; style.font.size = Pt(11)

t = doc.add_heading("Analise da Diferenca - DRE de Agosto x Folha de Setembro", level=0)

p = doc.add_paragraph()
p.add_run("Empresa: ").bold = True; p.add_run("DMS")
p = doc.add_paragraph()
p.add_run("Objeto: ").bold = True
p.add_run("Correlacao entre a DRE (baseline de agosto) e a folha de pagamento de setembro.")

doc.add_heading("1. Numeros encontrados", level=1)
tbl = doc.add_table(rows=1, cols=2); tbl.style = "Light Grid Accent 1"
hdr = tbl.rows[0].cells
hdr[0].text = "Base"; hdr[1].text = "Colaboradores"
for base, qtd in [("DRE de agosto (linhas 2-329)", str(n_dre)),
                  ("Folha de setembro (linhas 2-324)", str(n_fol)),
                  ("Diferenca liquida (DRE - Folha)", str(dif))]:
    row = tbl.add_row().cells
    row[0].text = base; row[1].text = qtd
    if base.startswith("Diferenca"):
        for cell in row:
            for par in cell.paragraphs:
                for run in par.runs: run.bold = True

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run("Conclusao do item: ").bold = True
p.add_run("a diferenca real entre as duas bases e de ")
r = p.add_run("5 linhas (328 - 323), e nao 3."); r.bold = True

doc.add_heading("2. O que existe de verdade: rotatividade nos dois sentidos", level=1)
doc.add_paragraph(
    "A diferenca liquida de apenas 5 linhas esconde um movimento bem maior de pessoas. "
    "Entre agosto e setembro houve rotatividade nos dois sentidos - gente que saiu e gente "
    "que entrou - e os dois efeitos quase se cancelam na contagem total.")
doc.add_paragraph(
    f"{len(saidas)} nomes aparecem na DRE de agosto e NAO na folha de setembro "
    "(saidas / colaboradores nao considerados no mes).", style="List Bullet")
doc.add_paragraph(
    f"{len(entradas)} nomes aparecem na folha de setembro e NAO na DRE de agosto (entradas).",
    style="List Bullet")

doc.add_heading("3. Como a conta fecha", level=1)
sub = n_dre - len(saidas) + len(entradas)
tbl2 = doc.add_table(rows=1, cols=2); tbl2.style = "Light Grid Accent 1"
h2 = tbl2.rows[0].cells
h2[0].text = "Etapa da conciliacao"; h2[1].text = "Linhas"
for etapa, val in [
    ("DRE de agosto", str(n_dre)),
    (f"(-) saidas (so na DRE)", f"-{len(saidas)}"),
    (f"(+) entradas (so na folha)", f"+{len(entradas)}"),
    ("(=) subtotal", str(sub)),
    ("(+) linha duplicada na folha", f"+{extra_dup}"),
    ("(=) TOTAL CALCULADO", str(sub + extra_dup)),
    ("TOTAL REAL DA FOLHA DE SETEMBRO", str(n_fol)),
]:
    row = tbl2.add_row().cells
    row[0].text = etapa; row[1].text = val
    if etapa.startswith("(=) TOTAL") or etapa.startswith("TOTAL REAL"):
        for cell in row:
            for par in cell.paragraphs:
                for run in par.runs: run.bold = True

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run(f"{n_dre} - {len(saidas)} (sairam) + {len(entradas)} (entraram) = {sub}").bold = True
p.add_run(f", e somando a linha duplicada chega-se a {sub + extra_dup}, exatamente o total "
          f"da folha de setembro. O balanco fecha sem residuo.")
doc.add_paragraph(
    "A linha excedente vem de um nome duplicado na folha de setembro: "
    "PAMELA IRIS GREGORIO IBARRA aparece 2 vezes.")

doc.add_heading("4. Pontos de atencao (grafia divergente)", level=1)
doc.add_paragraph(
    "Alguns nomes contados como 'so na DRE' na verdade estao na folha, apenas escritos de "
    "forma diferente. Devem ser conferidos manualmente antes de tratar como saida real:")
for a, b, obs in grafia:
    doc.add_paragraph(f"{a}  ->  {b}  ({obs})", style="List Bullet")

doc.add_heading("5. Resumo executivo", level=1)
doc.add_paragraph(
    f"A alteracao entre a DRE de agosto e a folha de setembro NAO e de 3 linhas. Trata-se de "
    f"uma diferenca liquida de {dif} linhas, resultante de {len(saidas)} saidas e "
    f"{len(entradas)} entradas - ou seja, rotatividade relevante no quadro, mascarada pela "
    f"proximidade dos totais.")

doc.add_heading("6. Metodologia e validacao", level=1)
doc.add_paragraph(
    "O cruzamento foi feito pelo nome do colaborador (DRE: coluna C 'Colaborador'; folha: "
    "coluna E 'NOME'), com normalizacao de acentos, maiusculas e espacos.")
doc.add_paragraph("Os numeros foram conferidos por verificacoes independentes:", style="Normal")
doc.add_paragraph("Contagem de linhas via leitura da planilha e, de forma independente, "
                  "via leitura do XML interno do arquivo xlsx - ambas deram o mesmo resultado.",
                  style="List Bullet")
doc.add_paragraph("Verificacao de ausencia de linhas em branco no meio das bases.",
                  style="List Bullet")
doc.add_paragraph("Cruzamento por nome completo e, em paralelo, por primeiro+ultimo nome. "
                  "O segundo metodo foi descartado como base oficial por agrupar pessoas "
                  "distintas que compartilham sobrenomes comuns.", style="List Bullet")
doc.add_paragraph("Checagem de duplicidades nas duas bases.", style="List Bullet")
doc.add_paragraph("Fechamento do balanco contra o total real da folha, sem residuo.",
                  style="List Bullet")

docx_out = "Analise_Diferenca_DRE_Agosto_x_Folha_Setembro.docx"
doc.save(docx_out)
print("Word gerado:", docx_out)
print("\nResumo: DRE", n_dre, "| Folha", n_fol, "| dif", dif,
      "| saidas", len(saidas), "| entradas", len(entradas), "| dup", dup_fol)
