#!/usr/bin/env bash
# Prepara o ambiente para gerar o PDF do relatório.
# Rode isto antes de `python3 build_pdf.py` em máquina nova ou após reset do sandbox.
set -euo pipefail

echo "==> Instalando dependências Python"
pip install --quiet weasyprint markdown pygments pypdf

echo "==> Verificando fontes DejaVu"
if fc-list : family 2>/dev/null | grep -qi "DejaVu Sans Mono"; then
    echo "    já instaladas"
else
    echo "    baixando DejaVu 2.37"
    # O ambiente padrão traz apenas Noto Sans: sem monospace, sem serif e sem
    # cobertura de ✓ ✗ ⚠ ★ ☐. Sem DejaVu os diagramas ASCII e os símbolos
    # das tabelas saem quebrados no PDF.
    mkdir -p "$HOME/.fonts"
    tmp="$(mktemp -d)"
    curl -sL --max-time 120 \
      "https://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.tar.bz2/download" \
      -o "$tmp/dejavu.tar.bz2"
    tar xjf "$tmp/dejavu.tar.bz2" -C "$tmp"
    cp "$tmp"/dejavu-fonts-ttf-2.37/ttf/*.ttf "$HOME/.fonts/"
    fc-cache -f >/dev/null 2>&1
    rm -rf "$tmp"
    echo "    instaladas"
fi

echo "==> Pronto. Agora rode: python3 build_pdf.py"
