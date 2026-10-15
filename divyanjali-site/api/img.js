import { getEvents, findEvent, driveId } from './_shared.js';
export const config = { runtime: 'edge' };
// Poster proxy, so WhatsApp preview cards get a direct, cacheable image.
export default async function handler(req) {
  const code = new URL(req.url).searchParams.get('code');
  const e = findEvent(await getEvents(), code);
  if (!e || !e.poster_link) return new Response('Not found', { status: 404 });
  const id = driveId(e.poster_link);
  if (!id) {
    // Uploaded to Supabase Storage (or another direct image link): pass it through as it is.
    const d = await fetch(e.poster_link);
    if (!d.ok) return new Response('Not found', { status: 404 });
    return new Response(d.body, { headers: { 'content-type': d.headers.get('content-type') || 'image/jpeg', 'cache-control': 'public, s-maxage=86400, max-age=86400' } });
  }
  // ?s=og: small copy for link previews (WhatsApp skips large images). Otherwise a sharp copy for the page.
  const size = new URL(req.url).searchParams.get('s') === 'og' ? 'w600-h600' : 'w1600';
  const r = await fetch('https://drive.google.com/thumbnail?id=' + id + '&sz=' + size);
  if (!r.ok) return new Response('Not found', { status: 404 });
  return new Response(r.body, { headers: { 'content-type': r.headers.get('content-type') || 'image/jpeg', 'cache-control': 'public, s-maxage=86400, max-age=86400' } });
}
