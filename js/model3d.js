import { h, icon } from './dom.js';
import { asset } from './config.js';
import { mountGlbViewer } from './glbviewer.js';

const SF_API = 'https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js';
const SF_API_VERSION = '1.12.1';

function loadScript(src, timeout = 9000) {
  return new Promise((resolve, reject) => {
    if (window.Sketchfab) return resolve();
    const s = document.createElement('script');
    s.src = src;
    s.async = true;
    const t = setTimeout(() => reject(new Error('timeout')), timeout);
    s.onload = () => { clearTimeout(t); resolve(); };
    s.onerror = () => { clearTimeout(t); reject(new Error('blocked')); };
    document.head.append(s);
  });
}

const sfEmbedUrl = (uid) =>
  `https://sketchfab.com/models/${uid}/embed?ui_ar=0&ui_ar_help=0&ui_ar_qrcode=0&ui_vr=0&dnt=1&ui_infos=1&ui_watermark=1`;

/**
 * Mounts the 3D model of an object into `root`.
 * Order: Sketchfab embed (if the object has one) -> local simplified model -> "not available" message.
 * There is no AR / WebXR anywhere: Sketchfab AR buttons are switched off and the local viewer has none.
 */
export function mount3D(root, obj) {
  const m = obj.model;
  const stage = h('div.m3d-stage');
  const status = h('p.m3d-status', { role: 'status' });
  const actions = h('div.m3d-actions');
  const credit = h('p.m3d-credit');
  root.replaceChildren(stage, status, actions, credit);
  let current = null; // { destroy }
  let hintTimer = null;

  const say = (msg, kind = '') => {
    status.textContent = msg || '';
    status.className = `m3d-status ${kind}`;
    status.hidden = !msg;
  };
  const clearStage = () => {
    clearTimeout(hintTimer);
    if (current && current.destroy) current.destroy();
    current = null;
    stage.replaceChildren();
  };

  function renderActions(mode) {
    actions.replaceChildren();
    if (m.sketchfab) {
      actions.append(
        h('a.btn.btn-ghost', { href: m.sketchfab.url, target: '_blank', rel: 'noopener noreferrer' }, icon('external', 16), 'Open on Sketchfab'),
      );
    } else if (m.searchUrl) {
      actions.append(
        h('a.btn.btn-ghost', { href: m.searchUrl, target: '_blank', rel: 'noopener noreferrer' }, icon('external', 16), 'Find more models on Sketchfab'),
      );
    }
    if (m.sketchfab && m.glb && mode === 'sketchfab') {
      actions.append(h('button.btn.btn-ghost', { type: 'button', onclick: () => showGlb('Showing the simplified model.') }, icon('cube', 16), 'Use simplified model'));
    }
    if (m.sketchfab && m.glb && mode === 'glb') {
      actions.append(h('button.btn.btn-ghost', { type: 'button', onclick: () => showSketchfab() }, icon('cube', 16), 'Show the Sketchfab model'));
    }
    if (mode === 'glb') {
      const v = current;
      let auto = true;
      const rot = h('button.btn.btn-ghost', { type: 'button', 'aria-pressed': 'true', onclick: () => {
        auto = !auto;
        rot.setAttribute('aria-pressed', String(auto));
        v && v.setAutoRotate && v.setAutoRotate(auto);
      } }, 'Auto-rotate');
      actions.append(rot, h('button.btn.btn-ghost', { type: 'button', onclick: () => v && v.reset && v.reset() }, 'Reset view'));
    }
  }

  function renderCredit(mode) {
    credit.replaceChildren();
    const sf = m.sketchfab;
    if (mode === 'sketchfab' && sf) {
      credit.append(
        h('strong', null, `“${sf.title}”`), ' by ',
        sf.creatorUrl ? h('a', { href: sf.creatorUrl, target: '_blank', rel: 'noopener noreferrer' }, sf.creator) : sf.creator,
        ' on ', h('a', { href: sf.url, target: '_blank', rel: 'noopener noreferrer' }, 'Sketchfab'),
        '. License: ', sf.license || 'not stated on the model page', '.',
      );
      if (sf.note) credit.append(h('span.m3d-credit-note', null, ' ', sf.note));
    } else if (mode === 'glb' && m.glb) {
      credit.append(m.glb.note || 'Simplified model generated for this project.');
    }
  }

  async function showGlb(message) {
    if (!m.glb) return showNone();
    clearStage();
    renderCredit('glb');
    say('Loading 3D model…');
    stage.classList.add('is-glb');
    try {
      current = await mountGlbViewer(stage, asset(m.glb.src), { alt: m.glb.alt });
      say(message || '');
      renderActions('glb');
      stage.append(h('p.m3d-hint', null, 'Drag to rotate · scroll or pinch to zoom · double-click to reset'));
    } catch (err) {
      console.warn('[model3d] local model failed:', err);
      stage.classList.remove('is-glb');
      current = null;
      stage.replaceChildren();
      say('The 3D model could not be displayed on this device (WebGL is needed).', 'warn');
      renderActions('none');
    }
  }

  function showNone() {
    clearStage();
    stage.classList.remove('is-glb');
    stage.append(h('div.m3d-soon', null, icon('cube', 36), h('p', null, 'The 3D model for this object is coming soon.')));
    say('');
    renderActions('none');
    renderCredit('none');
  }

  async function showSketchfab() {
    const sf = m.sketchfab;
    clearStage();
    stage.classList.remove('is-glb');
    renderCredit('sketchfab');
    say('Loading model from Sketchfab…');
    const iframe = h('iframe.m3d-frame', {
      title: `3D model: ${obj.title}`,
      allow: 'autoplay; fullscreen',
      allowfullscreen: true,
      referrerpolicy: 'strict-origin-when-cross-origin',
    });
    stage.append(iframe);
    renderActions('sketchfab');

    const fail = (why) => {
      console.warn('[model3d] Sketchfab failed:', why);
      if (m.glb) showGlb('The Sketchfab model could not be loaded, so a simplified model is shown instead.');
      else {
        clearStage();
        stage.append(h('div.m3d-soon', null, icon('warn', 32), h('p', null, 'The Sketchfab model could not be loaded.')));
        say('Try “Open on Sketchfab” below.', 'warn');
        renderActions('none');
      }
    };
    const slowHint = () => {
      hintTimer = setTimeout(() => say(m.glb ? 'Taking a while? Try “Use simplified model” below, or open the model on Sketchfab.' : 'Taking a while? Check your connection or open the model on Sketchfab.', 'warn'), 15000);
    };

    let api = false;
    try {
      await loadScript(SF_API);
      api = true;
    } catch {
      api = false;
    }
    if (!stage.contains(iframe)) return; // user switched view meanwhile
    if (api && window.Sketchfab) {
      try {
        const client = new window.Sketchfab(SF_API_VERSION, iframe);
        client.init(sf.uid, {
          success: (a) => {
            a.start();
            a.addEventListener('viewerready', () => {
              clearTimeout(hintTimer);
              say('');
            });
          },
          error: () => fail('viewer error'),
          ui_ar: 0, ui_vr: 0, ui_ar_help: 0, ui_ar_qrcode: 0, dnt: 1, ui_infos: 1, ui_watermark: 1,
        });
        slowHint();
        return;
      } catch (err) {
        console.warn('[model3d] Sketchfab API failed, using plain embed', err);
      }
    }
    // Plain iframe embed (works without the API script).
    iframe.src = sfEmbedUrl(sf.uid);
    iframe.addEventListener('load', () => say(''), { once: true });
    slowHint();
  }

  if (m.sketchfab) showSketchfab();
  else if (m.glb) showGlb();
  else showNone();

  return { destroy: clearStage };
}
