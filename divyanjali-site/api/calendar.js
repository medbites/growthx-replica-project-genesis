import { getEvents, icsFeed } from './_shared.js';
export const config = { runtime: 'edge' };
export default async function handler(req) {
  const origin = new URL(req.url).origin;
  return new Response(icsFeed(await getEvents(), origin), { headers: { 'content-type': 'text/calendar; charset=utf-8', 'cache-control': 'public, s-maxage=900, max-age=900' } });
}
