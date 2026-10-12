import { getEvents, findEvent, driveId } from './_shared.js';
export const config = { runtime: 'edge' };
// Poster proxy, so WhatsApp preview cards get a direct, cacheable image.
export default async function handler(req) {
  const code = new URL(req.url).searchParams.get('code');
  const e = findEvent(await getEvents(), code);
  const id = e && driveId(e.poster_link);
  if (!id) return new Response('Not found', { status: 404 });
  const r = await fetch('https://drive.google.com/thumbnail?id=' + id + '&sz=w1200');
  if (!r.ok) return new Response('Not found', { status: 404 });
  return new Response(r.body, { headers: { 'content-type': r.headers.get('content-type') || 'image/jpeg', 'cache-control': 'public, s-maxage=86400, max-age=86400' } });
}
