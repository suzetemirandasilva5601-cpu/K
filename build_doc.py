#!/usr/bin/env python3
"""
Gera um PDF de documento curto (briefing, frameworks) a partir de um Markdown.

Uso:
    python3 build_doc.py <origem.md> <saida.pdf> "<Título do cabeçalho>"

Exemplos:
    python3 build_doc.py briefing/briefing-pre-entrevista.md \\
        Briefing-Pre-Entrevista-ATY.pdf "Briefing Pré-Entrevista — ATY Consulting"

    python3 build_doc.py frameworks/frameworks-varejo.md \\
        Frameworks-Varejo-ATY.pdf "Frameworks de Case — Varejo"

Para o relatório completo (vários capítulos, capa e índice), use build_pdf.py.
Reaproveita as funções de normalização e o CSS base do build_pdf.py.
"""

import sys
from datetime import date
from pathlib import Path

import markdown
from weasyprint import HTML

from build_pdf import CSS, fix_tight_lists, normalize_symbols, outside_code, tag_markers

BASE = Path(__file__).parent

# CSS de documento curto: sem capa nem índice, mais denso, cabeçalho simples.
EXTRA_CSS = """
@page {
  size: A4;
  margin: 14mm 13mm 13mm 13mm;
  @top-left  { content: string(doctitle); font: 7pt "DejaVu Sans"; color: #9ca3af; }
  @top-right { content: none; }
  @bottom-right { content: counter(page) " / " counter(pages);
                  font: 7.5pt "DejaVu Sans"; color: #6b7280; }
  @bottom-left  { content: "Matteo Lucato"; font: 7pt "DejaVu Sans"; color: #b3b8c0; }
}

html { font-size: 9.4pt; }
body { line-height: 1.42; }

h1 { string-set: doctitle content(); font-size: 18pt; margin: 0 0 2mm;
     padding-bottom: 2.5mm; border-bottom: 1.4pt solid #14532d; }
h1 + p { margin-bottom: 3mm; }

/* h2 como faixa: separa visualmente os blocos do documento */
h2 { font-size: 11.5pt; margin: 7mm 0 3mm; padding: 2mm 3mm;
     background: #14532d; color: #fff; border: 0; border-radius: 2pt;
     page-break-after: avoid; }
h3 { font-size: 10pt; margin: 4.5mm 0 1.5mm; color: #14532d; }
h4 { font-size: 9pt;  margin: 3.5mm 0 1mm; }
p  { margin: 0 0 2mm; }

ul, ol { margin: 0 0 2mm; padding-left: 5mm; }
li { margin: 0.7mm 0; }

table { font-size: 7.8pt; margin: 2mm 0 3mm; }
th { padding: 1.5mm 2mm; font-size: 7.5pt; }
td { padding: 1.4mm 2mm; }

blockquote { margin: 2mm 0 2.5mm; padding: 2.2mm 3mm; font-size: 8.9pt; }

/* Diagramas ASCII: fonte menor e entrelinha justa para caber na folha */
pre { font-size: 6.9pt; padding: 2.2mm 2.8mm; margin: 2mm 0 3mm; line-height: 1.3; }
code { font-size: 8pt; }
hr { margin: 4mm 0; }

blockquote, table, pre { page-break-inside: avoid; }
"""


def build(src: Path, titulo: str) -> str:
    raw = src.read_text(encoding="utf-8")
    raw = normalize_symbols(raw)
    raw = outside_code(raw, fix_tight_lists)
    raw = outside_code(raw, tag_markers)

    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "sane_lists"])
    body = md.convert(raw)

    hoje = date.today().strftime("%d/%m/%Y")
    rodape = (
        f'<p style="text-align:center;font-family:\'DejaVu Sans\';font-size:7.5pt;'
        f'color:#9ca3af;margin-top:6mm">Gerado em {hoje}</p>'
    )

    return (
        f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
        f"<title>{titulo}</title>"
        f"<style>{CSS}{EXTRA_CSS}</style></head><body>{body}{rodape}</body></html>"
    )


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    titulo = sys.argv[3]

    if not src.exists():
        sys.exit(f"ERRO: não encontrei {src}")

    html = build(src, titulo)
    HTML(string=html, base_url=str(BASE)).write_pdf(out)
    print(f"OK  {out.name}  ({out.stat().st_size / 1024:.0f} KB)")
