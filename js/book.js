import { objects, parts, chaptersOfPart, partOf } from './data.js';
import { h, icon, topicNodes } from './dom.js';
import { asset } from './config.js';
import { createVideoPlayer } from './video.js';
import { createQrPanel } from './qrpanel.js';
import { getCompleted, isCompleted, markCompleted, resetProgress, onProgress } from './progress.js';

/*
 * The page list is built from data.js, so chapters can be added or reordered freely:
 *   cover | welcome | contents (several pages)
 *   for each part: part opener (left) + part overview (right), then per chapter: video+QR (left) + text (right)
 *   credits (several pages) | back cover | blank (back of the last leaf, never shown)
 * Desktop ("spread" mode): a leaf has two faces: page 2k on the front, page 2k+1 on the back.
 *   state s = number of turned leaves; visible = pages (2s-1, 2s). s=0 shows the closed cover.
 *   So every odd page is a left-hand page: part openers and chapter video pages must be odd.
 * Phone ("single" mode): one page per leaf; state p = number of turned leaves = index of the visible page.
 */

const MODES = {
  spread: { pw: 540, ph: 760 },
  single: { pw: 400, ph: 780 },
};

/* Contents: rows per contents page (the first page also holds the page title). */
const TOC_ROWS = [11, 13, 13, 13, 13];
/* Credits: model rows per credits page (the first page also holds the introduction). */
const CREDIT_ROWS = [10, 13, 13, 13, 13];

function chunk(items, sizes) {
  const out = [];
  let i = 0;
  let k = 0;
  while (i < items.length) {
    const n = sizes[Math.min(k, sizes.length - 1)];
    out.push(items.slice(i, i + n));
    i += n;
    k += 1;
  }
  return out.length ? out : [[]];
}

/** Build the ordered page plan, inserting a filler page wherever needed to keep left/right parity. */
function planPages() {
  const plan = [{ kind: 'cover' }, { kind: 'welcome' }];
  const tocRows = [];
  parts.forEach((p) => {
    tocRows.push({ part: p });
    chaptersOfPart(p.id).forEach((o) => tocRows.push({ o }));
  });
  const tocPages = chunk(tocRows, TOC_ROWS);
  tocPages.forEach((rows, i) => plan.push({ kind: 'contents', rows, first: i === 0, last: i === tocPages.length - 1 }));
  const padToOdd = () => { if (plan.length % 2 === 0) plan.push({ kind: 'note' }); };
  parts.forEach((p) => {
    padToOdd();
    plan.push({ kind: 'part', part: p }, { kind: 'part-list', part: p });
    chaptersOfPart(p.id).forEach((o) => plan.push({ kind: 'video', o }, { kind: 'text', o }));
  });
  padToOdd();
  const creditPages = chunk(objects, CREDIT_ROWS);
  // credits + back cover must end on an even page (the back cover is the front of the last leaf)
  creditPages.forEach((rows, i) => plan.push({ kind: 'credits', rows, first: i === 0 }));
  if (plan.length % 2 === 1) plan.push({ kind: 'note' });
  plan.push({ kind: 'back' }, { kind: 'blank' });
  return plan;
}

export function createBook(root) {
  const mql = window.matchMedia('(max-width: 899px)');
  let mode = mql.matches ? 'single' : 'spread';
  let state = 0;
  let leaves = [];
  let finalizeTimer = null;

  const plan = planPages();
  const TOTAL_PAGES = plan.length;
  const LAST_PAGE = TOTAL_PAGES - 2;
  const P = {
    cover: 0,
    welcome: 1,
    contents: 2,
    back: LAST_PAGE,
    credits: plan.findIndex((x) => x.kind === 'credits'),
  };
  const videoPageOf = new Map();
  const partPageOf = new Map();
  plan.forEach((x, i) => {
    if (x.kind === 'video') videoPageOf.set(x.o.slug, i);
    if (x.kind === 'part') partPageOf.set(x.part.id, i);
  });
  const videoPage = (c) => videoPageOf.get(objects[c].slug);
  const chapterOfPage = (pg) => {
    const x = plan[pg];
    if (!x || (x.kind !== 'video' && x.kind !== 'text')) return -1;
    return objects.indexOf(x.o);
  };

  /* ------------------------------------------------------------------ pages */
  const players = [];
  const qrs = [];
  const refreshers = [];
  const pages = new Array(TOTAL_PAGES);

  const pageShell = (index, cls, ...kids) =>
    h(`section.page.${cls}`, { 'data-page': index, 'aria-label': `Page ${index}` },
      h('div.page-inner', null, ...kids),
      index > 0 && index <= LAST_PAGE - 1 ? h('span.pageno', null, String(index)) : null,
    );

  function buildCover() {
    return h('section.page.page-cover', { 'data-page': 0, 'aria-label': 'Book cover' },
      h('div.cover-frame', null,
        h('p.cover-kicker', null, 'An interactive book'),
        h('h1.cover-title.long', null, 'KAZAKH ETHNOGRAPHIC TERMS:', h('br'), 'AN AI-BASED QR DICTIONARY'),
        h('p.cover-native', { lang: 'kk' }, 'Қазақ мұрасы'),
        h('div.cover-art', null, h('img', { src: asset('media/images/hero.svg'), alt: 'Illustration of a yurt and a dombyra', width: 640, height: 460 })),
        h('p.cover-sub', null, `${objects.length} words of the steppe — watch, scan, explore in 3D`),
        h('button.btn.btn-gold', { type: 'button', onclick: () => goToPage(P.welcome) }, 'Open the book', icon('right', 16)),
      ),
    );
  }

  function buildWelcome(idx) {
    const done = h('strong.progress-count', null, '0');
    const steps = [
      ['1', 'Watch', 'Each chapter has a short illustrated video on the left page.'],
      ['2', 'Scan', 'When the video ends, a QR code appears. Scan it with your phone.'],
      ['3', 'Explore', 'Turn the 3D model, listen to the recorded word and read about it.'],
    ];
    const el = pageShell(idx, 'page-welcome',
      h('p.kicker', null, 'Welcome'),
      h('h2.page-title', null, 'A book you can turn, watch and scan'),
      h('p.lead', null, `Kazakh Heritage presents ${objects.length} words from life on the steppe, in two parts: ${parts.map((p) => `${p.label}, ${p.title}`).join(', and ')}.`),
      h('ol.how', null, steps.map(([n, t, d]) => h('li', null, h('span.how-n', null, n), h('div', null, h('strong', null, t), h('p', null, d))))),
      h('div.progress-box', null,
        h('p', null, done, ' of ', String(objects.length), ' chapters watched'),
        h('div.meter', null, h('div.meter-fill')),
      ),
      h('p.tip', null, 'Turn pages with the arrows, the keyboard (← →), by swiping, or by clicking the page edges.'),
    );
    refreshers.push(() => {
      const n = getCompleted().filter((s) => objects.some((o) => o.slug === s)).length;
      done.textContent = String(n);
      el.querySelector('.meter-fill').style.width = `${(n / objects.length) * 100}%`;
    });
    return el;
  }

  const tocItem = (o) => h('li', null, h('button.toc-item', { type: 'button', 'data-slug': o.slug, onclick: () => goToChapter(objects.indexOf(o)) },
    h('span.toc-n', null, String(o.n)),
    h('span.toc-main', null, h('strong', null, o.title), h('span.toc-native', { lang: 'kk' }, o.native), h('span.toc-sum', null, o.summary)),
    h('span.toc-state', { 'aria-hidden': true }),
  ));

  function refreshTocItems(el) {
    const done = new Set(getCompleted());
    el.querySelectorAll('.toc-item').forEach((b) => {
      const d = done.has(b.dataset.slug);
      b.classList.toggle('done', d);
      b.querySelector('.toc-state').replaceChildren(d ? icon('check', 16) : '');
      b.setAttribute('aria-label', `Chapter ${b.querySelector('.toc-n').textContent}: ${b.querySelector('strong').textContent}${d ? ', watched' : ''}`);
    });
  }

  function buildContents(idx, { rows, first, last }) {
    const list = [];
    let ol = null;
    rows.forEach((r) => {
      if (r.part) {
        list.push(h('button.toc-part', { type: 'button', onclick: () => goToPage(partPageOf.get(r.part.id)) },
          h('span.toc-part-label', null, r.part.label), h('span.toc-part-title', null, r.part.title)));
        ol = null;
      } else {
        if (!ol) { ol = h('ol.toc.toc-compact', { start: r.o.n }); list.push(ol); }
        ol.append(tocItem(r.o));
      }
    });
    const el = pageShell(idx, 'page-contents',
      first ? h('p.kicker', null, 'Contents') : h('p.kicker', null, 'Contents (continued)'),
      first ? h('h2.page-title', null, `${objects.length} words of the steppe`) : null,
      ...list,
      !last ? null : h('button.btn.btn-ghost.reset', { type: 'button', onclick: () => { if (confirm('Reset your viewing progress on this device?')) resetProgress(); } }, 'Reset my progress'),
    );
    refreshers.push(() => refreshTocItems(el));
    return el;
  }

  function buildPart(idx, p) {
    const n = chaptersOfPart(p.id).length;
    return pageShell(idx, 'page-part',
      h('div.part-frame', null,
        h('p.part-label', null, p.label),
        h('h2.part-title', null, p.title),
        h('p.part-native', { lang: 'kk' }, p.native),
        h('div.part-orn', { 'aria-hidden': true }, '❖'),
        h('p.part-intro', null, p.intro),
        h('p.part-count', null, `${n} chapters`),
      ),
    );
  }

  function buildPartList(idx, p) {
    const items = chaptersOfPart(p.id);
    const grid = h('ul.part-grid', { class: items.length > 12 ? 'part-grid dense' : 'part-grid' }, items.map((o) =>
      h('li', null, h('button.part-chip', { type: 'button', 'data-slug': o.slug, onclick: () => goToChapter(objects.indexOf(o)) },
        h('span.chip-n', null, String(o.n)),
        h('span.chip-main', null, h('strong', null, o.title), h('span', { lang: 'kk' }, `${o.native} · ${o.transcription}`)),
      ))));
    const el = pageShell(idx, 'page-part-list',
      h('p.kicker', null, `${p.label} · In this part`),
      h('h2.page-title', null, p.title, h('span.native', { lang: 'kk' }, p.native)),
      grid,
      h('p.tip', null, 'Choose a word, or turn the page to start from the first chapter.'),
    );
    refreshers.push(() => {
      const done = new Set(getCompleted());
      el.querySelectorAll('.part-chip').forEach((b) => b.classList.toggle('done', done.has(b.dataset.slug)));
    });
    return el;
  }

  function buildVideoPage(idx, o) {
    const c = objects.indexOf(o);
    const qr = createQrPanel(o, isCompleted(o.slug));
    const player = createVideoPlayer(o, {
      onEnded: (simulated) => {
        if (!simulated) markCompleted(o.slug);
        qr.setUnlocked(true);
      },
    });
    players[c] = player;
    qrs[c] = qr;
    return pageShell(idx, 'page-video',
      h('header.ch-head', null,
        h('p.kicker', null, `${partOf(o).label} · Chapter ${o.n} of ${objects.length}`),
        h('h2.page-title', null, o.title, h('span.native', null, h('span', { lang: 'kk' }, o.native), h('span.transcr', null, ' · ', o.transcription))),
      ),
      player.el,
      h('p.vcaption', null, h('strong', null, o.subtitle + '. '), o.summary),
      h('button.btn.btn-ghost.only-single', { type: 'button', onclick: () => turn(1) }, `Read about the ${o.title}`, icon('right', 16)),
      qr.el,
    );
  }

  function buildTextPage(idx, o) {
    const c = objects.indexOf(o);
    const prev = c > 0 ? objects[c - 1] : null;
    const next = c < objects.length - 1 ? objects[c + 1] : null;
    return pageShell(idx, 'page-text',
      h('div.orn', { 'aria-hidden': true }, '❖'),
      h('p.kicker', null, `${o.title} · ${o.native} · ${o.transcription}`),
      h('h3.page-sub', null, o.subtitle),
      h('p.body', null, o.description),
      h('h4.facts-title', null, 'Good to know'),
      h('ul.facts', null, o.facts.map((f) => h('li', null, f))),
      h('h4.facts-title', null, 'The word in a sentence'),
      h('p.topic', null, topicNodes(o.topic)),
      h('div.ch-nav', null,
        prev ? h('button.link', { type: 'button', onclick: () => goToChapter(c - 1) }, icon('left', 14), prev.title) : h('span'),
        h('button.link', { type: 'button', onclick: () => goToPage(P.contents) }, icon('list', 14), 'Contents'),
        next ? h('button.link', { type: 'button', onclick: () => goToChapter(c + 1) }, next.title, icon('right', 14)) : h('span'),
      ),
    );
  }

  function creditRow(o) {
    const sf = o.model.sketchfab;
    const text = sf
      ? `“${sf.title}” by ${sf.creator} (Sketchfab) — ${sf.license || 'license not stated on the model page'}`
      : o.model.glb ? 'Simplified model made for this project' : '—';
    return h('li', null, h('strong', null, `${o.n}. ${o.title}: `), text);
  }

  function buildCredits(idx, { rows, first }) {
    return pageShell(idx, 'page-credits',
      h('p.kicker', null, first ? 'Credits' : 'Credits (continued)'),
      first ? h('h2.page-title', null, 'About this book') : null,
      first ? h('p.small', null, 'Illustrations, animations and music in the videos were created for this project; the videos have no spoken voice. The recorded narration on each 3D page was made for this book. Descriptions are written for general readers and are not a scholarly source.') : null,
      h('h4.facts-title', null, '3D models'),
      h('ul.credit-list', null, rows.map(creditRow)),
      h('p.small', null, 'Sketchfab models belong to their creators and are shown through the official Sketchfab viewer. Where a license is not stated on the model page, confirm the terms with the creator before a public launch.'),
    );
  }

  function buildNote(idx) {
    return pageShell(idx, 'page-note', h('div.note-orn', { 'aria-hidden': true }, '❖'));
  }

  function buildBack(idx) {
    return h('section.page.page-back', { 'data-page': idx, 'aria-label': 'Back cover' },
      h('div.cover-frame', null,
        h('p.cover-kicker', null, 'Thank you'),
        h('h2.cover-title.small', null, 'Rakhmet'),
        h('p.cover-native', { lang: 'kk' }, 'Рақмет'),
        h('p.cover-sub', null, 'Come back to any chapter at any time.'),
        h('button.btn.btn-gold', { type: 'button', onclick: () => goToPage(P.contents) }, icon('list', 16), 'Back to contents'),
        h('button.btn.btn-gold-ghost', { type: 'button', onclick: () => goToPage(P.cover) }, 'Close the book'),
      ),
    );
  }

  plan.forEach((x, i) => {
    switch (x.kind) {
      case 'cover': pages[i] = buildCover(); break;
      case 'welcome': pages[i] = buildWelcome(i); break;
      case 'contents': pages[i] = buildContents(i, x); break;
      case 'part': pages[i] = buildPart(i, x.part); break;
      case 'part-list': pages[i] = buildPartList(i, x.part); break;
      case 'video': pages[i] = buildVideoPage(i, x.o); break;
      case 'text': pages[i] = buildTextPage(i, x.o); break;
      case 'credits': pages[i] = buildCredits(i, x); break;
      case 'note': pages[i] = buildNote(i); break;
      case 'back': pages[i] = buildBack(i); break;
      default: pages[i] = h('section.page.page-blank', { 'data-page': i, 'aria-hidden': true });
    }
  });
  const refreshAll = () => refreshers.forEach((f) => f());
  refreshAll();

  /* ----------------------------------------------------------------- shell */
  const book = h('div.book');
  const viewport = h('div.book-viewport', null, book);
  const status = h('p.book-status', { 'aria-live': 'polite' });
  const prevBtn = h('button.nav-btn', { type: 'button', 'aria-label': 'Previous page', onclick: () => turn(-1) }, icon('left', 20), h('span', null, 'Previous'));
  const nextBtn = h('button.nav-btn', { type: 'button', 'aria-label': 'Next page', onclick: () => turn(1) }, h('span', null, 'Next'), icon('right', 20));
  const dotEls = [];
  const dots = h('div.dots', { role: 'group', 'aria-label': 'Chapters' },
    parts.map((p) => h('div.dot-group', null,
      h('button.dot-part', { type: 'button', title: `${p.label}: ${p.title}`, onclick: () => goToPage(partPageOf.get(p.id)) }, String(p.id)),
      chaptersOfPart(p.id).map((o) => {
        const d = h('button.dot', { type: 'button', 'data-slug': o.slug, title: `${o.n}. ${o.title}`, onclick: () => goToChapter(objects.indexOf(o)) });
        dotEls[objects.indexOf(o)] = d;
        return d;
      }),
    )));
  const homeBtn = h('button.nav-btn.nav-contents', { type: 'button', 'aria-label': 'Contents', onclick: () => goToPage(P.contents) }, icon('list', 18), h('span', null, 'Contents'));
  const bar = h('nav.book-bar', { 'aria-label': 'Book navigation' }, prevBtn, h('div.bar-mid', null, dots, status), nextBtn);
  const top = h('header.book-top', null,
    h('a.brand', { href: asset(''), 'aria-label': 'Kazakh Heritage — home' }, h('span.brand-mark', { 'aria-hidden': true }, '❖'), h('span', null, 'Kazakh Heritage')),
    homeBtn,
  );
  root.append(top, viewport, bar);
  root.classList.add('book-app');

  /* ----------------------------------------------------------- leaf layout */
  const leafCount = () => (mode === 'spread' ? TOTAL_PAGES / 2 : LAST_PAGE + 1);
  const maxState = () => leafCount() - 1;
  const pageToState = (pg) => (mode === 'spread' ? (pg === 0 ? 0 : Math.ceil(pg / 2)) : pg);
  const visiblePages = () => {
    if (mode === 'single') return [state];
    return state === 0 ? [0] : [2 * state - 1, 2 * state];
  };
  const primaryPage = () => (mode === 'single' ? state : state === 0 ? 0 : 2 * state - 1);

  function layout() {
    clearTimeout(finalizeTimer);
    players.forEach((p) => p.pause());
    book.replaceChildren();
    book.className = `book mode-${mode}`;
    const { pw, ph } = MODES[mode];
    book.style.setProperty('--pw', `${pw}px`);
    book.style.setProperty('--ph', `${ph}px`);
    book.style.width = `${mode === 'spread' ? pw * 2 : pw}px`;
    book.style.height = `${ph}px`;
    leaves = [];
    const n = leafCount();
    for (let i = 0; i < n; i++) {
      const front = h('div.face.front');
      const back = h('div.face.back');
      const leaf = h('div.leaf', null, front, back);
      if (mode === 'spread') {
        front.append(pages[2 * i]);
        back.append(pages[2 * i + 1]);
      } else {
        front.append(pages[i]);
      }
      book.append(leaf);
      leaves.push(leaf);
    }
    const zl = h('button.zone.zone-left', { type: 'button', 'aria-label': 'Previous page', tabindex: -1, onclick: () => turn(-1) });
    const zr = h('button.zone.zone-right', { type: 'button', 'aria-label': 'Next page', tabindex: -1, onclick: () => turn(1) });
    if (mode === 'spread') book.append(zl, zr);
    applyState(true);
    fit();
  }

  function setZ(i) {
    return i < state ? i + 1 : leafCount() - i;
  }

  /* Leaves far from the current one are hidden so that dozens of pages stay cheap to render. */
  const NEAR = 3;
  function updateVisibility(from) {
    const lo = Math.min(from, state) - NEAR;
    const hi = Math.max(from, state) + NEAR;
    leaves.forEach((leaf, i) => leaf.classList.toggle('far', i < lo || i > hi));
  }

  function applyState(immediate, from = state) {
    const n = leafCount();
    book.classList.toggle('no-anim', !!immediate);
    const lo = Math.min(from, state);
    const hi = Math.max(from, state);
    const dir = state >= from ? 1 : -1;
    const count = Math.max(1, hi - lo);
    const stagger = immediate ? 0 : Math.min(80, 420 / count);
    updateVisibility(from);
    leaves.forEach((leaf, i) => {
      leaf.classList.toggle('flipped', i < state);
      if (immediate || i < lo || i >= hi) {
        leaf.style.transitionDelay = '0ms';
        leaf.style.zIndex = String(setZ(i));
      } else {
        const k = dir > 0 ? i - lo : hi - 1 - i;
        leaf.style.transitionDelay = `${k * stagger}ms`;
        leaf.style.zIndex = String(100 + (dir > 0 ? i : n - i));
      }
    });
    book.classList.toggle('is-closed', mode === 'spread' && state === 0);
    book.classList.toggle('at-end', state === maxState());
    positionBook();
    updatePagesState();
    updateBar();
    clearTimeout(finalizeTimer);
    if (!immediate) {
      finalizeTimer = setTimeout(() => {
        leaves.forEach((leaf, i) => {
          leaf.style.zIndex = String(setZ(i));
          leaf.style.transitionDelay = '0ms';
        });
        updateVisibility(state);
      }, 900 + count * stagger);
    }
  }

  function updatePagesState() {
    const vis = visiblePages();
    pages.forEach((pg, i) => {
      const on = vis.includes(i);
      pg.inert = !on;
      pg.setAttribute('aria-hidden', on ? 'false' : 'true');
    });
    players.forEach((pl, c) => { if (!vis.includes(videoPage(c))) pl.pause(); });
  }

  /* ------------------------------------------------------------ navigation */
  function turn(d) {
    goState(state + d);
  }
  function goState(target) {
    target = Math.max(0, Math.min(maxState(), target));
    if (target === state) return;
    const from = state;
    state = target;
    applyState(false, from);
    syncHash();
  }
  function goToPage(pg) {
    goState(pageToState(Math.max(0, Math.min(LAST_PAGE, pg))));
  }
  function goToChapter(c) {
    goToPage(videoPage(c));
  }

  function currentChapter() {
    for (const pg of visiblePages()) {
      const c = chapterOfPage(pg);
      if (c >= 0) return c;
    }
    return -1;
  }
  function currentPart() {
    for (const pg of visiblePages()) {
      const x = plan[pg];
      if (x && x.part) return x.part;
      if (x && x.o) return partOf(x.o);
    }
    return null;
  }

  function describe() {
    const vis = visiblePages();
    const c = currentChapter();
    if (vis.includes(0)) return 'Cover';
    if (c >= 0) return `${partOf(objects[c]).label} · Chapter ${objects[c].n}: ${objects[c].title}`;
    const kinds = vis.map((i) => plan[i] && plan[i].kind);
    const p = currentPart();
    if (kinds.includes('part') || kinds.includes('part-list')) return `${p.label}: ${p.title}`;
    if (kinds.includes('welcome')) return kinds.includes('contents') ? 'Welcome · Contents' : 'Welcome';
    if (kinds.includes('contents')) return 'Contents';
    if (kinds.includes('credits')) return 'Credits';
    return 'Back cover';
  }

  function updateBar() {
    prevBtn.disabled = state === 0;
    nextBtn.disabled = state === maxState();
    const vis = visiblePages();
    const pgLabel = vis.length === 2 ? `Pages ${vis[0]}–${vis[1]}` : vis[0] === 0 ? '' : `Page ${vis[0]}`;
    status.textContent = [describe(), pgLabel].filter(Boolean).join(' · ');
    const done = new Set(getCompleted());
    const c = currentChapter();
    dotEls.forEach((d, i) => {
      d.classList.toggle('done', done.has(d.dataset.slug));
      d.classList.toggle('current', i === c);
      d.setAttribute('aria-current', i === c ? 'true' : 'false');
      d.setAttribute('aria-label', `Chapter ${objects[i].n}: ${objects[i].title}${done.has(d.dataset.slug) ? ', watched' : ''}`);
    });
    if (c >= 0 && dots.scrollWidth > dots.clientWidth) {
      const d = dotEls[c];
      dots.scrollTo({ left: d.offsetLeft - dots.clientWidth / 2, behavior: 'smooth' });
    }
  }

  function syncHash() {
    const c = currentChapter();
    const vis = visiblePages();
    const kinds = vis.map((i) => plan[i] && plan[i].kind);
    let hash = '';
    if (c >= 0) hash = `#${objects[c].slug}`;
    else if (kinds.includes('part')) hash = `#part-${currentPart().id}`;
    else if (kinds.includes('welcome') || kinds.includes('contents')) hash = '#contents';
    try {
      if (hash !== location.hash) history.replaceState(null, '', location.pathname + location.search + hash);
    } catch { /* ignore */ }
  }

  function applyHash() {
    const id = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (!id || id === 'cover') return goToPage(P.cover);
    if (id === 'contents') return goToPage(P.contents);
    const pm = /^part-(\d+)$/.exec(id);
    if (pm && partPageOf.has(Number(pm[1]))) return goToPage(partPageOf.get(Number(pm[1])));
    const c = objects.findIndex((o) => o.slug === id);
    if (c >= 0) goToChapter(c);
  }

  /* ----------------------------------------------------------- sizing/fit */
  let scale = 1;
  function fit() {
    const { pw, ph } = MODES[mode];
    const bw = mode === 'spread' ? pw * 2 : pw;
    const r = viewport.getBoundingClientRect();
    scale = Math.max(0.2, Math.min((r.width - 16) / bw, (r.height - 10) / ph, 1.25));
    positionBook();
  }
  function positionBook() {
    const { pw } = MODES[mode];
    const shift = mode === 'spread' && state === 0 ? -pw / 2 : 0;
    book.style.transform = `translate(-50%, -50%) scale(${scale}) translateX(${shift}px)`;
  }
  new ResizeObserver(fit).observe(viewport);

  mql.addEventListener('change', () => {
    const pg = primaryPage();
    mode = mql.matches ? 'single' : 'spread';
    state = pageToState(pg);
    layout();
  });

  /* -------------------------------------------------- input: keys & swipe */
  document.addEventListener('keydown', (e) => {
    if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
    const t = e.target;
    const tag = t && t.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); turn(1); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); turn(-1); }
  });

  let sw = null;
  viewport.addEventListener('pointerdown', (e) => {
    // swipe-to-turn is for touch/pen only, and never starts on controls, media or links
    if (e.pointerType === 'mouse' || e.target.closest('input, button, a, video, iframe, canvas, .vcontrols')) {
      sw = null;
      return;
    }
    sw = { x: e.clientX, y: e.clientY, t: performance.now() };
  });
  viewport.addEventListener('pointerup', (e) => {
    if (!sw) return;
    const dx = e.clientX - sw.x;
    const dy = e.clientY - sw.y;
    const dt = performance.now() - sw.t;
    sw = null;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.6 && dt < 900) turn(dx < 0 ? 1 : -1);
  });
  viewport.addEventListener('pointercancel', () => { sw = null; });

  /* -------------------------------------------------------------- progress */
  onProgress((e) => {
    refreshAll();
    const wasReset = e && e.detail && e.detail.slug === null;
    objects.forEach((o, c) => {
      if (wasReset) qrs[c].setUnlocked(false);
      else if (isCompleted(o.slug)) qrs[c].setUnlocked(true);
    });
    updateBar();
  });

  layout();
  applyHash();
  window.addEventListener('hashchange', applyHash);

  return { goToPage, goToChapter, turn, get state() { return state; }, plan };
}
