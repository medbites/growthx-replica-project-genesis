/**
 * Divyanjali Events · Google Sheet backend
 * Paste this whole file into Extensions > Apps Script, save, then run setup() once.
 * Deploy > New deployment > Web app > Execute as: Me · Who has access: Anyone.
 * Later changes: Deploy > Manage deployments > Edit > New version (keeps the same URL).
 */

// The sheet the website uses. Leave empty to use the sheet this script is attached to.
const SHEET_ID = '1kV0M-v6YTZ9LCVMgpGiGH-56VGsoIMVxKuWFqiZKLHU';
function book() {
  const a = SpreadsheetApp.getActive();
  if (!SHEET_ID || (a && a.getId() === SHEET_ID)) return a;
  return SpreadsheetApp.openById(SHEET_ID);
}
const TZ = 'Asia/Kolkata';
const TABS = {
  Events: ['event_code', 'status', 'date', 'start_time', 'duration', 'title', 'type', 'format', 'mode', 'lead_artist', 'guru', 'dancers', 'orchestra', 'music', 'venue_name', 'venue_address', 'maps_link', 'entry', 'ticket_link', 'presented_by', 'sponsor', 'why_attend', 'invite_message', 'about', 'poster_link', 'photos_link', 'video_link', 'photo_check'],
  Private: ['event_code', 'online_join_link', 'contact_person', 'contact_phone', 'notes'],
  Responses: ['timestamp', 'event_code', 'event_title', 'kind', 'name', 'city', 'rating', 'message', 'show_public', 'approved', 'notes'],
  Enquiries: ['timestamp', 'enquiry_type', 'from_event_code', 'name', 'organisation', 'whatsapp', 'email', 'date_needed', 'message', 'status', 'notes'],
  Slots: ['slot_id', 'date', 'start_time', 'end_time', 'venue_name', 'venue_address', 'maps_link', 'slot_for', 'status', 'application_id', 'notes'],
  Applications: ['timestamp', 'application_id', 'slot_id', 'slot_when', 'artist_name', 'format', 'dancers', 'guru', 'programme', 'music', 'whatsapp', 'email', 'city', 'video_link', 'message', 'status', 'event_code', 'reply_link', 'notes'],
  Settings: ['key', 'value', '', 'status', 'type', 'format', 'mode', 'music', 'entry', 'approved', 'enquiry_status', 'slot_status', 'slot_for', 'application_status']
};
const LISTS = {
  status: ['Draft', 'Published', 'Cancelled'],
  type: ['Performance', 'Arangetram', 'Workshop', 'Festival'],
  format: ['Solo', 'Group'],
  mode: ['In person', 'Online', 'Hybrid'],
  music: ['Live', 'Recorded'],
  entry: ['Free', 'Free, register', 'Ticketed', 'By invitation'],
  approved: ['Yes', 'No'],
  enquiry_status: ['New', 'Contacted', 'Won', 'Lost'],
  slot_status: ['Open', 'Held', 'Booked', 'Closed'],
  slot_for: ['Solo', 'Group', 'Solo or group'],
  application_status: ['Pending', 'Approved', 'Rejected']
};
const SETTINGS_DEFAULTS = [['admin_email', ''], ['whatsapp_number', '91XXXXXXXXXX'], ['season_banner', 'Dance Season 2026–27 · November to January'], ['site_url', 'https://divyanjalidance.com'], ['artist_form', 'Open']];
// Public fields the website may read. Everything else stays private.
const PUBLIC_FIELDS = TABS.Events.filter((h) => h !== 'status' && h !== 'photo_check');

/* ---------- Menu ---------- */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('Divyanjali')
    .addItem('Set up the sheet (run once)', 'setup')
    .addItem('Check photo links', 'checkPhotos')
    .addItem('Fill missing event codes', 'fillCodes')
    .addItem('Update season slots', 'syncSeason')
    .addSeparator()
    .addItem('Run website test', 'runTests')
    .addItem('Remove test rows', 'removeTests')
    .addToUi();
}

/* ---------- One-time setup ---------- */
function setup() {
  const ss = book();
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
  const keys = st.getRange(2, 1, 25, 1).getValues().map((r) => r[0]);
  SETTINGS_DEFAULTS.forEach((kv) => { if (keys.indexOf(kv[0]) < 0) { const r = keys.indexOf(''); st.getRange(r + 2, 1, 1, 2).setValues([kv]); keys[r] = kv[0]; } });
  Object.keys(LISTS).forEach((k) => {
    const col = TABS.Settings.indexOf(k) + 1;
    st.getRange(2, col, LISTS[k].length, 1).setValues(LISTS[k].map((v) => [v]));
  });

  const ev = ss.getSheetByName('Events');
  const col = (h) => TABS.Events.indexOf(h) + 1;
  ['Events', 'Responses', 'Enquiries', 'Slots', 'Applications'].forEach((n) => ss.getSheetByName(n).getRange(2, 1, ss.getSheetByName(n).getMaxRows() - 1, ss.getSheetByName(n).getMaxColumns()).clearDataValidations());
  const rows = 1000;
  const list = (h, k) => ev.getRange(2, col(h), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS[k], true).setAllowInvalid(false).build());
  ['status', 'type', 'format', 'mode', 'music'].forEach((h) => list(h, h));
  ev.getRange(2, col('entry'), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.entry, true).setAllowInvalid(true).build());
  ev.getRange(2, col('date'), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireDate().setAllowInvalid(true).setHelpText('Use a date, for example 8 Nov 2026').build()).setNumberFormat('dd mmm yyyy');
  ev.getRange(2, col('start_time'), rows, 1).setNumberFormat('h:mm am/pm');
  const rsp = ss.getSheetByName('Responses');
  rsp.getRange(2, TABS.Responses.indexOf('approved') + 1, rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.approved, true).build());
  const enq = ss.getSheetByName('Enquiries');
  enq.getRange(2, TABS.Enquiries.indexOf('status') + 1, rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.enquiry_status, true).build());
  const sl = ss.getSheetByName('Slots'), sc = (h) => TABS.Slots.indexOf(h) + 1;
  sl.getRange(2, sc('status'), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.slot_status, true).setHelpText('Open: shown on the website. Held and Booked are set by the website and the Applications tab.').build());
  sl.getRange(2, sc('slot_for'), rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.slot_for, true).build());
  sl.getRange(2, sc('date'), rows, 1).setNumberFormat('dd mmm yyyy');
  sl.getRange(2, sc('start_time'), rows, 2).setNumberFormat('h:mm am/pm');
  ss.getSheetByName('Applications').getRange(2, TABS.Applications.indexOf('status') + 1, rows, 1).setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(LISTS.application_status, true).setHelpText('Approved: books the slot and adds a Draft row to Events. Rejected: opens the slot again.').build());

  // Runs on every edit of this sheet, even when the script lives in another file.
  ScriptApp.getProjectTriggers().filter((t) => t.getHandlerFunction() === 'onSheetEdit').forEach((t) => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('onSheetEdit').forSpreadsheet(ss.getId()).onEdit().create();

  // Red rows: duplicate event codes, and two events at the same date, time and venue.
  const L = (h) => columnLetter(col(h));
  const cfRows = 500;
  const codeCells = ev.getRange(2, col('event_code'), cfRows, 1);
  const titleCells = ev.getRange(2, col('title'), cfRows, 1);
  const dup = SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=AND($A2<>"",COUNTIF($A$2:$A$' + (cfRows + 1) + ',$A2)>1)').setBackground('#FDEBEC').setRanges([codeCells]).build();
  const clash = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=AND($' + L('date') + '2<>"",$' + L('mode') + '2<>"Online",COUNTIFS($' + L('date') + '$2:$' + L('date') + '$' + (cfRows + 1) + ',$' + L('date') + '2,$' + L('start_time') + '$2:$' + L('start_time') + '$' + (cfRows + 1) + ',$' + L('start_time') + '2,$' + L('venue_name') + '$2:$' + L('venue_name') + '$' + (cfRows + 1) + ',$' + L('venue_name') + '2)>1)')
    .setBackground('#FBE3D0').setRanges([titleCells]).build();
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
  book().toast('Sheet is ready. Next: Deploy > New deployment > Web app.', 'Divyanjali', 8);
}

/* ---------- Event codes ---------- */
function onSheetEdit(e) {
  try {
    const sh = e.range.getSheet();
    if (e.range.getRow() < 2) return;
    if (sh.getName() === 'Slots' || sh.getName() === 'Applications') { withLock(syncSeason); return; }
    if (sh.getName() !== 'Events') return;
    CacheService.getScriptCache().remove('events');
    const head = TABS.Events, c0 = e.range.getColumn(), c1 = e.range.getLastColumn();
    const touches = (h) => { const c = head.indexOf(h) + 1; return c >= c0 && c <= c1; };
    if (touches('date') || touches('title')) fillCodes();
  } catch (err) { /* never block typing */ }
}
function fillCodes() {
  const sh = book().getSheetByName('Events');
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
  const sh = book().getSheetByName('Events');
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
  book().toast('Photo check done.', 'Divyanjali', 5);
}

/* ---------- Website reads ---------- */
function doGet(e) {
  const action = (e && e.parameter.action) || 'events';
  if (action === 'wishes') return json({ wishes: publicWishes(String(e.parameter.e || '')) });
  if (action === 'slots') return json(withLock(() => { syncSeason(); return { open: setting('artist_form') !== 'Closed', slots: openSlots() }; }));
  const cache = CacheService.getScriptCache();
  const hit = cache.get('events');
  if (hit) return ContentService.createTextOutput(hit).setMimeType(ContentService.MimeType.JSON);
  try { fillCodes(); } catch (err) { /* codes are optional at read time */ }
  const body = JSON.stringify({ events: publishedEvents(), updated: new Date().toISOString() });
  try { cache.put('events', body, 60); } catch (err) { /* too large to cache */ }
  return ContentService.createTextOutput(body).setMimeType(ContentService.MimeType.JSON);
}

function publishedEvents() {
  const sh = book().getSheetByName('Events');
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
  const sh = book().getSheetByName('Responses');
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
    const ss = book();
    const now = new Date();
    if (d.form === 'response') {
      if (!d.name || !d.message) return json({ ok: false, error: 'Name and message are required' });
      const title = (publishedEvents().find((x) => x.event_code === d.event_code) || {}).title || '';
      ss.getSheetByName('Responses').appendRow([now, clip(d.event_code, 60), title, clip(d.kind, 20), clip(d.name, 80), clip(d.city, 80), clip(d.rating, 2), clip(d.message, 2000), d.show_public === 'Yes' ? 'Yes' : 'No', '', '']);
      notify('New ' + clip(d.kind, 20) + ' for ' + (title || d.event_code), clip(d.name, 80) + ': ' + clip(d.message, 2000));
    } else if (d.form === 'application') {
      return json(apply(d, clip));
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
    const st = book().getSheetByName('Settings').getRange('A2:B20').getValues();
    const row = st.find((r) => r[0] === 'admin_email');
    if (row && row[1]) MailApp.sendEmail(String(row[1]), subject, body + '\n\nOpen the sheet: ' + book().getUrl());
  } catch (err) { /* email is optional */ }
}

/* ---------- Season artist slots ----------
 * Team adds rows to Slots (status Open). Artists pick one on the website.
 * The first request holds the slot, so two artists can never get the same one.
 * In Applications set status to Approved (slot Booked, Draft row added to Events)
 * or Rejected (slot Open again). */
function rowsOf(name) {
  const sh = book().getSheetByName(name);
  const v = sh.getDataRange().getValues(); const h = v.shift().map(String);
  return { sh, h, rows: v, col: (k) => h.indexOf(k) };
}
function slotTime(v) { return v instanceof Date ? Utilities.formatDate(v, TZ, 'HH:mm') : normalTime(String(v || '')); }
function slotDate(v) { return v instanceof Date ? Utilities.formatDate(v, TZ, 'yyyy-MM-dd') : String(v || '').trim(); }
function slotWhen(s) { return s.date + ' ' + s.start_time + (s.end_time ? '–' + s.end_time : '') + ' · ' + s.venue_name; }
function slotObj(S, r) { const o = {}; S.h.forEach((k, i) => { o[k] = r[i]; }); o.date = slotDate(o.date); o.start_time = slotTime(o.start_time); o.end_time = slotTime(o.end_time); return o; }

function openSlots() {
  const S = rowsOf('Slots'), today = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd');
  return S.rows.map((r) => slotObj(S, r)).filter((s) => s.slot_id && s.status === 'Open' && s.date >= today)
    .map((s) => ({ slot_id: s.slot_id, date: s.date, start_time: s.start_time, end_time: s.end_time, venue_name: String(s.venue_name), venue_address: String(s.venue_address), maps_link: String(s.maps_link), slot_for: String(s.slot_for || 'Solo or group') }))
    .sort((a, b) => (a.date + a.start_time).localeCompare(b.date + b.start_time));
}

function apply(d, clip) {
  if (setting('artist_form') === 'Closed') return { ok: false, error: 'Applications for this season are closed.' };
  if (!d.artist_name || !d.whatsapp || !d.slot_id) return { ok: false, error: 'Name, WhatsApp and a slot are required' };
  syncSeason();
  const S = rowsOf('Slots');
  const i = S.rows.findIndex((r) => String(r[S.col('slot_id')]) === String(d.slot_id));
  if (i < 0) return { ok: false, error: 'This slot no longer exists. Please pick another.', taken: true };
  const s = slotObj(S, S.rows[i]);
  if (s.status !== 'Open') return { ok: false, error: 'Sorry, someone just took this slot. Please pick another.', taken: true };
  const A = rowsOf('Applications');
  const wa = String(d.whatsapp).replace(/\D/g, '').slice(-10);
  if (wa.length < 10) return { ok: false, error: 'Please add a full WhatsApp number' };
  const mine = A.rows.filter((r) => String(r[A.col('whatsapp')]).replace(/\D/g, '').slice(-10) === wa && r[A.col('status')] === 'Pending');
  if (mine.length >= 2) return { ok: false, error: 'You already have two requests waiting. We will reply on WhatsApp soon.' };
  const id = 'A-' + Utilities.formatDate(new Date(), TZ, 'yyMMdd-HHmmss') + '-' + Math.floor(Math.random() * 90 + 10);
  const row = { timestamp: new Date(), application_id: id, slot_id: s.slot_id, slot_when: slotWhen(s), artist_name: clip(d.artist_name, 80), format: clip(d.format, 20), dancers: clip(d.dancers, 300), guru: clip(d.guru, 120), programme: clip(d.programme, 1500), music: clip(d.music, 20), whatsapp: "'" + clip(d.whatsapp, 20), email: clip(d.email, 120), city: clip(d.city, 80), video_link: clip(d.video_link, 300), message: clip(d.message, 1500), status: 'Pending' };
  A.sh.appendRow(TABS.Applications.map((h) => row[h] || ''));
  S.sh.getRange(i + 2, S.col('status') + 1, 1, 2).setValues([['Held', id]]);
  notify('Season slot request: ' + row.artist_name, row.slot_when + '\n' + row.artist_name + ' · ' + clip(d.whatsapp, 20) + '\n' + row.programme + '\n\nApprove or reject in the Applications tab.');
  return { ok: true, application_id: id, slot_when: row.slot_when };
}

// Keeps Slots, Applications and Events in step. Safe to run any time.
function syncSeason() {
  const S = rowsOf('Slots'), A = rowsOf('Applications');
  // Slot ids for new rows
  const used = new Set(S.rows.map((r) => String(r[0])).filter(Boolean));
  S.rows.forEach((r, i) => {
    if (r[0] || !(r[S.col('date')] instanceof Date) || !r[S.col('start_time')]) return;
    let id = 'S-' + Utilities.formatDate(r[S.col('date')], TZ, 'yyMMdd') + '-' + slotTime(r[S.col('start_time')]).replace(':', ''), k = 2;
    while (used.has(id)) id = id.replace(/-\d+$/, '') + '-' + k++;
    used.add(id); r[0] = id; S.sh.getRange(i + 2, 1).setValue(id);
    if (!r[S.col('status')]) { r[S.col('status')] = 'Open'; S.sh.getRange(i + 2, S.col('status') + 1).setValue('Open'); }
  });
  const slotRow = (id) => S.rows.findIndex((r) => String(r[0]) === String(id));
  const setSlot = (i, status, app) => {
    if (S.rows[i][S.col('status')] === status && String(S.rows[i][S.col('application_id')]) === app) return;
    S.rows[i][S.col('status')] = status; S.rows[i][S.col('application_id')] = app;
    S.sh.getRange(i + 2, S.col('status') + 1, 1, 2).setValues([[status, app]]);
  };
  A.rows.forEach((r, j) => {
    const id = String(r[A.col('application_id')]), st = String(r[A.col('status')]), i = slotRow(r[A.col('slot_id')]);
    if (!id || i < 0) return;
    const holder = String(S.rows[i][S.col('application_id')]);
    const cell = (k, v) => A.sh.getRange(j + 2, A.col(k) + 1).setValue(v);
    if (st === 'Rejected') {
      if (holder === id) setSlot(i, 'Open', '');
      if (!r[A.col('reply_link')]) cell('reply_link', waReply(r, A, 'Thank you for your interest in the Divyanjali Season. This slot is not available for you this time. We hope to see you on our stage soon.'));
    } else if (st === 'Approved') {
      if (holder && holder !== id) { cell('notes', 'Slot is held by ' + holder + '. Reject that one first.'); return; }
      setSlot(i, 'Booked', id);
      if (!r[A.col('event_code')]) {
        const s = slotObj(S, S.rows[i]);
        const clash = publishedOrDraftClash(s);
        if (clash) { cell('notes', 'Clash with event ' + clash + ' at the same date, time and venue. Not added to Events.'); return; }
        cell('event_code', addDraftEvent(s, r, A));
        cell('reply_link', waReply(r, A, 'Congratulations! Your Divyanjali Season slot is confirmed: ' + s.date + ' ' + s.start_time + ', ' + s.venue_name + '. We will share your event link soon.'));
      }
    } else if (st === 'Pending' && !holder) {
      setSlot(i, 'Held', id);
    }
  });
}
function publishedOrDraftClash(s) {
  const E = rowsOf('Events');
  const r = E.rows.find((x) => x[E.col('status')] !== 'Cancelled' && slotDate(x[E.col('date')]) === s.date && slotTime(x[E.col('start_time')]) === s.start_time && String(x[E.col('venue_name')]).trim().toLowerCase() === String(s.venue_name).trim().toLowerCase());
  return r ? String(r[0] || r[E.col('title')]) : '';
}
function addDraftEvent(s, r, A) {
  const ev = book().getSheetByName('Events');
  const g = (k) => String(r[A.col(k)] || '');
  const row = { status: 'Draft', date: new Date(s.date + 'T00:00:00+05:30'), start_time: s.start_time, duration: '', title: g('artist_name') + ' · Divyanjali Season', type: 'Performance', format: g('format') || 'Solo', mode: 'In person', lead_artist: g('artist_name'), guru: g('guru'), dancers: g('dancers'), music: g('music') || 'Live', venue_name: s.venue_name, venue_address: s.venue_address, maps_link: s.maps_link, entry: 'Free', presented_by: 'Divyanjali', about: g('programme') };
  ev.appendRow(TABS.Events.map((h) => row[h] || ''));
  fillCodes();
  CacheService.getScriptCache().remove('events');
  return String(ev.getRange(ev.getLastRow(), 1).getValue());
}
function waReply(r, A, text) {
  const n = String(r[A.col('whatsapp')]).replace(/\D/g, '');
  return n ? 'https://wa.me/' + (n.length === 10 ? '91' + n : n) + '?text=' + encodeURIComponent('Dear ' + r[A.col('artist_name')] + ', ' + text) : '';
}
function setting(key) {
  const row = book().getSheetByName('Settings').getRange('A2:B30').getValues().find((r) => r[0] === key);
  return row ? String(row[1]).trim() : '';
}
function withLock(fn) {
  const lock = LockService.getScriptLock(); lock.waitLock(20000);
  try { return fn(); } finally { lock.releaseLock(); }
}

/* ---------- Utilities ---------- */
// Sheets uploaded from Excel can be small; grow them so validation ranges fit.
function ensureSize(sh, rows, cols) {
  if (sh.getMaxRows() < rows) sh.insertRowsAfter(sh.getMaxRows(), rows - sh.getMaxRows());
  if (sh.getMaxColumns() < cols) sh.insertColumnsAfter(sh.getMaxColumns(), cols - sh.getMaxColumns());
}
function json(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function columnLetter(n) { let s = ''; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; }

/* ---------- Self test: adds a test event, wish and enquiry, then checks them ---------- */
const TEST_TITLE = 'TEST Website Check';
function runTests() {
  const ss = book();
  const out = [];
  const ok = (name, pass, detail) => out.push((pass ? 'PASS  ' : 'FAIL  ') + name + (detail ? '  (' + detail + ')' : ''));
  CacheService.getScriptCache().remove('events');

  // 1. Test event row
  const ev = ss.getSheetByName('Events');
  const head = TABS.Events;
  const d = new Date(); d.setDate(d.getDate() + 7); d.setHours(0, 0, 0, 0);
  const row = { status: 'Published', date: d, start_time: '18:00', duration: '2 hrs', title: TEST_TITLE, type: 'Performance', format: 'Solo', mode: 'In person', lead_artist: 'Test Dancer', guru: 'Dr. S. Divyasena', orchestra: 'Mridangam: Sri B.P. Haribabu', music: 'Live', venue_name: 'Test Sabha', venue_address: 'Chennai', maps_link: 'https://maps.google.com/?q=Chennai', entry: 'Free', presented_by: 'Divyanjali', why_attend: 'Test row. Safe to delete.', invite_message: 'Test invite.', about: 'Created by Run website test.' };
  ev.appendRow(head.map((h) => row[h] || ''));
  fillCodes();
  const code = String(ev.getRange(ev.getLastRow(), 1).getValue());
  ok('Event code filled in automatically', /^DV-\d{6}-TEST/.test(code), code);

  // 2. Website read
  const res = JSON.parse(doGet({ parameter: { action: 'events' } }).getContent());
  const mine = (res.events || []).find((x) => x.event_code === code);
  ok('Website can read published events', !!mine, (res.events || []).length + ' published');
  ok('Date and time come out in website format', !!mine && /^\d{4}-\d{2}-\d{2}$/.test(mine.date) && /^\d{2}:\d{2}$/.test(mine.start_time), mine ? mine.date + ' ' + mine.start_time : 'missing');
  ok('Private columns are hidden', !!mine && !('status' in mine) && !('photo_check' in mine));

  // 3. Wish / feedback form
  const w = JSON.parse(doPost({ postData: { contents: JSON.stringify({ form: 'response', event_code: code, kind: 'Wish', name: 'Test Visitor', city: 'Chennai', message: 'Test wish from Run website test', show_public: 'Yes' }) } }).getContent());
  ok('Wish form saves to Responses', w.ok === true, w.error || '');
  const rs = ss.getSheetByName('Responses');
  const last = rs.getRange(rs.getLastRow(), 1, 1, TABS.Responses.length).getValues()[0];
  ok('Wish is linked to the event', last[1] === code && last[2] === TEST_TITLE, last[2]);
  ok('Unapproved wish is not shown publicly', publicWishes(code).length === 0);
  rs.getRange(rs.getLastRow(), TABS.Responses.indexOf('approved') + 1).setValue('Yes');
  ok('Approved wish is shown on the event page', publicWishes(code).length === 1);

  // 4. Enquiry form
  const q = JSON.parse(doPost({ postData: { contents: JSON.stringify({ form: 'enquiry', enquiry_type: 'Performance booking', from_event_code: code, name: 'Test Visitor', whatsapp: '+91 90000 00000', message: 'Test enquiry from Run website test' }) } }).getContent());
  ok('Enquiry form saves to Enquiries', q.ok === true, q.error || '');

  // 5. Spam trap
  const before = rs.getLastRow();
  doPost({ postData: { contents: JSON.stringify({ form: 'response', event_code: code, name: 'Bot', message: 'spam', website: 'http://spam' }) } });
  ok('Spam trap blocks bots', rs.getLastRow() === before);

  // 6. Season artist slots
  const sl = ss.getSheetByName('Slots');
  const sd = new Date(d); sd.setDate(sd.getDate() + 1);
  sl.appendRow(TABS.Slots.map((h) => ({ date: sd, start_time: '17:00', end_time: '17:45', venue_name: 'Test Sabha', venue_address: 'Chennai', slot_for: 'Solo or group' })[h] || ''));
  syncSeason();
  const slot = openSlots().find((x) => x.venue_name === 'Test Sabha');
  ok('New slot gets an id and shows on the website', !!slot, slot ? slot.slot_id : 'missing');
  const app = (n) => JSON.parse(doPost({ postData: { contents: JSON.stringify({ form: 'application', slot_id: slot && slot.slot_id, artist_name: TEST_TITLE, format: 'Solo', guru: 'Test Guru', programme: 'Test programme from Run website test', music: 'Live', whatsapp: '+91 9000000' + n }) } }).getContent());
  const a1 = app('001'), a2 = app('002');
  ok('Artist request holds the slot', a1.ok === true && !openSlots().some((x) => x.venue_name === 'Test Sabha'), a1.error || '');
  ok('Second artist cannot take the same slot', a2.ok === false && a2.taken === true);
  const ap = ss.getSheetByName('Applications');
  ap.getRange(ap.getLastRow(), TABS.Applications.indexOf('status') + 1).setValue('Approved');
  syncSeason();
  const code2 = String(ap.getRange(ap.getLastRow(), TABS.Applications.indexOf('event_code') + 1).getValue());
  ok('Approved request adds a Draft event', /^DV-/.test(code2), code2 || 'none');

  const fails = out.filter((l) => l.indexOf('FAIL') === 0).length;
  Logger.log(out.join('\n'));
  CacheService.getScriptCache().remove('events');
  const msg = (fails ? fails + ' check(s) failed.\n\n' : 'All checks passed.\n\n') + out.join('\n') + '\n\nThe test event is live on the website now. Use Divyanjali > Remove test rows when done.';
  try { SpreadsheetApp.getUi().alert('Website test', msg, SpreadsheetApp.getUi().ButtonSet.OK); } catch (e) { /* run from editor: see Execution log */ }
}
function removeTests() {
  const ss = book();
  [['Events', TABS.Events.indexOf('title')], ['Responses', TABS.Responses.indexOf('event_title')], ['Enquiries', TABS.Enquiries.indexOf('message')], ['Slots', TABS.Slots.indexOf('venue_name')], ['Applications', TABS.Applications.indexOf('artist_name')]].forEach(([n, c]) => {
    const sh = ss.getSheetByName(n); if (!sh) return; const v = sh.getDataRange().getValues();
    for (let r = v.length - 1; r >= 1; r--) {
      const cell = String(v[r][c]);
      if (cell.indexOf(TEST_TITLE) === 0 || cell === 'Test Sabha' || cell.indexOf('Run website test') >= 0 || (n === 'Responses' && v[r][4] === 'Test Visitor')) sh.deleteRow(r + 1);
    }
  });
  CacheService.getScriptCache().remove('events');
  ss.toast('Test rows removed.', 'Divyanjali', 5);
}
