// Motor de layout: cada slide é uma lista de elementos em polegadas,
// renderizada em PPTX (pptxgenjs, editável) e em HTML (para gerar PDF e conferir).
const fs = require('fs');
const path = require('path');
const PptxGenJS = require('pptxgenjs');

const W = 13.333, H = 7.5;
const C = {
  red: 'C1272D', dark: '222222', grey: '595959', light: 'F2F2F2', tab: 'D9D9D9',
  border: 'A6A6A6', white: 'FFFFFF', blueGrey: '9AA5B8', green: '2E7D32', place: '8C8C8C',
};
const FONT = 'Calibri';
const HTML_FONT = "Calibri, Carlito, 'Noto Sans', sans-serif";
const ASSETS = __dirname;

// ---------- marcação de texto ----------
// Linhas: "• " bullet nível 1, "– " bullet nível 2, "" espaço, demais = parágrafo.
// Inline: **negrito**, __sublinhado__, [[placeholder]] (cinza itálico).
function parseLines(text) {
  return String(text).split('\n').map(raw => {
    let level = -1, t = raw;
    if (t.startsWith('• ')) { level = 0; t = t.slice(2); }
    else if (t.startsWith('– ')) { level = 1; t = t.slice(2); }
    let italic = false;
    if (t.startsWith('_ ')) { italic = true; t = t.slice(2); }
    const runs = [];
    t.split(/(\*\*.+?\*\*|__.+?__|\[\[.+?\]\])/).filter(s => s !== '').forEach(s => {
      if (s.startsWith('**')) runs.push({ t: s.slice(2, -2), bold: true });
      else if (s.startsWith('__')) runs.push({ t: s.slice(2, -2), underline: true });
      else if (s.startsWith('[[')) runs.push({ t: s.slice(2, -2), place: true });
      else runs.push({ t: s });
    });
    return { level, italic, runs, empty: raw.trim() === '' };
  });
}

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

function runsHtml(line, color) {
  return line.runs.map(r => {
    let st = '';
    if (r.bold) st += 'font-weight:700;';
    if (r.underline) st += 'text-decoration:underline;';
    if (r.place) st += `color:#${C.place};font-style:italic;`;
    return `<span style="${st}">${esc(r.t)}</span>`;
  }).join('');
}

function textHtml(text, o) {
  const lines = parseLines(text);
  return lines.map(l => {
    if (l.empty) return `<div style="height:${o.size * 0.55}pt"></div>`;
    const ital = l.italic ? 'font-style:italic;' : '';
    const sp = `margin:0 0 ${o.paraAfter ?? 2}pt 0;`;
    if (l.level >= 0) {
      const ind = l.level === 0 ? 14 : 30;
      const sym = l.level === 0 ? '•' : '–';
      return `<div style="${sp}${ital}padding-left:${ind}pt;position:relative"><span style="position:absolute;left:${ind - 10}pt">${sym}</span>${runsHtml(l)}</div>`;
    }
    return `<div style="${sp}${ital}">${runsHtml(l)}</div>`;
  }).join('');
}

function textRuns(text, o) {
  const lines = parseLines(text);
  const out = [];
  lines.forEach((l, i) => {
    const last = i === lines.length - 1;
    const para = {};
    if (l.level === 0) { para.bullet = { indent: 11 }; para.indentLevel = 0; }
    if (l.level === 1) { para.bullet = { code: '2013', indent: 11 }; para.indentLevel = 1; }
    if (l.empty) {
      out.push({ text: ' ', options: { fontSize: o.size * 0.55, breakLine: !last } });
      return;
    }
    l.runs.forEach((r, j) => {
      const op = { ...para };
      if (r.bold) op.bold = true;
      if (r.underline) op.underline = { style: 'sng' };
      if (r.place) { op.color = C.place; op.italic = true; }
      if (l.italic) op.italic = true;
      if (j === l.runs.length - 1 && !last) op.breakLine = true;
      out.push({ text: r.t, options: op });
    });
  });
  return out;
}

// ---------- elementos ----------
const el = {
  rect: (x, y, w, h, o = {}) => ({ type: 'rect', x, y, w, h, ...o }),
  text: (x, y, w, h, text, o = {}) => ({ type: 'text', x, y, w, h, text, ...o }),
  image: (x, y, w, h, file) => ({ type: 'image', x, y, w, h, file }),
  table: (x, y, w, colW, rows, o = {}) => ({ type: 'table', x, y, w, colW, rows, ...o }),
  balls: (x, y, d, gap, o = {}) => ({ type: 'balls', x, y, d, gap, ...o }),
  chart: (x, y, w, h, o) => ({ type: 'chart', x, y, w, h, ...o }),
};

// Caixa com aba cinza no canto, como nos casebooks.
function box(x, y, w, h, label, body, o = {}) {
  const size = o.size ?? 10;
  const labW = Math.min(w, Math.max(1.5, label.length * 0.068 + 0.3));
  const items = [
    el.rect(x, y, w, h, { fill: C.white, line: C.border }),
    el.rect(x, y, labW, 0.24, { fill: C.tab, line: C.border }),
    el.text(x + 0.06, y, labW - 0.08, 0.24, `**${label}**`, { size: 9, valign: 'middle', inset: 0 }),
  ];
  if (body !== null && body !== undefined) {
    items.push(el.text(x + 0.08, y + 0.3, w - 0.16, (o.bodyH ?? h - 0.36), body, { size, ...o.text }));
  }
  return items;
}

function header(title, opts = {}) {
  const h = opts.h ?? 1.05;
  const items = [
    el.rect(0, 0, W, h, { fill: C.red }),
    el.text(0.35, h - 0.62, opts.titleW ?? 8, 0.55, `**${title}**`, { size: 24, color: C.white, valign: 'bottom', inset: 0 }),
  ];
  return items;
}

function footer(n, label) {
  return [
    el.rect(0.35, 7.0, W - 0.7, 0.01, { fill: C.border }),
    el.image(0.35, 7.07, 2.06, 0.26, 'logo_orig.png'),
    el.text(2.6, 7.07, 7, 0.26, label, { size: 9, color: C.grey, valign: 'middle', inset: 0 }),
    el.text(W - 1.35, 7.07, 1.0, 0.26, String(n), { size: 9, color: C.grey, align: 'right', valign: 'middle', inset: 0 }),
  ];
}

// ---------- render PPTX ----------
function renderPptx(deck, outFile) {
  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_WIDE';
  pres.title = deck.title;
  pres.author = 'Clube de Consultoria Universitário';
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  deck.slides.forEach(items => {
    const s = pres.addSlide();
    s.background = { color: C.white };
    items.flat(Infinity).forEach(e => {
      const pos = { x: e.x, y: e.y, w: e.w, h: e.h };
      if (e.type === 'rect') {
        s.addShape(pres.ShapeType.rect, {
          ...pos, fill: e.fill ? { color: e.fill } : { type: 'none' },
          line: e.line ? { color: e.line, width: e.lineW ?? 0.75, dashType: e.dash ? 'dash' : 'solid' } : { type: 'none' },
        });
      } else if (e.type === 'text') {
        const ins = e.inset ?? 3;
        s.addText(textRuns(e.text, { size: e.size ?? 10 }), {
          ...pos, fontFace: FONT, fontSize: e.size ?? 10, color: e.color ?? C.dark,
          align: e.align ?? 'left', valign: e.valign ?? 'top', margin: [ins, ins, ins, ins],
          paraSpaceAfter: e.paraAfter ?? 2, lineSpacingMultiple: 1.0, fit: 'none',
        });
      } else if (e.type === 'image') {
        s.addImage({ path: path.join(ASSETS, e.file), ...pos });
      } else if (e.type === 'table') {
        const rows = e.rows.map((r, ri) => r.map(c => {
          const cell = typeof c === 'object' ? c : { t: c };
          const isHead = (e.head ?? true) && ri === 0;
          return {
            text: textRuns(cell.t ?? '', { size: e.size ?? 9 }),
            options: {
              bold: cell.bold ?? isHead, color: cell.color ?? (isHead ? C.white : C.dark),
              fill: { color: cell.fill ?? (isHead ? (e.headFill ?? C.red) : C.white) },
              align: cell.align ?? 'left', valign: 'middle', fontSize: cell.size ?? e.size ?? 9,
              colspan: cell.colspan, margin: [2, 4, 2, 4],
            },
          };
        }));
        s.addTable(rows, {
          x: e.x, y: e.y, w: e.w, colW: e.colW, rowH: e.rowH ?? 0.24, fontFace: FONT,
          border: { type: 'solid', pt: 0.75, color: C.border }, autoPage: false,
        });
      } else if (e.type === 'balls') {
        for (let i = 0; i < 5; i++) {
          const bx = e.x + i * (e.d + e.gap);
          s.addShape(pres.ShapeType.ellipse, { x: bx, y: e.y, w: e.d, h: e.d, fill: { color: C.white }, line: { color: C.dark, width: 1 } });
          if (i === 4) s.addShape(pres.ShapeType.ellipse, { x: bx, y: e.y, w: e.d, h: e.d, fill: { color: C.dark }, line: { color: C.dark, width: 1 } });
          else if (i > 0) s.addShape(pres.ShapeType.pie, { x: bx, y: e.y, w: e.d, h: e.d, fill: { color: C.dark }, line: { type: 'none' }, angleRange: [270, 270 + i * 90] });
          if (e.numbers) s.addText(String(i + 1), { x: bx - 0.05, y: e.y + e.d, w: e.d + 0.1, h: 0.16, fontSize: 7, align: 'center', color: C.grey, fontFace: FONT, margin: 0 });
        }
      } else if (e.type === 'chart') {
        s.addChart(pres.ChartType.bar, e.series.map(sr => ({ name: sr.name, labels: e.labels, values: sr.values })), {
          ...pos, barDir: 'bar', barGapWidthPct: 40, chartColors: e.series.map(sr => sr.color),
          showValue: true, dataLabelFontSize: 7, dataLabelFormatCode: '0"%"', dataLabelPosition: 'outEnd',
          catAxisLabelFontSize: 8, valAxisLabelFontSize: 7, valAxisMaxVal: 100, valAxisMinVal: 0,
          catAxisOrientation: 'maxMin', valAxisHidden: true, valGridLine: { style: 'none' },
          showLegend: true, legendPos: 'b', legendFontSize: 8, fontFace: FONT,
          showTitle: !!e.title, title: e.title, titleFontSize: 10, titleColor: C.dark,
        });
      }
    });
  });
  return pres.writeFile({ fileName: outFile });
}

// ---------- render HTML ----------
function renderHtml(deck) {
  const px = v => `${v}in`;
  const pages = deck.slides.map(items => {
    const inner = items.flat(Infinity).map(e => {
      const pos = `position:absolute;left:${px(e.x)};top:${px(e.y)};width:${px(e.w)};height:${px(e.h)};`;
      if (e.type === 'rect') {
        const b = e.line ? `border:${e.lineW ?? 0.75}pt ${e.dash ? 'dashed' : 'solid'} #${e.line};` : '';
        return `<div style="${pos}box-sizing:border-box;background:${e.fill ? '#' + e.fill : 'transparent'};${b}"></div>`;
      }
      if (e.type === 'text') {
        const ins = e.inset ?? 3;
        const jc = { top: 'flex-start', middle: 'center', bottom: 'flex-end' }[e.valign ?? 'top'];
        return `<div class="tx" style="${pos}box-sizing:border-box;padding:${ins}pt;display:flex;flex-direction:column;justify-content:${jc};font-size:${e.size ?? 10}pt;color:#${e.color ?? C.dark};text-align:${e.align ?? 'left'};overflow:hidden;line-height:1.17"><div>${textHtml(e.text, { size: e.size ?? 10, paraAfter: e.paraAfter })}</div></div>`;
      }
      if (e.type === 'image') {
        return `<img src="${e.file}" style="${pos}">`;
      }
      if (e.type === 'table') {
        const rows = e.rows.map((r, ri) => '<tr>' + r.map((c, ci) => {
          const cell = typeof c === 'object' ? c : { t: c };
          const isHead = (e.head ?? true) && ri === 0;
          const bg = cell.fill ?? (isHead ? (e.headFill ?? C.red) : C.white);
          const col = cell.color ?? (isHead ? C.white : C.dark);
          const fw = (cell.bold ?? isHead) ? 700 : 400;
          const span = cell.colspan ? ` colspan="${cell.colspan}"` : '';
          return `<td${span} style="width:${px(e.colW[ci] ?? 1)};height:${px(e.rowH ?? 0.24)};background:#${bg};color:#${col};font-weight:${fw};text-align:${cell.align ?? 'left'};font-size:${cell.size ?? e.size ?? 9}pt">${textHtml(cell.t ?? '', { size: e.size ?? 9, paraAfter: 0 })}</td>`;
        }).join('') + '</tr>').join('');
        return `<table class="tb" style="position:absolute;left:${px(e.x)};top:${px(e.y)};width:${px(e.w)};border-collapse:collapse;table-layout:fixed;line-height:1.12" data-maxh="${e.maxH ?? ''}">${rows}</table>`;
      }
      if (e.type === 'balls') {
        let s = '';
        for (let i = 0; i < 5; i++) {
          const bx = e.x + i * (e.d + e.gap);
          s += `<div style="position:absolute;left:${px(bx)};top:${px(e.y)};width:${px(e.d)};height:${px(e.d)};box-sizing:border-box;border:1pt solid #${C.dark};border-radius:50%;background:conic-gradient(#${C.dark} 0 ${i * 25}%, #fff ${i * 25}% 100%)"></div>`;
          if (e.numbers) s += `<div style="position:absolute;left:${px(bx - 0.05)};top:${px(e.y + e.d)};width:${px(e.d + 0.1)};font-size:7pt;text-align:center;color:#${C.grey}">${i + 1}</div>`;
        }
        return s;
      }
      if (e.type === 'chart') {
        const n = e.labels.length;
        const top = e.title ? 0.32 : 0.05;
        const rowH = (e.h - top - 0.35) / n;
        const lab = 1.45, area = e.w - lab - 0.45;
        let s = `<div style="${pos}">`;
        if (e.title) s += `<div style="position:absolute;left:0;top:0;width:100%;text-align:center;font-weight:700;font-size:10pt">${esc(e.title)}</div>`;
        e.labels.forEach((l, i) => {
          const y = top + i * rowH;
          s += `<div style="position:absolute;left:0;top:${px(y)};width:${px(lab - 0.08)};height:${px(rowH)};display:flex;align-items:center;justify-content:flex-end;font-size:8pt">${esc(l)}</div>`;
          e.series.forEach((sr, k) => {
            const bh = rowH * 0.32, by = y + rowH * 0.16 + k * bh;
            const bw = area * sr.values[i] / 100;
            s += `<div style="position:absolute;left:${px(lab)};top:${px(by)};width:${px(bw)};height:${px(bh * 0.9)};background:#${sr.color}"></div>`;
            s += `<div style="position:absolute;left:${px(lab + bw + 0.04)};top:${px(by - 0.02)};font-size:7pt;line-height:${px(bh)}">${sr.values[i]}%</div>`;
          });
        });
        s += `<div style="position:absolute;left:0;bottom:0;width:100%;text-align:center;font-size:8pt">` + e.series.map(sr => `<span style="display:inline-block;width:9pt;height:9pt;background:#${sr.color};vertical-align:middle;margin:0 4pt 0 10pt"></span>${esc(sr.name)}`).join('') + `</div>`;
        return s + '</div>';
      }
      return '';
    }).join('\n');
    return `<section class="slide">${inner}</section>`;
  }).join('\n');
  return `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>${esc(deck.title)}</title><style>
@page { size: ${W}in ${H}in; margin: 0; }
body { margin:0; font-family:${HTML_FONT}; color:#${C.dark}; }
.slide { position:relative; width:${W}in; height:${H}in; overflow:hidden; page-break-after:always; }
td { border:0.75pt solid #${C.border}; padding:2pt 4pt; vertical-align:middle; box-sizing:border-box; }
</style></head><body>${pages}</body></html>`;
}

module.exports = { W, H, C, el, box, header, footer, renderPptx, renderHtml };
