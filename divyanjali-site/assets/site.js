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
  if (ev.target.closest('.mx') || ev.target === modal || ev.target.classList.contains('mbody') || (ev.target.tagName === 'IMG' && !ev.target.closest('.qv'))) modal.close();
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
  if (pic && !pic.closest('.deck')) {
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

/* ----- Numbers count up when they come into view, and again on hover ----- */
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
function countUp(el) {
  const end = parseInt(el.dataset.count, 10), plus = el.dataset.plus || '';
  if (reduceMotion) { el.textContent = end + plus; return; }
  const t0 = performance.now();
  const step = (t) => { const k = Math.min(1, (t - t0) / 1200); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))) + plus; if (k < 1) requestAnimationFrame(step); };
  requestAnimationFrame(step);
}
const io = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (!en.isIntersecting) return;
    const el = en.target; io.unobserve(el);
    if (el.classList.contains('reveal')) { el.classList.add('in'); return; }
    countUp(el);
  });
}, { rootMargin: '0px 0px -10% 0px' }) : null;
// only real numbers count up; a filter bar's data-count points at its counter instead
$$('[data-count], .reveal').filter((el) => el.classList.contains('reveal') || /^\d+$/.test(el.dataset.count)).forEach((el) => { if (io) io.observe(el); else el.classList.add('in'); });
$$('a.stat').forEach((a) => {
  let last = 0;
  a.addEventListener('mouseenter', () => { const b = $('[data-count]', a); if (b && Date.now() - last > 1500) { last = Date.now(); countUp(b); } });
});

/* ----- Landing video: the dancers' photo shows first; the video fades in only once YouTube says it is really playing ----- */
(function landingVideo() {
  const vh = $('.vh[data-vh]'); if (!vh) return;
  const id = vh.dataset.vh, start = Number(vh.dataset.start || 0), media = $('.vh-media', vh), poster = $('.vh-poster', vh);
  poster.style.backgroundImage = 'url(https://i.ytimg.com/vi/' + id + '/maxresdefault.jpg), url(https://i.ytimg.com/vi/' + id + '/hqdefault.jpg)';
  const saveData = navigator.connection && navigator.connection.saveData;
  const btnPlay = $('[data-vh-play]', vh), btnMute = $('[data-vh-mute]', vh), hint = $('.vh-hint', vh);
  let player = null, userPaused = false, playing = false, wantSound = false;
  const setPaused = (p) => { vh.classList.toggle('paused', p); btnPlay.setAttribute('aria-label', p ? 'Play video' : 'Pause video'); };
  const setSound = (on) => { wantSound = on; vh.classList.toggle('sound', on); btnMute.setAttribute('aria-label', on ? 'Turn sound off' : 'Turn sound on'); hint.textContent = on ? 'Sound on' : 'Sound off · tap to listen'; };
  // If the phone blocks the player (low power mode and the like), open the normal player with sound instead.
  const fallback = () => { gallery = []; openModal('<iframe style="width:min(100%,1100px);height:auto;aspect-ratio:16/9;background:#000" src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1&start=' + start + '" title="Divyanjali on stage" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>', 'Divyanjali on stage', false); };
  function load() {
    if (player || window.__vhLoading) return; window.__vhLoading = true;
    const holder = document.createElement('div'); media.appendChild(holder);
    const make = () => {
      player = new YT.Player(holder, {
        host: 'https://www.youtube-nocookie.com', videoId: id,
        playerVars: { autoplay: 1, mute: 1, controls: 0, disablekb: 1, fs: 0, loop: 1, playlist: id, modestbranding: 1, playsinline: 1, rel: 0, iv_load_policy: 3, start, origin: location.origin },
        events: {
          onReady: (ev) => { ev.target.mute(); if (!userPaused) ev.target.playVideo(); const f = ev.target.getIframe(); f.tabIndex = -1; f.title = 'Divyanjali on stage (background video)'; },
          onStateChange: (ev) => {
            if (ev.data === 1) { playing = true; setTimeout(() => { if (playing) vh.classList.add('playing'); }, 600); setPaused(false); }
            if (ev.data === 2) { playing = false; }
            if (ev.data === 0) { ev.target.seekTo(start); ev.target.playVideo(); }
          },
          onError: () => { vh.classList.remove('playing'); setPaused(true); }
        }
      });
    };
    if (window.YT && YT.Player) make();
    else {
      const prev = window.onYouTubeIframeAPIReady;
      window.onYouTubeIframeAPIReady = () => { if (prev) prev(); make(); };
      const sc = document.createElement('script'); sc.src = 'https://www.youtube.com/iframe_api'; sc.async = true;
      sc.onerror = () => setPaused(true);
      document.head.appendChild(sc);
    }
    // Nothing playing after a few seconds: keep the photo, show the play button.
    setTimeout(() => { if (!playing) setPaused(true); }, 7000);
  }
  function play() {
    userPaused = false;
    if (!player) { load(); setPaused(false); return; }
    player.playVideo(); setPaused(false);
    setTimeout(() => { if (!playing) { setPaused(true); fallback(); } }, 2500);
  }
  btnPlay.addEventListener('click', () => {
    if (vh.classList.contains('paused')) return play();
    userPaused = true; if (player && player.pauseVideo) player.pauseVideo(); setPaused(true);
  });
  btnMute.addEventListener('click', () => {
    const on = !wantSound; setSound(on);
    if (!player || !player.unMute) { if (on) fallback(); return; }
    if (on) { player.unMute(); player.setVolume(100); if (!playing) play(); } else player.mute();
  });
  if (reduceMotion || saveData) { setPaused(true); hint.textContent = 'Tap play to watch'; }
  else load();
  // Pause when scrolled away, carry on when back (unless the visitor paused it).
  if ('IntersectionObserver' in window) new IntersectionObserver(([en]) => {
    if (!player || !player.playVideo || userPaused) return;
    if (en.isIntersecting) player.playVideo(); else player.pauseVideo();
  }, { threshold: 0.15 }).observe(vh);
  // Gentle depth on scroll: the words lift and fade, the video drifts slower.
  if (!reduceMotion) {
    const inner = $('.vh-in', vh); let ticking = false;
    addEventListener('scroll', () => {
      if (ticking) return; ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        const y = Math.min(scrollY, vh.offsetHeight);
        inner.style.transform = 'translateY(' + (-y * 0.18) + 'px)';
        inner.style.opacity = String(1 - y / vh.offsetHeight * 1.1);
        media.style.transform = 'translateY(' + (y * 0.3) + 'px)';
      });
    }, { passive: true });
  }
})();

/* ----- Class cards: tap to flip, dots follow the swipe, a gentle tilt under the mouse ----- */
(function classCards() {
  const wrap = $('#classCards'); if (!wrap) return;
  const sec = wrap.closest('section'), cards = $$('.cc', wrap), dots = $$('.cc-dots i', sec);
  if ('IntersectionObserver' in window) new IntersectionObserver(([en], o) => { if (en.isIntersecting) { sec.classList.add('seen'); o.disconnect(); } }, { threshold: 0.2 }).observe(sec);
  else sec.classList.add('seen');
  function flip(card, on) {
    $('.cc-in', card).style.transform = '';   // drop the hover tilt so the flip can run
    card.classList.toggle('flipped', on);
    $('.cc-f .cc-flip', card).setAttribute('aria-expanded', String(on));
    $('.cc-b', card).setAttribute('aria-hidden', String(!on));
    $$('.cc-b a, .cc-b button', card).forEach((el) => { el.tabIndex = on ? 0 : -1; });
    $('.cc-f .cc-flip', card).tabIndex = on ? -1 : 0;
    (on ? $('.cc-b .btn', card) : $('.cc-f .cc-flip', card)).focus({ preventScroll: true });
  }
  wrap.addEventListener('click', (ev) => {
    const card = ev.target.closest('.cc'); if (!card || ev.target.closest('a')) return;
    flip(card, !card.classList.contains('flipped'));
    cards.forEach((c) => { if (c !== card && c.classList.contains('flipped')) flip(c, false); });
  });
  wrap.addEventListener('scroll', () => {
    const i = Math.round(wrap.scrollLeft / (cards[0].offsetWidth + 14));
    dots.forEach((d, j) => d.classList.toggle('on', j === i));
  }, { passive: true });
  if (!reduceMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) cards.forEach((c) => {
    c.addEventListener('pointermove', (ev) => {
      if (c.classList.contains('flipped')) return;
      const r = c.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width - 0.5, y = (ev.clientY - r.top) / r.height - 0.5;
      $('.cc-in', c).style.transform = 'rotateX(' + (-y * 6) + 'deg) rotateY(' + (x * 8) + 'deg)';
    });
    c.addEventListener('pointerleave', () => { $('.cc-in', c).style.transform = ''; });
  });
})();

/* ----- Small helpers: a toast, and copying a link ----- */
function toast(msg) {
  let t = $('.toast'); if (!t) { t = document.createElement('div'); t.className = 'toast'; t.setAttribute('role', 'status'); document.body.appendChild(t); }
  t.textContent = msg; t.classList.add('on'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('on'), 1800);
}
async function copyText(text) {
  try { await navigator.clipboard.writeText(text); toast('Link copied'); }
  catch (err) { const i = Object.assign(document.createElement('input'), { value: text }); document.body.appendChild(i); i.select(); document.execCommand('copy'); i.remove(); toast('Link copied'); }
}

/* ----- A dancer's page: copy link, share, save as PDF ----- */
$$('[data-copy]').forEach((b) => b.addEventListener('click', () => copyText(location.href.split('#')[0])));
$$('[data-print]').forEach((b) => b.addEventListener('click', () => window.print()));
$$('[data-share]').forEach((b) => {
  if (!navigator.share) return;
  b.hidden = false;
  b.addEventListener('click', () => navigator.share({ title: document.title, url: location.href.split('#')[0] }).catch(() => {}));
});

/* ----- Accolades: find a dancer by name, together with the chips ----- */
(function accSearch() {
  const q = $('#accSearch'), grid = $('#studentGrid'); if (!q || !grid) return;
  const count = () => { const n = $$('.stc', grid).filter((c) => !c.classList.contains('off') && !c.classList.contains('hide')).length; $('#accCount').textContent = n ? 'Showing ' + n : 'No dancer by that name yet'; };
  q.addEventListener('input', () => { const v = q.value.trim().toLowerCase(); $$('.stc', grid).forEach((c) => c.classList.toggle('hide', !!v && !c.dataset.name.includes(v))); count(); });
  $$('[data-f]').forEach((c) => c.addEventListener('click', () => setTimeout(count)));
  $$('[data-jump]').forEach((a) => a.addEventListener('click', (ev) => { ev.preventDefault(); const c = $('[data-f="' + a.dataset.jump + '"]'); if (c) c.click(); grid.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' }); }));
})();

/* ----- 30 years: the souvenir as a book. Two pages side by side on wide screens, one on phones ----- */
(function flipBook() {
  const fb = $('#flip'); if (!fb) return;
  const N = Number(fb.dataset.pages), book = $('#fbBook'), range = $('#fbRange'), num = $('#fbNum'), thumbs = $('#fbThumbs'), textBox = $('#fbText');
  const src = (n) => '/assets/souvenir/' + String(n).padStart(2, '0') + '.webp';
  const img = (n) => n ? '<img src="' + src(n) + '" alt="Souvenir page ' + n + '" draggable="false">' : '';
  let spread = false, page = 1, busy = false, texts = null;
  // A spread shows [left, right]: the cover sits alone on the right, the back cover alone on the left.
  const view = (p) => { if (!spread) return [p]; if (p <= 1) return [0, 1]; const l = p % 2 === 0 ? p : p - 1; return [l, l + 1 <= N ? l + 1 : 0]; };
  const first = (v) => v.find((x) => x) || 1;
  function paint() {
    const v = view(page);
    book.innerHTML = spread
      ? '<div class="fb-pg l' + (v[0] ? '' : ' empty') + '">' + img(v[0]) + '</div><div class="fb-pg r' + (v[1] ? '' : ' empty') + '">' + img(v[1]) + '</div>'
      : '<div class="fb-pg">' + img(v[0]) + '</div>';
    const shown = v.filter(Boolean);
    num.textContent = shown[0] === 1 && shown.length === 1 ? 'Cover' : 'Page ' + shown.join('–') + ' / ' + N;
    range.value = shown[0];
    $('[data-fb="prev"]', fb).disabled = shown[0] <= 1;
    $('[data-fb="next"]', fb).disabled = shown[shown.length - 1] >= N;
    $$('button', thumbs).forEach((b) => b.classList.toggle('on', shown.includes(Number(b.dataset.goto))));
    const on = $('button.on', thumbs);
    if (on) { const r = on.getBoundingClientRect(), sr = thumbs.getBoundingClientRect(); if (r.left < sr.left || r.right > sr.right) thumbs.scrollTo({ left: thumbs.scrollLeft + r.left - sr.left - sr.width / 2 + r.width / 2, behavior: 'smooth' }); }
    history.replaceState(null, '', '#p=' + shown[0]);
    if (!textBox.hidden) showText();
    // fetch the next pages early so the turn is instant
    [shown[shown.length - 1] + 1, shown[shown.length - 1] + 2, shown[0] - 1].forEach((n) => { if (n >= 1 && n <= N) new Image().src = src(n); });
  }
  function go(target) {
    target = Math.max(1, Math.min(N, target));
    const from = view(page), to = view(target);
    if (busy || first(from) === first(to)) return;
    const dir = first(to) > first(from) ? 1 : -1;
    if (reduceMotion) { page = target; paint(); return; }
    busy = true;
    // the page underneath shows the destination; one leaf turns over the top
    const leaf = document.createElement('div');
    if (spread) {
      leaf.className = 'fb-leaf ' + (dir > 0 ? 'fwd' : 'back');
      leaf.innerHTML = dir > 0 ? '<div class="f">' + img(from[1]) + '</div><div class="b">' + img(to[0]) + '</div>' : '<div class="f">' + img(from[0]) + '</div><div class="b">' + img(to[1]) + '</div>';
      const under = dir > 0 ? $('.fb-pg.r', book) : $('.fb-pg.l', book);
      const n = dir > 0 ? to[1] : to[0];
      under.innerHTML = img(n); under.classList.toggle('empty', !n);
    } else {
      // one page at a time: the page peels off from the right corner, or peels back on
      leaf.className = 'fb-leaf fwd peel' + (dir > 0 ? '' : ' unpeel');
      if (dir > 0) { leaf.innerHTML = '<div class="f">' + img(from[0]) + '</div><div class="b"></div>'; $('.fb-pg', book).innerHTML = img(to[0]); }
      else { leaf.innerHTML = '<div class="f">' + img(to[0]) + '</div><div class="b"></div>'; }
    }
    book.appendChild(leaf);
    if (spread) requestAnimationFrame(() => requestAnimationFrame(() => { leaf.style.transform = dir > 0 ? 'rotateY(-180deg)' : 'rotateY(180deg)'; }));
    setTimeout(() => { page = target; busy = false; paint(); }, spread ? 760 : 820);
  }
  const step = (d) => { const v = view(page).filter(Boolean); go(d > 0 ? v[v.length - 1] + 1 : v[0] - 1); };
  async function showText() {
    if (!texts) { try { texts = await (await fetch('/assets/souvenir/text.json')).json(); } catch (err) { texts = []; } }
    const v = view(page).filter(Boolean);
    textBox.innerHTML = v.map((n) => '<h3>Page ' + n + '</h3>' + esc(texts[n - 1] || '(This page is a picture.)')).join('<br><br>');
  }
  function layout() {
    const s = fb.clientWidth >= 760;
    if (s !== spread) { spread = s; fb.classList.toggle('spread', s); paint(); }
  }
  fb.addEventListener('click', (ev) => {
    const b = ev.target.closest('[data-fb]');
    if (b) {
      const a = b.dataset.fb;
      if (a === 'next') step(1);
      if (a === 'prev') step(-1);
      return;
    }
    // tap the right half of the book to go on, the left half to go back
    const pg = ev.target.closest('.fb-book');
    if (pg) { const r = pg.getBoundingClientRect(); step(ev.clientX > r.left + r.width / 2 ? 1 : -1); }
  });
  document.addEventListener('click', (ev) => {
    const g = ev.target.closest('[data-goto]'); if (g) { ev.preventDefault(); go(Number(g.dataset.goto)); if (!g.closest('.fb-thumbs')) fb.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' }); return; }
    const t = ev.target.closest('.fb-tools [data-fb]'); if (!t) return;
    const a = t.dataset.fb;
    if (a === 'text') { const on = textBox.hidden; textBox.hidden = !on; t.setAttribute('aria-pressed', String(on)); if (on) showText(); }
    if (a === 'zoom') { const v = view(page).filter(Boolean); gallery = []; openModal(v.map((n) => '<img src="' + src(n) + '" alt="Souvenir page ' + n + '" style="max-width:' + (100 / v.length) + '%">').join(''), 'Souvenir 2026 · page ' + v.join('–'), false); $('.mbody', modal).style.display = 'flex'; $('.mbody', modal).style.justifyContent = 'center'; }
    if (a === 'full') { if (document.fullscreenElement) document.exitFullscreen(); else if (fb.requestFullscreen) fb.requestFullscreen(); else toast('Full screen is not available here'); }
    if (a === 'share') copyText(location.origin + location.pathname + '#p=' + view(page).filter(Boolean)[0]);
  });
  modal.addEventListener('close', () => { $('.mbody', modal).style.display = ''; });
  range.addEventListener('input', () => go(Number(range.value)));
  fb.addEventListener('keydown', (ev) => { if (ev.key === 'ArrowRight') { ev.preventDefault(); step(1); } if (ev.key === 'ArrowLeft') { ev.preventDefault(); step(-1); } });
  let x0 = null;
  book.addEventListener('touchstart', (ev) => { x0 = ev.touches[0].clientX; }, { passive: true });
  book.addEventListener('touchend', (ev) => { if (x0 === null) return; const dx = ev.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 40) { ev.preventDefault(); step(dx < 0 ? 1 : -1); } });
  const m = location.hash.match(/p=(\d+)/); if (m) page = Math.max(1, Math.min(N, Number(m[1])));
  spread = fb.clientWidth >= 760; fb.classList.toggle('spread', spread); paint();
  if (!m && 'IntersectionObserver' in window && !reduceMotion) {
    new IntersectionObserver(([en], o) => {
      if (!en.isIntersecting) return; o.disconnect();
      if (page !== 1) return;
      if (spread) setTimeout(() => go(2), 700);            // wide screens: the cover swings open
      else { const c = $('.fb-pg', book); c.classList.add('hint'); setTimeout(() => c.classList.remove('hint'), 1500); }   // phones: the corner lifts
    }, { threshold: 0.6 }).observe(fb);
  }
  addEventListener('resize', layout);
  addEventListener('hashchange', () => { const h = location.hash.match(/p=(\d+)/); if (h) go(Number(h[1])); });
})();

/* ----- Artist profile: share menu, tap-to-open cards, section tabs that follow the scroll ----- */
(function artistProfile() {
  const menu = $('[data-share-menu]'), pop = $('.share-pop');
  if (menu && pop) {
    const url = encodeURIComponent(location.href.split('#')[0]), title = encodeURIComponent(document.title);
    const x = $('[data-share-x]', pop), fbk = $('[data-share-fb]', pop);
    if (x) { x.href = 'https://twitter.com/intent/tweet?url=' + url + '&text=' + title; x.target = '_blank'; x.rel = 'noopener'; }
    if (fbk) { fbk.href = 'https://www.facebook.com/sharer/sharer.php?u=' + url; fbk.target = '_blank'; fbk.rel = 'noopener'; }
    const close = () => { pop.hidden = true; menu.setAttribute('aria-expanded', 'false'); };
    menu.addEventListener('click', (ev) => { ev.stopPropagation(); pop.hidden = !pop.hidden; menu.setAttribute('aria-expanded', String(!pop.hidden)); });
    document.addEventListener('click', (ev) => { if (!pop.hidden && !pop.contains(ev.target)) close(); });
    document.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') close(); });
  }
  $$('.lin, .ab').forEach((b) => b.addEventListener('click', () => b.setAttribute('aria-expanded', String(b.getAttribute('aria-expanded') !== 'true'))));
  const tabs = $('.bio-tabs'); if (!tabs || !('IntersectionObserver' in window)) return;
  const links = $$('a', tabs), strip = $('.wrap', tabs);
  const spy = new IntersectionObserver((ens) => ens.forEach((en) => {
    if (!en.isIntersecting) return;
    links.forEach((a) => {
      const on = a.getAttribute('href') === '#' + en.target.id;
      a.classList.toggle('on', on);
      if (on) strip.scrollTo({ left: a.offsetLeft - 16, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }), { rootMargin: '-45% 0px -50% 0px' });
  $$('.bio-sec').forEach((sec) => spy.observe(sec));
})();

/* ----- Her books: drag to turn the book, tap to open it, pick another from the shelf ----- */
(function bookShelf() {
  const stage = $('#bkStage'), book = $('#bk3d'), raw = $('#bookData'); if (!stage || !book || !raw) return;
  const items = JSON.parse(raw.textContent), mock = $('#bkMock');
  const mocks = items.map((it) => { const im = new Image(); im.onload = () => { it.ok = true; if (items[cur] === it) show(cur); }; im.src = it.f; return im; });
  let cur = 0, ry = -24, rx = 6;
  function show(i) {
    cur = i; const it = items[i];
    book.classList.remove('open'); book.setAttribute('aria-pressed', 'false');
    book.classList.toggle('cd', it.s === 'cd');
    $('#bkT').textContent = it.t; $('#bkSp').textContent = it.t;
    $('#bkIn').innerHTML = it.in.map((x) => '<li>' + esc(x) + '</li>').join('');
    stage.classList.toggle('has-mock', !!it.ok);
    mock.hidden = !it.ok; if (it.ok) { mock.src = it.f; mock.alt = it.t + ' by Dr. S. Divyasena'; }
    $$('.shelf-i').forEach((b, j) => b.setAttribute('aria-pressed', String(j === i)));
    $$('.bk-info-p').forEach((p, j) => { p.hidden = j !== i; });
    ry = -24; rx = 6; book.style.setProperty('--ry', ry + 'deg'); book.style.setProperty('--rx', rx + 'deg');
  }
  $$('.shelf-i').forEach((b) => b.addEventListener('click', () => show(Number(b.dataset.b))));
  const toggle = () => { const on = !book.classList.contains('open'); book.classList.toggle('open', on); book.setAttribute('aria-pressed', String(on)); if (on) { ry = book.classList.contains('cd') ? -10 : 8; book.style.setProperty('--ry', ry + 'deg'); } };
  book.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); toggle(); } if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') { ry += ev.key === 'ArrowLeft' ? -15 : 15; book.style.setProperty('--ry', ry + 'deg'); } });
  // drag to turn; a tap without movement opens the cover
  let sx = null, sy = null, r0 = 0, x0r = 0, moved = false;
  stage.addEventListener('pointerdown', (ev) => { sx = ev.clientX; sy = ev.clientY; r0 = ry; x0r = rx; moved = false; book.classList.add('drag'); stage.setPointerCapture(ev.pointerId); });
  stage.addEventListener('pointermove', (ev) => {
    if (sx === null) {
      if (stage.classList.contains('has-mock') && ev.pointerType === 'mouse') { const r = stage.getBoundingClientRect(); mock.style.setProperty('--my', ((ev.clientX - r.left) / r.width - .5) * 16 + 'deg'); mock.style.setProperty('--mx', -((ev.clientY - r.top) / r.height - .5) * 12 + 'deg'); }
      return;
    }
    const dx = ev.clientX - sx, dy = ev.clientY - sy;
    if (Math.abs(dx) > 4 || Math.abs(dy) > 4) moved = true;
    ry = Math.max(-80, Math.min(60, r0 + dx * .45)); rx = Math.max(-12, Math.min(20, x0r - dy * .15));
    book.style.setProperty('--ry', ry + 'deg'); book.style.setProperty('--rx', rx + 'deg');
  });
  const end = () => { if (sx === null) return; sx = null; book.classList.remove('drag'); if (!moved && !stage.classList.contains('has-mock')) toggle(); };
  stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
  stage.addEventListener('pointerleave', () => { mock.style.setProperty('--mx', '0deg'); mock.style.setProperty('--my', '0deg'); });
  show(0);
})();

/* ----- Choreographies: tap a production, read it in a sheet; arrows or swipe for the next ----- */
(function prodSheet() {
  const grid = $('#prodGrid'), sheet = $('#sheet'), raw = $('#prodData'); if (!grid || !sheet || !raw) return;
  const data = JSON.parse(raw.textContent), body = $('#shBody'), pos = $('#shPos');
  let cur = 0, lastFocus = null;
  function render(i, dir) {
    cur = (i + data.length) % data.length;
    const p = data[cur];
    const art = $('.pc[data-i="' + cur + '"] .pc-art', grid);
    const img = art && $('img', art) ? '<img src="' + esc($('img', art).src) + '" alt="">' : '';
    body.innerHTML = '<div class="sh-top"><span class="pc-art">' + img + '<span class="pc-t">' + esc(p.t) + '</span></span><div>'
      + (p.y ? '<small>' + esc(p.y) + '</small>' : '') + '<h2>' + esc(p.t) + '</h2><div class="sh-tags">' + p.c.map((c) => '<span>' + esc(c) + '</span>').join('') + '</div></div></div>'
      + '<p class="sh-line">' + esc(p.l) + '</p>'
      + (p.s ? '<p class="sh-story">' + esc(p.s) + '</p>' : '<p class="sh-story muted">The full story of this production is coming soon. Ask us about it on WhatsApp.</p>')
      + (p.cr.length ? '<dl class="sh-cr">' + p.cr.map((c) => '<dt>' + esc(c[0]) + '</dt><dd>' + esc(c[1]) + '</dd>').join('') + '</dl>' : '')
      + (p.su ? '<p class="sh-suits"><b>Suits:</b> ' + esc(p.su) + '</p>' : '')
      + '<div class="sh-acts">' + (p.u ? '<a class="btn" href="' + p.u + '">Full story and video</a>' : '')
      + '<a class="btn' + (p.u ? '-o' : '') + '" href="/book?type=Performance+booking&production=' + encodeURIComponent(p.t) + '">Book this production</a>'
      + '<a class="btn-o" href="' + waLink('Hello Divyanjali, I would like to know about the production ' + p.t + '.') + '" target="_blank" rel="noopener">WhatsApp</a></div>';
    body.scrollTop = 0;
    body.classList.remove('slide-l', 'slide-r'); void body.offsetWidth; if (dir) body.classList.add(dir > 0 ? 'slide-r' : 'slide-l');
    pos.textContent = (cur + 1) + ' of ' + data.length;
    history.replaceState(null, '', '#' + p.k);
  }
  function open(i) { lastFocus = document.activeElement; sheet.hidden = false; document.body.style.overflow = 'hidden'; render(i); $('.sheet-x', sheet).focus({ preventScroll: true }); }
  function close() { sheet.hidden = true; document.body.style.overflow = ''; history.replaceState(null, '', location.pathname); if (lastFocus) lastFocus.focus({ preventScroll: true }); }
  grid.addEventListener('click', (ev) => { const c = ev.target.closest('.pc'); if (c) open(Number(c.dataset.i)); });
  sheet.addEventListener('click', (ev) => {
    if (ev.target.closest('[data-close]')) return close();
    const st = ev.target.closest('[data-step]'); if (st) render(cur + Number(st.dataset.step), Number(st.dataset.step));
  });
  document.addEventListener('keydown', (ev) => {
    if (sheet.hidden) return;
    if (ev.key === 'Escape') close();
    if (ev.key === 'ArrowRight') render(cur + 1, 1);
    if (ev.key === 'ArrowLeft') render(cur - 1, -1);
  });
  // swipe sideways for the next production, pull down from the top to close
  let x0 = null, y0 = null;
  const inner = $('.sheet-in', sheet);
  inner.addEventListener('touchstart', (ev) => { x0 = ev.touches[0].clientX; y0 = ev.touches[0].clientY; }, { passive: true });
  inner.addEventListener('touchend', (ev) => {
    if (x0 === null) return;
    const dx = ev.changedTouches[0].clientX - x0, dy = ev.changedTouches[0].clientY - y0; x0 = null;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)) render(cur + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
    else if (dy > 90 && body.scrollTop <= 0) close();
  }, { passive: true });
  // a link to /choreographies#hanumath-margam opens that production
  const fromHash = () => { const h = location.hash.slice(1); const i = h ? data.findIndex((p) => p.k === h) : -1; if (i >= 0) { if (sheet.hidden) open(i); else render(i); } };
  fromHash();
  addEventListener('hashchange', fromHash);
})();

/* ----- WhatsApp links with a ready message ----- */
$$('[data-wa]').forEach((a) => { a.href = waLink((a.dataset.wa || 'Hello Divyanjali') + (a.hasAttribute('data-wa-url') ? '\n' + location.href.split('#')[0] : '')); a.target = '_blank'; a.rel = 'noopener'; });

/* ----- Enquiry forms: saved to the Enquiries tab of the Google Sheet ----- */
$$('form[data-enquiry]').forEach((f) => {
  const qs = new URLSearchParams(location.search);
  if (qs.get('type') && f.elements['enquiry_type']) f.elements['enquiry_type'].value = qs.get('type');
  if (qs.get('production') && f.elements['message'] && !f.elements['message'].value) f.elements['message'].value = 'About the production: ' + qs.get('production');
  if (qs.get('class') && f.elements['message'] && !f.elements['message'].value) f.elements['message'].value = 'I would like a trial class: ' + qs.get('class');
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

/* ----- Home: the season in one place. A highlight card for one event, a small month, and every event as a thumbnail ----- */
(async function homeCalendar() {
  const box = $('#homeCal'); if (!box) return;
  const tz = { timeZone: 'Asia/Kolkata' };
  const fmt = (x, o) => new Intl.DateTimeFormat('en-IN', Object.assign({}, tz, o)).format(x);
  const time = (x) => fmt(x, { hour: 'numeric', minute: '2-digit', hour12: true }).toUpperCase();
  const dayKey = (x) => fmt(x, { year: 'numeric', month: '2-digit', day: '2-digit' }).split('/').reverse().join('-');
  const durMin = (v) => { v = String(v || '').toLowerCase(); const h = v.match(/(\d+(?:\.\d+)?)\s*h/), m = v.match(/(\d+)\s*m/); return ((h ? parseFloat(h[1]) * 60 : 0) + (m ? parseInt(m[1], 10) : 0)) || 120; };
  const cache = (v) => { try { if (v === undefined) return JSON.parse(localStorage.getItem('dv_events') || 'null'); localStorage.setItem('dv_events', JSON.stringify(v)); } catch (err) { return null; } };
  const modeCls = (m) => m === 'Online' ? 'm-ol' : m === 'Hybrid' ? 'm-hy' : 'm-ip';
  const where = (x) => x.mode === 'Online' ? 'Live online' : (x.venue_name || 'Chennai');
  const driveId = (u) => (String(u || '').match(/\/d\/([\w-]{20,})/) || String(u || '').match(/[?&]id=([\w-]{20,})/) || [])[1];
  const posterSrc = (x) => { const id = driveId(x.poster_link); if (id) return '/img/' + encodeURIComponent(x.event_code) + '?p=' + id.slice(0, 8); return /^https?:/.test(x.poster_link || '') ? x.poster_link : ''; };
  const img = (x) => { const src = posterSrc(x); return src ? '<img src="' + esc(src) + '" alt="" loading="lazy" onerror="this.parentNode.classList.add(\'nophoto\');this.remove()">' : ''; };
  const stamp = (d) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
  const gcal = (x) => 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent(x.title + ' · Divyanjali') + '&dates=' + stamp(x.start) + '/' + stamp(x.end) + '&details=' + encodeURIComponent((x.why_attend || '') + '\n\n' + location.origin + '/e/' + x.event_code) + '&location=' + encodeURIComponent(x.mode === 'Online' ? 'Online' : [x.venue_name, x.venue_address].filter(Boolean).join(', '));
  const now = new Date();
  const prep = (list) => (list || []).map((x) => {
    const start = new Date(x.date + 'T' + String(x.start_time || '00:00').slice(0, 5) + ':00+05:30');
    return Object.assign({}, x, { start, end: new Date(start.getTime() + durMin(x.duration) * 60000), mode: x.mode || 'In person', type: x.type || 'Performance' });
  }).filter((x) => x.event_code && !isNaN(x.start) && x.end > now).sort((a, b) => a.start - b.start);

  let evs = [], idx = 0, month = null, tick = null;
  const monthOf = (x) => [Number(fmt(x.start, { year: 'numeric' })), Number(fmt(x.start, { month: 'numeric' })) - 1];

  /* the countdown, used in the landing card and the highlight card */
  function countdown(el, x, short) {
    const draw = () => {
      let s = Math.max(0, Math.floor((x.start - Date.now()) / 1000));
      if (!s) { el.innerHTML = short ? 'On now' : '<span><b>On now</b>or about to begin</span>'; return; }
      const d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600), m = Math.floor(s % 3600 / 60); s %= 60;
      el.innerHTML = short
        ? 'Starts in <b>' + (d ? d + 'd ' : '') + h + 'h ' + String(m).padStart(2, '0') + 'm</b>'
        : [[d, 'days'], [h, 'hrs'], [m, 'min']].concat(reduceMotion ? [] : [[s, 'sec']]).map(([n, l]) => '<span><b>' + String(n).padStart(2, '0') + '</b>' + l + '</span>').join('');
    };
    draw(); return setInterval(draw, reduceMotion || short ? 30000 : 1000);
  }

  /* landing: next on stage */
  let tickUp = null;
  function nextUp() {
    const el = $('#nextUp'); if (!el) return; const x = evs[0];
    clearInterval(tickUp);
    if (!x) { el.outerHTML = '<a class="next" id="nextUp" href="#season"><span class="next-date"><b>★</b><small>Soon</small></span><span class="next-i"><small>Next on stage</small><b>New dates are on their way</b><span>Subscribe and they reach your calendar first.</span></span></a>'; return; }
    el.outerHTML = '<a class="next" id="nextUp" href="/e/' + encodeURIComponent(x.event_code) + '"><span class="next-date"><b>' + fmt(x.start, { day: 'numeric' }) + '</b><small>' + fmt(x.start, { month: 'short' }) + '</small></span><span class="next-i"><small>Next on stage · ' + esc(x.type) + '</small><b>' + esc(x.title) + '</b><span>' + fmt(x.start, { weekday: 'long' }) + ', ' + time(x.start) + ' · ' + esc(where(x)) + '</span><span class="cd" id="cd"></span></span></a>';
    tickUp = countdown($('#cd'), x, false);
  }

  /* highlight card */
  function feature(i, dir) {
    const el = $('#feat');
    clearInterval(tick);
    if (!evs.length) { el.innerHTML = '<div class="feat-empty"><b>The new season is being planned.</b><span class="muted">Subscribe above and new dates reach your calendar as soon as we add them.</span></div>'; return; }
    idx = (i + evs.length) % evs.length;
    const x = evs[idx];
    el.innerHTML = '<a class="feat-p' + (posterSrc(x) ? '' : ' nophoto') + '" href="/e/' + encodeURIComponent(x.event_code) + '" aria-label="' + esc(x.title) + '">' + img(x) + '<span class="feat-d"><b>' + fmt(x.start, { day: 'numeric' }) + '</b><small>' + fmt(x.start, { month: 'short' }) + '</small></span></a>'
      + '<div class="feat-b"><span class="badge ' + modeCls(x.mode) + '">' + esc(x.type) + ' · ' + esc(x.mode) + '</span>'
      + '<h3>' + esc(x.title) + '</h3>'
      + '<p class="feat-when">' + fmt(x.start, { weekday: 'long', day: 'numeric', month: 'long' }) + ' · ' + time(x.start) + '<br>' + esc(x.mode === 'Online' ? 'Live online' : [x.venue_name, x.venue_address].filter(Boolean).join(', ')) + '</p>'
      + (x.why_attend ? '<p class="feat-why">' + esc(x.why_attend) + '</p>' : '')
      + '<p class="feat-cd" id="featCd"></p></div>'
      + '<div class="feat-f"><div class="feat-acts"><a class="btn" href="/e/' + encodeURIComponent(x.event_code) + '">Details</a><a class="btn-o" href="' + gcal(x) + '" target="_blank" rel="noopener">Add to calendar</a><a class="feat-share" href="' + waLink(x.title + ' · ' + fmt(x.start, { day: 'numeric', month: 'short' }) + '\n' + location.origin + '/e/' + x.event_code) + '" target="_blank" rel="noopener">Share</a></div>'
      + '<div class="feat-nav"><button type="button" class="cal-arr" data-step="-1" aria-label="Previous event">‹</button><span>' + (idx + 1) + ' of ' + evs.length + '</span><button type="button" class="cal-arr" data-step="1" aria-label="Next event">›</button></div></div>';
    el.classList.remove('in-l', 'in-r'); void el.offsetWidth; if (dir) el.classList.add(dir > 0 ? 'in-r' : 'in-l');
    tick = countdown($('#featCd'), x, true);
    month = monthOf(x);
    grid();
    const strip = $('#thumbs');
    $$('.th', box).forEach((t, j) => {
      t.setAttribute('aria-current', String(j === idx));
      // scroll only the thumbnail row, never the page
      if (j !== idx) return;
      const r = t.getBoundingClientRect(), sr = strip.getBoundingClientRect();
      if (r.left < sr.left || r.right > sr.right) strip.scrollTo({ left: strip.scrollLeft + r.left - sr.left, behavior: reduceMotion || !dir ? 'auto' : 'smooth' });
    });
  }

  /* small month */
  function grid() {
    const [y, m] = month;
    const first = new Date(Date.UTC(y, m, 1)), days = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
    const byDay = {}; evs.forEach((x, j) => { (byDay[dayKey(x.start)] = byDay[dayKey(x.start)] || []).push(j); });
    const today = dayKey(now), selKey = evs[idx] ? dayKey(evs[idx].start) : '';
    $('#calMonth').textContent = new Intl.DateTimeFormat('en-IN', { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(first);
    let h = '<span class="cal-d out"></span>'.repeat(first.getUTCDay()), count = 0;
    for (let d = 1; d <= days; d++) {
      const k = y + '-' + String(m + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0'), list = byDay[k] || [];
      count += list.length;
      const cls = 'cal-d' + (k < today ? ' past' : '') + (k === today ? ' today' : '') + (list.length ? ' has' : '') + (k === selKey ? ' sel' : '');
      h += list.length
        ? '<button type="button" class="' + cls + '" data-ev="' + list[0] + '" aria-label="' + d + ': ' + list.length + ' event' + (list.length > 1 ? 's' : '') + '">' + d + (list.length > 1 ? '<i>' + list.length + '</i>' : '') + '</button>'
        : '<span class="' + cls + '">' + d + '</span>';
    }
    $('#calDays').innerHTML = h;
    const nxt = evs.find((x) => x.start > new Date(Date.UTC(y, m + 1, 1)));
    $('#calNote').innerHTML = count ? count + ' event' + (count > 1 ? 's' : '') + ' this month · tap a date' : (nxt ? 'Nothing this month. <button type="button" data-ev="' + evs.indexOf(nxt) + '">Next: ' + fmt(nxt.start, { day: 'numeric', month: 'short' }) + ' ›</button>' : 'Nothing this month.');
    $('[data-cal="-1"]', box).disabled = y * 12 + m <= now.getFullYear() * 12 + now.getMonth();
    const last = evs[evs.length - 1];
    $('[data-cal="1"]', box).disabled = !last || y * 12 + m >= monthOf(last)[0] * 12 + monthOf(last)[1] + 1;
  }

  /* every event as a thumbnail */
  function thumbs() {
    const t = $('#thumbs');
    t.hidden = evs.length < 2;
    t.innerHTML = evs.map((x, j) => '<button type="button" class="th" data-ev="' + j + '"><span class="th-p' + (posterSrc(x) ? '' : ' nophoto') + '">' + img(x) + '</span><span class="th-t"><small>' + fmt(x.start, { day: 'numeric', month: 'short' }) + ' · ' + time(x.start) + '</small><b>' + esc(x.title) + '</b></span></button>').join('');
  }

  function render(list) { evs = prep(list); nextUp(); thumbs(); feature(Math.min(idx, Math.max(0, evs.length - 1))); if (!evs.length) { month = [now.getFullYear(), now.getMonth()]; grid(); } }

  box.addEventListener('click', (ev) => {
    const st = ev.target.closest('[data-step]'); if (st) return feature(idx + Number(st.dataset.step), Number(st.dataset.step));
    const e1 = ev.target.closest('[data-ev]'); if (e1) { const j = Number(e1.dataset.ev); return feature(j, j >= idx ? 1 : -1); }
    const arr = ev.target.closest('[data-cal]');
    if (arr) {
      const t = month[0] * 12 + month[1] + Number(arr.dataset.cal), nm = [Math.floor(t / 12), t % 12];
      const j = evs.findIndex((x) => { const k = monthOf(x); return k[0] === nm[0] && k[1] === nm[1]; });
      if (j >= 0) feature(j, Number(arr.dataset.cal)); else { month = nm; grid(); }
    }
  });
  box.addEventListener('keydown', (ev) => { if (ev.key === 'ArrowRight' || ev.key === 'ArrowLeft') { if (ev.target.closest('.cal-days')) return; ev.preventDefault(); feature(idx + (ev.key === 'ArrowRight' ? 1 : -1), ev.key === 'ArrowRight' ? 1 : -1); } });
  // swipe the highlight card on phones
  let x0 = null;
  $('#feat').addEventListener('touchstart', (ev) => { x0 = ev.touches[0].clientX; }, { passive: true });
  $('#feat').addEventListener('touchend', (ev) => { if (x0 === null) return; const dx = ev.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 45) feature(idx + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1); }, { passive: true });

  // Subscribe links point at this site's own feed, so they work on any domain.
  const feed = location.host + '/calendar.ics';
  if ($('#subG')) $('#subG').href = 'https://calendar.google.com/calendar/r?cid=' + encodeURIComponent('webcal://' + feed);
  if ($('#subA')) $('#subA').href = 'webcal://' + feed;

  // Show the last list straight away, then refresh from the sheet.
  const raw = cache();
  if (raw) render(raw);
  try {
    const ctrl = new AbortController(); setTimeout(() => ctrl.abort(), 9000);
    const j = await (await fetch(CONFIG.SCRIPT_URL + '?action=events', { signal: ctrl.signal })).json();
    if (j && Array.isArray(j.events)) { cache(j.events); render(j.events); return; }
  } catch (err) { /* keep what we have */ }
  if (!raw) render([]);
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
