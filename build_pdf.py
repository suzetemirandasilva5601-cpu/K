#!/usr/bin/env python3
"""
Gera um PDF único a partir dos documentos de preparacao-aty/.

Uso:  python3 build_pdf.py
Saída: Relatorio-ATY-Consulting.pdf

Dependências: pip install weasyprint markdown pygments
Fontes: DejaVu Sans / Serif / Mono (cobertura de acentos, setas e box-drawing)
"""

import re
import sys
from datetime import date
from pathlib import Path

import markdown
from weasyprint import HTML

BASE = Path(__file__).parent
SRC = BASE / "preparacao-aty"
OUT = BASE / "Relatorio-ATY-Consulting.pdf"

# Ordem dos capítulos
CHAPTERS = [
    "README.md",
    "01-empresa-aty.md",
    "02-socios-pontos-em-comum.md",
    "03-meu-perfil-e-fit.md",
    "04-cases-star.md",
    "05-perguntas-tecnicas.md",
    "06-fit-interview.md",
    "07-pitch-e-curriculo.md",
    "08-estrategia-e-plano.md",
    "09-preenchimento-e-reconstrucao.md",
    "10-cases-guesstimate.md",
    "11-perguntas-ferramentas.md",
    "12-dossie-varejo-cases.md",
    "13-frentes-malha-e-equipe.md",
]

# Títulos curtos para o cabeçalho corrido
# Alinhados com a numeração interna de cada documento
SHORT_TITLES = {
    "README.md": "Sumário Executivo",
    "01-empresa-aty.md": "Parte 1 — A Empresa",
    "02-socios-pontos-em-comum.md": "Parte 2 — Sócios e Conexões",
    "03-meu-perfil-e-fit.md": "Parte 3 — Perfil e Fit",
    "04-cases-star.md": "Parte 4.1 — Cases STAR",
    "05-perguntas-tecnicas.md": "Parte 4.2 — Perguntas Técnicas",
    "06-fit-interview.md": "Parte 5 — Fit Interview",
    "07-pitch-e-curriculo.md": "Parte 6 — Pitch e Currículo",
    "08-estrategia-e-plano.md": "Partes 7 e 8 — Estratégia e Plano",
    "09-preenchimento-e-reconstrucao.md": "Parte 9 — Preenchimento",
    "10-cases-guesstimate.md": "Parte 10 — Cases e Guesstimate",
    "11-perguntas-ferramentas.md": "Parte 11 — Ferramentas",
    "12-dossie-varejo-cases.md": "Parte 12 — Dossiê Varejo",
    "13-frentes-malha-e-equipe.md": "Parte 13 — Frentes e Equipe",
}

# ----------------------------------------------------------------------------
# Normalização de símbolos
# As fontes DejaVu não têm emoji colorido. Mapeamos os emoji semânticos para
# glifos equivalentes que existem na fonte e removemos os decorativos.
# ----------------------------------------------------------------------------

EMOJI_MAP = {
    "\u2705": "\u2713",  # ✅ -> ✓
    "\u274C": "\u2717",  # ❌ -> ✗
    "\u261D": "\u2192",  # ☝ -> →
    "\U0001F525": "\u2605",  # 🔥 -> ★
}

EMOJI_STRIP = [
    "\U0001F3AF",  # 🎯
    "\U0001F534",  # 🔴
    "\U0001F7E1",  # 🟡
    "\U0001F7E2",  # 🟢
    "\U0001F517",  # 🔗
    "\U0001F3F7",  # 🏷
    "\u23F1",      # ⏱
    "\U0001F333",  # 🌳
    "\U0001F52C",  # 🔬
    "\U0001F465",  # 👥
    "\U0001F9E9",  # 🧩
    "\uFE0F",      # variation selector-16
]


def normalize_symbols(text: str) -> str:
    # Runs de ⭐ viram escala textual: ⭐⭐⭐⭐ -> 4/5
    text = re.sub(r"\u2B50+", lambda m: f"{len(m.group(0))}/5", text)
    for src, dst in EMOJI_MAP.items():
        text = text.replace(src, dst)
    for ch in EMOJI_STRIP:
        text = text.replace(ch, "")
    # Checkbox de lista -> caixa desenhável
    text = re.sub(r"^(\s*)- \[ \] ", "\\1- \u2610 ", text, flags=re.M)
    text = re.sub(r"^(\s*)- \[x\] ", "\\1- \u2611 ", text, flags=re.M)
    return text


def clean_whitespace(text: str) -> str:
    """Limpa espaço redundante em títulos e células de tabela.

    ATENÇÃO: precisa rodar APENAS fora de blocos de código. Colapsar espaço
    dentro de um bloco destrói o alinhamento de qualquer diagrama ASCII, e o
    estrago não aparece na extração de texto do PDF (onde espaço colapsado
    parece artefato normal do extrator). Aplique sempre via outside_code().
    """
    text = re.sub(r"^(#{1,6})\s+", r"\1 ", text, flags=re.M)
    text = re.sub(r"\|\s{2,}", "| ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def outside_code(text: str, fn):
    """Aplica fn apenas fora de blocos de código cercados."""
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    return "".join(p if p.startswith("```") else fn(p) for p in parts)


LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")


def fix_tight_lists(text: str) -> str:
    """Insere linha em branco antes de lista que segue parágrafo.

    O Python-Markdown NÃO reconhece uma lista colada a um parágrafo (trata os
    itens como continuação do texto). O CommonMark reconhece, então o markdown
    "parece" certo no GitHub e quebra no PDF. Normalizamos aqui.
    """
    out = []
    for line in text.split("\n"):
        if LIST_ITEM.match(line) and out:
            prev = out[-1]
            is_paragraph = (
                prev.strip()
                and not LIST_ITEM.match(prev)
                and not prev.lstrip().startswith(("|", "#", ">", "`"))
                and not prev.startswith((" ", "\t"))
            )
            if is_paragraph:
                out.append("")
        out.append(line)
    return "\n".join(out)


def flatten_links(text: str) -> str:
    """Links para outros .md do relatório viram texto simples (o PDF é único)."""
    def repl(m):
        label, href = m.group(1), m.group(2)
        if href.endswith(".md") or ".md#" in href:
            return label
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def tag_markers(text: str) -> str:
    """Destaca [VERIFICAR] e [INFERÊNCIA] com estilo próprio.

    No markdown os marcadores vêm entre backticks (`[VERIFICAR]`). Os backticks
    precisam ser CONSUMIDOS: se sobrarem, o markdown trata o <span> como inline
    code e o HTML aparece literal no PDF. Passe único para não aninhar spans.
    """
    def repl(m):
        kind = "verificar" if m.group(1).upper() == "VERIFICAR" else "inferencia"
        label = "VERIFICAR" if kind == "verificar" else "INFERÊNCIA"
        return f'<span class="mk-{kind}">[{label}{m.group(2)}]</span>'

    return re.sub(r"`?\[(VERIFICAR|INFER[ÊE]NCIA)([^\]]*)\]`?", repl, text)


# ----------------------------------------------------------------------------
# Conversão
# ----------------------------------------------------------------------------

def slug(chapter_file: str) -> str:
    return "ch-" + re.sub(r"[^a-z0-9]+", "-", chapter_file.lower().replace(".md", ""))


def build_html() -> str:
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "attr_list", "sane_lists", "toc"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )

    chapters_html = []
    toc_entries = []

    for fname in CHAPTERS:
        path = SRC / fname
        if not path.exists():
            sys.exit(f"ERRO: não encontrei {path}")

        raw = path.read_text(encoding="utf-8")
        # O índice de arquivos do README é redundante: o PDF tem índice próprio
        if fname == "README.md":
            raw = re.sub(r"\n## Índice\n.*?\n---\n", "\n", raw, flags=re.S)
        raw = normalize_symbols(raw)
        raw = outside_code(raw, clean_whitespace)
        raw = outside_code(raw, fix_tight_lists)
        raw = outside_code(raw, flatten_links)
        raw = outside_code(raw, tag_markers)

        # O h1 do arquivo vira título do capítulo; removemos do corpo
        lines = raw.split("\n")
        h1 = ""
        for i, ln in enumerate(lines):
            if ln.startswith("# "):
                h1 = ln[2:].strip()
                lines = lines[i + 1:]
                break
        body_md = "\n".join(lines)

        md.reset()
        body = md.convert(body_md)

        cid = slug(fname)
        short = SHORT_TITLES.get(fname, h1)

        # Índice: capítulo + seções de nível 2
        sections = [
            (t["id"], t["name"])
            for t in md.toc_tokens
            if t["level"] == 2
        ]
        toc_entries.append((cid, short, h1, sections))

        chapters_html.append(
            f'<section class="chapter" id="{cid}">'
            f'<div class="chapter-label">{short}</div>'
            f'<h1 data-short="{short}">{h1}</h1>\n{body}</section>'
        )

    # Monta o índice
    toc_html = ['<section class="toc" id="toc"><h1 data-short="Índice">Índice</h1>']
    for cid, short, h1, sections in toc_entries:
        toc_html.append(f'<div class="toc-ch"><a href="#{cid}">{short}</a></div>')
        if sections:
            toc_html.append('<ul class="toc-sec">')
            for sid, sname in sections:
                toc_html.append(f'<li><a href="#{sid}">{sname}</a></li>')
            toc_html.append("</ul>")
    toc_html.append("</section>")

    hoje = date.today().strftime("%d/%m/%Y")

    cover = f"""
<section class="cover">
  <div class="cover-kicker">Relatório de Preparação para Processo Seletivo</div>
  <h1 class="cover-title">ATY Consulting</h1>
  <div class="cover-rule"></div>
  <div class="cover-sub">Análise da empresa, dos sócios, do fit do candidato,<br>
  cases estruturados, banco de perguntas e plano de preparação</div>

  <table class="cover-meta">
    <tr><td>Candidato</td><td><strong>Matteo Lucato</strong></td></tr>
    <tr><td>Formação</td><td>Bacharelado em Economia — UNICAMP (fev/2023 – dez/2027)</td></tr>
    <tr><td>Empresa-alvo</td><td>ATY Consulting — Advanced Analytics, IA e Transformação Digital</td></tr>
    <tr><td>Data</td><td>{hoje}</td></tr>
  </table>

  <div class="cover-src">
    <strong>Fontes</strong><br>
    Conteúdo integral do site atyconsulting.com (extraído em 30/09/2026) &middot;
    perfis públicos de LinkedIn de Gilberto Volpe, André Shirassu e Nicole Gradice Silva &middot;
    currículo do candidato.
  </div>

  <div class="cover-warn">
    <strong>Nota de uso.</strong> Trechos marcados
    <span class="mk-inferencia">[INFERÊNCIA]</span> são leitura analítica, não fato declarado
    pela empresa — não os apresente como fato na entrevista. Trechos marcados
    <span class="mk-verificar">[VERIFICAR]</span> exigem que você preencha com um número real
    do seu histórico ou remova a afirmação. Não invente dado.
  </div>
</section>
"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Relatório ATY Consulting — Matteo Lucato</title>
<style>{CSS}</style></head>
<body>{cover}{''.join(toc_html)}{''.join(chapters_html)}</body></html>"""


CSS = """
@page {
  size: A4;
  margin: 18mm 15mm 16mm 15mm;
  @top-left  { content: string(chaptitle); font: 7.5pt "DejaVu Sans"; color: #8a8f98; }
  @top-right { content: "ATY Consulting"; font: 7.5pt "DejaVu Sans"; color: #b3b8c0; }
  @bottom-right { content: counter(page); font: 8pt "DejaVu Sans"; color: #6b7280; }
  @bottom-left  { content: "Matteo Lucato"; font: 7.5pt "DejaVu Sans"; color: #b3b8c0; }
}
@page cover { margin: 0; @top-left{content:none} @top-right{content:none}
              @bottom-right{content:none} @bottom-left{content:none} }

html { font-size: 10pt; }
/* DejaVu Sans no fim da cadeia: cobre ✓ ✗ ⚠ ★ ☐, ausentes no Serif */
body { font-family: "DejaVu Serif", "DejaVu Sans", serif; color: #1f2328;
       line-height: 1.5; text-align: justify; hyphens: auto; }

/* ---------- Capa ---------- */
.cover { page: cover; padding: 34mm 22mm 18mm; height: 100%;
         border-top: 9mm solid #14532d; text-align: left; }
.cover-kicker { font-family:"DejaVu Sans"; font-size: 9.5pt; letter-spacing: .13em;
                text-transform: uppercase; color: #15803d; margin-bottom: 6mm; }
.cover-title { font-family:"DejaVu Serif"; font-size: 40pt; font-weight: bold;
               color: #14532d; margin: 0; line-height: 1.05; }
.cover-rule { width: 46mm; height: 2.4pt; background: #15803d; margin: 7mm 0; }
.cover-sub { font-size: 12.5pt; color: #374151; line-height: 1.45; margin-bottom: 16mm; }
.cover-meta { width: 100%; border-collapse: collapse; font-family:"DejaVu Sans";
              font-size: 9.5pt; margin-bottom: 14mm; }
.cover-meta td { padding: 2.4mm 0; border-bottom: .4pt solid #e5e7eb; vertical-align: top; }
.cover-meta td:first-child { width: 30mm; color: #6b7280; text-transform: uppercase;
                             font-size: 7.8pt; letter-spacing: .06em; padding-top: 3mm; }
.cover-src { font-family:"DejaVu Sans"; font-size: 8.2pt; color: #4b5563;
             line-height: 1.6; border-left: 2.4pt solid #d1d5db;
             padding: 1mm 0 1mm 4mm; margin-bottom: 7mm; }
.cover-warn { font-family:"DejaVu Sans"; font-size: 8.2pt; color: #713f12;
              background: #fefce8; border: .5pt solid #fde68a; border-left: 2.4pt solid #ca8a04;
              padding: 3.5mm 4mm; line-height: 1.6; }

/* ---------- Índice ---------- */
.toc { page-break-before: always; string-set: chaptitle "Índice"; }
.toc h1 { font-size: 21pt; border: 0; margin: 0 0 8mm; }
.toc a { text-decoration: none; color: #1f2328; }
.toc-ch { font-family:"DejaVu Sans"; font-weight: bold; font-size: 10pt;
          margin: 5mm 0 1.5mm; color: #14532d; }
.toc-sec { list-style: none; margin: 0 0 0 5mm; padding: 0;
           font-family:"DejaVu Sans"; font-size: 8.6pt; }
.toc-sec li { margin: .9mm 0; color: #374151; }
.toc a { display: block; }
.toc a::after {
  content: " " leader('.') " " target-counter(attr(href, url), page);
  color: #9ca3af; font-weight: normal;
}

/* ---------- Capítulos ---------- */
.chapter { page-break-before: always; }
.chapter-label { font-family:"DejaVu Sans"; font-size: 8pt; letter-spacing: .14em;
                 text-transform: uppercase; color: #15803d; margin-bottom: 2.5mm; }
h1 { string-set: chaptitle attr(data-short); font-family:"DejaVu Serif";
     font-size: 22pt; color: #14532d; margin: 0 0 7mm; line-height: 1.15;
     border-bottom: 1.6pt solid #14532d; padding-bottom: 3mm; text-align: left; }
h2 { font-family:"DejaVu Sans"; font-size: 13pt; color: #14532d; margin: 9mm 0 3mm;
     padding-bottom: 1.5mm; border-bottom: .5pt solid #d1d5db;
     page-break-after: avoid; text-align: left; }
h3 { font-family:"DejaVu Sans"; font-size: 11pt; color: #166534; margin: 6.5mm 0 2mm;
     page-break-after: avoid; text-align: left; }
h4 { font-family:"DejaVu Sans"; font-size: 9.6pt; color: #374151; margin: 5mm 0 1.5mm;
     page-break-after: avoid; text-align: left; }
p { margin: 0 0 2.6mm; orphans: 2; widows: 2; }

/* ---------- Listas ---------- */
ul, ol { margin: 0 0 3mm; padding-left: 5.5mm; }
li { margin: 1.1mm 0; }
li > ul, li > ol { margin: 1mm 0 0; }

/* ---------- Citações (respostas modelo) ---------- */
blockquote { margin: 3mm 0 3.5mm; padding: 2.8mm 4mm; background: #f6f8f7;
             border-left: 2.6pt solid #15803d; font-size: 9.3pt; color: #26303a;
             page-break-inside: avoid; }
blockquote p { margin: 0 0 2mm; }
blockquote p:last-child { margin: 0; }
blockquote blockquote { background: #eef2f1; border-left-color: #6b7280; }

/* ---------- Tabelas ---------- */
table { width: 100%; border-collapse: collapse; margin: 3mm 0 4mm;
        font-family:"DejaVu Sans"; font-size: 8.1pt; table-layout: fixed;
        page-break-inside: avoid; }
th { background: #14532d; color: #fff; text-align: left; font-weight: bold;
     padding: 1.9mm 2.2mm; font-size: 7.9pt; line-height: 1.35; }
td { padding: 1.7mm 2.2mm; border-bottom: .4pt solid #e5e7eb; vertical-align: top;
     line-height: 1.4; word-wrap: break-word; overflow-wrap: break-word; }
tr:nth-child(even) td { background: #fafbfa; }
table strong { color: #14532d; }

/* ---------- Código e diagramas ---------- */
pre { font-family:"DejaVu Sans Mono", monospace; font-size: 7.2pt; line-height: 1.38;
      background: #f4f6f5; border: .4pt solid #dfe3e1; border-left: 2.4pt solid #15803d;
      padding: 2.8mm 3.2mm; margin: 3mm 0 4mm; white-space: pre; overflow: hidden;
      page-break-inside: avoid; text-align: left; }
code { font-family:"DejaVu Sans Mono", monospace; font-size: 8.3pt;
       background: #eef1f0; padding: .3mm 1mm; border-radius: 1.5pt; color: #14532d; }
pre code { background: none; padding: 0; font-size: inherit; color: #1f2328; }

/* ---------- Marcadores ---------- */
.mk-verificar { font-family:"DejaVu Sans"; font-size: 7.6pt; font-weight: bold;
                background: #fef2f2; color: #991b1b; border: .4pt solid #fca5a5;
                padding: .2mm 1.1mm; border-radius: 1.5pt; white-space: nowrap; }
.mk-inferencia { font-family:"DejaVu Sans"; font-size: 7.6pt; font-weight: bold;
                 background: #eff6ff; color: #1e40af; border: .4pt solid #93c5fd;
                 padding: .2mm 1.1mm; border-radius: 1.5pt; white-space: nowrap; }

hr { border: 0; border-top: .5pt solid #e5e7eb; margin: 6mm 0; }
strong { color: #0f172a; }
a { color: #15803d; text-decoration: none; }
"""


if __name__ == "__main__":
    html = build_html()
    (BASE / ".build_relatorio.html").write_text(html, encoding="utf-8")
    HTML(string=html, base_url=str(BASE)).write_pdf(OUT)
    kb = OUT.stat().st_size / 1024
    print(f"OK  {OUT.name}  ({kb:.0f} KB)")
