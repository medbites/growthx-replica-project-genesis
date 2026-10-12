import { getEvents, findEvent, driveId, esc, niceDate, SITE_NAME } from './_shared.js';
export const config = { runtime: 'edge' };
// Event links (/e/CODE): the normal page, with that event's preview card tags.
export default async function handler(req) {
  const url = new URL(req.url);
  const code = url.searchParams.get('code');
  const [page, events] = await Promise.all([fetch(new URL('/index.html', url.origin)).then((r) => r.text()), getEvents()]);
  const headers = { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, s-maxage=120, max-age=60' };
  const e = findEvent(events, code);
  if (!e) return new Response(page, { headers });
  const origin = 'https://' + (req.headers.get('x-forwarded-host') || url.host);
  const title = esc(e.title + ' · ' + SITE_NAME);
  const where = e.mode === 'Online' ? 'Online' : (e.venue_name || '');
  const desc = esc(niceDate(e) + (where ? ' · ' + where : '') + (e.why_attend ? '. ' + e.why_attend : ''));
  const image = driveId(e.poster_link) ? origin + '/img/' + e.event_code : '';
  const extra =
    '<meta property="og:type" content="website"><meta property="og:url" content="' + esc(origin + '/e/' + e.event_code) + '"><meta property="og:site_name" content="' + SITE_NAME + '">' +
    (image ? '<meta property="og:image" content="' + esc(image) + '"><meta property="og:image:width" content="1200"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="' + esc(image) + '">' : '<meta name="twitter:card" content="summary">');
  const html = page
    .replace(/<title>[^<]*<\/title>/, '<title>' + title + '</title>')
    .replace(/(<meta name="description" content=")[^"]*/, '$1' + desc)
    .replace(/(<meta property="og:title" content=")[^"]*/, '$1' + title)
    .replace(/(<meta property="og:description" content=")[^"]*/, '$1' + desc)
    .replace('</head>', extra + '</head>');
  return new Response(html, { headers });
}
