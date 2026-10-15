import { SCRIPT_URL } from './_shared.js';
export const config = { runtime: 'edge' };
// Health check: is the Google Sheet reachable and how many published events does it return?
export default async function handler() {
  try {
    const r = await fetch(SCRIPT_URL + '?action=events', { redirect: 'follow' });
    const text = await r.text();
    let events = null;
    try { events = JSON.parse(text).events.length; } catch (err) { /* not JSON */ }
    return Response.json({ status: r.status, final_url: r.url.split('?')[0], published_events: events, message: events === null ? text.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 600) : undefined }, { headers: { 'cache-control': 'no-store' } });
  } catch (err) {
    return Response.json({ error: String(err) });
  }
}
