// Builds the printable book (print/book.html) from js/data.js. Every page carries a QR code:
// chapter pages link to <SITE>/object/<slug> (the 3D page); other pages link into the online book.
// Usage: node print_book.mjs [https://your-site]      then print with tools/make_print.sh
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { objects, parts, chaptersOfPart, partOf } from '../js/data.js';
import { qrSvg } from '../js/qr.js';

const SITE = (process.argv[2] || 'https://kazakhheritage.netlify.app').replace(/\/+$/, '').replace(/\/?#.*$/, '');
const here = dirname(fileURLToPath(import.meta.url));
const OUT = join(here, '..', 'print', 'book.html');

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const topicHtml = (t) => esc(t).replace(/\[\[([^\]]+)\]\]/g, '<mark>$1</mark>');
const short = (url) => url.replace(/^https?:\/\//, '');
const qr = (url, label) => `<div class="qr">${qrSvg(url, { dark: '#2a1c12', title: label })}</div>`;

/* ------------------------------------------------------------------ page plan */
const pages = [];
const pageOf = new Map();
pages.push({ kind: 'cover' });
pages.push({ kind: 'contents' });
parts.forEach((p) => {
  pages.push({ kind: 'part', p });
  chaptersOfPart(p.id).forEach((o) => { pageOf.set(o.slug, pages.length + 1); pages.push({ kind: 'chapter', o }); });
});
const CREDIT_ROWS = 20;
for (let i = 0; i < objects.length; i += CREDIT_ROWS) pages.push({ kind: 'credits', rows: objects.slice(i, i + CREDIT_ROWS), first: i === 0 });
pages.push({ kind: 'back' });
const partPage = (id) => pages.findIndex((x) => x.kind === 'part' && x.p.id === id) + 1;

/* ------------------------------------------------------------------ pages */
const footer = (n, url, text) => `
  <footer class="foot">
    ${qr(url, text)}
    <div class="foot-text"><strong>${esc(text)}</strong><span>${esc(short(url))}</span></div>
    <span class="pageno">${n}</span>
  </footer>`;

function cover() {
  const url = `${SITE}/`;
  return `<section class="page cover">
    <div class="frame">
      <p class="kick">An interactive book</p>
      <h1 class="long">KAZAKH ETHNOGRAPHIC TERMS:<br>AN AI-BASED QR DICTIONARY</h1>
      <p class="native">Қазақ мұрасы</p>
      <div class="hero"><img src="../media/images/hero.svg" alt=""></div>
      <p class="sub">${objects.length} words of the steppe in two parts.<br>Read, scan the QR codes and explore every word in 3D.</p>
      <div class="cover-qr">${qr(url, 'Open the interactive book')}<p><strong>Open the interactive book</strong><br>${esc(short(url))}</p></div>
    </div>
  </section>`;
}

function contents(n) {
  const block = (p) => `
    <div class="toc-part"><span>${esc(p.label)}</span> ${esc(p.title)} <em lang="kk">${esc(p.native)}</em><b>${partPage(p.id)}</b></div>
    <ol class="toc">${chaptersOfPart(p.id).map((o) => `
      <li><span class="n">${o.n}</span><span class="t">${esc(o.title)}</span><span class="k"><span lang="kk">${esc(o.native)}</span> · <i>${esc(o.transcription)}</i></span><span class="dots"></span><span class="pg">${pageOf.get(o.slug)}</span></li>`).join('')}
    </ol>`;
  return `<section class="page">
    <div class="body">
      <p class="kicker">How to use this book</p>
      <div class="how">
        <div><b>1</b><p><strong>Read</strong> each word: its story, pictures and facts.</p></div>
        <div><b>2</b><p><strong>Scan</strong> the QR code at the bottom of the page with a phone camera.</p></div>
        <div><b>3</b><p><strong>Explore</strong> the 3D model and listen to the recorded word.</p></div>
      </div>
      <h2 class="title">Contents</h2>
      <div class="toc-cols">${parts.map(block).join('')}</div>
    </div>
    ${footer(n, `${SITE}/#contents`, 'Open the interactive book')}
  </section>`;
}

function partOpener(n, p) {
  const items = chaptersOfPart(p.id);
  return `<section class="page part">
    <div class="frame">
      <p class="part-label">${esc(p.label)}</p>
      <h2>${esc(p.title)}</h2>
      <p class="native" lang="kk">${esc(p.native)}</p>
      <div class="orn">❖</div>
      <p class="intro">${esc(p.intro)}</p>
      <ul class="chips ${items.length > 12 ? 'dense' : ''}">${items.map((o) => `<li><b>${o.n}</b><div class="cw">${esc(o.title)}<span><span lang="kk">${esc(o.native)}</span> · <i>${esc(o.transcription)}</i></span></div></li>`).join('')}</ul>
    </div>
    ${footer(n, `${SITE}/#part-${p.id}`, `${p.label} in the interactive book`)}
  </section>`;
}

function chapter(n, o) {
  const p = partOf(o);
  const url = `${SITE}/object/${o.slug}`;
  return `<section class="page chapter">
    <div class="body">
      <header class="ch-top"><span>${esc(p.label)} · ${esc(p.title)}</span><span>Chapter ${String(o.n).padStart(2, '0')} of ${objects.length}</span></header>
      <h2 class="title">${esc(o.title)} <span class="native"><span lang="kk">${esc(o.native)}</span> · <i>${esc(o.transcription)}</i></span></h2>
      <p class="subtitle">${esc(o.subtitle)}</p>
      <figure class="pic"><img src="images/${o.slug}.png" alt="Illustration: ${esc(o.title)}"></figure>
      <p class="desc">${esc(o.description)}</p>
      <h3>Good to know</h3>
      <ul class="facts">${o.facts.map((f) => `<li>${esc(f)}</li>`).join('')}</ul>
      <h3>The word in a sentence</h3>
      <p class="topic">${topicHtml(o.topic)}</p>
    </div>
    <footer class="foot big">
      ${qr(url, `3D model of ${o.title}`)}
      <div class="foot-text"><strong>Scan to explore ${esc(o.title)} in 3D</strong>
        <p>Turn the 3D model, listen to the recorded word and read more.</p>
        <span>${esc(short(url))}</span></div>
      <span class="pageno">${n}</span>
    </footer>
  </section>`;
}

function credits(n, { rows, first }) {
  const row = (o) => {
    const sf = o.model.sketchfab;
    const t = sf ? `“${esc(sf.title)}” by ${esc(sf.creator)} (Sketchfab) — ${esc(sf.license || 'license not stated on the model page')}` : 'Simplified model made for this project';
    return `<li><strong>${o.n}. ${esc(o.title)}:</strong> ${t}</li>`;
  };
  return `<section class="page credits">
    <div class="body">
      <p class="kicker">${first ? 'Credits' : 'Credits (continued)'}</p>
      ${first ? `<h2 class="title">About this book</h2>
      <p class="small">Illustrations were created for this project. The recorded narration and the 3D models are on the web pages that the QR codes open. Descriptions are written for general readers and are not a scholarly source.</p>` : ''}
      <h3>3D models</h3>
      <ul class="credit-list">${rows.map(row).join('')}</ul>
      <p class="small">Sketchfab models belong to their creators and are shown through the official Sketchfab viewer. Where a license is not stated on the model page, confirm the terms with the creator before publication.</p>
    </div>
    ${footer(n, `${SITE}/`, 'Open the interactive book')}
  </section>`;
}

function back(n) {
  const url = `${SITE}/`;
  return `<section class="page cover back">
    <div class="frame">
      <p class="kick">Thank you</p>
      <h1 class="small">Rakhmet</h1>
      <p class="native">Рақмет</p>
      <p class="sub">The interactive book has a short video, a 3D model and a recorded narration for every word.</p>
      <div class="cover-qr">${qr(url, 'Open the interactive book')}<p><strong>Open the interactive book</strong><br>${esc(short(url))}</p></div>
    </div>
  </section>`;
}

const html = pages.map((x, i) => {
  const n = i + 1;
  switch (x.kind) {
    case 'cover': return cover();
    case 'contents': return contents(n);
    case 'part': return partOpener(n, x.p);
    case 'chapter': return chapter(n, x.o);
    case 'credits': return credits(n, x);
    default: return back(n);
  }
}).join('\n');

writeFileSync(OUT, `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Kazakh Heritage — printable book</title>
<link rel="stylesheet" href="print.css">
</head><body>
${html}
</body></html>
`);
console.log(`${OUT}: ${pages.length} pages, QR base ${SITE}`);
