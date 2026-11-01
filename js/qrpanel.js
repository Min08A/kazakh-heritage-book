import { h, icon } from './dom.js';
import { qrSvg } from './qr.js';
import { getQrTarget } from './qrtarget.js';

/**
 * QR panel: locked until the chapter video has genuinely ended, then shows the QR code that opens
 * /object/<slug> (the mobile 3D page).
 */
export function createQrPanel(obj, initiallyUnlocked) {
  const root = h('div.qr-panel', { 'aria-live': 'polite' });
  let unlocked = false;

  function renderLocked() {
    root.className = 'qr-panel is-locked';
    root.replaceChildren(
      h('div.qr-lock', null, icon('lock', 26)),
      h('div.qr-text', null,
        h('strong', null, 'QR code locked'),
        h('p', null, 'Watch the whole video to the end and your QR code for the 3D model will appear here.'),
      ),
    );
  }

  function renderUnlocked() {
    const t = getQrTarget(obj.slug);
    root.className = 'qr-panel is-open';
    const box = h('div.qr-box', { html: qrSvg(t.url, { title: `QR code: open the 3D model of ${obj.title} on your phone` }) });
    const text = h('div.qr-text', null,
      h('strong', null, 'Scan with your phone'),
      h('p', null, `Opens the 3D model, audio narration and transcript for “${obj.title}”.`),
      h('a.qr-url', { href: t.url, target: '_blank', rel: 'noopener' }, t.url.replace(/^https?:\/\//, '')),
      h('a.btn.btn-small', { href: t.url, target: '_blank', rel: 'noopener' }, icon('cube', 15), 'Open 3D page'),
    );
    root.replaceChildren(box, text);
    if (t.warning) {
      root.append(h('p.qr-warn', { role: 'note' }, icon('warn', 15), t.warning));
    }
  }

  function setUnlocked(v) {
    if (v === unlocked && root.firstChild) return;
    unlocked = v;
    if (v) renderUnlocked();
    else renderLocked();
  }

  setUnlocked(!!initiallyUnlocked);
  return { el: root, setUnlocked, isUnlocked: () => unlocked };
}
