// Gera PPTX + HTML de cada material, converte o HTML em PDF e checa se algum texto estoura a caixa.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { renderPptx, renderHtml } = require('./motor');
const { femvest, ficha, template, MARCOS_FEMVEST } = require('./decks');
const { chromium } = require(path.join(process.env.G, '@playwright/mcp/node_modules/playwright-core'));

const OUT = process.env.OUT;
const decks = [
  ['Case_01_FemVest', femvest()],
  ['Template_de_Case', template()],
  ['Ficha_de_Avaliacao_em_branco', ficha()],
];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  for (const [name, deck] of decks) {
    await renderPptx(deck, path.join(OUT, name + '.pptx'));
    const htmlFile = path.join(__dirname, name + '.html');
    fs.writeFileSync(htmlFile, renderHtml(deck));
    await page.goto('file://' + htmlFile);
    await page.waitForTimeout(300);
    const problems = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('.slide').forEach((s, si) => {
        s.querySelectorAll('.tx').forEach(t => {
          if (t.scrollHeight > t.clientHeight + 1) out.push(`slide ${si + 1}: texto estourou ${t.scrollHeight - t.clientHeight}px: "${t.innerText.slice(0, 50)}"`);
        });
        const sb = s.getBoundingClientRect();
        s.querySelectorAll('table').forEach(tb => {
          const r = tb.getBoundingClientRect();
          out.push(`slide ${si + 1}: tabela termina em y=${((r.bottom - sb.top) / 96).toFixed(2)}in`);
        });
      });
      return out;
    });
    console.log('==', name); problems.forEach(p => console.log('  ' + p));
    execFileSync(process.env.CHROME, ['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files', '--no-pdf-header-footer', `--print-to-pdf=${path.join(OUT, name + '.pdf')}`, 'file://' + htmlFile], { stdio: 'ignore' });
  }
  await browser.close();
})();
