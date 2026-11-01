import { h, icon, fmtTime } from './dom.js';
import { asset, isDevHost } from './config.js';
import { videoSources, coverOf } from './data.js';
import { isCompleted } from './progress.js';

/**
 * Chapter video player with custom controls.
 * `onEnded(simulated)` is called ONLY from the video's real `ended` event
 * (or from the development-only "simulate end" button, which passes simulated = true).
 */
export function createVideoPlayer(obj, { onEnded }) {
  const src = videoSources(obj);
  const video = h('video.vid', {
    preload: 'none',
    playsinline: true,
    poster: asset(coverOf(obj)),
    'aria-label': `Video: ${obj.title}`,
    controlslist: 'nodownload noremoteplayback',
  });
  const sMp4 = h('source', { src: asset(src.mp4), type: 'video/mp4; codecs="avc1.640028, mp4a.40.2"' });
  const sWebm = h('source', { src: asset(src.webm), type: 'video/webm; codecs="vp9, opus"' });
  video.append(sMp4, sWebm);

  let maxWatched = 0;
  let failed = 0;
  let seeking = false;
  const unlockedSeek = () => isCompleted(obj.slug);

  const big = h('button.vbig', { type: 'button', 'aria-label': `Play video: ${obj.title}` }, icon('play', 34));
  const missing = h('div.vmissing', { hidden: true, role: 'alert' },
    icon('warn', 28),
    h('p', null, 'The video for this chapter could not be loaded.'),
    h('button.btn.btn-ghost', { type: 'button', onclick: () => { failed = 0; missing.hidden = true; video.load(); video.play().catch(() => {}); } }, 'Try again'),
    isDevHost() ? h('p.vdev', null, `Missing file? Expected ${src.mp4} and ${src.webm} — run tools/render.py.`) : null,
  );
  const playBtn = h('button.vbtn', { type: 'button', 'aria-label': 'Play' }, icon('play', 18));
  const bar = h('input.vbar', { type: 'range', min: 0, max: 1000, value: 0, step: 1, 'aria-label': 'Video position' });
  const time = h('span.vtime', null, '0:00');
  const muteBtn = h('button.vbtn', { type: 'button', 'aria-label': 'Mute' }, icon('volume', 18));
  const fsBtn = h('button.vbtn', { type: 'button', 'aria-label': 'Full screen' }, icon('full', 18));
  const dev = isDevHost()
    ? h('button.vdevbtn', { type: 'button', title: 'Development only: shows the QR code for this session without saving progress.', onclick: () => onEnded(true) }, 'DEV: simulate end')
    : null;
  const controls = h('div.vcontrols', null, playBtn, bar, time, muteBtn, fsBtn);
  const wrap = h('div.vwrap', null, video, big, missing, controls);
  const el = h('div.player', null, wrap, dev);

  const setPlayIcon = (playing, ended = false) => {
    playBtn.replaceChildren(icon(playing ? 'pause' : ended ? 'replay' : 'play', 18));
    playBtn.setAttribute('aria-label', playing ? 'Pause' : ended ? 'Replay' : 'Play');
    big.replaceChildren(icon(ended ? 'replay' : 'play', 34));
    big.setAttribute('aria-label', ended ? `Replay video: ${obj.title}` : `Play video: ${obj.title}`);
    wrap.classList.toggle('is-playing', playing);
  };
  const paintBar = () => {
    const v = Number(bar.value) / 10;
    bar.style.setProperty('--v', `${v}%`);
  };

  const toggle = () => {
    if (video.ended) video.currentTime = 0;
    if (video.paused) video.play().catch(() => {});
    else video.pause();
  };
  big.addEventListener('click', toggle);
  playBtn.addEventListener('click', toggle);
  video.addEventListener('click', toggle);

  video.addEventListener('play', () => { setPlayIcon(true); wrap.classList.add('started'); });
  video.addEventListener('pause', () => setPlayIcon(false, video.ended));
  video.addEventListener('ended', () => {
    setPlayIcon(false, true);
    // A real end of playback: the video reached its duration without being skipped.
    if (Number.isFinite(video.duration) && video.currentTime >= video.duration - 0.6) onEnded(false);
  });
  video.addEventListener('timeupdate', () => {
    const d = video.duration;
    if (!seeking && !video.seeking) maxWatched = Math.max(maxWatched, video.currentTime);
    if (d) {
      bar.value = String(Math.round((video.currentTime / d) * 1000));
      paintBar();
    }
    time.textContent = `${fmtTime(video.currentTime)} / ${fmtTime(d)}`;
  });
  video.addEventListener('loadedmetadata', () => { time.textContent = `0:00 / ${fmtTime(video.duration)}`; });
  video.addEventListener('seeking', () => {
    // First viewing: do not allow skipping ahead (so the QR code is earned by watching to the end).
    if (!unlockedSeek() && video.currentTime > maxWatched + 1.5) video.currentTime = maxWatched;
  });
  bar.addEventListener('pointerdown', () => { seeking = true; });
  bar.addEventListener('change', () => { seeking = false; });
  bar.addEventListener('input', () => {
    if (!video.duration) return;
    let t = (Number(bar.value) / 1000) * video.duration;
    if (!unlockedSeek() && t > maxWatched + 1.5) {
      t = maxWatched;
      bar.value = String(Math.round((t / video.duration) * 1000));
    }
    video.currentTime = t;
    paintBar();
  });

  muteBtn.addEventListener('click', () => {
    video.muted = !video.muted;
    muteBtn.replaceChildren(icon(video.muted ? 'mute' : 'volume', 18));
    muteBtn.setAttribute('aria-label', video.muted ? 'Unmute' : 'Mute');
  });
  fsBtn.addEventListener('click', () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (wrap.requestFullscreen) wrap.requestFullscreen().catch(() => {});
    else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
  });

  const fail = () => {
    failed += 1;
    if (failed >= 2 || video.error) {
      missing.hidden = false;
      wrap.classList.add('is-missing');
    }
  };
  sMp4.addEventListener('error', fail);
  sWebm.addEventListener('error', fail);
  video.addEventListener('error', () => { missing.hidden = false; wrap.classList.add('is-missing'); });

  return {
    el,
    video,
    pause: () => { if (!video.paused) video.pause(); },
    isPlaying: () => !video.paused,
  };
}
