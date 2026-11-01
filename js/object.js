import { objects, bySlug, neighbours, coverOf } from './data.js';
import { h, icon } from './dom.js';
import { asset } from './config.js';
import { mount3D } from './model3d.js';
import { createNarration } from './audio.js';

const app = document.getElementById('app');

function slugFromLocation() {
  const q = new URLSearchParams(location.search).get('o');
  if (q) return q;
  const parts = location.pathname.split('/').filter(Boolean);
  const i = parts.indexOf('object');
  if (i >= 0 && parts[i + 1]) return decodeURIComponent(parts[i + 1]).replace(/\.html$/, '');
  return '';
}

const home = (hash = '') => asset('') + (hash ? `#${hash}` : '');
const objectUrl = (slug) => `/object/${slug}`;

function header() {
  return h('header.obj-top', null,
    h('a.brand', { href: home() }, h('span.brand-mark', { 'aria-hidden': true }, '❖'), h('span', null, 'Kazakh Heritage')),
    h('a.btn.btn-ghost.btn-small', { href: home('contents') }, icon('list', 15), 'Contents'),
  );
}

function notFound(slug) {
  document.title = 'Not found · Kazakh Heritage';
  app.replaceChildren(
    header(),
    h('main.obj-main', null,
      h('h1.obj-title', null, 'This page was not found'),
      h('p', null, slug ? `There is no object called “${slug}”.` : 'No object was specified.'),
      h('ul.obj-list', null, objects.map((o) => h('li', null, h('a', { href: objectUrl(o.slug) }, `${o.n}. ${o.title}`)))),
      h('a.btn.btn-primary', { href: home('contents') }, icon('book', 16), 'Back to the book'),
    ),
  );
}

function render(o) {
  const { prev, next } = neighbours(o.slug);
  document.title = `${o.title} (${o.native}) · Kazakh Heritage`;
  const meta = document.querySelector('meta[name="description"]');
  if (meta) meta.setAttribute('content', `${o.title}: ${o.summary} Explore the 3D model and listen to the story.`);

  const viewer = h('div.m3d', { 'aria-label': `3D model of ${o.title}` });
  const narration = createNarration(o);

  app.replaceChildren(
    header(),
    h('main.obj-main', null,
      h('p.kicker', null, `Chapter ${o.n} of ${objects.length}`),
      h('h1.obj-title', null, o.title, h('span.native', { lang: 'kk' }, o.native)),
      h('p.lead', null, o.subtitle),
      h('section.obj-section', { 'aria-label': '3D model' }, viewer),
      h('section.obj-section.card', null, narration),
      h('section.obj-section.card', null,
        h('h2.sec-title', null, 'About'),
        h('p.body', null, o.description),
        h('h3.sec-sub', null, 'Good to know'),
        h('ul.facts', null, o.facts.map((f) => h('li', null, f))),
      ),
      h('nav.obj-nav', { 'aria-label': 'Chapters' },
        prev ? h('a.btn.btn-ghost', { href: objectUrl(prev.slug) }, icon('left', 16), prev.title) : h('span'),
        h('a.btn.btn-primary', { href: home('contents') }, icon('book', 16), 'Back to contents'),
        next ? h('a.btn.btn-ghost', { href: objectUrl(next.slug) }, next.title, icon('right', 16)) : h('span'),
      ),
      h('a.obj-back-chapter', { href: home(o.slug) }, `Back to the “${o.title}” pages in the book`),
    ),
  );
  mount3D(viewer, o);
}

const slug = slugFromLocation();
const obj = bySlug(slug);
if (obj) render(obj);
else notFound(slug);
