const KEY = 'kazakh-heritage-book:completed:v1';
const EVT = 'kh:progress';

function read() {
  try {
    const raw = localStorage.getItem(KEY);
    const v = raw ? JSON.parse(raw) : [];
    return Array.isArray(v) ? v.filter((x) => typeof x === 'string') : [];
  } catch {
    return [];
  }
}

function write(list) {
  try {
    localStorage.setItem(KEY, JSON.stringify(list));
  } catch {
    /* storage unavailable (private mode): progress simply will not persist */
  }
}

export const getCompleted = () => read();
export const isCompleted = (slug) => read().includes(slug);

/** Mark a chapter as genuinely finished (only called after the video's real `ended` event). */
export function markCompleted(slug) {
  const list = read();
  if (!list.includes(slug)) write([...list, slug]);
  window.dispatchEvent(new CustomEvent(EVT, { detail: { slug } }));
}

export function resetProgress() {
  write([]);
  window.dispatchEvent(new CustomEvent(EVT, { detail: { slug: null } }));
}

export const onProgress = (fn) => {
  window.addEventListener(EVT, fn);
  window.addEventListener('storage', fn);
};
