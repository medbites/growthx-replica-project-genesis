import { getEvents, findEvent, driveId, esc, niceDate, SITE_NAME } from './_shared.js';
export const config = { runtime: 'edge' };
// The home page and event links (/e/CODE): the normal page, with preview card tags
// for WhatsApp, Instagram, Facebook and LinkedIn.
export default async function handler(req) {
  const url = new URL(req.url);
  const code = url.searchParams.get('code');
  const origin = 'https://' + (req.headers.get('x-forwarded-host') || url.host);
  const [page, events] = await Promise.all([fetch(new URL('/index.html', url.origin)).then((r) => r.text()), code ? getEvents() : []]);
  const headers = { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, s-maxage=120, max-age=60' };
  const e = code && findEvent(events, code);
  const card = e
    ? {
        title: e.title + ' · ' + SITE_NAME,
        desc: niceDate(e) + ' · ' + (e.mode === 'Online' ? 'Online' : (e.venue_name || '')) + (e.why_attend ? '. ' + e.why_attend : ''),
        link: origin + '/e/' + e.event_code,
        // Small copy of the poster: WhatsApp skips preview images over about 300 KB.
        image: driveId(e.poster_link) ? origin + '/img/' + e.event_code + '?s=og&p=' + driveId(e.poster_link).slice(0, 8) : '',
      }
    : { title: 'Divyanjali Events', desc: 'Performances, arangetrams and workshops by Divyanjali, Bharatanatyam since 1994, Chennai.', link: origin + '/', image: '' };
  const img = card.image || origin + '/assets/og-default.jpg';
  const extra =
    '<meta property="og:type" content="website"><meta property="og:url" content="' + esc(card.link) + '"><meta property="og:site_name" content="' + SITE_NAME + '">' +
    '<meta property="og:image" content="' + esc(img) + '"><meta property="og:image:secure_url" content="' + esc(img) + '"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt" content="' + esc(card.title) + '">' +
    (card.image ? '' : '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">') +
    '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="' + esc(img) + '">';
  const title = esc(card.title), desc = esc(card.desc);
  const html = page
    .replace(/<title>[^<]*<\/title>/, '<title>' + title + '</title>')
    .replace(/(<meta name="description" content=")[^"]*/, '$1' + desc)
    .replace(/(<meta property="og:title" content=")[^"]*/, '$1' + title)
    .replace(/(<meta property="og:description" content=")[^"]*/, '$1' + desc)
    .replace('</head>', extra + '</head>');
  return new Response(html, { headers });
}
