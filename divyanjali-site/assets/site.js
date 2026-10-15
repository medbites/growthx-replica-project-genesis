/* Divyanjali site: small shared script, no libraries. */
const CONFIG = {
  SCRIPT_URL: 'https://script.google.com/macros/s/AKfycbwlZ0KujTvaUagVM4TVpEUeVyp2XH2svG3bRkh-k7ipESLJchbw4Bj6afAUSl-JWfWE/exec',
  WHATSAPP: '919000000000'
};
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const waLink = (text) => 'https://wa.me/' + CONFIG.WHATSAPP + '?text=' + encodeURIComponent(text);

/* ----- One shared full-screen viewer for photos, videos and Instagram ----- */
const modal = document.createElement('dialog');
modal.id = 'modal';
modal.innerHTML = '<p class="mcap"></p><button class="mx" type="button" aria-label="Close">×</button><button class="mnav mprev" type="button" aria-label="Previous">‹</button><button class="mnav mnext" type="button" aria-label="Next">›</button><div class="mbody"></div>';
document.body.appendChild(modal);
let gallery = [], gi = 0;
function openModal(html, cap, nav) {
  $('.mbody', modal).innerHTML = html;
  $('.mcap', modal).textContent = cap || '';
  $$('.mnav', modal).forEach((b) => { b.hidden = !nav; });
  if (!modal.open) modal.showModal();
}
function showPhoto(i) {
  gi = (i + gallery.length) % gallery.length;
  const img = gallery[gi];
  openModal('<img src="' + esc(img.currentSrc || img.src) + '" alt="' + esc(img.alt) + '">', img.alt + (gallery.length > 1 ? '  ·  ' + (gi + 1) + ' / ' + gallery.length : ''), gallery.length > 1);
}
modal.addEventListener('close', () => { $('.mbody', modal).innerHTML = ''; });
modal.addEventListener('click', (ev) => {
  if (ev.target.closest('.mprev')) return showPhoto(gi - 1);
  if (ev.target.closest('.mnext')) return showPhoto(gi + 1);
  if (ev.target.closest('.mx') || ev.target === modal || ev.target.classList.contains('mbody') || ev.target.tagName === 'IMG') modal.close();
});
document.addEventListener('keydown', (ev) => {
  if (!modal.open || !gallery.length || !$('.mbody img', modal)) return;
  if (ev.key === 'ArrowLeft') showPhoto(gi - 1);
  if (ev.key === 'ArrowRight') showPhoto(gi + 1);
});

/* ----- Image slots: the photo shows once the file exists; until then the labelled placeholder stays ----- */
$$('.ph[data-src]').forEach((ph) => {
  const img = new Image();
  img.loading = 'lazy'; img.decoding = 'async';
  img.alt = ph.dataset.alt || $('span', ph)?.textContent || '';
  img.onerror = () => img.remove();
  img.src = ph.dataset.src;
  ph.appendChild(img);
});

/* ----- YouTube: thumbnail first, the player loads (and plays here) on tap ----- */
function ytId(u) {
  const m = String(u).match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([\w-]{11})/);
  return m ? m[1] : (/^[\w-]{11}$/.test(u) ? u : '');
}
$$('.yt[data-yt]').forEach((b) => {
  const id = ytId(b.dataset.yt);
  if (!id) return;
  b.style.backgroundImage = 'url(https://i.ytimg.com/vi/' + id + '/hqdefault.jpg)';
  if (!$('.play', b)) b.insertAdjacentHTML('afterbegin', '<span class="play" aria-hidden="true"></span>');
});

document.addEventListener('click', (ev) => {
  const yt = ev.target.closest('.yt[data-yt]');
  if (yt && !$('iframe', yt)) {
    ev.preventDefault();
    const id = ytId(yt.dataset.yt);
    yt.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1' + (yt.dataset.start ? '&start=' + yt.dataset.start : '') + '" title="' + esc(yt.getAttribute('aria-label') || 'Video') + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
    return;
  }
  const ig = ev.target.closest('[data-ig]');
  if (ig) {
    ev.preventDefault();
    const base = ig.dataset.ig.split('?')[0].replace(/\/?$/, '/');
    gallery = [];
    openModal('<iframe src="' + esc(base) + 'embed/" title="Instagram post" loading="lazy" allowfullscreen></iframe>', 'Instagram · @divyanjalidance', false);
    return;
  }
  const pic = ev.target.closest('.ph > img');
  if (pic) {
    const scope = pic.closest('[data-gallery]') || document;
    gallery = $$('.ph > img', scope).filter((i) => i.complete && i.naturalWidth);
    showPhoto(Math.max(0, gallery.indexOf(pic)));
    return;
  }
  const chip = ev.target.closest('[data-filter] [data-f]');
  if (chip) {
    const bar = chip.closest('[data-filter]');
    $$('[data-f]', bar).forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
    const f = chip.dataset.f;
    let shown = 0;
    $$(bar.dataset.filter + ' [data-cat]').forEach((it) => {
      const on = f === 'All' || it.dataset.cat.split('|').includes(f);
      it.classList.toggle('off', !on); if (on) shown++;
    });
    const count = $(bar.dataset.count || '#none'); if (count) count.textContent = 'Showing ' + shown;
    return;
  }
  const yr = ev.target.closest('[data-track] [data-y]');
  if (yr) {
    const bar = yr.closest('[data-track]');
    $$('[data-y]', bar).forEach((c) => c.setAttribute('aria-pressed', String(c === yr)));
    $(bar.dataset.track).innerHTML = yr.dataset.html;
  }
});

/* ----- Numbers count up once, when they come into view ----- */
const io = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (!en.isIntersecting) return;
    const el = en.target; io.unobserve(el);
    if (el.classList.contains('reveal')) { el.classList.add('in'); return; }
    const end = parseInt(el.dataset.count, 10), plus = el.dataset.plus || '';
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = end + plus; return; }
    const t0 = performance.now();
    const step = (t) => { const k = Math.min(1, (t - t0) / 1200); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))) + plus; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  });
}, { rootMargin: '0px 0px -10% 0px' }) : null;
$$('[data-count], .reveal').forEach((el) => { if (io) io.observe(el); else el.classList.add('in'); });

/* ----- WhatsApp links with a ready message ----- */
$$('[data-wa]').forEach((a) => { a.href = waLink(a.dataset.wa || 'Hello Divyanjali'); a.target = '_blank'; a.rel = 'noopener'; });

/* ----- Enquiry forms: saved to the Enquiries tab of the Google Sheet ----- */
$$('form[data-enquiry]').forEach((f) => {
  const qs = new URLSearchParams(location.search);
  if (qs.get('type') && f.elements['enquiry_type']) f.elements['enquiry_type'].value = qs.get('type');
  if (qs.get('production') && f.elements['message'] && !f.elements['message'].value) f.elements['message'].value = 'About the production: ' + qs.get('production');
  $$('[data-settype]').forEach((b) => b.addEventListener('click', () => {
    f.elements['enquiry_type'].value = b.dataset.settype;
    $$('[data-settype]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    f.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }));
  f.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const box = $('.msg', f) || f.appendChild(Object.assign(document.createElement('div'), { className: 'msg', role: 'status' }));
    const name = (f.elements['name'] || {}).value || '', wa = (f.elements['whatsapp'] || {}).value || '';
    if (!name.trim() || wa.replace(/\D/g, '').length < 10) { box.className = 'msg err'; box.textContent = 'Please add your name and a full WhatsApp number.'; return; }
    const data = { form: 'enquiry', enquiry_type: f.dataset.enquiry };
    const extra = [];
    new FormData(f).forEach((v, k) => {
      const field = f.elements[k]; v = String(v).trim();
      if (field && field.dataset && field.dataset.extra !== undefined) { if (v) extra.push(field.dataset.extra + ': ' + v); }
      else data[k] = v;
    });
    if (extra.length) data.message = extra.join('\n') + (data.message ? '\n\n' + data.message : '');
    box.className = 'msg'; box.textContent = 'Sending…';
    try {
      const r = await fetch(CONFIG.SCRIPT_URL, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(data) });
      const res = await r.json();
      if (!res.ok) throw new Error(res.error || 'failed');
      location.href = '/thank-you';
    } catch (err) { box.className = 'msg err'; box.textContent = 'Could not send. Please try again, or message us on WhatsApp.'; }
  });
});

/* ----- Home: the next three events, from the same Google Sheet as the calendar ----- */
(async function nextEvents() {
  const box = $('#nextEvents'); if (!box) return;
  let list = null;
  try { const r = await fetch(CONFIG.SCRIPT_URL + '?action=events'); list = (await r.json()).events; } catch (err) { try { list = JSON.parse(localStorage.getItem('dv_events') || 'null'); } catch (e) { list = null; } }
  const now = Date.now();
  const up = (list || []).map((e) => Object.assign(e, { start: new Date(e.date + 'T' + String(e.start_time || '00:00').slice(0, 5) + ':00+05:30') }))
    .filter((e) => !isNaN(e.start) && e.start.getTime() > now - 3 * 3600e3).sort((a, b) => a.start - b.start).slice(0, 3);
  if (!up.length) { box.innerHTML = '<div class="empty">New events will appear here soon. <a href="/events">See the calendar</a>.</div>'; return; }
  const d = (x, o) => new Intl.DateTimeFormat('en-IN', Object.assign({ timeZone: 'Asia/Kolkata' }, o)).format(x);
  box.innerHTML = up.map((e) => '<a class="tile" href="/e/' + encodeURIComponent(e.event_code) + '"><span class="meta">' + d(e.start, { weekday: 'short', day: 'numeric', month: 'short' }) + ' · ' + d(e.start, { hour: 'numeric', minute: '2-digit', hour12: true }).toUpperCase() + '</span><h3>' + esc(e.title) + '</h3><p class="muted">' + esc(e.type || '') + ' · ' + esc(e.mode === 'Online' ? 'Online' : (e.venue_name || '')) + '</p><span class="badge ' + (e.mode === 'Online' ? 'm-ol' : e.mode === 'Hybrid' ? 'm-hy' : 'm-ip') + '" style="align-self:flex-start">' + esc(e.mode || 'In person') + '</span></a>').join('');
})();

/* ----- Gallery videos and Instagram posts, from assets/media.json (easy to edit, no rebuild) ----- */
(async function mediaLists() {
  const yt = $('#ytList'), ig = $('#igList'); if (!yt && !ig) return;
  let m = { youtube: [], instagram: [] };
  try { m = await (await fetch('/assets/media.json', { cache: 'no-cache' })).json(); } catch (err) { /* keep empty */ }
  if (yt) {
    yt.innerHTML = (m.youtube || []).map((v) => '<a class="yt" data-cat="Videos|' + esc(v.cat || '') + '" href="' + esc(v.link) + '" data-yt="' + esc(v.link) + '" aria-label="Play: ' + esc(v.title) + '"><span class="cap">' + esc(v.title) + '</span></a>').join('')
      + '<a class="ig" href="https://www.youtube.com/channel/UCLPvhdH5qXt0R4IyDt1eSHg" target="_blank" rel="noopener" style="aspect-ratio:16/9"><b>More on our YouTube channel ›</b></a>';
    $$('.yt[data-yt]', yt).forEach((b) => { const id = ytId(b.dataset.yt); b.style.backgroundImage = 'url(https://i.ytimg.com/vi/' + id + '/hqdefault.jpg)'; b.insertAdjacentHTML('afterbegin', '<span class="play" aria-hidden="true"></span>'); });
  }
  if (ig) {
    ig.innerHTML = (m.instagram || []).map((p) => '<button class="ig" type="button" data-ig="' + esc(p.link) + '"><b>▶ ' + esc(p.title || 'Instagram') + '</b></button>').join('')
      + '<a class="ig" href="https://www.instagram.com/divyanjalidance/" target="_blank" rel="noopener"><b>Follow @divyanjalidance ›</b></a>';
  }
})();
