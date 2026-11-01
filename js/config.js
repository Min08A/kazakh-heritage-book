/**
 * Site configuration.
 *
 * PUBLIC_SITE_URL: the public HTTPS address of the published site, no trailing slash,
 * e.g. 'https://kazakh-heritage.vercel.app'.
 * Leave it empty to let the site detect its own address automatically: once the site is
 * deployed, QR codes will use that real address. On localhost / a LAN address the book
 * shows a "testing only" warning next to the QR code.
 */
export const PUBLIC_SITE_URL = '';

/** Root of the site, resolved from this file's location (works from any page depth). */
export const BASE = new URL('../', import.meta.url);

/** Turn a site-relative path such as 'media/videos/dombra.mp4' into an absolute URL. */
export const asset = (p) => new URL(p, BASE).href;

/** True when the page runs on a development machine (localhost, *.local, LAN address). */
export function isDevHost(hostname = location.hostname) {
  const h = hostname.toLowerCase();
  return (
    h === 'localhost' || h.endsWith('.localhost') || h.endsWith('.local') || h === '[::1]' || h === '::1' ||
    /^127\./.test(h) || /^10\./.test(h) || /^192\.168\./.test(h) || /^169\.254\./.test(h) ||
    /^172\.(1[6-9]|2\d|3[01])\./.test(h)
  );
}
