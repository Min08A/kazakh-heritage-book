import { h, icon, fmtTime } from './dom.js';
import { asset } from './config.js';
import { audioUrlOf } from './data.js';

async function audioFileExists(url) {
  try {
    const r = await fetch(url, { method: 'HEAD', cache: 'no-cache' });
    if (!r.ok) return false;
    const t = (r.headers.get('content-type') || '').toLowerCase();
    return t.startsWith('audio/') || t.includes('mpeg') || t.includes('ogg');
  } catch {
    return false;
  }
}

const splitSentences = (text) => (text.match(/[^.!?]+[.!?]+["”']?|[^.!?]+$/g) || [text]).map((s) => s.trim()).filter(Boolean);

/**
 * Narration + transcript.
 * 1) If media/audio/<slug>.mp3 exists, a normal audio player is used.
 * 2) Otherwise the browser's built-in English speech synthesis reads the transcript (clearly labelled).
 * 3) If neither is available, the transcript is still shown.
 */
export function createNarration(obj) {
  const sentences = splitSentences(obj.transcript);
  const spans = sentences.map((s, i) => h('span.tr-s', { 'data-i': i }, s, ' '));
  const transcript = h('div.transcript', { id: 'transcript' }, h('p', null, spans));
  const root = h('section.narration', { 'aria-labelledby': 'narr-title' });
  const title = h('h2.sec-title', { id: 'narr-title' }, 'Listen');
  const note = h('p.narr-note');
  const controls = h('div.narr-controls');
  const trTitle = h('h3.sec-sub', null, 'Transcript');
  root.append(title, controls, note, trTitle, transcript);

  const mark = (i) => {
    spans.forEach((s, k) => s.classList.toggle('on', k === i));
    if (i >= 0 && spans[i]) spans[i].scrollIntoView?.({ block: 'nearest', behavior: 'smooth' });
  };

  function mountFile(url) {
    const a = new Audio();
    a.preload = 'none';
    a.src = url;
    const btn = h('button.btn.btn-primary.narr-btn', { type: 'button', 'aria-label': 'Play narration' }, icon('play', 18), h('span', null, 'Play narration'));
    const bar = h('input.narr-bar', { type: 'range', min: 0, max: 1000, value: 0, 'aria-label': 'Narration position' });
    const time = h('span.narr-time', null, '0:00');
    const setBtn = (playing) => {
      btn.replaceChildren(icon(playing ? 'pause' : 'play', 18), h('span', null, playing ? 'Pause' : a.currentTime > 0 && !a.ended ? 'Resume' : 'Play narration'));
      btn.setAttribute('aria-label', playing ? 'Pause narration' : 'Play narration');
    };
    btn.addEventListener('click', () => (a.paused ? a.play().catch(() => note.append(' The audio could not be played.')) : a.pause()));
    a.addEventListener('play', () => setBtn(true));
    a.addEventListener('pause', () => setBtn(false));
    a.addEventListener('ended', () => setBtn(false));
    a.addEventListener('timeupdate', () => {
      if (a.duration) bar.value = String(Math.round((a.currentTime / a.duration) * 1000));
      time.textContent = `${fmtTime(a.currentTime)} / ${fmtTime(a.duration)}`;
    });
    bar.addEventListener('input', () => { if (a.duration) a.currentTime = (Number(bar.value) / 1000) * a.duration; });
    controls.replaceChildren(btn, bar, time);
    note.textContent = 'Recorded audio narration.';
    trTitle.textContent = 'Text';
  }

  function mountSpeech() {
    const synth = window.speechSynthesis;
    let idx = 0;
    let playing = false;
    let token = 0;
    const btn = h('button.btn.btn-primary.narr-btn', { type: 'button', 'aria-label': 'Play narration' }, icon('play', 18), h('span', null, 'Play narration'));
    const restart = h('button.btn.btn-ghost', { type: 'button', onclick: () => { stop(); idx = 0; mark(-1); } }, icon('replay', 16), 'Restart');
    const setBtn = () => {
      btn.replaceChildren(icon(playing ? 'pause' : 'play', 18), h('span', null, playing ? 'Pause' : idx > 0 ? 'Resume' : 'Play narration'));
      btn.setAttribute('aria-label', playing ? 'Pause narration' : 'Play narration');
    };
    const pickVoice = () => {
      const vs = synth.getVoices();
      return vs.find((v) => /^en[-_]/i.test(v.lang) && v.localService) || vs.find((v) => /^en[-_]/i.test(v.lang)) || null;
    };
    function speakFrom(i) {
      const my = ++token;
      synth.cancel();
      if (i >= sentences.length) {
        playing = false;
        idx = 0;
        mark(-1);
        setBtn();
        return;
      }
      idx = i;
      mark(i);
      const u = new SpeechSynthesisUtterance(sentences[i]);
      u.lang = 'en-US';
      u.rate = 0.95;
      const v = pickVoice();
      if (v) u.voice = v;
      u.onend = () => { if (my === token && playing) speakFrom(i + 1); };
      u.onerror = (e) => {
        if (my !== token || e.error === 'canceled' || e.error === 'interrupted') return;
        playing = false;
        setBtn();
        note.textContent = 'The browser voice could not be started. You can still read the transcript below.';
      };
      synth.speak(u);
    }
    function stop() {
      token++;
      playing = false;
      synth.cancel();
      setBtn();
    }
    btn.addEventListener('click', () => {
      if (playing) {
        stop(); // pause: keep idx so "Resume" continues from this sentence
      } else {
        playing = true;
        setBtn();
        speakFrom(idx);
      }
    });
    window.addEventListener('pagehide', stop);
    document.addEventListener('visibilitychange', () => document.hidden && stop());
    controls.replaceChildren(btn, restart);
    note.textContent = 'Narration uses your browser’s built-in English voice (no recorded audio file is included). The transcript is below.';
  }

  (async () => {
    if (await audioFileExists(asset(audioUrlOf(obj)))) return mountFile(asset(audioUrlOf(obj)));
    if ('speechSynthesis' in window && 'SpeechSynthesisUtterance' in window) return mountSpeech();
    controls.hidden = true;
    note.textContent = 'Audio narration is not available in this browser. Please read the transcript below.';
  })();

  return root;
}
