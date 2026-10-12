/**
 * Divyanjali Events · Google Sheet backend
 * Paste this whole file into Extensions > Apps Script, save, then run setup() once.
 * Deploy > New deployment > Web app > Execute as: Me · Who has access: Anyone.
 * Later changes: Deploy > Manage deployments > Edit > New version (keeps the same URL).
 */

const TZ = 'Asia/Kolkata';
const TABS = {
  Events: ['event_code', 'status', 'date', 'start_time', 'duration', 'title', 'type', 'format', 'mode', 'lead_artist', 'guru', 'dancers', 'orchestra', 'music', 'venue_name', 'venue_address', 'maps_link', 'entry', 'ticket_link', 'presented_by', 'sponsor', 'why_attend', 'invite_message', 'about', 'poster_link', 'photos_link', 'video_link', 'photo_check'],
  Private: ['event_code', 'online_join_link', 'contact_person', 'contact_phone', 'notes'],
  Responses: ['timestamp', 'event_code', 'event_title', 'kind', 'name', 'city', 'rating', 'message', 'show_public', 'approved', 'notes'],
  Enquiries: ['timestamp', 'enquiry_type', 'from_event_code', 'name', 'organisation', 'whatsapp', 'email', 'date_needed', 'message', 'status', 'notes'],
  Settings: ['key', 'value', '', 'status', 'type', 'format', 'mode', 'music', 'entry', 'approved', 'enquiry_status']
};
const LISTS = {
  status: ['Draft', 'Published', 'Cancelled'],
  type: ['Performance', 'Arangetram', 'Workshop', 'Festival'],
  format: ['Solo', 'Group'],
  mode: ['In person', 'Online', 'Hybrid'],
  music: ['Live', 'Recorded'],
  entry: ['Free', 'Free, register', 'Ticketed', 'By invitation'],
  approved: ['Yes', 'No'],
  enquiry_status: ['New', 'Contacted', 'Won', 'Lost']
};
// Public fields the website may read. Everything else stays private.
const PUBLIC_FIELDS = TABS.Events.filter((h) => h !== 'status' && h !== 'photo_check');

/* ---------- Menu ---------- */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('Divyanjali')
    .addItem('Set up the sheet (run once)', 'setup')
    .addItem('Check photo links', 'checkPhotos')
    .addItem('Fill missing event codes', 'fillCodes')
    .addToUi();
}

/* ---------- One-time setup ---------- */
function setup() {
  const ss = SpreadsheetApp.getActive();
  ss.setSpreadsheetTimeZone(TZ);
  ss.setSpreadsheetLocale('en_IN');
  Object.keys(TABS).forEach((name) => {
    const sh = ss.getSheetByName(name) || ss.insertSheet(name);
    const head = TABS[name];
    ensureSize(sh, name === 'Settings' ? 30 : 1001, head.length);
    sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold').setBackground('#FFF3EA');
    sh.setFrozenRows(1);
    const p = sh.getRange(1, 1, 1, head.length).protect().setDescription('Headings: do not edit');
    p.setWarningOnly(true);
  });
  const st = ss.getSheetByName('Settings');
  if (!st.getRange('A2').getValue()) {
    st.getRange('A2:B5').setValues([['admin_email', ''], ['whatsapp_number', '91XXXXXXXXXX'], ['season_banner', 'Dance Season 2026–27 · November to January'], ['site_url', 'https://divyanjalidance.com']]);
  }
  Object.keys(LISTS).forEach((k) => {
    const col = TABS.Settings.indexOf(k) + 1;
    st.getRange(2, col, LISTS[k].length, 1).setValues(LISTS[k].map((v) => [v]));
  });

  const ev = ss.getSheetByName('Events');
  const col = (h) => TABS.Events.indexOf(h) + 1;
  const rows = 1000;
  const list = (h, k) => ev.getRange(2, col(h), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS[k], true).setAllowInvalid(false).build());
  ['status', 'type', 'format', 'mode', 'music'].forEach((h) => list(h, h));
  ev.getRange(2, col('entry'), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.entry, true).setAllowInvalid(true).build());
  ev.getRange(2, col('date'), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireDate().setAllowInvalid(false).build()).setNumberFormat('dd mmm yyyy');
  ev.getRange(2, col('start_time'), rows, 1).setNumberFormat('h:mm am/pm');
  const rsp = ss.getSheetByName('Responses');
  rsp.getRange(2, TABS.Responses.indexOf('approved') + 1, rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.approved, true).build());
  const enq = ss.getSheetByName('Enquiries');
  enq.getRange(2, TABS.Enquiries.indexOf('status') + 1, rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.enquiry_status, true).build());

  // Red rows: duplicate event codes, and two events at the same date, time and venue.
  const L = (h) => columnLetter(col(h));
  const all = ev.getRange(2, 1, rows, TABS.Events.length);
  const dup = SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=AND($A2<>"",COUNTIF($A:$A,$A2)>1)').setBackground('#FDEBEC').setRanges([all]).build();
  const clash = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=AND($' + L('date') + '2<>"",$' + L('mode') + '2<>"Online",COUNTIFS($' + L('date') + ':$' + L('date') + ',$' + L('date') + '2,$' + L('start_time') + ':$' + L('start_time') + ',$' + L('start_time') + '2,$' + L('venue_name') + ':$' + L('venue_name') + ',$' + L('venue_name') + '2)>1)')
    .setBackground('#FBE3D0').setRanges([all]).build();
  ev.setConditionalFormatRules([dup, clash]);

  if (ev.getLastRow() < 2) {
    const sample = {
      status: 'Draft', date: new Date(2026, 10, 8), start_time: '18:30', duration: '2 hrs', title: 'Margam Recital', type: 'Performance', format: 'Solo', mode: 'In person',
      lead_artist: 'Student name', guru: 'Dr. S. Divyasena', orchestra: 'Nattuvangam: Dr. S. Divyasena; Mridangam: Sri B.P. Haribabu; Vocal: Vocalist name', music: 'Live',
      venue_name: 'Sabha name', venue_address: 'Area, Chennai', maps_link: 'https://maps.google.com/?q=Chennai', entry: 'Free', presented_by: 'Divyanjali',
      why_attend: 'A full margam with a live orchestra.', invite_message: 'I would be honoured to have you in the audience.', about: 'Sample row. Change it, then set status to Published.'
    };
    ev.getRange(2, 1, 1, TABS.Events.length).setValues([TABS.Events.map((h) => sample[h] || '')]);
    fillCodes();
  }
  SpreadsheetApp.getActive().toast('Sheet is ready. Next: Deploy > New deployment > Web app.', 'Divyanjali', 8);
}

/* ---------- Event codes ---------- */
function onEdit(e) {
  try {
    CacheService.getScriptCache().remove('events');
    const sh = e.range.getSheet();
    if (sh.getName() !== 'Events' || e.range.getRow() < 2) return;
    fillCodes();
  } catch (err) { /* never block typing */ }
}
function fillCodes() {
  const sh = SpreadsheetApp.getActive().getSheetByName('Events');
  const n = sh.getLastRow() - 1; if (n < 1) return;
  const head = TABS.Events;
  const data = sh.getRange(2, 1, n, head.length).getValues();
  const used = new Set(data.map((r) => String(r[0])).filter(Boolean));
  data.forEach((r, i) => {
    const date = r[head.indexOf('date')], title = r[head.indexOf('title')];
    if (r[0] || !(date instanceof Date) || !title) return;
    const word = String(title).toUpperCase().replace(/[^A-Z0-9 ]/g, '').split(' ').filter((w) => w.length > 2)[0] || 'EVENT';
    let code = 'DV-' + Utilities.formatDate(date, TZ, 'yyMMdd') + '-' + word.slice(0, 10), k = 2;
    while (used.has(code)) code = code.replace(/-\d+$/, '') + '-' + k++;
    used.add(code);
    sh.getRange(i + 2, 1).setValue(code);
  });
}

/* ---------- Photo check ---------- */
function checkPhotos() {
  const sh = SpreadsheetApp.getActive().getSheetByName('Events');
  const n = sh.getLastRow() - 1; if (n < 1) return;
  const pCol = TABS.Events.indexOf('poster_link') + 1, cCol = TABS.Events.indexOf('photo_check') + 1;
  const links = sh.getRange(2, pCol, n, 1).getValues();
  const out = links.map(([u]) => {
    if (!u) return ['No poster'];
    const m = String(u).match(/\/d\/([\w-]{20,})/) || String(u).match(/[?&]id=([\w-]{20,})/);
    if (!m) return ['OK (not Drive)'];
    try {
      const f = DriveApp.getFileById(m[1]);
      const a = f.getSharingAccess();
      if (a !== DriveApp.Access.ANYONE_WITH_LINK && a !== DriveApp.Access.ANYONE) return ['Not shared: set Anyone with the link'];
      if (/heic|heif/i.test(f.getMimeType())) return ['iPhone HEIC: please upload JPG'];
      if (f.getSize() > 600 * 1024) return ['OK but large: under 300 KB is best'];
      return ['OK'];
    } catch (err) { return ['Not found'] }
  });
  sh.getRange(2, cCol, n, 1).setValues(out);
  SpreadsheetApp.getActive().toast('Photo check done.', 'Divyanjali', 5);
}

/* ---------- Website reads ---------- */
function doGet(e) {
  const action = (e && e.parameter.action) || 'events';
  if (action === 'wishes') return json({ wishes: publicWishes(String(e.parameter.e || '')) });
  const cache = CacheService.getScriptCache();
  const hit = cache.get('events');
  if (hit) return ContentService.createTextOutput(hit).setMimeType(ContentService.MimeType.JSON);
  const body = JSON.stringify({ events: publishedEvents(), updated: new Date().toISOString() });
  try { cache.put('events', body, 60); } catch (err) { /* too large to cache */ }
  return ContentService.createTextOutput(body).setMimeType(ContentService.MimeType.JSON);
}

function publishedEvents() {
  const sh = SpreadsheetApp.getActive().getSheetByName('Events');
  const values = sh.getDataRange().getValues();
  const head = values.shift().map((h) => String(h).trim().toLowerCase());
  return values.map((r) => {
    const o = {};
    head.forEach((h, i) => { o[h] = r[i]; });
    return o;
  }).filter((o) => String(o.status).trim() === 'Published' && o.event_code && o.date).map((o) => {
    const ev = {};
    PUBLIC_FIELDS.forEach((h) => {
      let v = o[h];
      if (h === 'date' && v instanceof Date) v = Utilities.formatDate(v, TZ, 'yyyy-MM-dd');
      else if (h === 'start_time' && v instanceof Date) v = Utilities.formatDate(v, TZ, 'HH:mm');
      else if (h === 'start_time' && v) v = normalTime(String(v));
      ev[h] = v === undefined || v === null ? '' : String(v).trim();
    });
    return ev;
  });
}
function normalTime(s) {
  const m = s.trim().match(/^(\d{1,2})[:.](\d{2})\s*(am|pm)?$/i);
  if (!m) return s;
  let h = parseInt(m[1], 10);
  if (m[3] && /pm/i.test(m[3]) && h < 12) h += 12;
  if (m[3] && /am/i.test(m[3]) && h === 12) h = 0;
  return ('0' + h).slice(-2) + ':' + m[2];
}
function publicWishes(code) {
  if (!code) return [];
  const sh = SpreadsheetApp.getActive().getSheetByName('Responses');
  const v = sh.getDataRange().getValues(); const h = v.shift();
  const i = (k) => h.indexOf(k);
  return v.filter((r) => r[i('event_code')] === code && r[i('approved')] === 'Yes' && r[i('show_public')] === 'Yes')
    .slice(-12).reverse().map((r) => ({ kind: r[i('kind')], name: r[i('name')], city: r[i('city')], message: r[i('message')] }));
}

/* ---------- Website writes ---------- */
function doPost(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return json({ ok: false, error: 'Bad request' }); }
  if (d.website) return json({ ok: true }); // spam trap filled in: pretend success, save nothing
  const clip = (s, n) => String(s || '').slice(0, n || 500);
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const ss = SpreadsheetApp.getActive();
    const now = new Date();
    if (d.form === 'response') {
      if (!d.name || !d.message) return json({ ok: false, error: 'Name and message are required' });
      const title = (publishedEvents().find((x) => x.event_code === d.event_code) || {}).title || '';
      ss.getSheetByName('Responses').appendRow([now, clip(d.event_code, 60), title, clip(d.kind, 20), clip(d.name, 80), clip(d.city, 80), clip(d.rating, 2), clip(d.message, 2000), d.show_public === 'Yes' ? 'Yes' : 'No', '', '']);
      notify('New ' + clip(d.kind, 20) + ' for ' + (title || d.event_code), clip(d.name, 80) + ': ' + clip(d.message, 2000));
    } else if (d.form === 'enquiry') {
      if (!d.name || !d.whatsapp) return json({ ok: false, error: 'Name and WhatsApp are required' });
      ss.getSheetByName('Enquiries').appendRow([now, clip(d.enquiry_type, 60), clip(d.from_event_code, 60), clip(d.name, 80), clip(d.organisation, 120), "'" + clip(d.whatsapp, 20), clip(d.email, 120), clip(d.date_needed, 20), clip(d.message, 2000), 'New', '']);
      notify('New enquiry: ' + clip(d.enquiry_type, 60), clip(d.name, 80) + ' · ' + clip(d.whatsapp, 20) + '\n' + clip(d.message, 2000));
    } else {
      return json({ ok: false, error: 'Unknown form' });
    }
    return json({ ok: true });
  } finally {
    lock.releaseLock();
  }
}
function notify(subject, body) {
  try {
    const st = SpreadsheetApp.getActive().getSheetByName('Settings').getRange('A2:B20').getValues();
    const row = st.find((r) => r[0] === 'admin_email');
    if (row && row[1]) MailApp.sendEmail(String(row[1]), subject, body + '\n\nOpen the sheet: ' + SpreadsheetApp.getActive().getUrl());
  } catch (err) { /* email is optional */ }
}

/* ---------- Utilities ---------- */
// Sheets uploaded from Excel can be small; grow them so validation ranges fit.
function ensureSize(sh, rows, cols) {
  if (sh.getMaxRows() < rows) sh.insertRowsAfter(sh.getMaxRows(), rows - sh.getMaxRows());
  if (sh.getMaxColumns() < cols) sh.insertColumnsAfter(sh.getMaxColumns(), cols - sh.getMaxColumns());
}
function json(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function columnLetter(n) { let s = ''; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; }
