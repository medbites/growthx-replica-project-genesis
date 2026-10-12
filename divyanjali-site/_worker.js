// Cloudflare Pages worker: gives every /e/EVENT-CODE link its own preview card
// (WhatsApp, Instagram, Facebook, LinkedIn) with the event's poster, title and date.
// Everything else is served as the normal static site.

const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycby1jf4-uZtCLtY4Im3zvBlnm5gMTmncxx-pIG14BjkDIAmzH8_J1lWOu5ThyC-vf4yt/exec';
const SITE_NAME = 'Divyanjali';

async function getEvents() {
  try {
    const r = await fetch(SCRIPT_URL + '?action=events', { cf: { cacheTtl: 120, cacheEverything: true } });
    const j = await r.json();
    return Array.isArray(j.events) ? j.events : [];
  } catch (err) {
    return [];
  }
}

function driveId(u) {
  const m = String(u || '').match(/\/d\/([\w-]{20,})/) || String(u || '').match(/[?&]id=([\w-]{20,})/);
  return m ? m[1] : null;
}

function niceDate(e) {
  const d = new Date(e.date + 'T' + (e.start_time || '00:00') + ':00+05:30');
  if (isNaN(d)) return e.date;
  const day = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Kolkata' }).format(d);
  const time = new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' }).format(d).toUpperCase();
  return day + ' · ' + time;
}

class SetAttr {
  constructor(attr, value) { this.attr = attr; this.value = value; }
  element(el) { el.setAttribute(this.attr, this.value); }
}
class SetText {
  constructor(value) { this.value = value; }
  element(el) { el.setInnerContent(this.value); }
}
class AddToHead {
  constructor(html) { this.html = html; }
  element(el) { el.append(this.html, { html: true }); }
}
const esc = (s) => String(s || '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// Calendar feed: every published event, for "subscribe" in Google, Apple and Outlook calendars.
function durMin(s) { s = String(s || '').toLowerCase(); const h = s.match(/(\d+(?:\.\d+)?)\s*h/); const m = s.match(/(\d+)\s*m/); const t = (h ? parseFloat(h[1]) * 60 : 0) + (m ? parseInt(m[1], 10) : 0); return t || 120; }
function stamp(d) { return d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, ''); }
function icsText(s) { return String(s || '').replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/([,;])/g, '\\$1'); }
function fold(line) { const out = []; while (line.length > 74) { out.push(line.slice(0, 74)); line = ' ' + line.slice(74); } out.push(line); return out.join('\r\n'); }
function icsFeed(events, origin) {
  const now = stamp(new Date());
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Divyanjali//Events//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'X-WR-CALNAME:Divyanjali Events', 'X-WR-TIMEZONE:Asia/Kolkata', 'REFRESH-INTERVAL;VALUE=DURATION:PT6H', 'X-PUBLISHED-TTL:PT6H'];
  events.forEach((e) => {
    const start = new Date(e.date + 'T' + (e.start_time || '00:00') + ':00+05:30');
    if (isNaN(start)) return;
    const end = new Date(start.getTime() + durMin(e.duration) * 60000);
    const where = e.mode === 'Online' ? 'Online' : [e.venue_name, e.venue_address].filter(Boolean).join(', ');
    const link = origin + '/e/' + e.event_code;
    lines.push('BEGIN:VEVENT', 'UID:' + e.event_code + '@divyanjalidance.com', 'DTSTAMP:' + now, 'DTSTART:' + stamp(start), 'DTEND:' + stamp(end),
      fold('SUMMARY:' + icsText(e.title + ' · Divyanjali')), fold('LOCATION:' + icsText(where)),
      fold('DESCRIPTION:' + icsText([e.type, e.mode, e.entry].filter(Boolean).join(' · ') + '\n' + (e.why_attend || '') + '\n' + link)), fold('URL:' + link), 'END:VEVENT');
  });
  lines.push('END:VCALENDAR');
  return lines.join('\r\n') + '\r\n';
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/calendar.ics') {
      return new Response(icsFeed(await getEvents(), url.origin), { headers: { 'content-type': 'text/calendar; charset=utf-8', 'cache-control': 'public, max-age=900' } });
    }

    // Poster image proxy, so preview cards get a direct, cacheable image.
    const img = url.pathname.match(/^\/img\/([\w-]+)$/);
    if (img) {
      const e = (await getEvents()).find((x) => x.event_code.toUpperCase() === img[1].toUpperCase());
      const id = e && driveId(e.poster_link);
      if (!id) return new Response('Not found', { status: 404 });
      const r = await fetch('https://drive.google.com/thumbnail?id=' + id + '&sz=w1200', { cf: { cacheTtl: 86400, cacheEverything: true } });
      if (!r.ok) return new Response('Not found', { status: 404 });
      return new Response(r.body, { headers: { 'content-type': r.headers.get('content-type') || 'image/jpeg', 'cache-control': 'public, max-age=86400' } });
    }

    // Event links: serve the page with event-specific preview tags.
    const ev = url.pathname.match(/^\/e\/([\w-]+)\/?$/);
    if (ev) {
      const page = await env.ASSETS.fetch(new URL('/index.html', url.origin));
      const e = (await getEvents()).find((x) => x.event_code.toUpperCase() === ev[1].toUpperCase());
      if (!e) return page;
      const title = e.title + ' · ' + SITE_NAME;
      const where = e.mode === 'Online' ? 'Online' : (e.venue_name || '');
      const desc = niceDate(e) + (where ? ' · ' + where : '') + (e.why_attend ? '. ' + e.why_attend : '');
      const image = driveId(e.poster_link) ? url.origin + '/img/' + e.event_code : '';
      const extra =
        '<meta property="og:type" content="website">' +
        '<meta property="og:url" content="' + esc(url.origin + '/e/' + e.event_code) + '">' +
        '<meta property="og:site_name" content="' + SITE_NAME + '">' +
        (image ? '<meta property="og:image" content="' + esc(image) + '"><meta property="og:image:width" content="1200"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="' + esc(image) + '">' : '<meta name="twitter:card" content="summary">');
      return new HTMLRewriter()
        .on('title', new SetText(esc(title)))
        .on('meta[name="description"]', new SetAttr('content', desc))
        .on('meta[property="og:title"]', new SetAttr('content', title))
        .on('meta[property="og:description"]', new SetAttr('content', desc))
        .on('head', new AddToHead(extra))
        .transform(new Response(page.body, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, max-age=120' } }));
    }

    return env.ASSETS.fetch(request);
  }
};
