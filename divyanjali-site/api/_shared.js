// Shared by the Vercel functions. Same logic as _worker.js (Cloudflare).
export const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwlZ0KujTvaUagVM4TVpEUeVyp2XH2svG3bRkh-k7ipESLJchbw4Bj6afAUSl-JWfWE/exec';
export const SITE_NAME = 'Divyanjali';

export async function getEvents() {
  try {
    const r = await fetch(SCRIPT_URL + '?action=events', { redirect: 'follow' });
    const j = await r.json();
    return Array.isArray(j.events) ? j.events : [];
  } catch (err) {
    return [];
  }
}
export function findEvent(events, code) {
  return events.find((x) => String(x.event_code).toUpperCase() === String(code || '').toUpperCase());
}
export function driveId(u) {
  const m = String(u || '').match(/\/d\/([\w-]{20,})/) || String(u || '').match(/[?&]id=([\w-]{20,})/);
  return m ? m[1] : null;
}
export const esc = (s) => String(s || '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
export function niceDate(e) {
  const d = new Date(e.date + 'T' + (e.start_time || '00:00') + ':00+05:30');
  if (isNaN(d)) return e.date;
  const day = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Kolkata' }).format(d);
  const time = new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' }).format(d).toUpperCase();
  return day + ' · ' + time;
}
function durMin(s) { s = String(s || '').toLowerCase(); const h = s.match(/(\d+(?:\.\d+)?)\s*h/); const m = s.match(/(\d+)\s*m/); const t = (h ? parseFloat(h[1]) * 60 : 0) + (m ? parseInt(m[1], 10) : 0); return t || 120; }
function stamp(d) { return d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, ''); }
function icsText(s) { return String(s || '').replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/([,;])/g, '\\$1'); }
function fold(line) { const out = []; while (line.length > 74) { out.push(line.slice(0, 74)); line = ' ' + line.slice(74); } out.push(line); return out.join('\r\n'); }
export function icsFeed(events, origin) {
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
