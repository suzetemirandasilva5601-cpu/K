#!/usr/bin/env python3
"""
Gera o briefing pré-entrevista em PDF (documento curto, de consulta rápida).

Uso:  python3 build_briefing.py
Saída: Briefing-Pre-Entrevista-ATY.pdf

Reaproveita as funções de normalização e o CSS do build_pdf.py, com ajustes
de layout para documento curto: sem capa separada, sem índice, fonte um pouco
menor e margens mais apertadas para caber mais por página.
"""

from datetime import date
from pathlib import Path

import markdown
from weasyprint import HTML

from build_pdf import CSS, fix_tight_lists, normalize_symbols, outside_code, tag_markers

BASE = Path(__file__).parent
SRC = BASE / "briefing" / "briefing-pre-entrevista.md"
OUT = BASE / "Briefing-Pre-Entrevista-ATY.pdf"

EXTRA_CSS = """
/* ---- Ajustes para documento curto de consulta rápida ---- */
@page {
  size: A4;
  margin: 14mm 13mm 13mm 13mm;
  @top-left  { content: "Briefing Pré-Entrevista — ATY Consulting";
               font: 7pt "DejaVu Sans"; color: #9ca3af; }
  @top-right { content: none; }
  @bottom-right { content: counter(page) " / " counter(pages);
                  font: 7.5pt "DejaVu Sans"; color: #6b7280; }
  @bottom-left  { content: "Matteo Lucato"; font: 7pt "DejaVu Sans"; color: #b3b8c0; }
}

html { font-size: 9.4pt; }
body { line-height: 1.42; }

/* Cabeçalho do documento, no topo da primeira página */
h1:first-of-type {
  font-size: 19pt; margin: 0 0 2mm; padding-bottom: 2.5mm;
  border-bottom: 1.4pt solid #14532d;
}

/* H2 vira faixa de bloco — separa visualmente os 4 blocos */
h2 {
  font-size: 11.5pt; margin: 7mm 0 3mm; padding: 2mm 3mm;
  background: #14532d; color: #fff; border: 0; border-radius: 2pt;
  page-break-after: avoid;
}
h3 { font-size: 10pt; margin: 4.5mm 0 1.5mm; color: #14532d; }
h4 { font-size: 9pt; margin: 3.5mm 0 1mm; }
p  { margin: 0 0 2mm; }

ul, ol { margin: 0 0 2mm; padding-left: 5mm; }
li { margin: 0.7mm 0; }

table { font-size: 7.8pt; margin: 2mm 0 3mm; }
th { padding: 1.5mm 2mm; font-size: 7.5pt; }
td { padding: 1.4mm 2mm; }

blockquote { margin: 2mm 0 2.5mm; padding: 2.2mm 3mm; font-size: 8.9pt; }
pre { font-size: 6.9pt; padding: 2.2mm 2.8mm; margin: 2mm 0 3mm; line-height: 1.32; }
code { font-size: 8pt; }
hr { margin: 4mm 0; }

/* Evita quebra feia dentro de bloco de resposta */
blockquote, table, pre { page-break-inside: avoid; }
"""


def build() -> str:
    raw = SRC.read_text(encoding="utf-8")
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
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
        "<title>Briefing Pré-Entrevista — ATY Consulting</title>"
        f"<style>{CSS}{EXTRA_CSS}</style></head><body>{body}{rodape}</body></html>"
    )


if __name__ == "__main__":
    html = build()
    (BASE / ".build_briefing.html").write_text(html, encoding="utf-8")
    HTML(string=html, base_url=str(BASE)).write_pdf(OUT)
    print(f"OK  {OUT.name}  ({OUT.stat().st_size / 1024:.0f} KB)")
