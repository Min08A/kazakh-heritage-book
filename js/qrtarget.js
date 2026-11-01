import { PUBLIC_SITE_URL, isDevHost } from './config.js';

function isPublicHttps(url) {
  try {
    const u = new URL(url);
    return u.protocol === 'https:' && !isDevHost(u.hostname);
  } catch {
    return false;
  }
}

/**
 * URL encoded in the QR code for an object page, and whether it is safe to print/share.
 * Never reports a localhost / private address as production ready.
 */
export function getQrTarget(slug) {
  const path = `/object/${slug}`;
  const configured = PUBLIC_SITE_URL.replace(/\/+$/, '');
  if (configured) {
    const url = configured + path;
    return isPublicHttps(url)
      ? { url, productionReady: true, warning: null }
      : { url, productionReady: false, warning: 'PUBLIC_SITE_URL in js/config.js is not a public HTTPS address. This QR code is for testing only.' };
  }
  const url = location.origin + path;
  if (isPublicHttps(url)) return { url, productionReady: true, warning: null };
  return {
    url,
    productionReady: false,
    warning:
      'Testing mode: the site is not published yet, so this QR code points to a local address and only works on this network. ' +
      'Publish the site, then the QR codes will use the real address automatically.',
  };
}
