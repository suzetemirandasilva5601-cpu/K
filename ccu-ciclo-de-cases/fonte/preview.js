// Renderiza as páginas de um PDF em PNG (pdf.js no Chromium) para conferência visual.
const path = require('path');
const fs = require('fs');
const { chromium } = require(path.join(process.env.G, '@playwright/mcp/node_modules/playwright-core'));

(async () => {
  const [, , pdfPath, outDir, scaleArg] = process.argv;
  fs.mkdirSync(outDir, { recursive: true });
  const data = fs.readFileSync(pdfPath).toString('base64');
  const browser = await chromium.launch({ executablePath: process.env.CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
  await page.setContent('<html><body style="margin:0"><canvas id="c"></canvas></body></html>');
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js' });
  const n = await page.evaluate(async (b64) => {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js';
    const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    window._doc = await pdfjsLib.getDocument({ data: bytes }).promise;
    return window._doc.numPages;
  }, data);
  for (let i = 1; i <= n; i++) {
    await page.evaluate(async ([i, sc]) => {
      const p = await window._doc.getPage(i);
      const vp = p.getViewport({ scale: sc });
      const c = document.getElementById('c');
      c.width = vp.width; c.height = vp.height;
      await p.render({ canvasContext: c.getContext('2d'), viewport: vp }).promise;
    }, [i, Number(scaleArg || 1.0)]);
    await page.locator('#c').screenshot({ path: path.join(outDir, `p${String(i).padStart(2, '0')}.png`) });
  }
  console.log('pages', n);
  await browser.close();
})();
