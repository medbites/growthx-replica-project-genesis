#!/usr/bin/env python3
"""Builds the Divyanjali site pages into ../divyanjali-site.

Run:  python3 divyanjali-build/build.py
Every page shares one header, footer and menu from this file. Page text lives below, one function per page.
Image slots: each ph(...) call is a photo slot. Put a file with that name in divyanjali-site/assets/img/
and it appears on the page. The full list is written to divyanjali-site/IMAGE-SLOTS.md.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, '..', 'divyanjali-site')
e = html.escape
SLOTS = []          # (page, file, label, size)
PAGE = ['']         # current page, for the slot list

# ---------------------------------------------------------------- building blocks
def ph(file, label, size='1600×1000', cls='', alt=None):
    SLOTS.append((PAGE[0], file, label, size))
    return f'<figure class="ph {cls}" data-src="/assets/img/{file}" data-alt="{e(alt or label)}"><span>Photo · {e(label)} · {size}</span></figure>'

def yt(link, cap, start=None):
    s = f' data-start="{start}"' if start else ''
    return f'<a class="yt" href="{e(link)}" data-yt="{e(link)}"{s} aria-label="Play: {e(cap)}"><span class="cap">{e(cap)}</span></a>'

def todo(t):
    return f'<mark class="todo">{e(t)}</mark>'

def head(eyebrow, title, extra=''):
    return f'<div class="sec-head"><div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div>{extra}</div>'

def faq(items):
    qa = ''.join(f'<details class="faq"><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in items)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in items]}
    return f'<div class="faqs">{qa}</div><script type="application/ld+json">{json.dumps(ld)}</script>'

def faq_section(items, alt=False):
    return f'<section{" class=alt" if alt else ""}><div class="wrap">{head("Questions", "Frequently asked")}{faq(items)}</div></section>'

def cta(title, text, btn, href, wa=None):
    w = f'<a class="btn-o" data-wa="{e(wa)}" href="#">WhatsApp us</a>' if wa else ''
    return f'<section class="dark"><div class="wrap cta"><div class="stack" style="gap:8px"><h2>{title}</h2><p class="muted">{text}</p></div><div class="row"><a class="btn" href="{href}">{btn}</a>{w}</div></div></section>'

def crumbs(*parts):
    links = ['<a href="/">Home</a>'] + [f'<a href="{h}">{e(t)}</a>' if h else e(t) for t, h in parts]
    return '<div class="wrap crumbs">' + ' / '.join(links) + '</div>'

def stats(items):
    """(number, suffix, label) or (number, suffix, label, link, hint). With a link the number becomes tappable."""
    out = ''
    for it in items:
        n, p, l = it[:3]
        inner = f'<b data-count="{n}" data-plus="{p}">{n}{p}</b><span>{e(l)}</span>'
        if len(it) > 3:
            out += f'<a class="stat reveal" href="{it[3]}">{inner}<small>{e(it[4])} <i aria-hidden="true">→</i></small></a>'
        else:
            out += f'<div class="stat reveal">{inner}</div>'
    return f'<div class="stats">{out}</div>'

ICONS = {'person-arms-spread': '<path d="M104,40a24,24,0,1,1,24,24A24,24,0,0,1,104,40ZM212,80H44c-12.87,0-16.71,17.5-5,22.9L96,128,73.13,214.93a12,12,0,0,0,21.75,10.14L128,168l33.12,57.07a12,12,0,0,0,21.75-10.14L160,128l57-25.1C228.69,97.5,224.85,80,212,80Z" opacity="0.2"/><path d="M160,40a32,32,0,1,0-32,32A32,32,0,0,0,160,40ZM128,56a16,16,0,1,1,16-16A16,16,0,0,1,128,56ZM231.5,87.71A19.62,19.62,0,0,0,212,72H44a20,20,0,0,0-8.38,38.16l.13.06,50.75,22.35-21,79.72A20,20,0,0,0,102,228.82l26-44.88,26,44.88a20,20,0,0,0,36.4-16.53l-21-79.72,50.75-22.35.13-.06A19.63,19.63,0,0,0,231.5,87.71Zm-17.8,7.9-56.93,25.07a8,8,0,0,0-4.51,9.36L175.13,217a7,7,0,0,0,.49,1.35,4,4,0,1,1-7.25,3.38c-.11-.22-.22-.43-.34-.63L134.92,164a8,8,0,0,0-13.84,0L88,221.06c-.12.2-.23.41-.34.63a4,4,0,1,1-7.25-3.38,7,7,0,0,0,.49-1.35L103.74,130a8,8,0,0,0-4.51-9.36L42.3,95.61A4,4,0,0,1,44,88H212a4,4,0,0,1,1.73,7.61Z"/>', 'person-simple-tai-chi': '<path d="M152,48a24,24,0,1,1-24-24A24,24,0,0,1,152,48Z" opacity="0.2"/><path d="M128,80A32,32,0,1,0,96,48,32,32,0,0,0,128,80Zm0-48a16,16,0,1,1-16,16A16,16,0,0,1,128,32Zm96,72a8,8,0,0,1-8,8H136v26.72l51.15,21.93A8,8,0,0,1,192,168v48a8,8,0,0,1-16,0V173.28l-46.45-19.91L53.35,222a8,8,0,1,1-10.7-11.9L120,140.44V112H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,104Z"/>', 'monitor-play': '<path d="M208,48H48A16,16,0,0,0,32,64V176a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V64A16,16,0,0,0,208,48ZM112,152V88l48,32Z" opacity="0.2"/><path d="M208,40H48A24,24,0,0,0,24,64V176a24,24,0,0,0,24,24H208a24,24,0,0,0,24-24V64A24,24,0,0,0,208,40Zm8,136a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V64a8,8,0,0,1,8-8H208a8,8,0,0,1,8,8Zm-48,48a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h64A8,8,0,0,1,168,224Zm-3.56-110.66-48-32A8,8,0,0,0,104,88v64a8,8,0,0,0,12.44,6.66l48-32a8,8,0,0,0,0-13.32ZM120,137.05V103l25.58,17Z"/>', 'mask-happy': '<path d="M216,48v55.77C216,174.6,176.6,232,128,232S40,174.6,40,103.79V48a8,8,0,0,1,10.89-7.47C66,46.41,95.11,55.71,128,55.71s62-9.3,77.11-15.16A8,8,0,0,1,216,48Z" opacity="0.2"/><path d="M217,34.8a15.94,15.94,0,0,0-14.82-1.71C188.15,38.55,159.82,47.71,128,47.71S67.84,38.55,53.79,33.09A16,16,0,0,0,32,48v55.77c0,35.84,9.65,69.65,27.18,95.18,18.16,26.46,42.6,41,68.82,41s50.66-14.57,68.82-41C214.35,173.44,224,139.63,224,103.79V48A16,16,0,0,0,217,34.8Zm-9,69c0,32.64-8.66,63.23-24.37,86.13C168.54,211.9,148.79,224,128,224s-40.54-12.1-55.63-34.08C56.66,167,48,136.43,48,103.79V48c15.11,5.87,45.58,15.71,80,15.71S192.9,53.87,208,48v55.81Zm-18,18.87A8,8,0,1,1,178,133.33c-2.68-3-8.85-5.33-14-5.33s-11.36,2.34-14,5.33A8,8,0,1,1,138,122.66c5.71-6.38,16.14-10.66,26-10.66S184.25,116.28,190,122.66ZM92,128c-5.19,0-11.36,2.34-14,5.33A8,8,0,1,1,66,122.66C71.75,116.28,82.18,112,92,112s20.25,4.28,26,10.66A8,8,0,1,1,106,133.33C103.36,130.34,97.19,128,92,128Zm76.45,45.19a52.9,52.9,0,0,1-80.9,0A8,8,0,1,1,99.72,162.8a36.89,36.89,0,0,0,56.56,0,8,8,0,0,1,12.17,10.39Z"/>', 'book-open-text': '<path d="M232,56V200H160a32,32,0,0,0-32,32V88a32,32,0,0,1,32-32Z" opacity="0.2"/><path d="M232,48H160a40,40,0,0,0-32,16A40,40,0,0,0,96,48H24a8,8,0,0,0-8,8V200a8,8,0,0,0,8,8H96a24,24,0,0,1,24,24,8,8,0,0,0,16,0,24,24,0,0,1,24-24h72a8,8,0,0,0,8-8V56A8,8,0,0,0,232,48ZM96,192H32V64H96a24,24,0,0,1,24,24V200A39.81,39.81,0,0,0,96,192Zm128,0H160a39.81,39.81,0,0,0-24,8V88a24,24,0,0,1,24-24h64ZM160,88h40a8,8,0,0,1,0,16H160a8,8,0,0,1,0-16Zm48,40a8,8,0,0,1-8,8H160a8,8,0,0,1,0-16h40A8,8,0,0,1,208,128Zm0,32a8,8,0,0,1-8,8H160a8,8,0,0,1,0-16h40A8,8,0,0,1,208,160Z"/>', 'metronome': '<path d="M200,216H56a8,8,0,0,1-7.63-10.43l12-37.57H195.66l12,37.57A8,8,0,0,1,200,216Z" opacity="0.2"/><path d="M187.14,114.84l26.78-29.46a8,8,0,0,0-11.84-10.76l-20.55,22.6-17.2-54.07A15.94,15.94,0,0,0,149.08,32H106.91A15.94,15.94,0,0,0,91.66,43.15l-50.91,160A16,16,0,0,0,56,224H200a16,16,0,0,0,15.25-20.85ZM184.72,160H146.08l28.62-31.48ZM106.91,48h42.17l20,62.9L124.46,160H71.27ZM56,208l10.18-32H189.81L200,208Z"/>', 'hand-heart': '<path d="M16,152H48v56H16a8,8,0,0,1-8-8V160A8,8,0,0,1,16,152ZM192.54,40A39.12,39.12,0,0,0,156,64a39.12,39.12,0,0,0-36.54-24C97.67,40,80,58.31,80,80c0,14.56,7,27.71,16.73,40H140a20,20,0,0,1,0,40h4l37.78-8.68C203.82,135.07,232,109.23,232,80,232,58.31,214.33,40,192.54,40Z" opacity="0.2"/><path d="M230.33,141.06a24.34,24.34,0,0,0-18.61-4.77C230.5,117.33,240,98.48,240,80c0-26.47-21.29-48-47.46-48A47.58,47.58,0,0,0,156,48.75,47.58,47.58,0,0,0,119.46,32C93.29,32,72,53.53,72,80c0,11,3.24,21.69,10.06,33a31.87,31.87,0,0,0-14.75,8.4L44.69,144H16A16,16,0,0,0,0,160v40a16,16,0,0,0,16,16H120a7.93,7.93,0,0,0,1.94-.24l64-16a6.94,6.94,0,0,0,1.19-.4L226,182.82l.44-.2a24.6,24.6,0,0,0,3.93-41.56ZM119.46,48A31.15,31.15,0,0,1,148.6,67a8,8,0,0,0,14.8,0,31.15,31.15,0,0,1,29.14-19C209.59,48,224,62.65,224,80c0,19.51-15.79,41.58-45.66,63.9l-11.09,2.55A28,28,0,0,0,140,112H100.68C92.05,100.36,88,90.12,88,80,88,62.65,102.41,48,119.46,48ZM16,160H40v40H16Zm203.43,8.21-38,16.18L119,200H56V155.31l22.63-22.62A15.86,15.86,0,0,1,89.94,128H140a12,12,0,0,1,0,24H112a8,8,0,0,0,0,16h32a8.32,8.32,0,0,0,1.79-.2l67-15.41.31-.08a8.6,8.6,0,0,1,6.3,15.9Z"/>', 'users-three': '<path d="M168,144a40,40,0,1,1-40-40A40,40,0,0,1,168,144ZM64,56A32,32,0,1,0,96,88,32,32,0,0,0,64,56Zm128,0a32,32,0,1,0,32,32A32,32,0,0,0,192,56Z" opacity="0.2"/><path d="M244.8,150.4a8,8,0,0,1-11.2-1.6A51.6,51.6,0,0,0,192,128a8,8,0,0,1,0-16,24,24,0,1,0-23.24-30,8,8,0,1,1-15.5-4A40,40,0,1,1,219,117.51a67.94,67.94,0,0,1,27.43,21.68A8,8,0,0,1,244.8,150.4ZM190.92,212a8,8,0,1,1-13.85,8,57,57,0,0,0-98.15,0,8,8,0,1,1-13.84-8,72.06,72.06,0,0,1,33.74-29.92,48,48,0,1,1,58.36,0A72.06,72.06,0,0,1,190.92,212ZM128,176a32,32,0,1,0-32-32A32,32,0,0,0,128,176ZM72,120a8,8,0,0,0-8-8A24,24,0,1,1,87.24,82a8,8,0,1,0,15.5-4A40,40,0,1,0,37,117.51,67.94,67.94,0,0,0,9.6,139.19a8,8,0,1,0,12.8,9.61A51.6,51.6,0,0,1,64,128,8,8,0,0,0,72,120Z"/>', 'airplane-tilt': '<path d="M209,81l-33,31,32,88-24,24-48-72-24,24v24L88,224,72,184,32,168l24-24H80l24-24L32,72,56,48l88,32,31-33A24,24,0,0,1,209,81Z" opacity="0.2"/><path d="M185.33,114.21l29.14-27.43.17-.16a32,32,0,0,0-45.26-45.26l-.16.17L141.79,70.67l-83-30.2a8,8,0,0,0-8.39,1.86l-24,24a8,8,0,0,0,1.22,12.31l63.89,42.59L76.69,136H56a8,8,0,0,0-5.65,2.34l-24,24A8,8,0,0,0,29,175.42l36.82,14.73,14.7,36.75.06.16a8,8,0,0,0,13.18,2.47l23.87-23.88A8,8,0,0,0,120,200V179.31l14.76-14.76,42.59,63.89a8,8,0,0,0,12.31,1.22l24-24a8,8,0,0,0,1.86-8.39Zm-.07,97.23-42.59-63.89A8,8,0,0,0,136.8,144a7.09,7.09,0,0,0-.79,0,8,8,0,0,0-5.66,2.34l-24,24A8,8,0,0,0,104,176v20.69L90.93,209.76,79.43,181A8,8,0,0,0,75,176.57l-28.74-11.5L59.32,152H80a8,8,0,0,0,5.66-2.34l24-24a8,8,0,0,0-1.22-12.32L44.56,70.74l13.5-13.49,83.22,30.26a8,8,0,0,0,8.56-2l30.94-32.88A16,16,0,0,1,203.4,75.22l-32.87,30.94a8,8,0,0,0-2,8.56l30.26,83.22Z"/>', 'music-notes': '<path d="M208,164a28,28,0,1,1-28-28A28,28,0,0,1,208,164ZM52,168a28,28,0,1,0,28,28A28,28,0,0,0,52,168Z" opacity="0.2"/><path d="M212.92,17.69a8,8,0,0,0-6.86-1.45l-128,32A8,8,0,0,0,72,56V166.08A36,36,0,1,0,88,196V110.25l112-28v51.83A36,36,0,1,0,216,164V24A8,8,0,0,0,212.92,17.69ZM52,216a20,20,0,1,1,20-20A20,20,0,0,1,52,216ZM88,93.75V62.25l112-28v31.5ZM180,184a20,20,0,1,1,20-20A20,20,0,0,1,180,184Z"/>', 'hands-clapping': '<path d="M199,187.76h0A71.67,71.67,0,0,0,190.34,140l-20.2-35a18,18,0,0,0-31.55,17.26L114.71,81A18,18,0,1,0,83.54,99L77.81,89,65.1,67A18,18,0,1,1,96.28,49L102,59a18,18,0,1,1,31.17-18l24.23,42a18,18,0,0,1,31.2-18l21.11,36.57A72,72,0,0,1,199,187.76Z" opacity="0.2"/><path d="M160.22,24V8a8,8,0,0,1,16,0V24a8,8,0,0,1-16,0ZM196.1,41a7.91,7.91,0,0,0,4.17,1.17,8,8,0,0,0,6.84-3.83l8-13.11a8,8,0,0,0-13.68-8.33l-8,13.1A8,8,0,0,0,196.1,41Zm47.51,12.59a8,8,0,0,0-10.08-5.16l-15.06,4.85a8,8,0,0,0,2.46,15.62,8.15,8.15,0,0,0,2.46-.39l15.05-4.85A8,8,0,0,0,243.61,53.55ZM217,97.58a80.22,80.22,0,0,1-10.22,94c-.34,1.73-.72,3.46-1.19,5.18A80.17,80.17,0,0,1,58.77,216L23.5,155a26,26,0,0,1,19.24-38.79l-3-5.2a26,26,0,0,1,19.2-38.78L58.24,71A26,26,0,0,1,95.47,36.53,26.06,26.06,0,0,1,140.3,37l12.26,21.2A26.07,26.07,0,0,1,195.81,61ZM109.07,55l0,0h0l25,43.17a26,26,0,0,1,17.33-10L126.42,45a10,10,0,1,0-17.35,10ZM72.12,63l6.46,11.17a26.05,26.05,0,0,1,17.32-10L89.45,53A10,10,0,1,0,72.12,63Zm111.54,81-20.22-35a10,10,0,0,0-17.74,9.25L158.3,140a8,8,0,0,1-13.87,8l-36.5-63A10,10,0,1,0,90.58,95l26.05,45a8,8,0,0,1-13.87,8L71,93h0l0,0a10,10,0,0,0-17.33,10l35.22,61A8,8,0,0,1,75,172L54.72,137a10,10,0,0,0-17.34,10l35.27,61a64.12,64.12,0,0,0,117.42-15.44A63.52,63.52,0,0,0,183.66,144Zm19.41-38.42L181.93,69A10,10,0,0,0,164.55,79l33,57.05A80.2,80.2,0,0,1,207,161.51,64.23,64.23,0,0,0,203.07,105.58Z"/>', 'certificate': '<path d="M224,56V90.06h0a44,44,0,1,0-56,67.88h0V192H40a8,8,0,0,1-8-8V56a8,8,0,0,1,8-8H216A8,8,0,0,1,224,56Z" opacity="0.2"/><path d="M128,136a8,8,0,0,1-8,8H72a8,8,0,0,1,0-16h48A8,8,0,0,1,128,136Zm-8-40H72a8,8,0,0,0,0,16h48a8,8,0,0,0,0-16Zm112,65.47V224A8,8,0,0,1,220,231l-24-13.74L172,231A8,8,0,0,1,160,224V200H40a16,16,0,0,1-16-16V56A16,16,0,0,1,40,40H216a16,16,0,0,1,16,16V86.53a51.88,51.88,0,0,1,0,74.94ZM160,184V161.47A52,52,0,0,1,216,76V56H40V184Zm56-12a51.88,51.88,0,0,1-40,0v38.22l16-9.16a8,8,0,0,1,7.94,0l16,9.16Zm16-48a36,36,0,1,0-36,36A36,36,0,0,0,232,124Z"/>', 'graduation-cap': '<path d="M216,113.07v53.22a8,8,0,0,1-2,5.31c-11.3,12.59-38.9,36.4-86,36.4s-74.68-23.81-86-36.4a8,8,0,0,1-2-5.31V113.07L128,160Z" opacity="0.2"/><path d="M251.76,88.94l-120-64a8,8,0,0,0-7.52,0l-120,64a8,8,0,0,0,0,14.12L32,117.87v48.42a15.91,15.91,0,0,0,4.06,10.65C49.16,191.53,78.51,216,128,216a130,130,0,0,0,48-8.76V240a8,8,0,0,0,16,0V199.51a115.63,115.63,0,0,0,27.94-22.57A15.91,15.91,0,0,0,224,166.29V117.87l27.76-14.81a8,8,0,0,0,0-14.12ZM128,200c-43.27,0-68.72-21.14-80-33.71V126.4l76.24,40.66a8,8,0,0,0,7.52,0L176,143.47v46.34C163.4,195.69,147.52,200,128,200Zm80-33.75a97.83,97.83,0,0,1-16,14.25V134.93l16-8.53ZM188,118.94l-.22-.13-56-29.87a8,8,0,0,0-7.52,14.12L171,128l-43,22.93L25,96,128,41.07,231,96Z"/>', 'whatsapp-logo': '<path d="M128,32A96,96,0,0,0,44.89,176.07L32.42,213.46a8,8,0,0,0,10.12,10.12l37.39-12.47A96,96,0,1,0,128,32Zm24,152a80,80,0,0,1-80-80,32,32,0,0,1,32-32l16,32-12.32,18.47a48.19,48.19,0,0,0,25.85,25.85L152,136l32,16A32,32,0,0,1,152,184Z" opacity="0.2"/><path d="M187.58,144.84l-32-16a8,8,0,0,0-8,.5l-14.69,9.8a40.55,40.55,0,0,1-16-16l9.8-14.69a8,8,0,0,0,.5-8l-16-32A8,8,0,0,0,104,64a40,40,0,0,0-40,40,88.1,88.1,0,0,0,88,88,40,40,0,0,0,40-40A8,8,0,0,0,187.58,144.84ZM152,176a72.08,72.08,0,0,1-72-72A24,24,0,0,1,99.29,80.46l11.48,23L101,118a8,8,0,0,0-.73,7.51,56.47,56.47,0,0,0,30.15,30.15A8,8,0,0,0,138,155l14.62-9.74,23,11.48A24,24,0,0,1,152,176ZM128,24A104,104,0,0,0,36.18,176.88L24.83,210.93a16,16,0,0,0,20.24,20.24l34.05-11.35A104,104,0,1,0,128,24Zm0,192a87.87,87.87,0,0,1-44.06-11.81,8,8,0,0,0-6.54-.67L40,216,52.47,178.6a8,8,0,0,0-.66-6.54A88,88,0,1,1,128,216Z"/>', 'phone': '<path d="M223.94,174.08A48.33,48.33,0,0,1,176,216,136,136,0,0,1,40,80,48.33,48.33,0,0,1,81.92,32.06a8,8,0,0,1,8.3,4.8l21.13,47.2a8,8,0,0,1-.66,7.53L89.32,117a7.93,7.93,0,0,0-.54,7.81c8.27,16.93,25.77,34.22,42.75,42.41a7.92,7.92,0,0,0,7.83-.59l25-21.3a8,8,0,0,1,7.59-.69l47.16,21.13A8,8,0,0,1,223.94,174.08Z" opacity="0.2"/><path d="M222.37,158.46l-47.11-21.11-.13-.06a16,16,0,0,0-15.17,1.4,8.12,8.12,0,0,0-.75.56L134.87,160c-15.42-7.49-31.34-23.29-38.83-38.51l20.78-24.71c.2-.25.39-.5.57-.77a16,16,0,0,0,1.32-15.06l0-.12L97.54,33.64a16,16,0,0,0-16.62-9.52A56.26,56.26,0,0,0,32,80c0,79.4,64.6,144,144,144a56.26,56.26,0,0,0,55.88-48.92A16,16,0,0,0,222.37,158.46ZM176,208A128.14,128.14,0,0,1,48,80,40.2,40.2,0,0,1,82.87,40a.61.61,0,0,0,0,.12l21,47L83.2,111.86a6.13,6.13,0,0,0-.57.77,16,16,0,0,0-1,15.7c9.06,18.53,27.73,37.06,46.46,46.11a16,16,0,0,0,15.75-1.14,8.44,8.44,0,0,0,.74-.56L168.89,152l47,21.05h0s.08,0,.11,0A40.21,40.21,0,0,1,176,208Z"/>', 'envelope-simple': '<path d="M224,56l-96,88L32,56Z" opacity="0.2"/><path d="M224,48H32a8,8,0,0,0-8,8V192a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A8,8,0,0,0,224,48ZM203.43,64,128,133.15,52.57,64ZM216,192H40V74.19l82.59,75.71a8,8,0,0,0,10.82,0L216,74.19V192Z"/>', 'map-pin': '<path d="M128,24a80,80,0,0,0-80,80c0,72,80,128,80,128s80-56,80-128A80,80,0,0,0,128,24Zm0,112a32,32,0,1,1,32-32A32,32,0,0,1,128,136Z" opacity="0.2"/><path d="M128,64a40,40,0,1,0,40,40A40,40,0,0,0,128,64Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,128Zm0-112a88.1,88.1,0,0,0-88,88c0,31.4,14.51,64.68,42,96.25a254.19,254.19,0,0,0,41.45,38.3,8,8,0,0,0,9.18,0A254.19,254.19,0,0,0,174,200.25c27.45-31.57,42-64.85,42-96.25A88.1,88.1,0,0,0,128,16Zm0,206c-16.53-13-72-60.75-72-118a72,72,0,0,1,144,0C200,161.23,144.53,209,128,222Z"/>'}

def icon(name):
    """Phosphor duotone icon (MIT), inlined so it needs no extra download."""
    return f'<svg class="ic" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">{ICONS[name]}</svg>'

# ---------------------------------------------------------------- layout
NAV = [
    ('About', '/about', [('Dance school', '/about', 'Divyanjali since 1994'), ('Dr. S. Divyasena', '/divyasena', 'Founder and guru'),
                         ('Sri B.P. Haribabu', '/haribabu', 'Mridangam and rhythm'), ('Media Room', '/media', 'Press kit, facts and photos')]),
    ('30 Years', '/30-years', [('The souvenir book', '/30-years#souvenir', 'Page through Souvenir 2026'), ('Messages', '/30-years#messages', 'From fellow artists'),
                               ('Timeline', '/30-years#timeline', '1994 to 2024, year by year'), ('The 2015 flood', '/30-years#flood', 'And the way back')]),
    ('Accolades', '/accolades', [('All dancers', '/accolades', 'Every profile in one place'), ('Faculty', '/accolades#faculty', 'Our teachers'),
                                 ('Students', '/accolades#students', 'Students and alumni')]),
    ('Choreographies', '/choreographies', [('All productions', '/choreographies', 'Every production, newest first'), ('Hanumath Margam', '/productions/hanumath-margam', 'World premiere, 2026'),
                                           ('Andal Vaibhavam', '/productions/andal-vaibhavam', 'Staged on 13 stages in a year'), ('Thirumurugaatrupadai', '/productions/thirumurugaatrupadai', 'A Sangam-era poem, staged'),
                                           ('Gallery', '/gallery', 'Photos and videos')]),
    ('Learn', '/learn', [('Find your class', '/learn#finder', 'Three taps to the right batch'), ('The path', '/learn#path', 'From adavus to arangetram'),
                         ('Batches and timings', '/learn#batches', 'Days, times and places'), ('Natya IQ', '/natya-iq', 'Games to practise theory'), ('Store', '/store', 'Books, the CD and more')]),
    ('Calendar', '/events', None),
]
CHEVRON = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'

def header(path):
    def on(h):
        h = h.split('#')[0]
        return h == path or (h != '/' and path.startswith(h + '/')) or (h == '/accolades' and path.startswith('/students/')) or (h == '/choreographies' and path.startswith('/productions/'))
    cur = lambda h: ' aria-current="page"' if '#' not in h and on(h) else ''
    group_on = lambda t, h, kids: on(h) or any(on(k) for _, k, _ in (kids or []))
    nav = ''
    for i, (t, h, kids) in enumerate(NAV):
        if not kids:
            nav += f'<a class="navcal" href="{h}"{cur(h)}>{t}</a>'
            continue
        sub = ''.join(f'<a href="{kh}"{cur(kh)}><b>{kt}</b><small>{kd}</small></a>' for kt, kh, kd in kids)
        mark = ' aria-current="page"' if group_on(t, h, kids) else ''
        nav += f'<div class="dd hide-m{" r" if i >= len(NAV) - 3 else ""}"><a class="dd-t" href="{h}"{mark} aria-haspopup="true">{t}{CHEVRON}</a><div class="dd-p">{sub}</div></div>'
    menu = f'<a href="/"{cur("/")}>Home</a>'
    for t, h, kids in NAV:
        if not kids:
            menu += f'<a href="{h}"{cur(h)}>Events calendar</a>'
            continue
        menu += (f'<details class="mg"{" open" if group_on(t, h, kids) else ""}><summary>{t}{CHEVRON}</summary>'
                 + ''.join(f'<a class="menu-sub" href="{kh}"{cur(kh)}>{kt}</a>' for kt, kh, _ in kids) + '</details>')
    menu += '<a class="menu-cta" href="/book">Book and Enquire</a>'
    return f'''<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Divyanjali home"><img src="/assets/logo-mark.webp" alt="" width="46" height="45"><b>Divyanjali</b></a>
    <nav class="nav" aria-label="Main">{nav}<a class="btn" href="/book">Book &amp; enquire</a>
      <details class="menu"><summary aria-label="Menu">☰</summary><div class="menu-panel">{menu}</div></details>
    </nav>
  </div>
</header>'''

FOOTER = '''<footer>
  <div class="wrap cols">
    <div class="stack" style="gap:8px"><a class="logo" href="/"><img src="/assets/logo-mark-white.webp" alt="" width="56" height="55"><b>Divyanjali</b></a><p class="muted">Bharatanatyam since 1994 · CIT Nagar, Chennai</p></div>
    <div class="stack" style="gap:4px"><p class="muted">Visit</p><p id="fAddr">[Address], CIT Nagar, Chennai</p><p id="fWa">WhatsApp +919000000000</p></div>
    <div class="stack" style="gap:4px"><p class="muted">Explore</p><a href="/about">About</a><a href="/choreographies">Choreographies</a><a href="/learn">Learn</a><a href="/events">Events</a><a href="/gallery">Gallery and Videos</a></div>
    <div class="stack" style="gap:4px"><p class="muted">More</p><a href="/media">Media Room</a><a href="/store">Store</a><a href="/book">Book and Enquire</a><a href="/privacy">Privacy</a></div>
    <div class="stack" style="gap:4px"><p class="muted">Follow</p><a id="fIg" href="https://www.instagram.com/divyanjalidance/" target="_blank" rel="noopener">Instagram</a><a id="fYt" href="https://www.youtube.com/channel/UCLPvhdH5qXt0R4IyDt1eSHg" target="_blank" rel="noopener">YouTube</a><a id="fFb" href="https://www.facebook.com/divyanjali.dance/" target="_blank" rel="noopener">Facebook</a></div>
  </div>
  <div class="wrap fine">© Divyanjali Dance School and Trust, Chennai · <a href="/privacy">Privacy</a></div>
</footer>'''

WA = '<a class="wa" data-wa="Hello Divyanjali" href="#" aria-label="Chat with Divyanjali on WhatsApp"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 20l1.5-4A8 8 0 1 1 8 18.5z"/></svg></a>'

def page(path, title, desc, body, extra_head='', scripts=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&amp;family=Montserrat:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="/assets/site.css">
{extra_head}</head>
<body>
{header(path)}
<div class="season"><a href="/events" style="color:inherit">Dance Season 2026–27 · November to January · see the calendar</a></div>
<main>
{body}
</main>
{FOOTER}
{WA}
<script src="/assets/site.js" defer></script>
{scripts}</body>
</html>
'''

# ---------------------------------------------------------------- productions
PRODUCTIONS = [
    dict(slug='hanumath-margam', title='Hanumath Margam', year='2026', cats=['Devotional', 'Margam'], line='World premiere, 50th Cleveland Thyagaraja Festival',
         story='A margam on the life and devotion of Hanuman, conceptualized and choreographed by Dr. S. Divyasena, with lyrics and music composed by Dr R. Suryaprakash. It had its world premiere at the 50th Cleveland Thyagaraja Festival, USA.',
         credits=[('Concept and choreography', 'Dr. S. Divyasena'), ('Lyrics and music', 'Dr R. Suryaprakash')], suits='Festivals, Hanuman Jayanthi, international stages'),
    dict(slug='thirumurugaatrupadai', title='Thirumurugaatrupadai', year='2019', cats=['Tamil literature', 'Devotional', 'Dance drama'], line='A Sangam-era poem, staged',
         story='A famous work of Tamil literature from the Sangam era, staged as a dance production on the story behind the birth of Lord Muruga. The original work by Nakkeerar is combined with the Thirupugazh of Arunagirinadhar, which describes the six abodes (Arupadai Veedu) of Lord Muruga.',
         credits=[('Concept and choreography', 'Dr. S. Divyasena'), ('Music', 'Yuvakalabharathi Sri R.K. Shriramkumar'), ('Resource', 'Dr. S. Raghuraman')], suits='Margazhi, Murugan festivals, Tamil literature festivals'),
    dict(slug='shiva-shakti-margam', title='Shiva Shakti Margam', year='2018', cats=['Margam', 'Devotional'], line='Shiva and Parvathi in the margam format',
         story='A thematic presentation of compositions by various poets in praise of Lord Shiva and Goddess Parvathi, arranged in the format of a Bharatanatyam repertoire.',
         credits=[('Concept and choreography', 'Dr. S. Divyasena')], suits='Shivaratri, temple festivals, sabhas'),
    dict(slug='dasavatharam', title='Dasavatharam', year='2017', cats=['Epics', 'Devotional', 'Dance drama'], line='The ten avatars of Vishnu', video='https://www.youtube.com/watch?v=So5SO_M4zZ8',
         story='An attempt to present the ten incarnations of Lord Vishnu through Bharatanatyam, with new lyrics written and music composed by Sri T.H. Thiyagarajan.',
         credits=[('Choreography', 'Dr. S. Divyasena'), ('Lyrics and music', 'Sri T.H. Thiyagarajan')], suits='Vaishnava festivals, Margazhi, school audiences'),
    dict(slug='annamayya-navarasa-nrithyamala', title='Annamayya Navarasa Nrithyamala', year='2016', cats=['Devotional', 'Margam'], line='Annamacharya and the nine rasas',
         story='Popular compositions of Tallapaka Annamacharya, an ardent devotee of Lord Venkateshwara, woven into a garland. The chosen compositions bring out the nine rasas of Indian theatre.',
         credits=[('Choreography', 'Dr. S. Divyasena')], suits='Tirupati and Venkateshwara festivals, sabhas'),
    dict(slug='andal-vaibhavam', title='Andal Vaibhavam', year='2015', cats=['Devotional', 'Tamil literature', 'Dance drama'], line='Staged on 13 stages in one year',
         story='A thematic production made only from the verses of Aandal (Nachiyar Thirumozhi) and a few verses of Periyalwar. It follows the life of Aandal from her birth in the thulasi garden to her union with Lord Ranganathar. Staged with a grant from the Iyal Isai Nataka Mandram, Tamil Nadu, it was presented on 13 stages across India in a single year.',
         credits=[('Choreography', 'Dr. S. Divyasena'), ('Music', 'Sri T.H. Thiyagarajan'), ('Resource', 'Sri Kannan')], suits='Margazhi, Vaishnava temples, Tamil festivals'),
    dict(slug='nava-vidha-sambandham', title='Nava Vidha Sambandham', year='2014', cats=['Devotional', 'Tamil literature'], line='Nine relationships with the divine',
         story="Kulasekara Alwar, one of the twelve Vaishnavite saints, composed ten pasurams in 'Aindhaam Thirumozhi' on the relationship between the Jeevatma and Sriman Narayana, using nine kinds of worldly relationship. Divyanjali presented them as a dance production, supported by a grant from the Ministry of Culture, Government of India, under the Production Grant Scheme.",
         credits=[('Choreography', 'Dr. S. Divyasena'), ('Music', 'Sri Rajkumar Bharathi'), ('Resource', 'Sri Kannan')], suits='Vaishnava festivals, cultural bodies'),
    dict(slug='tribute-to-lalgudi', title='A Tribute to Lalgudi Sri G. Jayaraman', year='2014', cats=['Tributes', 'Margam'], line='A margam of the maestro’s compositions',
         story="A Bharatanatyam margam made entirely of the maestro's compositions, woven into a garland and presented before Sri Lalgudi Krishnan and Smt. Lalgudi Vijayalakshmi.",
         credits=[('Choreography', 'Dr. S. Divyasena')], suits='Music festivals, tribute evenings'),
    dict(slug='krishna-margam', title='Krishna Margam', year='2013', cats=['Margam', 'Devotional'], line='The mischievous Krishna, with a live orchestra',
         story='Tales of the mischievous Lord Krishna, told through well-known compositions by renowned poets, presented as a Bharatanatyam repertoire with a live orchestra.',
         credits=[('Choreography', 'Dr. S. Divyasena')], suits='Janmashtami, temples, sabhas'),
    dict(slug='laya-thrayam', title='Laya Thrayam', year='2012', cats=['Rhythm'], line='Rhythm as the main idea',
         story='A production built around laya, rhythm. It includes compositions by different composers and a special segment of tala and swaras on the idea of layam, composed by Sri Srikanth Gopalakrishnan and Sri B.P. Haribabu. First staged in New Delhi in 2012, then in the Margazhi Season.',
         credits=[('Choreography', 'Dr. S. Divyasena'), ('Rhythm segment', 'Sri Srikanth Gopalakrishnan and Sri B.P. Haribabu')], suits='Music and dance festivals, lecture demonstrations'),
    dict(slug='pannum-bharathamum', title='Pannum Bharathamum', year='', cats=['Tamil literature', 'Margam'], line='Featured in The Hindu',
         story='A thematic presentation in the margam format on the importance of Tamil literature. Nadaswaram vidwan Sri T.A.P. Ravishankar composed a mallari and a varnam for the production, which was featured in the national daily The Hindu.',
         credits=[('Choreography', 'Dr. S. Divyasena'), ('Mallari and varnam', 'Sri T.A.P. Ravishankar')], suits='Tamil festivals, sabhas'),
    dict(slug='jai-hanuman', title='Jai Hanuman', year='', cats=['Devotional', 'Dance drama'], line='The life of Hanuman',
         story='A thematic production on the life of Lord Hanuman. Compositions such as the Hanuman Chalisa and the Panchamukha Hanumath Stothram were choreographed and presented as part of it.',
         credits=[('Choreography', 'Dr. S. Divyasena'), ('Music', 'Sri Ramesh Babu')], suits='Hanuman Jayanthi, temple festivals'),
    dict(slug='thrayee', title='Thrayee', year='', cats=['Tributes', 'Jugalbandhi'], line='A tribute to the Carnatic Trinity',
         story='A tribute to the Sangeetha Mummoorthigal, the Carnatic Trinity of Thyagaraja, Shyama Sastri and Muthuswami Dikshitar, choreographed as a jugalbandhi of Kuchipudi and Bharatanatyam.',
         credits=[('Kuchipudi choreography', 'Sri Jai Kishore Mosalikanti'), ('Bharatanatyam choreography', 'Dr. S. Divyasena')], suits='Music festivals, Thyagaraja Aradhana'),
    dict(slug='puratchi-mandhaar', title='Puratchi Mandhaar', year='', cats=['Epics', 'Dance drama'], line='Four strong women of the epics',
         story='A production on four strong and powerful women from the itihasas and puranas: Draupathi, Tarai, Mandodhari and Ahalya.',
         credits=[('Choreography', 'Dr. S. Divyasena'), ('Lyrics', 'Dr. Raghuraman')], suits="Women's Day, cultural festivals"),
    dict(slug='', title='Pasurapadi Ramayanam', year='2023', cats=['Epics', 'Dance drama'], line='The life of Lord Rama'),
    dict(slug='', title='Sita Kalyanam', year='2023', cats=['Epics', 'Dance drama'], line='The wedding of Sita and Rama'),
    dict(slug='', title='Krishna Leela', year='', cats=['Devotional'], line='Stories of Krishna'),
    dict(slug='', title='Moondrum Moondrum Moondru', year='', cats=['Tamil literature'], line='Production'),
    dict(slug='', title='Laya Nrityam', year='', cats=['Rhythm'], line='Rhythm in dance'),
    dict(slug='', title='Ramana Vaibhavam', year='', cats=['Devotional'], line='Production'),
    dict(slug='', title='Veeram', year='', cats=['Epics'], line='Valour'),
    dict(slug='', title='Sakthi Prabhavam', year='', cats=['Devotional'], line='The power of Shakti'),
    dict(slug='', title='Rukmini Vivaham', year='', cats=['Epics', 'Dance drama'], line='The wedding of Rukmini'),
]
THEMES = ['Devotional', 'Tamil literature', 'Epics', 'Rhythm', 'Tributes', 'Dance drama', 'Margam', 'Jugalbandhi']

def prod_card(p):
    img = ph(f"prod-{p['slug'] or re.sub('[^a-z]+', '-', p['title'].lower()).strip('-')}.jpg", f"poster · {p['title']}", '1500×900', 'wide')
    meta = (p['year'] + ' · ' if p['year'] else '') + p['cats'][0]
    inner = f'{img}<span class="meta">{e(meta)}</span><h3>{e(p["title"])}</h3><p class="muted">{e(p["line"])}</p>'
    cat = '|'.join(p['cats'])
    if p['slug']:
        return f'<a class="tile" data-cat="{cat}" href="/productions/{p["slug"]}">{inner}</a>'
    return f'<div class="tile" data-cat="{cat}">{inner}<a href="/book?type=Performance+booking&amp;production={e(p["title"])}" style="font-size:.85rem">Ask about this production</a></div>'

# ---------------------------------------------------------------- pages
HOME_VIDEO = 'https://youtu.be/7g505MXqnec'

def marquee_rows():
    ps = [p for p in STUDENTS if p['photo']]
    half = (len(ps) + 1) // 2
    def row(lst, rev):
        cards = ''.join(f'<a class="mq" href="/students/{p["slug"]}"><img src="{p["photo"]}" alt="" loading="lazy" width="360" height="360"><b>{e(p["display"])}</b></a>' for p in lst)
        return f'<div class="mq-row{" rev" if rev else ""}"><div class="mq-track">{cards}{cards.replace('<a class="mq"', '<a class="mq" aria-hidden="true" tabindex="-1"')}</div></div>'
    return row(ps[:half], False) + row(ps[half:], True)

def home():
    feat = [p for p in PRODUCTIONS if p['slug'] in ('hanumath-margam', 'andal-vaibhavam', 'thirumurugaatrupadai', 'dasavatharam')]
    def bento(p, i):
        img = ph(f"prod-{p['slug']}.jpg", f"poster · {p['title']}", '1500×900' if i else '1200×1500', '' if i else 'tall')
        return f'<a class="bento-i{" big" if i == 0 else ""} reveal" href="/productions/{p["slug"]}">{img}<span class="bento-t"><small>{e(p["year"])} · {e(p["cats"][0])}</small><b>{e(p["title"])}</b></span></a>'
    classes = [('01', 'Children', 'person-arms-spread', f'From {todo("youngest age")} · weekday and weekend batches in CIT Nagar',
                ['Small batches grouped by age', 'Adavus, rhythm and simple items first', 'A path to arangetram for those who wish'], 'Children'),
               ('02', 'Teens and adults', 'person-simple-tai-chi', 'Beginners, and dancers coming back after a break',
                ['Complete beginners welcome', 'Abhinaya and theory alongside technique', 'Come back after a break at your own pace'], 'Teens and adults'),
               ('03', 'Online, from abroad', 'monitor-play', 'Live classes from Chennai, set to your time zone',
                ['Live with the teacher, not recorded', 'Batches set to your time zone', 'The same syllabus as the Chennai classes'], 'Online')]
    flip = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M13 6.5A5.5 5.5 0 0 0 3.2 4.6M3 9.5a5.5 5.5 0 0 0 9.8 1.9M3 2v3h3M13 14v-3h-3" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
    cards = ''.join(f'''<article class="cc" style="--i:{i}">
      <div class="cc-in">
        <div class="cc-f">
          <span class="ci">{icon(ic)}</span>
          <h3>{t}</h3>
          <p class="muted">{d}</p>
          <button class="cc-flip" type="button" aria-expanded="false" aria-label="More about {t}">{flip}<span>See what you learn</span></button>
        </div>
        <div class="cc-b" aria-hidden="true">
          <div class="cc-bh"><span class="ci sm">{icon(ic)}</span><h3>{t}</h3></div>
          <ul>{"".join(f"<li>{e(x)}</li>" for x in pts)}</ul>
          <a class="btn" href="/learn?class={tag.replace(" ", "+")}#enquire" tabindex="-1">Book a trial</a>
          <button class="cc-flip back" type="button" tabindex="-1" aria-label="Back">{flip}<span>Back</span></button>
        </div>
      </div>
    </article>''' for i, (n, t, ic, d, pts, tag) in enumerate(classes))
    return page('/', 'Divyanjali · Bharatanatyam school in Chennai since 1994',
        'Divyanjali, the Bharatanatyam school of Dr. S. Divyasena and Sri B.P. Haribabu in CIT Nagar, Chennai. See the season calendar of performances, workshops and arangetrams.', f'''
<section class="vh" data-vh="7g505MXqnec" data-start="12" aria-label="Divyanjali on stage">
  <div class="vh-media" aria-hidden="true"><div class="vh-poster"></div></div>
  <div class="vh-shade" aria-hidden="true"></div>
  <div class="wrap vh-in">
    <p class="vh-kicker">Divyanjali · Bharatanatyam since 1994 · Chennai</p>
    <h1 class="vh-title">{''.join(f'<span style="--i:{i}">{w}</span> ' for i, w in enumerate(['The', 'dancer', 'is', 'the'])) + '<em style="--i:4">dance.</em>'}</h1>
    <p class="vh-quote">There is no dancer separate from the dance.<br>No dance separate from the dancer.</p>
    <p class="vh-lead">Natyacharya Dr. S. Divyasena and Sri B.P. Haribabu. Thirty years of classes, productions and arangetrams, from CIT Nagar to stages around the world.</p>
    <div class="row vh-cta"><a class="btn vh-btn" href="#season">See the season</a><a class="btn-o vh-btn-o" href="/learn">Learn with us</a></div>
  </div>
  <div class="wrap vh-bar">
    <div class="vh-ctrl">
      <button class="vh-b" type="button" data-vh-play aria-label="Pause video"><svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z"/></svg><svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l11 7-11 7z"/></svg></button>
      <button class="vh-b" type="button" data-vh-mute aria-label="Turn sound on"><svg class="i-muted" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M16 9l5 6M21 9l-5 6" fill="none" stroke="currentColor" stroke-width="2"/></svg><svg class="i-sound" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>
      <span class="vh-hint" aria-live="polite">Sound off · tap to listen</span>
    </div>
    <a class="next" id="nextUp" href="#season"><span class="next-skel"></span></a>
  </div>
  <a class="vh-down" href="#season" aria-label="Scroll to the calendar"><span></span></a>
</section>
<section class="alt numbers"><div class="wrap">{stats([(30, '', 'years of teaching', '/30-years', 'Our story since 1994'), (71, '', 'arangetrams', '/accolades', 'Meet the students'), (300, '+', 'dancers trained', '/learn', 'Join a batch'), (len(PRODUCTIONS), '', 'productions', '/choreographies', 'Explore the works')])}</div></section>
<section class="ss" id="season"><div class="wrap">
  <div class="ss-head">
    <h2>The season</h2>
    <p class="ss-sub">Subscribe: <a id="subG" href="/events" target="_blank" rel="noopener">Google</a> · <a id="subA" href="/calendar.ics">Apple and Outlook</a> · <a data-wa="Hello Divyanjali, please add me to your events list on WhatsApp." href="#">WhatsApp</a><span class="ss-sep"> · </span><a class="ss-all" href="/events">Full calendar ›</a></p>
  </div>
  <div class="ss-box" id="homeCal">
    <article class="feat" id="feat" aria-live="polite"><div class="feat-skel"></div></article>
    <div class="mini" aria-label="Month calendar">
      <div class="cal-top">
        <button class="cal-arr" type="button" data-cal="-1" aria-label="Previous month">‹</button>
        <h3 class="cal-m" id="calMonth">Calendar</h3>
        <button class="cal-arr" type="button" data-cal="1" aria-label="Next month">›</button>
      </div>
      <div class="cal-dow" aria-hidden="true"><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
      <div class="cal-days" id="calDays"></div>
      <p class="mini-note" id="calNote"></p>
    </div>
    <div class="thumbs" id="thumbs"></div>
  </div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="sec-head"><div><h2>Two gurus, one stage</h2></div></div>
  <div class="duo">
    <a class="duo-i reveal" href="/divyasena">{ph('home-divyasena.jpg', 'Dr. S. Divyasena, portrait', '1200×1500', 'tall')}<span class="duo-t"><b>Dr. S. Divyasena</b><span>Founder · Natyacharya · Doordarshan A grade artist</span><span class="muted">Dancer, choreographer and nattuvanar. More than twenty productions in India and abroad.</span></span></a>
    <a class="duo-i off reveal" href="/haribabu">{ph('home-haribabu.jpg', 'Sri B.P. Haribabu with mridangam', '1200×1500', 'tall')}<span class="duo-t"><b>Sri B.P. Haribabu</b><span>Mridangam · nattuvangam · rhythm composer</span><span class="muted">Over 85 tours to some 20 countries. He teaches laya, rhythm, as a subject of its own.</span></span></a>
  </div>
</div></section>
<section><div class="wrap">
  <div class="sec-head"><div><h2>Enchanting choreographies</h2></div><a class="btn-o" href="/choreographies">All {len(PRODUCTIONS)} productions</a></div>
  <div class="bento">{''.join(bento(p, i) for i, p in enumerate(feat))}</div>
</div></section>
<section class="alt classes"><div class="wrap">
  <div class="cls-head">
    <div class="stack" style="gap:12px"><h2>Find your class</h2><p class="muted">Technique, abhinaya, laya and theory, taught in small batches. Tap a card, then book a trial.</p><a class="btn-o" href="/learn" style="align-self:flex-start">All about classes</a></div>
    <figure class="cls-group" aria-hidden="false"><img src="/assets/img/dancers-group.webp" alt="Students of Divyanjali in Bharatanatyam poses" width="1241" height="612" loading="lazy"></figure>
  </div>
  <div class="cards" id="classCards">{cards}</div>
  <div class="cc-dots" aria-hidden="true"><i class="on"></i><i></i><i></i></div>
</div></section>
<section class="alumni"><div class="wrap al-grid">
  <div class="al-copy">
    <h2><b data-count="71">71</b> arangetrams. Stages from Chennai to the world.</h2>
    <p class="muted">Scholarship holders, Doordarshan graded artists, and teachers who now run their own schools.</p>
    <div class="al-where" aria-label="Where our alumni teach"><span>Alumni teach in</span>{''.join(f'<i style="--i:{i}">{c}</i>' for i, c in enumerate(['India', 'USA', 'UK', 'Singapore']))}</div>
    <a class="btn" href="/accolades" style="align-self:flex-start">Meet all {len(STUDENTS)} dancers</a>
  </div>
</div>
  <div class="marq" aria-label="Dancers of Divyanjali">{marquee_rows()}</div>
</section>
<section class="dark"><div class="wrap split">
  <div class="stack"><h2>How well do you know Bharatanatyam?</h2><p class="muted">Natya IQ: a quick quiz, a tala calculator and a mudra and rasa match. Share your score card.</p><div class="row"><a class="btn" href="/natya-iq">Take the quiz</a></div></div>
  {ph('home-natyaiq.jpg', 'Natya IQ share card', '1080×1080', 'sq')}
</div></section>
<section><div class="wrap">{head('Kind words', 'From rasikas and families')}
  <div class="quotes"><blockquote><p>“{todo('Quote from the Souvenir or the press')}”</p><cite>{todo('Name, title')}</cite></blockquote><blockquote><p>“{todo('Quote from a parent or student')}”</p><cite>{todo('Name')}</cite></blockquote></div></div></section>
{faq_section([
    ('How do I know when the next performance is?', 'Every date is on the <a href="/events">calendar</a>. Tap Subscribe and new dates appear in your phone calendar on their own.'),
    ('What age can my child start?', f'Children can start from {todo("youngest age")}. Adults and complete beginners of any age are welcome.'),
    ('Do you teach online?', 'Yes. Live classes from Chennai for students abroad, with batches set to your time zone.'),
    ('Do you teach Kuchipudi?', 'Divyanjali teaches Bharatanatyam only: technique, abhinaya, laya and theory.'),
    ('Can we book a production for our festival?', 'Yes. Send the date, venue and audience through <a href="/book">Book and Enquire</a>, and we reply on WhatsApp within 24 hours.'),
], alt=True)}
{cta('Begin your Bharatanatyam journey', 'Classes for children and adults in Chennai, and live online classes worldwide.', 'Ask about classes', '/learn#enquire', 'Hello Divyanjali, I would like to know about classes.')}
''')

BOOKS = [
    dict(key='essence', file='book-essence.png', kind='Book · 2006', title='Essence and Essentials of Dance', short='Essence and Essentials', shape='book',
         lead='The Divyanjali syllabus, in her own words.',
         body=['Dr. S. Divyasena wrote down what Divyanjali teaches, in theory and in practice, planned around the needs and abilities of students of every age group.',
               'It was released on 6 June 2006, and it is the syllabus every Divyanjali student learns from.'],
         inside=['The theory of dance', 'Practical training', 'Planned by age group', 'The Divyanjali syllabus'],
         facts=[('Author', 'Dr. S. Divyasena'), ('Released', '6 June 2006'), ('For', 'Students, parents and teachers of Bharatanatyam')]),
    dict(key='duta', file='book-duta-mahima.png', kind='Book', title='Duta Mahima', short='Duta Mahima', shape='book',
         lead='A book by Dr. S. Divyasena, published by Divyanjali.',
         body=['Duta Mahima is authored by Dr. S. Divyasena and published by Divyanjali, alongside Sri B.P. Haribabu\'s book on rhythm.'],
         inside=['Authored by Dr. S. Divyasena', 'Published by Divyanjali'],
         facts=[('Author', 'Dr. S. Divyasena'), ('Publisher', 'Divyanjali')]),
    dict(key='cd', file='cd-nrithyaharam.png', kind='Audio CD', title='Nrithyaharam', short='Nrithyaharam CD', shape='cd',
         lead='The adavus of Bharatanatyam, to practise at home.',
         body=['Dr. S. Divyasena compiled the adavus of Bharatanatyam on an audio CD, so that students can practise on their own between classes.'],
         inside=['The adavus of Bharatanatyam', 'For practice at home'],
         facts=[('Compiled by', 'Dr. S. Divyasena'), ('Format', 'Audio CD')]),
]

def books_section():
    for b in BOOKS: SLOTS.append(('/divyasena', b['file'], f"mock-up · {b['title']} (PNG, transparent background)", '1200×1200'))
    shelf = ''.join(f'<button type="button" class="shelf-i" data-b="{i}" aria-pressed="{str(i == 0).lower()}"><small>{e(b["kind"])}</small><b>{e(b["short"])}</b></button>' for i, b in enumerate(BOOKS))
    panels = ''.join(f'''<div class="bk-info-p" data-b="{i}"{'' if i == 0 else ' hidden'}>
      <p class="cv-role">{e(b['kind'])}</p><h3>{e(b['title'])}</h3><p class="bk-lead">{e(b['lead'])}</p>
      {''.join(f'<p>{e(t)}</p>' for t in b['body'])}
      <dl class="bk-facts">{''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in b['facts'])}</dl>
      <div class="cv-acts"><a class="btn" data-wa="Hello Divyanjali, I would like a copy of {e(b['title'])} by Dr. S. Divyasena." href="#">Ask for a copy</a><a class="btn-o" href="/store">See the Store</a></div>
    </div>''' for i, b in enumerate(BOOKS))
    data = json.dumps([{'t': b['title'], 'k': b['kind'], 'f': '/assets/img/' + b['file'], 's': b['shape'], 'in': b['inside']} for b in BOOKS], ensure_ascii=False)
    return f'''<section id="books" class="bio-sec bk-sec"><div class="wrap">
  <h2>Her books and recordings</h2>
  <p class="bio-sub">Drag the book to turn it, and tap it to open. Pick another from the shelf.</p>
  <div class="bk-grid">
    <div class="bk-stage" id="bkStage" aria-label="The book, in 3D. Drag to turn, tap to open.">
      <img class="bk-mock" id="bkMock" alt="" hidden>
      <div class="bk3d" id="bk3d" role="button" tabindex="0" aria-pressed="false">
        <div class="bk-cover"><div class="bk-face bk-front"><span class="bk-logo"></span><b id="bkT"></b><small>Dr. S. Divyasena</small></div><div class="bk-face bk-endpaper"></div></div>
        <div class="bk-face bk-inside"><small>Inside</small><ul id="bkIn"></ul></div>
        <div class="bk-face bk-spine"><span id="bkSp"></span></div>
        <div class="bk-face bk-pages"></div>
        <div class="bk-face bk-back"></div>
        <div class="bk-disc" aria-hidden="true"></div>
      </div>
      <div class="bk-shadow" aria-hidden="true"></div>
    </div>
    <div class="bk-side">
      <div class="shelf">{shelf}</div>
      {panels}
    </div>
  </div>
  <script type="application/json" id="bookData">{data}</script>
</div></section>
'''

def divyasena():
    facts = [('Art form', 'Bharatanatyam'), ('Roles', 'Dancer, choreographer, nattuvanar, guru'), ('Arangetram', '1985'),
             ('Founded', 'Divyanjali, Chennai, 1994'), ('Doordarshan', "'A' grade artist"),
             ('Education', 'Bachelor of Music · Master\'s in Kuchipudi · Doctorate in Bharatanatyam'),
             ('University', 'Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya'), ('Doctoral guide', 'Dr. Ambika Kameshwar'),
             ('Trust', 'Founder and Managing Trustee, Divyanjali (registered 2011)'), ('Service', "Secretary, 'Prayathnam', a forum for young classical dance teachers"),
             ('Arangetrams', '71 conducted by Divyanjali, including one abroad'), ('Performed in', 'India, USA, Thailand, Singapore, UAE, UK, Australia, Sri Lanka')]
    gurus = [('1985', 'Smt. Saroja Rani', 'First steps in Bharatanatyam, and her arangetram in 1985'),
             ('Bharatanatyam', "'Yuva Kala Bharathi' Sri J. Suryanarayana Murthy", 'Rigorous advanced training'),
             ('Abhinaya', "'Padma Bhushan' Smt. Kalanidhi Narayanan", 'Meticulous training in abhinaya'),
             ('Kuchipudi', "'Padma Bhushan' Dr. Vempati Chinna Satyam", 'Initiation at the Kuchipudi Arts Academy (her own training)'),
             ('Kuchipudi', 'Sri Udayakanth and Smt. Renuka', 'Initial years of Kuchipudi'),
             ('Kuchipudi', 'Sri Jaikishore Mosalikanti', 'Advanced training, ongoing'),
             ('Nattuvangam', 'Sri B.P. Haribabu', 'The art of wielding the cymbals')]
    abroad = [('USA', 'Cleveland Thyagaraja Festival · Nrithya Nataka Mala tour · Hanumath Margam premiere, 2026'), ('Thailand', 'Navarathri Festival, Bangkok'),
              ('Singapore', 'Navarathri Festival'), ('UAE', 'Performances in Dubai'), ('UK', 'Performances'), ('Australia', 'Melbourne, from 2013, with Nadanalaya'), ('Sri Lanka', 'Performances')]
    media = [('Jaya TV', 'Judge, Takadimi Tha dance show · interview'), ('Raj TV', "Judge, Aaseervath 'Abhinaya'"), ('Sun TV', 'Dance performances'),
             ('Makkal TV', 'Dance performances'), ('Podhigai', 'Dance performances'), ('Star Vijay', 'Divyanjali on air'), ('Kavasam web TV · Rasa web channel', 'Online performances')]
    works = [('Book · 2006', 'Essence and Essentials of Dance', "Divyanjali's full syllabus, theory and practice, written for every age group"),
             ('Book', 'Duta Mahima', 'Authored by Dr. S. Divyasena'),
             ('Audio CD', 'Nrithyaharam', 'The adavus of Bharatanatyam, compiled so students can practise on their own')]
    peers = [('Sri V. V. Sundaram', 'Her abhinaya is never very overt but gives the essence of the rasa while leaving some to the imagination of the audience.', 15),
             ('Smt. Nandini Ramani, veteran Bharatanatyam exponent', 'Divyasena is a very talented performer and teacher whose hard work and commitment have brought her good recognition and respect in the Bharatanatyam scene.', 14),
             ('Dr. Ambika Kameshwar, RASA', 'She trains her disciples in a focused and disciplined manner and brings out the best in them as well.', 19),
             ('Smt. Hema Rajagopalan, Natya Dance Theatre, Chicago', 'Divyasena has always worked very hard to maintain the integrity of the art form while being creative.', 21),
             ('Smt. Savithri Jagannath Rao', 'She has a brilliant approach in Layam. She is a very patient, brilliant and kind teacher.', 25)]
    prods = [p for p in PRODUCTIONS if p['slug']]
    tabs = [('profile', 'Profile'), ('lineage', 'Gurus'), ('education', 'Education'), ('work', 'Work'), ('books', 'Books'), ('stage', 'On stage'), ('media', 'Media'), ('words', 'In her words'), ('peers', 'Peers')]
    ld = {'@context': 'https://schema.org', '@type': 'Person', 'name': 'Dr. S. Divyasena', 'honorificPrefix': 'Natyacharya Dr.',
          'jobTitle': 'Bharatanatyam dancer, choreographer, nattuvanar and teacher', 'image': '/assets/img/divyasena-portrait.webp',
          'worksFor': {'@type': 'DanceGroup', 'name': 'Divyanjali', 'foundingDate': '1994', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Chennai', 'addressCountry': 'IN'}},
          'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya'},
          'hasCredential': ['Doctorate in Bharatanatyam', "Master's in Kuchipudi", 'Bachelor of Music', "Doordarshan 'A' grade artist"],
          'knowsAbout': ['Bharatanatyam', 'Abhinaya', 'Nattuvangam', 'Choreography', 'Kuchipudi'], 'spouse': {'@type': 'Person', 'name': 'B. P. Haribabu'},
          'sameAs': ['https://www.instagram.com/divyanjalidance/', 'https://www.youtube.com/channel/UCLPvhdH5qXt0R4IyDt1eSHg', 'https://www.facebook.com/divyanjali.dance/']}
    return page('/divyasena', 'Dr. S. Divyasena · Bharatanatyam dancer, choreographer and guru, Chennai',
        "Natyacharya Dr. S. Divyasena: Bharatanatyam dancer, choreographer and nattuvanar, founder of Divyanjali (1994), Doordarshan 'A' grade artist with a doctorate in Bharatanatyam. Full biography, gurus, productions and media.", f'''
{crumbs(('About', '/about'), ('Dr. S. Divyasena', None))}
<article class="bio">
<header class="bio-hero"><div class="wrap bio-hero-in">
  <figure class="bio-photo"><img src="/assets/img/divyasena-portrait.webp" alt="Dr. S. Divyasena in an abhinaya pose" width="1053" height="692" fetchpriority="high"></figure>
  <div class="bio-id">
    <p class="cv-role">Natyacharya · Founder of Divyanjali</p>
    <h1>Dr. S. Divyasena</h1>
    <p class="bio-line">Bharatanatyam dancer, choreographer, nattuvanar and guru. She founded Divyanjali in Chennai in 1994 and has shaped it for over thirty years.</p>
    <div class="cv-tags"><span>Doctorate in Bharatanatyam</span><span>Doordarshan 'A' grade</span><span>Secretary, Prayathnam</span></div>
    <div class="cv-acts">
      <button class="btn" type="button" data-share-menu aria-expanded="false">Share profile</button>
      <button class="btn-o" type="button" data-print>Download biodata</button>
      <a class="btn-o" href="/book?type=Performance+booking">Invite to perform</a>
    </div>
    <div class="share-pop" hidden>
      <button type="button" data-copy>Copy link</button>
      <a data-wa="Dr. S. Divyasena, Bharatanatyam guru and founder of Divyanjali" data-wa-url href="#">WhatsApp</a>
      <a href="#" data-share-x>X (Twitter)</a>
      <a href="#" data-share-fb>Facebook</a>
      <button type="button" data-share hidden>More options</button>
    </div>
  </div>
</div></header>

<nav class="bio-tabs" aria-label="On this page"><div class="wrap">{''.join(f'<a href="#{i}">{t}</a>' for i, t in tabs)}</div></nav>

<section id="profile" class="bio-sec"><div class="wrap bio-two">
  <div class="prose">
    <h2>Profile</h2>
    <p><b>Dr. S. Divyasena</b> is a versatile and accomplished Bharatanatyam artist, choreographer and teacher from Chennai. She trained in the preliminaries of Bharatanatyam under Smt. Saroja Rani and made her stage debut with her arangetram in 1985. She continued her rigorous training under 'Yuva Kala Bharathi' Sri J. Suryanarayana Murthy, and trained meticulously in abhinaya under 'Padma Bhushan' Smt. Kalanidhi Narayanan.</p>
    <p>Alongside Bharatanatyam she trained in Kuchipudi for her own growth as an artist: her initiation came at the Kuchipudi Arts Academy, led by the legendary 'Padma Bhushan' Dr. Vempati Chinna Satyam, with her first years under Sri Udayakanth and Smt. Renuka, and her advanced training under Sri Jaikishore Mosalikanti. She learnt nattuvangam, the art of wielding the cymbals, from Sri B.P. Haribabu.</p>
    <p>She is an 'A' grade artist of Doordarshan. She holds a Bachelor's in Music, a Master's in Kuchipudi and a Doctorate in Bharatanatyam from Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya, under the guidance of Dr. Ambika Kameshwar. She is also the secretary of 'Prayathnam', a forum for young classical dance teachers.</p>
    <p>In 1994 she founded <a href="/about">Divyanjali</a>. Its syllabus, written by her and published as <i>Essence and Essentials of Dance</i> in 2006, covers theory and practice for every age group. Students also learn thalam, ithihasam, puranas and moral values, which she calls "Poorna Vidhya". Divyanjali has conducted 71 arangetrams, including one she conducted abroad. At Divyanjali she teaches Bharatanatyam.</p>
  </div>
  <aside class="facts-card" aria-label="Biodata">
    <h3>Biodata</h3>
    <dl>{''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in facts)}</dl>
  </aside>
</div></section>

<section id="lineage" class="bio-sec alt"><div class="wrap">
  <h2>Gurus and lineage</h2>
  <p class="muted bio-sub">Tap a guru to see what she learnt from them.</p>
  <ol class="lineage">{''.join(f'<li class="reveal" style="--i:{i}"><button type="button" class="lin" aria-expanded="false"><span class="lin-k">{e(k)}</span><b>{e(n)}</b><span class="lin-d">{e(d)}</span></button></li>' for i, (k, n, d) in enumerate(gurus))}</ol>
</div></section>

<section id="education" class="bio-sec"><div class="wrap">
  <h2>Education</h2>
  <div class="edu">
    <div class="edu-c reveal"><small>Doctorate</small><b>Bharatanatyam</b><span>Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya, guided by Dr. Ambika Kameshwar</span></div>
    <div class="edu-c reveal"><small>Master's</small><b>Kuchipudi</b><span>Postgraduate study, part of her own training</span></div>
    <div class="edu-c reveal"><small>Bachelor's</small><b>Music</b><span>Carnatic music</span></div>
    <div class="edu-c reveal"><small>Doordarshan</small><b>'A' grade artist</b><span>Graded by the national broadcaster</span></div>
  </div>
</div></section>

<section id="work" class="bio-sec alt"><div class="wrap">
  <h2>Founder, teacher and author</h2>
  <ol class="tl">
    <li><b>1994</b><span>Founded Divyanjali in CIT Nagar, Chennai</span></li>
    <li><b>2004</b><span>Divyanjali's own workspace, inaugurated by Smt. Chithra Visweswaran and Smt. Nandini Ramani</span></li>
    <li><b>2006</b><span>Published the syllabus as <i>Essence and Essentials of Dance</i></span></li>
    <li><b>2011</b><span>Divyanjali registered as a trust, with herself as Founder and Managing Trustee; grants from the Government of India and Tamil Isai Sangam followed</span></li>
    <li><b>2015</b><span>Rebuilt the school after the Chennai floods</span></li>
    <li><b>2017</b><span>Started Kalarpanam, a platform for young artists</span></li>
    <li><b>2018</b><span>Sangeet International Festival, with the All India Dancers Association</span></li>
    <li><b>2019–20</b><span>Nrithya Utsav, a season of festivals, lecture demonstrations and competitions for the Silver Jubilee</span></li>
    <li><b>2024</b><span>Thirty years of Divyanjali · <a href="/30-years">read the Souvenir 2026</a></span></li>
  </ol>
  <p class="bio-sub" style="margin-top:22px">Her books and the Nrithyaharam CD are below. <a href="#books">See them</a></p>
</div></section>

{books_section()}
<section id="stage" class="bio-sec"><div class="wrap">
  <h2>Choreographer and performer</h2>
  <p class="bio-sub">She has composed and presented group productions across India and abroad. <i>Andal Vaibhavam</i> was staged on 13 stages in a single year, and <i>Hanumath Margam</i> premiered at the 50th Cleveland Thyagaraja Festival in 2026.</p>
  <div class="prod-chips">{''.join(f'<a href="/productions/{p["slug"]}">{e(p["title"])}{"<small>" + p["year"] + "</small>" if p["year"] else ""}</a>' for p in prods)}<a href="/choreographies" class="all">All productions ›</a></div>
  <h3 class="bio-h3">Performances abroad</h3>
  <div class="abroad">{''.join(f'<button type="button" class="ab" aria-expanded="false"><b>{e(c)}</b><span>{e(d)}</span></button>' for c, d in abroad)}</div>
  <div class="vids" style="margin-top:26px">{yt('https://www.youtube.com/watch?v=So5SO_M4zZ8', 'Dasavatharam')}{yt(HOME_VIDEO, 'Divyanjali on stage', 12)}</div>
</div></section>

<section id="media" class="bio-sec alt"><div class="wrap">
  <h2>Media and television</h2>
  <div class="media-grid">{''.join(f'<div class="mg reveal"><b>{e(c)}</b><span>{e(d)}</span></div>' for c, d in media)}</div>
</div></section>

<section id="words" class="bio-sec"><div class="wrap bio-two">
  <div>
    <h2>In her words</h2>
    <blockquote class="her-q">"Not all the fingers are the same. Every dancer has a unique talent. I strive hard to make all my students realise their uniqueness and potential."</blockquote>
    <div class="prose">
      <p>"Every day has been a new learning experience with the art. I started teaching with the motive of sharing what I had learned from natyam with as many young minds as possible."</p>
      <p>"As a teacher, the most joyous moment was when my students pursued the art form and were appreciated. Watching the world of natyam flourish in my students' minds and souls makes me the happiest person."</p>
      <p class="muted">From her Letter from the Founder, Souvenir 2026. <a href="/30-years#p=5">Read the full letter</a></p>
    </div>
  </div>
  <figure class="bio-duo"><img src="/assets/img/founders-together.webp" alt="Sri B.P. Haribabu and Dr. S. Divyasena" width="1200" height="993" loading="lazy"><figcaption>With Sri B.P. Haribabu, mridangam artist and Secretary-Trustee of Divyanjali. <a href="/haribabu">His profile</a></figcaption></figure>
</div></section>

<section id="peers" class="bio-sec alt"><div class="wrap">
  <h2>What fellow artists say</h2>
  <div class="peer-row">{''.join(f'<figure class="peer reveal" style="--i:{i}"><blockquote>"{e(q)}"</blockquote><figcaption>{e(n)} · <a href="/30-years#p={pg}">souvenir p.{pg}</a></figcaption></figure>' for i, (n, q, pg) in enumerate(peers))}</div>
</div></section>
</article>
{faq_section([
    ('Who is Dr. S. Divyasena?', "A Bharatanatyam dancer, choreographer, nattuvanar and teacher from Chennai, the founder of Divyanjali (1994), a Doordarshan 'A' grade artist with a doctorate in Bharatanatyam."),
    ('Who are her gurus?', 'Smt. Saroja Rani, Sri J. Suryanarayana Murthy and, for abhinaya, Smt. Kalanidhi Narayanan. She also trained in Kuchipudi under the academy of Dr. Vempati Chinna Satyam and Sri Jaikishore Mosalikanti, and in nattuvangam under Sri B.P. Haribabu.'),
    ('What is her doctorate in?', 'Bharatanatyam, from Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya, under the guidance of Dr. Ambika Kameshwar.'),
    ('Does Divyanjali teach Kuchipudi?', 'No. Kuchipudi is part of her own training and informs her work; Divyanjali teaches Bharatanatyam.'),
    ('Can we invite her for a performance, workshop or lecture demonstration?', 'Yes. Send the details through <a href="/book?type=Workshop+or+lecture+demonstration">Book and Enquire</a>.'),
])}
{cta('Invite Dr. Divyasena', 'For performances, workshops, lecture demonstrations and productions.', 'Send an enquiry', '/book?type=Workshop+or+lecture+demonstration', 'Hello Divyanjali, I would like to invite Dr. Divyasena.')}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
''', extra_head='<meta property="og:image" content="/assets/img/divyasena-portrait.webp">\n<meta property="og:type" content="profile">\n<link rel="canonical" href="/divyasena">\n')

STORY = [
    ('1994', 'The school begins', 'Dr. S. Divyasena founds Divyanjali in CIT Nagar, Chennai, to share what she had learnt from natyam with as many young minds as possible.'),
    ('2004', 'A home of its own', 'Divyanjali opens its own workspace, inaugurated by Smt. Chithra Visweswaran and Smt. Nandini Ramani.'),
    ('2006', 'The syllabus, in a book', 'The Divyanjali syllabus, theory and practice planned for every age group, is published as <i>Essence and Essentials of Dance</i>.'),
    ('2011', 'A registered trust', 'Divyanjali becomes a trust. Grants from the Government of India and Tamil Isai Sangam make productions like <i>Nava Vidha Sambandham</i> and <i>Andal Vaibhavam</i> possible.'),
    ('2015', 'The floods, and the way back', 'The Chennai floods hit the school hard. Students, parents and friends helped Divyanjali dance again. <a href="/30-years">Read the story</a>'),
    ('2017', 'Kalarpanam', 'Divyanjali starts its own platform for young, deserving artists to perform.'),
    ('2018', 'Sangeet International Festival', 'Hosted with the All India Dancers Association, with music and dance of many styles.'),
    ('2019', 'Nrithya Utsav', 'For the Silver Jubilee: festivals, lecture demonstrations, workshops and competitions, month on month, from July 2019 to February 2020.'),
    ('2024', 'Thirty years', 'Divyanjali completes thirty years. 71 arangetrams so far, including one abroad. <a href="/30-years">Open the Souvenir 2026</a>'),
]
TEACH = [
    ('person-arms-spread', 'Bharatanatyam', 'Adavus, items and the full margam, step by step up to the arangetram.'),
    ('metronome', 'Laya, rhythm', 'Tala and rhythm as a subject of its own, with Sri B.P. Haribabu.'),
    ('mask-happy', 'Abhinaya', 'Expression and storytelling, taught by engaging children creatively.'),
    ('book-open-text', 'Theory', 'From the school\'s own published syllabus, for every age group.'),
]
FACULTY_SLUGS = ['upanisha-k', 'akshaya-s', 'krishnapriya', 'sweta-n', 'shabin-bright', 'sukanya']
EARLIER_FACULTY = ['Aiswarya Ramanan', 'S. Mahati', 'Harini N.', 'Mohanambal P.', 'S. Sivagami', 'Shyamala Aadith', 'Archana Kanthan', 'Preeti P.', 'Shantha',
                   'Swarna Varsha Gurumoorthy', 'Krithika S.', 'Roopa S.', 'Sharmili N.', 'Vinaya Skandaprasad']

def about():
    by = {p['slug']: p for p in STUDENTS}
    fac = [by[s] for s in FACULTY_SLUGS if s in by]
    return page('/about', 'About Divyanjali · Bharatanatyam school in Chennai since 1994',
        'Divyanjali, founded in 1994 by Dr. S. Divyasena, teaches Bharatanatyam in Chennai with laya, abhinaya and theory. Our story, what we teach, the trust and our faculty.', f'''
{crumbs(('About', None))}
<section class="ab-hero"><div class="wrap ab-hero-in">
  <div class="ab-copy">
    <p class="eyebrow">Dance school · since 1994</p>
    <h1>Divyanjali</h1>
    <p class="lead">A Bharatanatyam school in Chennai, founded by Dr. S. Divyasena. Thirty years on, it is still the same idea: teach the whole art, and make the school a second home.</p>
    <ul class="ab-facts"><li><b>1994</b><span>founded</span></li><li><b>2011</b><span>registered trust</span></li><li><b>71</b><span>arangetrams</span></li></ul>
    <div class="row"><a class="btn" href="/learn">Join a class</a><a class="btn-o" href="/30-years">Our 30 years</a></div>
  </div>
  <figure class="ab-photo"><img src="/assets/img/dancers-group.webp" alt="Divyanjali dancers together on stage" width="1161" height="541" fetchpriority="high"></figure>
</div></section>

<section class="alt"><div class="wrap">
  {head('Our story', 'Thirty years, one year at a time')}
  <p class="muted yr-hint">Tap a year.</p>
  <div class="yr" data-yr>
    <div class="yr-rail" role="tablist" aria-label="Years">{''.join(f'<button type="button" role="tab" aria-selected="{str(i == 0).lower()}" aria-controls="yr-{y}" id="yrt-{y}">{y}</button>' for i, (y, t, d) in enumerate(STORY))}</div>
    {''.join(f'<article class="yr-p" role="tabpanel" id="yr-{y}" aria-labelledby="yrt-{y}"{"" if i == 0 else " hidden"}><b class="yr-y" aria-hidden="true">{y}</b><div><h3>{t}</h3><p>{d}</p></div></article>' for i, (y, t, d) in enumerate(STORY))}
    <div class="yr-nav"><button type="button" class="yr-b" data-yr-step="-1" aria-label="Previous year">‹</button><button type="button" class="yr-b" data-yr-step="1" aria-label="Next year">›</button></div>
  </div>
</div></section>

<section><div class="wrap">
  {head('What we teach', 'Four parts of one art')}
  <div class="teach">{''.join(f'<div class="tc reveal" style="--i:{i}">{icon(ic)}<h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(TEACH))}</div>
  <blockquote class="ab-q">"Along with natyam my students learn thalam, ithihasam, puranas and moral values, to impart <i>Poorna Vidhya</i>. I always try to make Divyanjali their second home."<cite>Dr. S. Divyasena, <a href="/30-years#p=5">Letter from the Founder</a></cite></blockquote>
</div></section>

<section class="alt"><div class="wrap">
  {head('The trust', 'The people behind Divyanjali')}
  <div class="trust">
    <a class="tr reveal" href="/divyasena"><img src="/assets/img/divyasena-portrait.webp" alt="Dr. S. Divyasena" width="1053" height="692" loading="lazy" style="object-position:32% 40%"><span class="tr-r">Founder and Managing Trustee</span><b>Dr. S. Divyasena</b><span class="tr-d">Dancer, choreographer, nattuvanar and guru</span><span class="tr-go">Her profile ›</span></a>
    <a class="tr reveal" href="/haribabu" style="--i:1"><img src="/assets/img/haribabu-portrait.webp" alt="Sri B.P. Haribabu" width="555" height="820" loading="lazy" style="object-position:50% 18%"><span class="tr-r">Secretary and Trustee</span><b>Sri B.P. Haribabu</b><span class="tr-d">Mridangam artist, nattuvanar and rhythm composer</span><span class="tr-go">His profile ›</span></a>
    <div class="tr reveal" style="--i:2"><img src="/assets/img/lakshmi.webp" alt="Smt. S. Lakshmi" width="300" height="300" loading="lazy" style="object-position:50% 30%"><span class="tr-r">Treasurer and Trustee</span><b>Smt. S. Lakshmi</b><span class="tr-d">Trustee of Divyanjali</span></div>
  </div>
</div></section>

<section><div class="wrap">
  {head('Faculty', 'Our teachers')}
  <p class="muted bio-sub">Every one of them trained at Divyanjali. Tap a teacher to see their profile.</p>
  <div class="fac">{''.join(f'<a class="fc reveal" href="/students/{p["slug"]}" style="--i:{i}">{st_face(p)}<b>{e(p["display"])}</b><span>{e(st_tags(p)[1] if len(st_tags(p)) > 1 else "Faculty")}</span></a>' for i, p in enumerate(fac))}</div>
  <details class="fac-more"><summary>Teachers over the years</summary><p>{', '.join(EARLIER_FACULTY)}.</p></details>
</div></section>
{faq_section([
    ('When was Divyanjali founded?', 'In 1994, by Dr. S. Divyasena, in CIT Nagar, Chennai.'),
    ('Is Divyanjali a registered trust?', 'Yes. Divyanjali was registered as a trust in 2011. Dr. S. Divyasena is the Founder and Managing Trustee, Sri B.P. Haribabu the Secretary-Trustee and Smt. S. Lakshmi the Treasurer-Trustee.'),
    ('Who teaches the classes?', 'Dr. S. Divyasena leads the teaching, Sri B.P. Haribabu teaches laya, and the Divyanjali faculty, all trained at the school, teach alongside them.'),
    ('Which dance form does Divyanjali teach?', 'Bharatanatyam, with laya, abhinaya and theory as part of every student\'s training.'),
], alt=True)}
{cta('Come and watch a class', 'See how we teach before you join.', 'Ask about classes', '/learn#enquire', 'Hello Divyanjali, can I come and watch a class?')}
''', extra_head='<meta property="og:image" content="/assets/img/dancers-group.webp">\n<link rel="canonical" href="/about">\n')

def haribabu():
    facts = [('Instrument', 'Mridangam'), ('Also plays', 'Pakhawaj'), ('Also', 'Nattuvangam and rhythm composition'),
             ('Title', "'Vaadhya Visharadha'"), ('Trained at', 'Tamil Nadu Government Music College'),
             ('Gurus', "'Kalaimamani' Sri V.P. Ramadoss and 'Kalaimamani' Sri Thiruvaroor Bhakthavatchalam"),
             ('Specialist in', 'Bharatanatyam and Kuchipudi concerts'), ('Accompanying', 'For over 25 years'),
             ('Abroad', 'More than 85 tours to around 20 countries since 1993'), ('Also', 'Has worked with major dance companies in the USA'),
             ('Divyanjali', 'Secretary and Trustee'), ('Book', 'Essence and Essentials of Rhythm')]
    gurus = [('Mridangam', "'Kalaimamani' Sri V.P. Ramadoss", 'His guru at the Tamil Nadu Government Music College'),
             ('Mridangam', "'Kalaimamani' Sri Thiruvaroor Bhakthavatchalam", 'His guru at the Tamil Nadu Government Music College'),
             ('Title', "'Vaadhya Visharadha'", 'Conferred on him for his mastery of the art')]
    crafts = [('music-notes', 'Mridangam', 'His main instrument. He accompanies solo recitals, arangetrams and productions.'),
              ('metronome', 'Pakhawaj', 'The barrel drum of the north, played with the same command.'),
              ('hands-clapping', 'Nattuvangam', 'Conducting a performance with the cymbals. He taught it to Dr. S. Divyasena.'),
              ('certificate', 'Rhythm composition', 'Jathis and rhythmic passages composed for dance.')]
    peers = [('Sri V. V. Sundaram', 'The jathis he composes are intellectually challenging and aesthetically pleasing and a pleasure to see them naturally molded into the performances.', 15),
             ('Sri Kuldeep M Pai, musician', 'As a singer, I have always admired and relished every stroke of his Mridangam playing!', 26),
             ('Smt. Savithri Jagannath Rao', 'Shri B P Haribabu is an excellent mridangist and accompaniment for both vocal and Natya.', 25),
             ('Smt. Anitha Guha, Bharathanjali', 'Vidwan Hari Babu sir who has actually been the Rhythm of your life and Natyam.', 24),
             ('Smt. Nandini Ramani, veteran Bharatanatyam exponent', 'Haribabu, her life partner and ace Mridangam artist who is the pillar of support to Divya.', 14),
             ('Dr. P. Ramaa, singer', 'We have been working together since 35 years.', 26)]
    book_q = [('Dr. Padma Subrahmanyam', 'I am sure the book written by Sri. Haribabu on Rhythm will be a valuable addition to the world of music and dance.', 16),
              ('Smt. Vasanthalakshmi Narasimhachari', 'True to the title, I am sure the book will be a reflection of your vast experience, both as a much sought-after Mridangam player and a composer in the field of Bharatanatyam.', 22)]
    tabs = [('profile', 'Profile'), ('gurus', 'Gurus'), ('craft', 'His craft'), ('tala', 'Try a tala'), ('book', 'His book'), ('peers', 'Peers')]
    ld = {'@context': 'https://schema.org', '@type': 'Person', 'name': 'B. P. Haribabu', 'honorificPrefix': 'Sri',
          'jobTitle': 'Mridangam artist, nattuvanar and rhythm composer', 'image': '/assets/img/haribabu-portrait.webp',
          'award': 'Vaadhya Visharadha', 'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Tamil Nadu Government Music College'},
          'worksFor': {'@type': 'DanceGroup', 'name': 'Divyanjali', 'foundingDate': '1994'}, 'spouse': {'@type': 'Person', 'name': 'Dr. S. Divyasena'},
          'knowsAbout': ['Mridangam', 'Pakhawaj', 'Nattuvangam', 'Rhythm composition', 'Bharatanatyam', 'Kuchipudi']}
    return page('/haribabu', 'Sri B.P. Haribabu · Mridangam artist, nattuvanar and rhythm composer, Chennai',
        "Sri B.P. Haribabu: 'Vaadhya Visharadha' mridangam artist, nattuvanar and rhythm composer. Over 25 years accompanying Bharatanatyam and Kuchipudi, more than 85 tours abroad. Secretary-Trustee of Divyanjali.", f'''
{crumbs(('About', '/about'), ('Sri B.P. Haribabu', None))}
<article class="bio">
<header class="bio-hero"><div class="wrap bio-hero-in">
  <figure class="bio-photo por"><img src="/assets/img/haribabu-portrait.webp" alt="Sri B.P. Haribabu" width="555" height="820" fetchpriority="high"></figure>
  <div class="bio-id">
    <p class="cv-role">Vaadhya Visharadha · Secretary-Trustee of Divyanjali</p>
    <h1>Sri B.P. Haribabu</h1>
    <p class="bio-line">Mridangam artist, nattuvanar and rhythm composer. He has accompanied Bharatanatyam and Kuchipudi for over 25 years, and teaches laya to every Divyanjali student.</p>
    <div class="cv-tags"><span>Mridangam · Pakhawaj</span><span>Nattuvangam</span><span>85+ tours abroad</span></div>
    <div class="cv-acts">
      <button class="btn" type="button" data-share-menu aria-expanded="false">Share profile</button>
      <button class="btn-o" type="button" data-print>Download biodata</button>
      <a class="btn-o" href="/book?type=Performance+booking">Book him to accompany</a>
    </div>
    <div class="share-pop" hidden>
      <button type="button" data-copy>Copy link</button>
      <a data-wa="Sri B.P. Haribabu, mridangam artist and Secretary-Trustee of Divyanjali" data-wa-url href="#">WhatsApp</a>
      <a href="#" data-share-x>X (Twitter)</a>
      <a href="#" data-share-fb>Facebook</a>
      <button type="button" data-share hidden>More options</button>
    </div>
  </div>
</div></header>

<nav class="bio-tabs" aria-label="On this page"><div class="wrap">{''.join(f'<a href="#{i}">{t}</a>' for i, t in tabs)}</div></nav>

<section id="profile" class="bio-sec"><div class="wrap bio-two">
  <div class="prose">
    <h2>Profile</h2>
    <p><b>Sri B.P. Haribabu</b> is a versatile mridangam exponent from Chennai. He trained under the exemplary gurus 'Kalaimamani' Sri V.P. Ramadoss and 'Kalaimamani' Sri Thiruvaroor Bhakthavatchalam at the Tamil Nadu Government Music College, and was conferred the title 'Vaadhya Visharadha' in recognition of his mastery of the art.</p>
    <p>Besides the mridangam he is equally proficient in pakhawaj, nattuvangam and rhythm composition. A specialist in playing for Bharatanatyam and Kuchipudi concerts, he is a sought-after mridangam artist who has accompanied many artists for over 25 years. Since 1993 he has travelled widely, with more than 85 tours abroad to around 20 countries, and has worked with major dance companies in the USA.</p>
    <p>At <a href="/about">Divyanjali</a> he is the Secretary-Trustee and teaches laya, the rhythm of dance, as a subject of its own. He taught nattuvangam to <a href="/divyasena">Dr. S. Divyasena</a>, his wife and artistic partner, and composes the jathis for her productions.</p>
  </div>
  <aside class="facts-card" aria-label="Biodata">
    <h3>Biodata</h3>
    <dl>{''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in facts)}</dl>
  </aside>
</div></section>

<section id="gurus" class="bio-sec alt"><div class="wrap">
  <h2>Gurus and title</h2>
  <p class="muted bio-sub">Tap a card to read more.</p>
  <ol class="lineage">{''.join(f'<li class="reveal" style="--i:{i}"><button type="button" class="lin" aria-expanded="false"><span class="lin-k">{e(k)}</span><b>{e(n)}</b><span class="lin-d">{e(d)}</span></button></li>' for i, (k, n, d) in enumerate(gurus))}</ol>
</div></section>

<section id="craft" class="bio-sec"><div class="wrap">
  <h2>His craft</h2>
  <div class="teach">{''.join(f'<div class="tc reveal" style="--i:{i}">{icon(ic)}<h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(crafts))}</div>
  <h3 class="bio-h3">Rhythm on stage</h3>
  <ol class="tl">
    <li><b>1993</b><span>Begins touring abroad: more than 85 tours to around 20 countries since</span></li>
    <li><b>1994</b><span>Divyanjali begins; he builds it with Dr. S. Divyasena and teaches laya</span></li>
    <li><b>2012</b><span><a href="/productions/laya-thrayam">Laya Thrayam</a>, a production with rhythm at its heart, premieres in New Delhi. Its tala and swara segment is composed by him and Sri Srikanth Gopalakrishnan</span></li>
    <li><b>2020</b><span>His book on rhythm is announced at Divyanjali's Silver Jubilee</span></li>
  </ol>
</div></section>

<section id="tala" class="bio-sec alt"><div class="wrap">
  <h2>Try a tala</h2>
  <p class="bio-sub">Every Divyanjali student learns to keep the tala with their hands. Press play and count along: clap, then the fingers, then clap and wave.</p>
  <div class="tala" data-tala>
    <div class="tala-top">
      <div class="tala-pick" role="radiogroup" aria-label="Tala">
        <button type="button" role="radio" aria-checked="true" data-t="adi">Adi · 8 beats</button>
        <button type="button" role="radio" aria-checked="false" data-t="rupaka">Rupakam · 6 beats</button>
      </div>
      <label class="tala-sp">Speed <input type="range" min="50" max="140" value="80" aria-label="Beats per minute"><output>80</output></label>
    </div>
    <ol class="tala-beats" aria-live="off"></ol>
    <div class="tala-acts"><button type="button" class="btn tala-play" aria-pressed="false">Play</button><label class="tala-snd"><input type="checkbox" checked> Sound</label></div>
    <p class="muted tala-note">A simple guide for counting. The real teaching happens in class.</p>
  </div>
</div></section>

<section id="book" class="bio-sec"><div class="wrap bio-two">
  <div>
    <h2>His book on rhythm</h2>
    <div class="prose">
      <p><i>Essence and Essentials of Rhythm</i> is his book on the concepts of rhythm, written to nurture young artists. It is published by Divyanjali, alongside Dr. S. Divyasena's <i>Duta Mahima</i>.</p>
      <p>Fellow artists looked forward to it when it was announced at the school's Silver Jubilee.</p>
    </div>
    <div class="peer-row one">{''.join(f'<figure class="peer reveal" style="--i:{i}"><blockquote>"{e(q)}"</blockquote><figcaption>{e(n)} · <a href="/30-years#p={pg}">souvenir p.{pg}</a></figcaption></figure>' for i, (n, q, pg) in enumerate(book_q))}</div>
  </div>
  <div class="hb-book" aria-hidden="true"><div class="hb-cover"><small>B.P. Haribabu</small><b>Essence and Essentials of Rhythm</b><span>Divyanjali</span></div></div>
</div></section>

<section id="peers" class="bio-sec alt"><div class="wrap">
  <h2>What fellow artists say</h2>
  <div class="peer-row">{''.join(f'<figure class="peer reveal" style="--i:{i}"><blockquote>"{e(q)}"</blockquote><figcaption>{e(n)} · <a href="/30-years#p={pg}">souvenir p.{pg}</a></figcaption></figure>' for i, (n, q, pg) in enumerate(peers))}</div>
  <figure class="bio-duo" style="margin-top:34px"><img src="/assets/img/founders-together.webp" alt="Sri B.P. Haribabu and Dr. S. Divyasena" width="1200" height="993" loading="lazy"><figcaption>With Dr. S. Divyasena, founder of Divyanjali. <a href="/divyasena">Her profile</a></figcaption></figure>
</div></section>
</article>
{faq_section([
    ('Who is Sri B.P. Haribabu?', "A mridangam artist, nattuvanar and rhythm composer from Chennai, titled 'Vaadhya Visharadha', and the Secretary-Trustee of Divyanjali."),
    ('Who are his gurus?', "'Kalaimamani' Sri V.P. Ramadoss and 'Kalaimamani' Sri Thiruvaroor Bhakthavatchalam, at the Tamil Nadu Government Music College."),
    ('Can he accompany our performance or arangetram?', 'Yes. Send the date and venue through <a href="/book?type=Performance+booking">Book and Enquire</a>.'),
    ('Does he teach rhythm to dancers?', 'Yes. Laya is taught as a subject of its own to every Divyanjali student.'),
    ('What is nattuvangam?', 'The art of conducting a Bharatanatyam performance with cymbals, reciting the rhythmic syllables that the dancer follows.'),
])}
{cta('Book Sri Haribabu', 'Mridangam and nattuvangam for performances, arangetrams and productions.', 'Send an enquiry', '/book?type=Performance+booking', 'Hello Divyanjali, I would like to book Sri Haribabu.')}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
''', extra_head='<meta property="og:image" content="/assets/img/haribabu-portrait.webp">\n<meta property="og:type" content="profile">\n<link rel="canonical" href="/haribabu">\n')

# ---------------------------------------------------------------- students (from the Souvenir 2026, pages 50 to 55)
STUDENTS = json.load(open(os.path.join(ROOT, 'students.json'), encoding='utf-8'))
ABROAD = ['usa', 'united states', 'singapore', 'bangkok', 'dubai', 'uae', 'united arab', ' uk', 'germany', 'sri lanka', 'srilanka', 'jaffna', 'mauritius', 'australia', 'cleveland', 'nizwa']

def st_tags(p):
    t = ' ' + ' '.join(p['items']).lower()
    tags = []
    if p['group'] == 'Faculty': tags.append('Faculty')
    elif p['group'] == 'Alumni': tags.append('Alumni')
    else: tags.append('Students')
    if any(k in t for k in ('doordarshan', 'doordharsan', 'doordharshab', 'podhigai')): tags.append('Doordarshan graded')
    if 'scholarship' in t or 'fellowship' in t: tags.append('Scholarship')
    if any(k in t for k in ABROAD): tags.append('Performed abroad')
    if 'founder' in t or 'director -' in t or 'director of' in t: tags.append('Runs a school')
    return tags

def initials(n):
    w = [x for x in re.sub(r'\b(Dr|S)\.?\s', '', n).replace('.', ' ').split() if len(x) > 1]
    return (w[0][0] + (w[1][0] if len(w) > 1 else '')).upper() if w else n[:2].upper()

def st_face(p, cls='face'):
    if p['photo']:
        return f'<span class="{cls}"><img src="{p["photo"]}" alt="{e(p["display"])}" loading="lazy" width="360" height="360"></span>'
    return f'<span class="{cls} none" aria-hidden="true">{initials(p["display"])}</span>'

def st_card(p, i=0):
    tags = st_tags(p)
    return (f'<a class="stc reveal" href="/students/{p["slug"]}" data-cat="{"Faculty" if p["group"] == "Faculty" else "Students"}" data-name="{e(p["display"].lower())}" style="--i:{i % 6}">'
            f'{st_face(p)}<b>{e(p["display"])}</b><small>{e(tags[0] if tags[0] != "Students" else "Student")}</small>'
            f'<span class="stc-one">{e(p["items"][0][:90])}{"…" if len(p["items"][0]) > 90 else ""}</span></a>')

def accolades():
    chips = ['All', 'Faculty', 'Students']
    return page('/accolades', "Student's Accolades · Divyanjali", 'Faculty, students and alumni of Divyanjali: Doordarshan graded artists, scholarship holders, prize winners and teachers. Each dancer has a page of their own.', f'''
<section class="acc-hero"><div class="wrap">
  <h1>Student's Accolades</h1>
  <p class="lead">The faculty, students and alumni of Divyanjali, with every award listed in the Souvenir 2026. Tap a dancer to open their page, share it, or save it as a one-page résumé.</p>
</div></section>
<section class="alt acc-list"><div class="wrap">
  <div class="acc-tools">
    <div class="chipbar" data-filter="#studentGrid" data-count="#accCount">{''.join(f'<button class="chip" type="button" data-f="{f}" aria-pressed="{str(f == "All").lower()}">{f}</button>' for f in chips)}</div>
  </div>
  <p class="muted acc-count" id="accCount">Showing {len(STUDENTS)}</p>
  <div class="stgrid" id="studentGrid">{''.join(st_card(p, i) for i, p in enumerate(STUDENTS))}</div>
  <p class="muted acc-src">From the Divyanjali Souvenir 2026, pages 50 to 55. <a href="/30-years#p=50">Read those pages in the souvenir</a>. To add or correct a profile, <a data-wa="Hello Divyanjali, I would like to update a profile on Student's Accolades." href="#">message us on WhatsApp</a>.</p>
</div></section>
<section><div class="wrap two">
  <div class="stack">{head('Alumni', 'Students who started schools')}<ol class="tl"><li><b>Kala Roopam</b><span><a href="/students/s-roopa-s">Dr. S. Roopa S</a></span></li><li><b>Shiva Nrittam</b><span><a href="/students/sumodh">Sumodh</a></span></li><li><b>Ananda Natyakshethra</b><span><a href="/students/anandaraj-a">Anandaraj A</a>, Thiruverkadu</span></li></ol></div>
  <div class="stack">{head('Recognition', 'Scholarships and prizes')}<ul class="list">
    <li>CCRT Scholarship, Government of India</li><li>Bharat Kalachar Scholarship</li><li>Iyal Isai Nataka Mandram Scholarship</li>
    <li>Prizes at the Cleveland Thyagaraja Festival, Ohio, USA</li><li>All India Dance Festival, Kalamandir College of Fine Arts, Kannur</li>
    <li>Natyarangam and Spirit of Youth competitions, Music Academy, Chennai</li></ul></div>
</div></section>
{cta('Your child could be next', 'Classes for children from their first steps to arangetram.', 'Ask about classes', '/learn#enquire')}
''')

def student_page(p):
    i = STUDENTS.index(p)
    prev, nxt = STUDENTS[i - 1], STUDENTS[(i + 1) % len(STUDENTS)]
    tags = st_tags(p)
    lis = ''.join(f'<li><span class="dot" aria-hidden="true"></span><span>{e(t)}</span></li>' for t in p['items'])
    ig = p.get('instagram', '').strip().lstrip('@')
    ig_btn = f'<a class="btn-o ig" href="https://www.instagram.com/{e(ig)}/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>@{e(ig)}</a>' if ig else ''
    role = {'Faculty': 'Faculty, Divyanjali', 'Alumni': 'Alumna of Divyanjali', 'Student': 'Student of Divyanjali'}[p['group']]
    if p['display'] in ('Sumodh', 'Anandaraj A', 'Dr. Shabin Bright'): role = role.replace('Alumna', 'Alumnus')
    ld = {'@context': 'https://schema.org', '@type': 'Person', 'name': p['display'], 'description': role + '. ' + p['items'][0],
          'affiliation': {'@type': 'Organization', 'name': 'Divyanjali', 'url': '/'}, 'award': p['items'][:8]}
    if p['photo']: ld['image'] = p['photo']
    desc = f"{p['display']}, {role.lower()}. {p['items'][0]}"
    og = f'<meta property="og:image" content="{p["photo"]}">\n' if p['photo'] else ''
    return page(f'/students/{p["slug"]}', f"{p['display']} · Divyanjali", desc[:300], f'''
{crumbs(("Student's Accolades", '/accolades'), (p['display'], None))}
<article class="cv">
  <div class="wrap cv-top">
    {st_face(p, 'cv-face')}
    <div class="cv-id">
      <p class="cv-role">{e(role)}</p>
      <h1>{e(p['display'])}</h1>
      <div class="cv-tags">{''.join(f'<span>{e(t)}</span>' for t in tags if t not in ('Students', 'Faculty', 'Alumni'))}</div>
      <div class="cv-acts">
        <button class="btn" type="button" data-copy>Copy link</button>
        {ig_btn}
        <a class="btn-o" data-wa="{e(p['display'])}, {e(role)}" data-wa-url href="#">WhatsApp</a>
        <button class="btn-o" type="button" data-share hidden>Share</button>
        <button class="btn-o" type="button" data-print>Save as PDF</button>
      </div>
    </div>
  </div>
  <div class="wrap cv-body">
    <h2>Awards and accomplishments</h2>
    <ol class="cv-list">{lis}</ol>
    <p class="muted cv-src">Source: Divyanjali Souvenir 2026, page {p['page']}. <a href="/30-years#p={p['page']}">See the page</a></p>
  </div>
</article>
<nav class="wrap cv-nav" aria-label="More dancers">
  <a href="/students/{prev['slug']}">{st_face(prev, 'face sm')}<span><small>Previous</small>{e(prev['display'])}</span></a>
  <a href="/accolades" class="cv-all">All dancers</a>
  <a href="/students/{nxt['slug']}" class="nx"><span><small>Next</small>{e(nxt['display'])}</span>{st_face(nxt, 'face sm')}</a>
</nav>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
''', extra_head=og)

# ---------------------------------------------------------------- 30 years: the souvenir as a flip book
SOUV_CHAPTERS = [(1, 'Cover'), (2, 'The dancer is the dance'), (3, 'Trust and faculty'), (5, "Founder's letter"), (7, 'The story'), (11, 'The founders'),
                 (14, 'Messages'), (39, 'Former faculty'), (41, 'Productions'), (50, 'Awards'), (55, 'Alumni'), (58, 'Nrithya Utsav'), (59, 'Kalarpanam')]
SOUV_MESSAGES = [(14, 'Smt. Nandini Ramani', 'Veteran Bharatanatyam exponent'), (15, 'Sri V. V. Sundaram', 'Message for the Silver Jubilee'),
                 (16, 'The Dhananjayans', 'Bharatakalanjali, Chennai'), (19, 'Dr. Ambika Kameshwar', 'Director-Trustee, RASA'),
                 (21, 'Smt. Hema Rajagopalan', 'Artistic Director, Natya Dance Theatre, Chicago'), (22, 'Smt. Vasanthalakshmi Narasimhachari', 'Director, Kalasamarpana Foundation'),
                 (24, 'Smt. Parvathi Ravi Ghantasala', 'Managing Trustee, Kala Pradarshini'), (25, 'Sri Srikanth Gopalakrishnan', 'Singer'),
                 (26, 'Dr. P. Ramaa', 'Singer'), (34, 'Nadanalaya', 'Melbourne, Australia')]

def flipbook():
    chips = ''.join(f'<button class="chip" type="button" data-goto="{n}">{e(t)} <small>p.{n}</small></button>' for n, t in SOUV_CHAPTERS)
    return f'''<section class="fb-sec" id="souvenir"><div class="wrap">
  <div class="fb-head">
    <div><h2>Souvenir 2026</h2><p class="muted">68 pages. Turn them like a book: tap the edges, swipe, or use the arrow keys.</p></div>
    <div class="fb-tools">
      <button class="fb-t" type="button" data-fb="text" aria-pressed="false">Read text</button>
      <button class="fb-t" type="button" data-fb="zoom">Zoom</button>
      <button class="fb-t" type="button" data-fb="full">Full screen</button>
      <button class="fb-t" type="button" data-fb="share">Copy link</button>
      <a class="fb-t" href="/assets/souvenir/Divyanjali-Souvenir-2026.pdf" download>Download PDF</a>
    </div>
  </div>
  <div class="fb" id="flip" data-pages="68" tabindex="0" aria-label="Souvenir 2026, a book you can page through">
    <div class="fb-stage">
      <button class="fb-edge fb-p" type="button" data-fb="prev" aria-label="Previous page">‹</button>
      <div class="fb-book" id="fbBook"></div>
      <button class="fb-edge fb-n" type="button" data-fb="next" aria-label="Next page">›</button>
    </div>
    <div class="fb-bar"><input type="range" id="fbRange" min="1" max="68" value="1" aria-label="Go to page"><span id="fbNum" aria-live="polite">Cover</span></div>
    <div class="fb-text" id="fbText" hidden></div>
  </div>
  <div class="chipbar fb-chap">{chips}</div>
  <div class="fb-thumbs" id="fbThumbs">{''.join(f'<button type="button" data-goto="{n}" aria-label="Page {n}"><img src="/assets/souvenir/t/{n:02d}.webp" alt="" loading="lazy" width="140" height="198"><span>{n}</span></button>' for n in range(1, 69))}</div>
</div></section>'''

def thirty():
    msgs = ''.join(f'<button class="msg-c reveal" type="button" data-goto="{n}" style="--i:{i % 5}"><b>{e(nm)}</b><small>{e(t)}</small><span>Read on page {n} ›</span></button>' for i, (n, nm, t) in enumerate(SOUV_MESSAGES))
    return page('/30-years', '30 Years of Divyanjali · Souvenir 2026', 'Thirty years of Divyanjali: read the Souvenir 2026 as a flip book, with messages from fellow artists, productions, awards and the story of the school.', f'''
<section class="ty-hero"><div class="wrap">
  <p class="kicker">1994 to 2024 · Souvenir 2026</p>
  <h1>Thirty years of a divine offering</h1>
  <p class="lead">A small class that grew into a trust, a flood that took everything, and the students who carried the school forward. Read the whole story in the souvenir below.</p>
</div></section>
{flipbook()}
<section class="alt" style="padding-block:40px"><div class="wrap">{stats([(1994, '', 'founded'), (71, '', 'arangetrams'), (300, '+', 'dancers trained'), (150, '+', 'books in the rebuilt library')])}</div></section>
<section id="messages"><div class="wrap">
  <div class="sec-head"><div><h2>Messages from fellow artists</h2></div></div>
  <div class="msgs">{msgs}</div>
  <p class="muted" style="margin-top:14px">More messages follow on pages 17 to 38 of the souvenir.</p>
</div></section>
<section class="alt" id="timeline"><div class="wrap">{head('Timeline', 'The years, one by one')}
  <ol class="tl">
    <li><b>1994</b><span>First classes in CIT Nagar, Chennai</span></li>
    <li><b>2004</b><span>Own workspace inaugurated by Smt. Chithra Visweswaran and Smt. Nandini Ramani</span></li>
    <li><b>2006</b><span>Syllabus published as <i>Essence and Essentials of Dance</i></span></li>
    <li><b>2011</b><span>Registered as a Trust · first government grant</span></li>
    <li><b>2012–23</b><span>Dated productions from Laya Thrayam to Sita Kalyanam · <a href="/choreographies">see Choreographies</a></span></li>
    <li><b>2015</b><span>50th arangetram · Andal Vaibhavam on 13 stages · Chennai floods</span></li>
    <li><b>2017</b><span>Kalarpanam platform launched for young artists</span></li>
    <li><b>2018</b><span>Sangeet International Festival with the All India Dancers Association</span></li>
    <li><b>2019</b><span>60th arangetram · Silver Jubilee · Nrithya Utsav, month on month until 2020</span></li>
    <li><b>2024</b><span>30 years · Souvenir 2026</span></li>
    <li><b>2026</b><span>Hanumath Margam premieres at the 50th Cleveland Thyagaraja Festival</span></li>
  </ol></div></section>
<section id="flood"><div class="wrap two">
  <div class="stack">{head('2015', 'The flood, and the way back')}<div class="prose"><p>In the 2015 Chennai floods the workspace stood under seven feet of water. Choreographies in digital format, library books and musical instruments, the school's treasures, were lost.</p>
  <p>Divyanjali did not lose hope. It came back with the help of many institutions and legends: Smt. Chithra Visweswaran through ABHAI, the Music Academy, Narada Gana Sabha, Sri Nellai Kannan, Sri C.V. Chandrasekar, the core members of Prayathnam, Smt. Vasanthalakshmi Narasimhachari and Sri Jaikishore Mosalikanti, and others who asked not to be named. Today the library holds over 150 books, contributed by Smt. Nandini Ramani.</p></div></div>
  <div class="tiles" data-gallery>{ph('flood-before.jpg', 'the workspace after the flood', '1200×900')}{ph('flood-after.jpg', 'the rebuilt library', '1200×900')}</div>
</div></section>
{faq_section([
    ('When did Divyanjali complete 30 years?', 'In 2024. The school was founded in 1994, and the 30-year Souvenir was released in 2026.'),
    ('Can I download the souvenir?', 'Yes. Use Download PDF above the book, or open any page and copy its link to share that page.'),
    ('What happened in the 2015 floods?', 'The workspace was under seven feet of water and the library, instruments and recordings were lost. Friends and institutions helped the school rebuild.'),
    ('How many arangetrams has Divyanjali conducted?', 'Seventy-one, including one abroad. The 50th was in 2015 and the 60th in 2019.'),
], alt=True)}
{cta('Be part of the next chapter', 'Join a class, or bring a production to your stage.', 'Join a class', '/learn')}
''')

def prod_key(p):
    return p['slug'] or re.sub('[^a-z]+', '-', p['title'].lower()).strip('-')

def choreographies():
    order = sorted([p for p in PRODUCTIONS if p['year']], key=lambda p: p['year'], reverse=True) + [p for p in PRODUCTIONS if not p['year']]
    data = [{'k': prod_key(p), 't': p['title'], 'y': p['year'], 'c': p['cats'], 'l': p['line'], 's': p.get('story', ''),
             'cr': p.get('credits', []), 'su': p.get('suits', ''), 'u': '/productions/' + p['slug'] if p['slug'] else ''} for p in order]
    def card(i, p):
        k = prod_key(p)
        SLOTS.append((PAGE[0], f'prod-{k}.jpg', 'poster · ' + p['title'], '1200×1500'))
        yr = '<small>' + p['year'] + '</small>' if p['year'] else ''
        return (f'<button type="button" class="pc reveal" data-i="{i}" style="--i:{i % 6}" aria-haspopup="dialog">'
                f'<span class="pc-art ph" data-src="/assets/img/prod-{k}.jpg" data-alt="{e(p["title"])}"><span class="pc-t">{e(p["title"])}</span></span>'
                f'<span class="pc-b">{yr}<b>{e(p["title"])}</b><span>{e(p["line"])}</span></span></button>')
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return page('/choreographies', 'Enchanting Choreographies · Divyanjali productions', 'Bharatanatyam productions by Dr. S. Divyasena from Tamil, Sanskrit and Telugu literature, presented across India and abroad.', f'''
{crumbs(('Choreographies', None))}
<section class="ch-intro"><div class="wrap">
  <h1>Enchanting Choreographies</h1>
  <p class="lead">Bharatanatyam productions conceived and choreographed by Dr. S. Divyasena, from Tamil, Sanskrit and Telugu literature, the epics and the great composers. Staged across India and abroad, from Chennai sabhas to the Cleveland Thyagaraja Festival. Tap a production to read its story.</p>
  <a class="btn" href="/book?type=Performance+booking">Plan a performance</a>
</div></section>
<section class="ch-list" id="all"><div class="wrap">
  <div class="pcs" id="prodGrid">{''.join(card(i, p) for i, p in enumerate(order))}</div>
</div></section>
<div class="sheet" id="sheet" hidden>
  <div class="sheet-bg" data-close></div>
  <div class="sheet-in" role="dialog" aria-modal="true" aria-label="Production">
    <div class="sheet-grab" aria-hidden="true"></div>
    <button type="button" class="sheet-x" data-close aria-label="Close">×</button>
    <div class="sheet-body" id="shBody"></div>
    <div class="sheet-nav"><button type="button" data-step="-1">‹ Previous</button><span id="shPos"></span><button type="button" data-step="1">Next ›</button></div>
  </div>
</div>
<script type="application/json" id="prodData">{blob}</script>
<section><div class="wrap">{head('On tour', 'Where we have danced')}
  <div class="mapgrid">
    <div><b>India</b><span class="muted">Chennai sabhas, Margazhi Season, New Delhi, 13 stages for Andal Vaibhavam</span></div>
    <div><b>USA</b><span class="muted">Cleveland Thyagaraja Festival · Nrithya Nataka Mala tour · Hanumath Margam premiere</span></div>
    <div><b>Thailand</b><span class="muted">Navarathri Festival, Bangkok</span></div>
    <div><b>Singapore</b><span class="muted">Navarathri Festival</span></div>
    <div><b>UK</b><span class="muted">Performances</span></div>
    <div><b>Australia</b><span class="muted">Performances</span></div>
    <div><b>Sri Lanka</b><span class="muted">Performances</span></div>
  </div></div></section>
<section class="alt"><div class="wrap">{head('Festivals we host', 'Platforms for dance')}
  <div class="tiles">
    <div class="tile"><span class="meta">Since 2017</span><h3>Kalarpanam</h3><p class="muted">A fine arts festival for young and upcoming talent, held at different venues across Chennai and its outskirts. Inaugurated by Smt. Nandini Ramani.</p></div>
    <div class="tile"><span class="meta">International</span><h3>Nritya Sangamam</h3><p class="muted">Solo Bharatanatyam and Kuchipudi by artists from Singapore, South Africa, the USA and Australia.</p></div>
    <div class="tile"><span class="meta">Talent search</span><h3>Nrithya Saavishkar</h3><p class="muted">A solo competition for ages 8 to 25, with cash prizes and a performance at a Chennai sabha for the winners.</p></div>
    <div class="tile"><span class="meta">Lecture demonstrations</span><h3>Natya Satsang</h3><p class="muted">Lectures, debates and quizzes with Ganamukundhapriya and Yathnam.</p></div>
    <div class="tile"><span class="meta">2019–20</span><h3>Nrithya Utsav</h3><p class="muted">Silver Jubilee festivals, lecture demonstrations and competitions, month on month.</p></div>
    <div class="tile"><span class="meta">Seminar</span><h3>Vachika Abhinaya</h3><p class="muted">A national seminar with Prayathnam, inaugurated by Padma Bhushan Dr. Padma Subrahmanyam.</p></div>
  </div></div></section>
<section><div class="wrap two">
  <div class="stack">{head('Creative endeavour', 'Beyond the stage')}<ul class="list"><li><b>Nrithyaharam</b>: an audio CD of the adavus of Bharatanatyam, for practice at home</li><li><b>Essence and Essentials of Dance</b>: the Divyanjali syllabus as a book (2006)</li><li>Lecture demonstrations, workshops and summer camps</li><li>Sangeet International Festival, 2018, with the All India Dancers Association</li></ul></div>
  <div class="stack">{head('On screen', 'Television and web')}<p>Jaya TV · Sun TV · Star Vijay · Makkal TV · Podhigai · Raj TV · Kavasam web TV · Rasa web channel</p><a class="btn-o" href="/gallery" style="align-self:flex-start">Watch videos</a></div>
</div></section>
{faq_section([
    ('Can we book a production for our festival?', 'Yes. Send the date, venue and audience through <a href="/book?type=Performance+booking">Book and Enquire</a>.'),
    ('Can a production be shorter?', 'Most productions can be adapted for a shorter slot. Tell us the time you have.'),
    ('Do you perform with live music?', 'Yes. Productions can be staged with a live orchestra or with recorded music.'),
    ('What themes do you cover?', 'Devotional themes, Tamil literature, the epics, rhythm, tributes to composers, dance dramas and full margams.'),
    ('Has Divyanjali performed abroad?', 'Yes: in the USA, Thailand, Singapore, the UK, Australia and Sri Lanka.'),
], alt=True)}
{cta('Bring a production to your stage', 'Festivals, temples, sabhas and cultural bodies, in India and abroad.', 'Plan a performance', '/book?type=Performance+booking')}
''')

PROD_PHOTOS = json.load(open(os.path.join(ROOT, 'prod_photos.json'), encoding='utf-8'))

def production(p):
    key = prod_key(p)
    photos = PROD_PHOTOS.get(key, [])
    live = [x for x in PRODUCTIONS if x['slug']]
    i = live.index(p)
    prev_p, next_p = live[i - 1], live[(i + 1) % len(live)]
    others = [x for x in live if x['slug'] != p['slug'] and set(x['cats']) & set(p['cats'])][:3] or [x for x in live if x['slug'] != p['slug']][:3]
    book_url = f"/book?type=Performance+booking&amp;production={e(p['title'])}"
    if photos:
        f, w, h = photos[0]
        hero = f'<img src="/assets/img/{f}" alt="{e(p["title"])} on stage" width="{w}" height="{h}" fetchpriority="high">'
    else:
        hero = ''
    gal = ''.join(f'<figure class="ph pg-i reveal" style="--i:{n % 6}"><img src="/assets/img/{f}" alt="{e(p["title"])}, photo {n + 1}" width="{w}" height="{h}" loading="lazy"></figure>' for n, (f, w, h) in enumerate(photos))
    video = yt(p['video'], p['title']) if p.get('video') else ''
    facts = [('Year', p['year'] or 'In the repertoire')] + list(p['credits']) + [('Suits', p['suits']), ('Music', 'Live orchestra or recorded')]
    ld = {'@context': 'https://schema.org', '@type': 'CreativeWork', 'name': p['title'], 'genre': 'Bharatanatyam dance production',
          'description': p['story'], 'creator': {'@type': 'Person', 'name': 'Dr. S. Divyasena'}, 'producer': {'@type': 'DanceGroup', 'name': 'Divyanjali'}}
    if p['year']: ld['dateCreated'] = p['year']
    if photos: ld['image'] = '/assets/img/' + photos[0][0]
    return page('/productions/' + p['slug'], f"{p['title']} · Bharatanatyam production by Divyanjali", (p['story'][:150] + '…'), f'''
{crumbs(('Choreographies', '/choreographies'), (p['title'], None))}
<header class="pr-hero{' has-img' if hero else ''}">
  {hero}
  <div class="wrap pr-hero-in">
    <div class="pr-tags">{''.join(f'<span>{e(c)}</span>' for c in p['cats'])}</div>
    <h1>{e(p['title'])}</h1>
    <p class="pr-line">{e(p['line'])}{' · ' + e(p['year']) if p['year'] else ''}</p>
    <div class="row"><a class="btn" href="{book_url}">Stage this production</a><button class="btn-o pr-share" type="button" data-share>Share</button><button class="btn-o pr-share" type="button" data-copy>Copy link</button></div>
  </div>
</header>

<section><div class="wrap bio-two">
  <div class="prose">
    <h2>The story</h2>
    <p class="pr-story">{e(p['story'])}</p>
    {f'<p class="muted">From the Souvenir 2026. <a href="/30-years">Read the souvenir</a></p>' if photos else ''}
  </div>
  <aside class="facts-card" aria-label="Production details">
    <h3>Details</h3>
    <dl>{''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in facts)}<dt>Duration</dt><dd>{todo('Add')}</dd></dl>
  </aside>
</div></section>

{f"""<section class="alt"><div class="wrap">{head('On stage', 'Photos')}<p class="muted bio-sub">Tap a photo to see it full size.</p>
  <div class="pg" data-gallery>{gal}</div></div></section>""" if photos else ''}
{f"""<section><div class="wrap">{head('Watch', 'On video')}<div class="vids">{video}</div></div></section>""" if video else ''}

<nav class="pr-nav wrap" aria-label="More productions">
  <a href="/productions/{prev_p['slug']}" class="pr-n prev"><small>‹ Previous</small><b>{e(prev_p['title'])}</b></a>
  <a href="/choreographies" class="pr-all">All productions</a>
  <a href="/productions/{next_p['slug']}" class="pr-n next"><small>Next ›</small><b>{e(next_p['title'])}</b></a>
</nav>
<section class="alt"><div class="wrap">{head('You may also like', 'Related productions')}
  <div class="tiles">{''.join(prod_card(x) for x in others)}</div></div></section>
{cta(f"Stage {e(p['title'])} at your festival", 'Tell us the date, venue and audience. We reply on WhatsApp within 24 hours.', 'Stage this production', book_url)}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
''', extra_head=(f'<meta property="og:image" content="/assets/img/{photos[0][0]}">\n' if photos else '') + f'<link rel="canonical" href="/productions/{p["slug"]}">\n')

PATH_STEPS = [
    ('Adavus', 'The basic steps and postures', 'Every dancer starts here: the adavus, the building blocks of Bharatanatyam, with the right posture, hands and footwork. The Nrithyaharam CD helps with practice at home.'),
    ('First items', 'Alarippu, jathiswaram', 'The first short dances. Students learn to join adavus into a piece, keep the tala and perform for an audience.'),
    ('Margam', 'Varnam, padams, thillana', 'The full concert repertoire, item by item, with the varnam at its heart.'),
    ('Abhinaya and laya', 'Expression and rhythm in depth', 'Storytelling through expression, and rhythm taught as its own subject by Sri B.P. Haribabu.'),
    ('Arangetram', 'The first full solo recital', 'When Dr. Divyasena decides a student is ready, the first full solo recital on stage. Divyanjali has conducted 71 arangetrams.'),
]

def learn():
    by = {p['slug']: p for p in STUDENTS}
    fac = [by[s] for s in FACULTY_SLUGS if s in by]
    teachers = ('<a class="fc reveal" href="/divyasena"><span class="face"><img src="/assets/img/divyasena-portrait.webp" alt="Dr. S. Divyasena" loading="lazy" width="360" height="360" style="object-position:32% 40%"></span><b>Dr. S. Divyasena</b><span>Founder and guru</span></a>'
                '<a class="fc reveal" href="/haribabu" style="--i:1"><span class="face"><img src="/assets/img/haribabu-portrait.webp" alt="Sri B.P. Haribabu" loading="lazy" width="360" height="360" style="object-position:50% 18%"></span><b>Sri B.P. Haribabu</b><span>Laya, rhythm</span></a>'
                + ''.join(f'<a class="fc reveal" href="/students/{p["slug"]}" style="--i:{i + 2}">{st_face(p)}<b>{e(p["display"])}</b><span>Faculty</span></a>' for i, p in enumerate(fac)))
    q = lambda name, label, opts: (f'<fieldset class="fd-q" data-q="{name}"><legend>{label}</legend><div class="fd-o">'
        + ''.join(f'<button type="button" data-v="{e(v)}" aria-pressed="false">{icon(ic)}<b>{e(t)}</b><small>{e(s)}</small></button>' for v, ic, t, s in opts) + '</div></fieldset>')
    return page('/learn', 'Learn Bharatanatyam in Chennai and online · Divyanjali',
        'Bharatanatyam classes for children, teens and adults in CIT Nagar, Chennai, and live online classes from Chennai for students abroad. Find your class in three taps.', f'''
{crumbs(('Learn', None))}
<section class="ln-hero"><div class="wrap ln-hero-in">
  <div class="ln-copy">
    <p class="eyebrow">Classes · Chennai and online</p>
    <h1>Learn Bharatanatyam</h1>
    <p class="lead">Classes for children, teens and adults in CIT Nagar, Chennai, and live online classes from Chennai for students abroad. Laya, abhinaya and theory come with every class.</p>
    <div class="row"><a class="btn" href="#finder">Find your class</a><a class="btn-o" data-wa="Hello Divyanjali, I would like to know about Bharatanatyam classes." href="#">WhatsApp us</a></div>
  </div>
  <figure class="ln-photo"><img src="/assets/img/dancers-group.webp" alt="Divyanjali students on stage" width="1161" height="541" fetchpriority="high"></figure>
</div></section>

<section class="alt" id="finder"><div class="wrap">
  {head('Find your class', 'Three taps to the right batch')}
  <div class="fd" data-finder>
    <ol class="fd-dots" aria-hidden="true"><li class="on"></li><li></li><li></li></ol>
    {q('who', '1. Who is learning?', [('Child', 'person-simple-tai-chi', 'A child', 'School age'), ('Teen', 'person-arms-spread', 'A teen', '13 to 19'), ('Adult', 'users-three', 'An adult', 'Beginners welcome')])}
    {q('where', '2. Where?', [('Chennai', 'hand-heart', 'In Chennai', 'At CIT Nagar'), ('Online', 'monitor-play', 'Online', 'Live from Chennai, abroad too')])}
    {q('level', '3. Any training so far?', [('Beginner', 'book-open-text', 'New to dance', 'Start with adavus'), ('Some training', 'metronome', 'Some training', 'Continue where you left off'), ('Arangetram preparation', 'certificate', 'Preparing for arangetram', 'With Dr. Divyasena')])}
    <div class="fd-res" hidden aria-live="polite">
      <p class="eyebrow">Your class</p>
      <h3 class="fd-t"></h3>
      <p class="fd-d"></p>
      <div class="row"><a class="btn fd-wa" href="#">Book a trial on WhatsApp</a><a class="btn-o fd-form" href="#enquire">Fill the form instead</a><button type="button" class="fd-again">Start again</button></div>
    </div>
  </div>
</div></section>

<section id="path"><div class="wrap">
  {head('The path', 'From first steps to arangetram')}
  <p class="muted bio-sub">Tap a step.</p>
  <div class="lp" data-steps>
    <ol class="lp-rail">{''.join(f'<li><button type="button" aria-expanded="{str(i == 0).lower()}" aria-controls="lp-{i}"><span class="lp-n">{i + 1}</span><b>{e(t)}</b><small>{e(s)}</small></button></li>' for i, (t, s, d) in enumerate(PATH_STEPS))}</ol>
    {''.join(f'<p class="lp-d" id="lp-{i}"{"" if i == 0 else " hidden"}>{e(d)}</p>' for i, (t, s, d) in enumerate(PATH_STEPS))}
  </div>
  <p class="muted" style="margin-top:12px">Names and durations of the levels: {todo('confirm with Dr. Divyasena')}</p>
</div></section>

<section class="alt"><div class="wrap">
  {head('Beyond steps', 'What makes a complete dancer')}
  <div class="teach">
    <a class="tc reveal" href="/haribabu#tala">{icon('metronome')}<h3>Laya</h3><p>Rhythm as its own subject, with Sri B.P. Haribabu. Try a tala on his page.</p></a>
    <div class="tc reveal" style="--i:1">{icon('book-open-text')}<h3>Theory</h3><p>From the school's own syllabus, <i>Essence and Essentials of Dance</i>.</p></div>
    <div class="tc reveal" style="--i:2">{icon('hand-heart')}<h3>Poorna Vidhya</h3><p>Thalam, ithihasam, puranas and moral values, alongside the dance.</p></div>
    <a class="tc reveal" href="/natya-iq" style="--i:3">{icon('monitor-play')}<h3>Practice at home</h3><p>Natya IQ games, and the Nrithyaharam adavu CD.</p></a>
  </div>
</div></section>

<section id="batches"><div class="wrap">{head('Batches', 'Days and timings')}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Batch</th><th>Days</th><th>Time</th><th>Where</th></tr></thead><tbody>
    <tr><td>Children</td><td>{todo('Days')}</td><td>{todo('Time')}</td><td>CIT Nagar</td></tr>
    <tr><td>Teens and adults</td><td>{todo('Days')}</td><td>{todo('Time')}</td><td>CIT Nagar</td></tr>
    <tr><td>Online</td><td>{todo('Days')}</td><td>{todo('Time, IST and local')}</td><td>Online</td></tr>
  </tbody></table></div></div></section>

<section class="alt"><div class="wrap">{head('Teachers', 'Who teaches you')}
  <div class="fac">{teachers}</div>
</div></section>

<section id="enquire"><div class="wrap two">
  <div class="stack"><p class="eyebrow">Enquiry</p><h2>Ask about a class</h2><p class="muted">We reply on WhatsApp within 24 hours.</p></div>
  <form class="f box" data-enquiry="Classes for a student" novalidate>
    <div class="fr"><label class="l">Student name<input name="name" required autocomplete="name"></label><label class="l">Age<input name="age" data-extra="Age" inputmode="numeric"></label></div>
    <label class="l">Parent's name, if under 18<input name="parent" data-extra="Parent"></label>
    <div class="fr"><label class="l">WhatsApp, with country code<input name="whatsapp" required inputmode="tel" placeholder="+91"></label><label class="l">Email (optional)<input name="email" type="email"></label></div>
    <div class="fr"><label class="l">Chennai or online<select name="where" data-extra="Where"><option>Chennai</option><option>Online</option></select></label>
    <label class="l">Level<select name="level" data-extra="Level"><option>Beginner</option><option>Some training</option><option>Advanced</option><option>Arangetram preparation</option></select></label></div>
    <label class="l">Message (optional)<textarea name="message"></textarea></label>
    <input class="hp" tabindex="-1" autocomplete="off" name="website" aria-hidden="true">
    <div class="row"><button class="btn" type="submit">Send enquiry</button></div><div class="msg" role="status"></div>
  </form></div></section>
{faq_section([
    ('What age can my child start?', f'From {todo("youngest age")}. We will suggest the right batch after a short chat.'),
    ('Am I too old to learn?', 'No. Adults and complete beginners are welcome in the teens and adults batch.'),
    ('How long until an arangetram?', 'It depends on the student. Most students take several years of regular classes; Dr. Divyasena decides when a student is ready.'),
    ('How do online classes work across time zones?', 'Live classes from Chennai, with batches set at times that suit students abroad.'),
    ('What do I need to buy?', 'Comfortable practice clothes to start. Dance sarees, salangai (ankle bells) and other items come later; we will guide you.'),
], alt=True)}
''', extra_head='<link rel="canonical" href="/learn">\n')

ENQ_TYPES = [
    ('Performance booking', 'music-notes', 'Book a performance', 'A production or recital for your stage'),
    ('Classes for a student', 'graduation-cap', 'Join a class', 'Chennai or online, any age'),
    ('Workshop or lecture demonstration', 'book-open-text', 'Workshop or lec-dem', 'With Dr. Divyasena or Sri Haribabu'),
    ('Collaboration', 'hand-heart', 'Collaborate', 'Festivals, artists and institutions'),
]

def book():
    perf_for = [('music-notes', 'Festivals and sabhas', 'Margazhi, Navaratri and music seasons'),
                ('hand-heart', 'Temples', 'Utsavams and special days'),
                ('airplane-tilt', 'Cultural bodies', 'In India and abroad: USA, Thailand, Singapore, UAE, UK, Australia, Sri Lanka'),
                ('users-three', 'Events and institutions', 'Schools, colleges and organisations')]
    return page('/book', 'Book and Enquire · Divyanjali',
        'Book a Divyanjali performance or production, ask about classes, invite a workshop or collaborate. We reply on WhatsApp within 24 hours.', f'''
{crumbs(('Book and Enquire', None))}
<section class="bk-hero"><div class="wrap">
  <p class="eyebrow">Book and Enquire</p>
  <h1>How can we help?</h1>
  <p class="lead">Pick one. The form below asks only what we need for it, and we reply on WhatsApp within 24 hours.</p>
  <div class="enq-types" role="radiogroup" aria-label="What is this about?">{''.join(f'<button type="button" role="radio" class="et" data-settype="{e(v)}" aria-pressed="{str(i == 0).lower()}" aria-checked="{str(i == 0).lower()}">{icon(ic)}<b>{e(t)}</b><small>{e(s)}</small></button>' for i, (v, ic, t, s) in enumerate(ENQ_TYPES))}</div>
</div></section>

<section class="alt" id="form"><div class="wrap enq-wrap">
  <form class="f box enq-f" data-enquiry="Performance booking" data-enq-form novalidate>
    <input type="hidden" name="enquiry_type" value="Performance booking">
    <h2 class="enq-h" aria-live="polite">Book a performance</h2>
    <div class="fr"><label class="l">Your name<input name="name" required autocomplete="name"></label><label class="l">WhatsApp, with country code<input name="whatsapp" required inputmode="tel" placeholder="+91" autocomplete="tel"></label></div>
    <label class="l">Email (optional)<input name="email" type="email" autocomplete="email"></label>

    <div class="enq-g" data-for="Performance booking|Workshop or lecture demonstration|Collaboration">
      <label class="l">Organisation (optional)<input name="organisation"></label>
    </div>
    <div class="enq-g" data-for="Performance booking|Workshop or lecture demonstration">
      <div class="fr"><label class="l">Date (optional)<input name="date_needed" type="date"></label><label class="l">City and venue<input name="venue" data-extra="City and venue"></label></div>
    </div>
    <div class="enq-g" data-for="Performance booking">
      <div class="fr"><label class="l">Occasion<select name="occasion" data-extra="Occasion"><option>Festival or sabha</option><option>Temple</option><option>Cultural body</option><option>Event or institution</option></select></label>
      <label class="l">Production, if known<select name="production" data-extra="Production"><option>Suggest one for us</option>{''.join(f'<option>{e(p["title"])}</option>' for p in PRODUCTIONS)}</select></label></div>
    </div>
    <div class="enq-g" data-for="Workshop or lecture demonstration">
      <label class="l">Topic or audience<input name="topic" data-extra="Topic" placeholder="For example: abhinaya for students, laya for dancers"></label>
    </div>
    <div class="enq-g" data-for="Classes for a student" hidden>
      <div class="fr"><label class="l">Student's age<input name="age" data-extra="Age" inputmode="numeric"></label><label class="l">Chennai or online<select name="where" data-extra="Where"><option>Chennai</option><option>Online</option></select></label></div>
      <label class="l">Training so far<select name="level" data-extra="Level"><option>Beginner</option><option>Some training</option><option>Advanced</option><option>Arangetram preparation</option></select></label>
    </div>
    <label class="l"><span class="enq-ml">Audience size and anything else</span><textarea name="message"></textarea></label>
    <input class="hp" tabindex="-1" autocomplete="off" name="website" aria-hidden="true">
    <div class="row"><button class="btn" type="submit">Send enquiry</button><a class="btn-o" data-wa="Hello Divyanjali" href="#">Or WhatsApp us</a></div><div class="msg" role="status"></div>
  </form>
  <aside class="enq-side">
    <h3>Other ways to reach us</h3>
    <a class="ct" data-wa="Hello Divyanjali" href="#">{icon('whatsapp-logo')}<span><small>WhatsApp</small><b>+91 90000 00000</b><em>{todo('real number')}</em></span></a>
    <div class="ct">{icon('phone')}<span><small>Call</small><b>{todo('Number')}</b></span></div>
    <div class="ct">{icon('envelope-simple')}<span><small>Email</small><b>{todo('Email')}</b></span></div>
    <a class="ct" href="https://maps.google.com/?q=CIT+Nagar+Chennai" target="_blank" rel="noopener">{icon('map-pin')}<span><small>Visit</small><b>CIT Nagar, Chennai</b><em>{todo('Full address')} · Open in Maps</em></span></a>
    <p class="muted">We usually reply on WhatsApp within 24 hours.</p>
  </aside>
</div></section>

<section><div class="wrap">{head('Who we perform for', 'Stages we bring dance to', '<a class="btn-o" href="/choreographies">See the productions</a>')}
  <div class="teach">{''.join(f'<div class="tc reveal" style="--i:{i}">{icon(ic)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (ic, t, d) in enumerate(perf_for))}</div>
</div></section>
{faq_section([
    ('How far ahead should we book?', 'As early as possible, especially for the Margazhi Season. Two to three months ahead is ideal for a production.'),
    ('Can a production be shorter?', 'Yes, most productions can be adapted to your time slot.'),
    ('Live or recorded music?', 'Both are possible. Live orchestra details are planned with you.'),
    ('Do you travel abroad?', 'Yes. Divyanjali has performed in the USA, Thailand, Singapore, the UAE, the UK, Australia and Sri Lanka.'),
    ('Can Sri Haribabu accompany our own performance?', 'Yes. Choose "Book a performance" and mention it in the message, or see <a href="/haribabu">his profile</a>.'),
], alt=True)}
''', extra_head='<link rel="canonical" href="/book">\n')

def gallery_items():
    titles = {prod_key(p): p['title'] for p in PRODUCTIONS}
    items = []
    for key, photos in PROD_PHOTOS.items():
        for n, (f, w, h) in enumerate(photos):
            items.append((key, titles.get(key, key), f, w, h, n))
    order = {prod_key(p): i for i, p in enumerate(PRODUCTIONS)}
    items.sort(key=lambda x: (x[5], order.get(x[0], 99)))
    return items

def gallery():
    items = gallery_items()
    with_photos = [p for p in PRODUCTIONS if prod_key(p) in PROD_PHOTOS]
    family = [('dancers-group.webp', 'Divyanjali dancers together', 1161, 541), ('founders-together.webp', 'Sri B.P. Haribabu and Dr. S. Divyasena', 1200, 993),
              ('divyasena-portrait.webp', 'Dr. S. Divyasena', 1053, 692)]
    tiles = ''.join(f'<figure class="ph pg-i" data-cat="{e(t)}"><img src="/assets/img/{f}" alt="{e(t)}" width="{w}" height="{h}" loading="lazy"><figcaption>{e(t)}</figcaption></figure>' for key, t, f, w, h, n in items)
    tiles += ''.join(f'<figure class="ph pg-i" data-cat="Divyanjali family"><img src="/assets/img/{f}" alt="{e(t)}" width="{w}" height="{h}" loading="lazy"><figcaption>{e(t)}</figcaption></figure>' for f, t, w, h in family)
    chips = ['All'] + [p['title'] for p in with_photos] + ['Divyanjali family']
    return page('/gallery', 'Gallery · Divyanjali Bharatanatyam productions in photos and video', f'Photos from {len(with_photos)} Divyanjali productions, from the Souvenir 2026, and videos of the dancers on stage.', f'''
{crumbs(('Gallery', None))}
<section class="gl-hero"><div class="wrap">
  <p class="eyebrow">Gallery</p>
  <h1>Thirty years on stage</h1>
  <p class="lead">{len(items)} stage photos from {len(with_photos)} productions, with videos below. Tap a photo to see it full size; use the arrows or swipe for the next.</p>
</div></section>
<section class="gl-sec"><div class="wrap">
  <div class="chipbar gl-chips" data-filter="#glGrid">{''.join(f'<button class="chip" type="button" data-f="{e(c)}" aria-pressed="{str(c == "All").lower()}">{e(c)}</button>' for c in chips)}</div>
  <div class="pg gl-grid" id="glGrid" data-gallery>{tiles}</div>
  <p class="muted" style="margin-top:14px">Photos from the Divyanjali Souvenir 2026. More photos from classes, arangetrams and the Dance Season are coming.</p>
</div></section>
<section class="alt"><div class="wrap">{head('Videos', 'Watch on stage', '<a class="btn-o" href="https://www.youtube.com/channel/UCLPvhdH5qXt0R4IyDt1eSHg" target="_blank" rel="noopener">YouTube channel</a>')}<div class="vids" id="ytList"></div></div></section>
<section><div class="wrap">{head('Instagram', 'Reels and posts', '<a class="btn-o" href="https://www.instagram.com/divyanjalidance/" target="_blank" rel="noopener">Follow on Instagram</a>')}<div class="tiles" id="igList"></div></div></section>
''', extra_head=f'<meta property="og:image" content="/assets/img/{items[0][2]}">\n<link rel="canonical" href="/gallery">\n' if items else '')

def media():
    facts = [('Name', 'Divyanjali School of Classical Dance'), ('Founded', '1994, Chennai, by Dr. S. Divyasena'), ('Status', 'Registered trust (2011)'),
             ('Art form', 'Bharatanatyam'), ('Founder', "Natyacharya Dr. S. Divyasena, Doordarshan 'A' grade artist, doctorate in Bharatanatyam"),
             ('Secretary', "Sri B.P. Haribabu, mridangam artist, 'Vaadhya Visharadha'"), ('Arangetrams', '71, including one abroad'),
             ('Performed in', 'India, USA, Thailand, Singapore, UAE, UK, Australia, Sri Lanka'), ('Recent', 'Hanumath Margam premiered at the 50th Cleveland Thyagaraja Festival, 2026'),
             ('Online', 'Instagram @divyanjalidance · YouTube: Divyanjali')]
    fact_text = '\n'.join(f'{k}: {v}' for k, v in facts)
    picks = [x for x in gallery_items() if x[5] == 0][:6]
    kit = [('book-open-text', 'Souvenir 2026', '30 years of Divyanjali, 68 pages, PDF', '/assets/souvenir/Divyanjali-Souvenir-2026.pdf', True),
           ('certificate', 'Dr. S. Divyasena biodata', 'Open her profile and tap Download biodata', '/divyasena', False),
           ('metronome', 'Sri B.P. Haribabu biodata', 'Open his profile and tap Download biodata', '/haribabu', False),
           ('hand-heart', 'Logo', 'Official Divyanjali logo', '/assets/logo-full.webp', True)]
    return page('/media', 'Media Room · Divyanjali press kit, facts and photos', 'Press kit for Divyanjali, Chennai: quick facts to copy, biodatas, the Souvenir 2026, logos, approved photos and media contact.', f'''
{crumbs(('Media Room', None))}
<section class="gl-hero"><div class="wrap">
  <p class="eyebrow">Press</p>
  <h1>Media Room</h1>
  <p class="lead">For journalists, presenters and festival curators: facts to copy, biodatas, photos and contacts in one place.</p>
</div></section>
<section class="alt"><div class="wrap bio-two">
  <div>
    <h2>Quick facts</h2>
    <p class="muted bio-sub">Copy them straight into a programme note or article.</p>
    <dl class="mf">{''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in facts)}</dl>
    <button class="btn" type="button" data-copy-text="{e(fact_text)}">Copy all facts</button>
  </div>
  <div>
    <h2>Press kit</h2>
    <div class="kit">{''.join(f'<a class="ct" href="{u}"{" download" if dl else ""}>{icon(ic)}<span><small>{"Download" if dl else "Open"}</small><b>{e(t)}</b><em>{e(d)}</em></span></a>' for ic, t, d, u, dl in kit)}</div>
  </div>
</div></section>
<section><div class="wrap">{head('Approved photos', 'For print and web', '<a class="btn-o" href="/gallery">All photos</a>')}
  <p class="muted bio-sub">Free to use with the credit "Divyanjali". Tap a photo to open it, or download it.</p>
  <div class="mp">{''.join(f'<figure class="mp-i"><img src="/assets/img/{f}" alt="{e(t)}" width="{w}" height="{h}" loading="lazy"><figcaption><b>{e(t)}</b><a href="/assets/img/{f}" download>Download</a></figcaption></figure>' for key, t, f, w, h, n in picks)}</div>
</div></section>
<section class="alt"><div class="wrap">{head('In the press', 'Coverage')}
  <ol class="tl"><li><b>The Hindu</b><span>Pannum Bharathamum · {todo('date and link')}</span></li><li><b>Mylapore Times</b><span>Divyanjali productions and events · <a href="https://www.mylaporetimes.com/tag/divyasena/" target="_blank" rel="noopener">Read</a></span></li><li><b>Narthaki</b><span>Reviews of Divyanjali performances · <a href="https://narthaki.com/info/rev08/rev596.html" target="_blank" rel="noopener">Read</a></span></li></ol></div></section>
<section><div class="wrap stack"><p class="eyebrow">Media contact</p><h2>{todo('Contact name')}</h2><p>{todo('Phone')} · {todo('Email')}</p><p class="muted">We answer media requests within one working day.</p><div class="row"><a class="btn-o" data-wa="Hello Divyanjali, I am writing from the press." href="#">WhatsApp us</a></div></div></section>
''', extra_head='<link rel="canonical" href="/media">\n')

def store():
    items = [('store-nrithyaharam.jpg', 'Nrithyaharam', 'Audio CD of the adavus of Bharatanatyam · Dr. S. Divyasena'), ('store-essence.jpg', 'Essence and Essentials of Dance', 'The Divyanjali syllabus as a book · Dr. S. Divyasena'), ('store-duta-mahima.jpg', 'Duta Mahima', 'Book · Dr. S. Divyasena')]
    return page('/store', 'Store · Divyanjali', 'Practice material and books from Divyanjali. Order on WhatsApp.', f'''
{crumbs(('Store', None))}
<section style="padding-top:28px"><div class="wrap stack"><p class="eyebrow">Store</p><h1>Store</h1><p class="lead">Practice material and books from Divyanjali. Order on WhatsApp: no payment gateway and no account needed.</p></div></section>
<section class="alt"><div class="wrap"><div class="tiles">{''.join(f'<div class="tile">{ph(f, "cover · " + t, "1000×1000", "sq")}<h3>{e(t)}</h3><p class="muted">{e(d)}</p><p><b>{todo("Price")}</b></p><a class="btn" data-wa="Hello Divyanjali, I would like to order: {e(t)}" href="#" style="align-self:flex-start">Order on WhatsApp</a></div>' for f, t, d in items)}</div>
<p class="muted" style="margin-top:16px">Delivery and pickup details: {todo('confirm')}</p></div></section>
''')

def natya_iq():
    src = open(os.path.join(ROOT, 'natya-iq-tool.html'), encoding='utf-8').read()
    css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    body = re.search(r'</style>\s*(.*?)<script>', src, re.S).group(1)
    js = re.search(r'<script>(.*?)</script>', src, re.S).group(1).replace('https://divyanjali.dance', 'https://divyanjalidance.com')
    body = body.replace('<footer>', '<p class="niq-note">').replace('</footer>', '</p>').replace('Prototype for divyanjali.dance · ', '')
    css = re.sub(r'@media \(prefers-color-scheme: dark\)\s*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', css)
    css = re.sub(r':root\[data-theme="dark"\]\s*\{[^}]*\}', '', css)
    def scope(block):
        out = []
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', block):
            sel, rules = m.group(1).strip(), m.group(2)
            if sel.startswith('@') or re.match(r'^(from|to|\d+%)', sel): out.append(f'{sel}{{{rules}}}'); continue
            sels = []
            for s in sel.split(','):
                s = s.strip()
                if s in (':root', 'body', '*'): sels.append('.niq' if s != '*' else '.niq *')
                elif s.startswith(':root'): sels.append('.niq' + s[5:])
                else: sels.append('.niq ' + s)
            out.append(', '.join(sels) + '{' + rules + '}')
        return '\n'.join(out)
    parts, i = [], 0
    for m in re.finditer(r'@(media|keyframes)[^{]*\{((?:[^{}]*\{[^{}]*\})*)[^{}]*\}', css):
        parts.append(scope(css[i:m.start()]))
        inner = m.group(2)
        parts.append(m.group(0).split('{', 1)[0] + '{' + (inner if m.group(1) == 'keyframes' else scope(inner)) + '}')
        i = m.end()
    parts.append(scope(css[i:]))
    brand = '.niq{--bg:#FAF6EF;--surface:#FFFFFF;--ink:#3D3532;--muted:#6B625D;--accent:#B23C00;--accent-ink:#FFFFFF;--gold:#9A6B1F;--line:#EAE4DA;--good:#346538;--bad:#9F2F2D;--tint:#FFF3EA;--display:"Cormorant Garamond",Georgia,serif;--body:"Montserrat","Segoe UI",system-ui,sans-serif;--mono:ui-monospace,Menlo,monospace}\n.niq section{padding-block:0}.niq-note{font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:14px}'
    style = '<style>' + '\n'.join(p for p in parts if p.strip()) + '\n' + brand + '</style>'
    return page('/natya-iq', 'Natya IQ · Bharatanatyam quiz, tala calculator, mudra match', 'Test what you know about Bharatanatyam, count a tala, and match mudras and rasas. Share your score card.',
        f'{crumbs(("Natya IQ", None))}<div class="niq">{body}</div>' + cta('Learn the real thing', 'Join a class in Chennai or online.', 'See classes', '/learn'),
        extra_head=style, scripts=f'<script>{js}</script>')

def simple(path, title, h1, text, buttons):
    return page(path, title, text, f'<section style="padding-block:clamp(64px,12vw,140px)"><div class="wrap stack" style="max-width:720px"><h1>{h1}</h1><p class="lead">{text}</p><div class="row">{buttons}</div></div></section>')

def privacy():
    return page('/privacy', 'Privacy · Divyanjali', 'How Divyanjali uses the details you send through this website.', f'''
<section><div class="wrap prose"><p class="eyebrow">Privacy</p><h1>Privacy</h1>
<p>This page explains what we collect through this website and how we use it. {todo('Have this reviewed before launch')}</p>
<h3>What we collect</h3><p>Only what you type into our forms: your name, WhatsApp number, email if you give it, and your message. Wishes and feedback on event pages also include your city and, if you choose, a rating.</p>
<h3>Where it is kept</h3><p>Form entries are saved in a private Google Sheet used only by the Divyanjali team. Wishes are shown on an event page only if you tick "show my message" and the team approves it.</p>
<h3>How we use it</h3><p>To reply to you, usually on WhatsApp, and to pass your wishes to the artist. We do not sell or share your details.</p>
<h3>Videos and posts</h3><p>YouTube and Instagram content loads only when you tap to play it; those services then apply their own privacy policies.</p>
<h3>Deleting your details</h3><p>Message us on <a data-wa="Hello Divyanjali, please delete my details." href="#">WhatsApp</a> and we will remove them.</p>
</div></section>''')

# ---------------------------------------------------------------- events app: shared header and footer
def patch_events_app():
    p = os.path.join(SITE, 'app.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<header class="top">.*?</header>', header('/events'), s, count=1, flags=re.S)
    s = re.sub(r'<footer>.*?</footer>', FOOTER, s, count=1, flags=re.S)
    if '/assets/site.css' not in s:
        s = s.replace('<style>', '<link rel="stylesheet" href="/assets/site.css">\n<style>', 1)
    open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- write everything
def write(name, fn, *args):
    PAGE[0] = '/' + name.replace('.html', '').replace('home', '')
    out = os.path.join(SITE, name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(fn(*args))

if __name__ == '__main__':
    write('home.html', home)
    write('about.html', about)
    write('divyasena.html', divyasena)
    write('haribabu.html', haribabu)
    write('30-years.html', thirty)
    write('accolades.html', accolades)
    for p in STUDENTS: write(f"students/{p['slug']}.html", student_page, p)
    write('choreographies.html', choreographies)
    for p in PRODUCTIONS:
        if p['slug']: write(f"productions/{p['slug']}.html", production, p)
    write('learn.html', learn)
    write('book.html', book)
    write('gallery.html', gallery)
    write('media.html', media)
    write('store.html', store)
    write('natya-iq.html', natya_iq)
    write('privacy.html', privacy)
    write('thank-you.html', simple, '/thank-you', 'Thank you · Divyanjali', 'Thank you. We have your message.', 'We reply on WhatsApp within 24 hours. For anything urgent, message us now.',
          '<a class="btn" data-wa="Hello Divyanjali" href="#">Message on WhatsApp</a><a class="btn-o" href="/">Back to home</a><a class="btn-o" href="/choreographies">See the productions</a>')
    write('404.html', simple, '/404', 'Page not found · Divyanjali', 'This page has stepped off the stage.', 'The link may be old. These are the pages people look for most.',
          '<a class="btn" href="/learn">Classes</a><a class="btn-o" href="/choreographies">Productions</a><a class="btn-o" href="/events">Events</a><a class="btn-o" href="/book">Book and Enquire</a>')
    patch_events_app()
    seen, rows = set(), []
    for pg, f, label, size in SLOTS:
        if f in seen: continue
        seen.add(f); rows.append(f'| `{f}` | {label} | {size} | {pg or "/"} |')
    open(os.path.join(SITE, 'IMAGE-SLOTS.md'), 'w').write(
        '# Image slots\n\nUpload each photo to `divyanjali-site/assets/img/` with exactly this file name (JPG, about the size shown, under 300 KB).\n'
        'It appears on the site at once. Slots without a photo show a labelled placeholder.\n\n'
        'Videos and Instagram posts for the Gallery: edit `divyanjali-site/assets/media.json`.\n\n'
        '| File name | What to show | Size (px) | Page |\n|---|---|---|---|\n' + '\n'.join(rows) + '\n')
    print(f'Built pages. {len(seen)} image slots.')
