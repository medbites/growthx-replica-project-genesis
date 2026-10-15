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

ICONS = {'person-arms-spread': '<path d="M104,40a24,24,0,1,1,24,24A24,24,0,0,1,104,40ZM212,80H44c-12.87,0-16.71,17.5-5,22.9L96,128,73.13,214.93a12,12,0,0,0,21.75,10.14L128,168l33.12,57.07a12,12,0,0,0,21.75-10.14L160,128l57-25.1C228.69,97.5,224.85,80,212,80Z" opacity="0.2"/><path d="M160,40a32,32,0,1,0-32,32A32,32,0,0,0,160,40ZM128,56a16,16,0,1,1,16-16A16,16,0,0,1,128,56ZM231.5,87.71A19.62,19.62,0,0,0,212,72H44a20,20,0,0,0-8.38,38.16l.13.06,50.75,22.35-21,79.72A20,20,0,0,0,102,228.82l26-44.88,26,44.88a20,20,0,0,0,36.4-16.53l-21-79.72,50.75-22.35.13-.06A19.63,19.63,0,0,0,231.5,87.71Zm-17.8,7.9-56.93,25.07a8,8,0,0,0-4.51,9.36L175.13,217a7,7,0,0,0,.49,1.35,4,4,0,1,1-7.25,3.38c-.11-.22-.22-.43-.34-.63L134.92,164a8,8,0,0,0-13.84,0L88,221.06c-.12.2-.23.41-.34.63a4,4,0,1,1-7.25-3.38,7,7,0,0,0,.49-1.35L103.74,130a8,8,0,0,0-4.51-9.36L42.3,95.61A4,4,0,0,1,44,88H212a4,4,0,0,1,1.73,7.61Z"/>', 'person-simple-tai-chi': '<path d="M152,48a24,24,0,1,1-24-24A24,24,0,0,1,152,48Z" opacity="0.2"/><path d="M128,80A32,32,0,1,0,96,48,32,32,0,0,0,128,80Zm0-48a16,16,0,1,1-16,16A16,16,0,0,1,128,32Zm96,72a8,8,0,0,1-8,8H136v26.72l51.15,21.93A8,8,0,0,1,192,168v48a8,8,0,0,1-16,0V173.28l-46.45-19.91L53.35,222a8,8,0,1,1-10.7-11.9L120,140.44V112H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,104Z"/>', 'monitor-play': '<path d="M208,48H48A16,16,0,0,0,32,64V176a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V64A16,16,0,0,0,208,48ZM112,152V88l48,32Z" opacity="0.2"/><path d="M208,40H48A24,24,0,0,0,24,64V176a24,24,0,0,0,24,24H208a24,24,0,0,0,24-24V64A24,24,0,0,0,208,40Zm8,136a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V64a8,8,0,0,1,8-8H208a8,8,0,0,1,8,8Zm-48,48a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h64A8,8,0,0,1,168,224Zm-3.56-110.66-48-32A8,8,0,0,0,104,88v64a8,8,0,0,0,12.44,6.66l48-32a8,8,0,0,0,0-13.32ZM120,137.05V103l25.58,17Z"/>'}

def icon(name):
    """Phosphor duotone icon (MIT), inlined so it needs no extra download."""
    return f'<svg class="ic" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">{ICONS[name]}</svg>'

# ---------------------------------------------------------------- layout
NAV = [('About', '/about'), ('30 Years', '/30-years'), ('Accolades', '/accolades'), ('Choreographies', '/choreographies'), ('Learn', '/learn'), ('Calendar', '/events')]
ABOUT = [('Dance school', '/about', 'Divyanjali since 1994'), ('Dr. S. Divyasena', '/divyasena', 'Founder and guru'), ('Sri B.P. Haribabu', '/haribabu', 'Mridangam and rhythm')]
MENU = [('Home', '/'), ('About', ABOUT), ('30 Years', '/30-years'),
        ("Student's Accolades", '/accolades'), ('Choreographies', '/choreographies'), ('Learn', '/learn'), ('Events calendar', '/events'),
        ('Gallery and Videos', '/gallery'), ('Natya IQ', '/natya-iq'), ('Media Room', '/media'), ('Store', '/store'), ('Book and Enquire', '/book')]

def header(path):
    cur = lambda h: ' aria-current="page"' if h == path or (h != '/' and path.startswith(h + '/')) or (h == '/accolades' and path.startswith('/students/')) else ''
    about_on = ' aria-current="page"' if path in [h for _, h, _ in ABOUT] else ''
    sub = ''.join(f'<a href="{h}"{cur(h)}><b>{t}</b><small>{d}</small></a>' for t, h, d in ABOUT)
    def nav_item(t, h):
        if h == '/about':
            return f'<div class="dd hide-m"><a class="dd-t" href="/about"{about_on} aria-haspopup="true">About<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></a><div class="dd-p">{sub}</div></div>'
        return f'<a class="{"navcal" if h == "/events" else "hide-m"}" href="{h}"{cur(h)}>{t}</a>'
    nav = ''.join(nav_item(t, h) for t, h in NAV)
    menu = ''.join(f'<p class="menu-g">{t}</p>' + ''.join(f'<a class="menu-sub" href="{h2}"{cur(h2)}>{t2}</a>' for t2, h2, _ in h) if isinstance(h, list) else f'<a href="{h}"{cur(h)}>{t}</a>' for t, h in MENU)
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

THIRTY = [('1994', 'Divyanjali begins', 'Dr. S. Divyasena starts teaching Bharatanatyam in CIT Nagar, Chennai.', '/30-years#p=7'),
          ('2004', 'A home of its own', 'The workspace is inaugurated by Smt. Chithra Visweswaran and Smt. Nandini Ramani.', '/30-years#p=7'),
          ('2006', 'The syllabus, in print', 'Essence and Essentials of Dance sets down what every age group learns.', '/30-years#p=7'),
          ('2011', 'A registered trust', 'Grants from the Government of India and Tamil Isai Sangam fund new productions.', '/30-years#p=7'),
          ('2015', 'The flood, and the comeback', 'Seven feet of water took the library and instruments. Friends helped rebuild, and Andal Vaibhavam played 13 stages that year.', '/30-years#p=8'),
          ('2017', 'Kalarpanam', 'A stage of its own for young and upcoming artists.', '/30-years#p=59'),
          ('2019', 'Silver Jubilee', 'Nrithya Utsav: festivals, lecture demonstrations and competitions from July 2019 to February 2020.', '/30-years#p=58'),
          ('2026', 'Hanumath Margam', 'World premiere at the 50th Cleveland Thyagaraja Festival, and the Souvenir 2026.', '/productions/hanumath-margam')]

def thirty_orbit():
    n = len(THIRTY)
    nodes = ''.join(f'<button type="button" class="orb-n" style="--a:{round(-90 + i * 360 / n)}deg" data-i="{i}" aria-label="{y}: {e(t)}"><span>{y}</span></button>' for i, (y, t, d, h) in enumerate(THIRTY))
    cards = ''.join(f'<div class="orb-card" data-i="{i}" hidden><small>{y}</small><b>{e(t)}</b><p>{e(d)}</p><a href="{h}">{"See the production" if h.startswith("/productions") else "Read it in the souvenir"} ›</a></div>' for i, (y, t, d, h) in enumerate(THIRTY))
    return f'''<section class="orb-sec" id="thirty"><div class="wrap orb-grid">
  <div class="orb-copy">
    <p class="kicker" style="color:#FFB585">1994 to 2024 and beyond</p>
    <h2>Thirty years of a divine offering</h2>
    <p class="muted">Tap a year around the logo to open that chapter. The full story is in the souvenir.</p>
    <div class="row"><a class="btn" href="/30-years">Open the souvenir</a><a class="btn-o" href="/accolades">Meet the dancers</a></div>
  </div>
  <div class="orb-side">
  <div class="orb" id="orb">
    <div class="orb-ring" aria-hidden="true"></div>
    <img class="orb-logo" src="/assets/logo-30-mark.png" alt="Divyanjali 30 years" width="640" height="640" loading="lazy">
    {nodes}
  </div>
  <div class="orb-pop" id="orbPop" aria-live="polite">{cards}<button type="button" class="orb-x" aria-label="Close">×</button></div>
  </div>
</div></section>
'''

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
{thirty_orbit()}
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

def about():
    return page('/about', 'About Divyanjali · Bharatanatyam since 1994', 'Founded in 1994 by Dr. S. Divyasena, Divyanjali teaches Bharatanatyam with theory, rhythm and expression.', f'''
{crumbs(('About', None))}
<section style="padding-top:28px"><div class="wrap hero2">
  <div class="stack"><p class="eyebrow">About</p><h1>About Divyanjali</h1><p class="lead">Founded in 1994 by Dr. S. Divyasena, Divyanjali teaches Bharatanatyam with theory, rhythm and expression, and treats every student as part of the family.</p><div class="row"><a class="btn" href="/learn">Join a class</a><a class="btn-o" href="/30-years">Our 30 years</a></div></div>
  {ph('about-hero.jpg', 'the school, a class in progress', '1600×1200')}
</div></section>
<section class="alt"><div class="wrap two">
  <div class="stack">{head('Our story', 'From one class to a trust')}
    <div class="prose"><p>Divyanjali Dance School was established in 1994 by Dr. S. Divyasena and has since trained dancers of remarkable talent, earning a place among the leading schools for Bharatanatyam in Chennai. The school opened its own workspace in 2004 in the presence of Smt. Chithra Visweswaran and Smt. Nandini Ramani.</p>
    <p>Its syllabus, drafted by Dr. Divyasena for students of every age, covers both theory and practice and was published in 2006 as the book <i>Essence and Essentials of Dance</i>. Students also receive special training in laya, the rhythm of dance, from Sri B.P. Haribabu, and learn abhinaya, expression, through creative, engaging teaching.</p>
    <p>Divyanjali was registered as a Trust in 2011 and received grants from the Government of India and the Iyal Isai Nataka Mandram, which made productions like <i>Nava Vidha Sambandham</i> and <i>Andal Vaibhavam</i> possible.</p></div></div>
  <ol class="tl">
    <li><b>1994</b><span>School founded in CIT Nagar, Chennai</span></li>
    <li><b>2004</b><span>Own workspace inaugurated</span></li>
    <li><b>2006</b><span>Syllabus published: <i>Essence and Essentials of Dance</i></span></li>
    <li><b>2011</b><span>Registered as a Trust</span></li>
    <li><b>2015</b><span>Chennai floods, and the way back</span></li>
    <li><b>2019</b><span>Silver Jubilee · Nrithya Utsav</span></li>
    <li><b>2024</b><span>30 years</span></li>
  </ol>
</div></section>
<section><div class="wrap">{head('What we teach', 'Four parts of one art')}
  <div class="tiles">
    <div class="tile">{ph('teach-technique.jpg', 'adavu practice', '1200×900')}<h3>Bharatanatyam</h3><p class="muted">Adavus, items and the full margam, step by step to arangetram.</p></div>
    <div class="tile">{ph('teach-laya.jpg', 'laya class with mridangam', '1200×900')}<h3>Laya, rhythm</h3><p class="muted">Tala and rhythm taught as a subject of its own by Sri B.P. Haribabu.</p></div>
    <div class="tile">{ph('teach-abhinaya.jpg', 'abhinaya, expression', '1200×900')}<h3>Abhinaya</h3><p class="muted">Expression and storytelling, taught creatively for every age.</p></div>
    <div class="tile">{ph('teach-theory.jpg', 'theory class', '1200×900')}<h3>Theory</h3><p class="muted">Natya Shastra, mudras and rasas, from our own published syllabus.</p></div>
  </div></div></section>
<section class="alt"><div class="wrap">{head('The founders', 'Two artists, one school')}
  <div class="tiles">
    <a class="tile" href="/divyasena">{ph('founder-divyasena.jpg', 'Dr. S. Divyasena', '1200×1500', 'tall')}<span class="meta">Founder and Managing Trustee</span><h3>Dr. S. Divyasena</h3><p class="muted">Dancer, choreographer, nattuvanar</p></a>
    <a class="tile" href="/haribabu">{ph('founder-haribabu.jpg', 'Sri B.P. Haribabu', '1200×1500', 'tall')}<span class="meta">Secretary and Trustee</span><h3>Sri B.P. Haribabu</h3><p class="muted">Mridangam, nattuvangam, rhythm</p></a>
  </div></div></section>
<section><div class="wrap">{head('Faculty', 'Our teachers')}
  <div class="people">
    {''.join(f'<div>{ph(f, n, "800×1000", "tall")}<b>{n}</b><span class="muted">{r}</span></div>' for f, n, r in [('faculty-aiswarya.jpg', 'Aiswarya Ramanan', 'Faculty and Admin'), ('faculty-mahati.jpg', 'S. Mahati', 'Faculty and Admin'), ('faculty-harini.jpg', 'Harini N.', 'Faculty'), ('faculty-upanisha.jpg', 'Upanisha K.', 'Faculty')])}
  </div>
  <p class="muted" style="margin-top:20px">Former faculty: Akshaya S., Mohanambal P., S. Sivagami, Shyamala Aadith, Archana Kanthan, Preeti P., Shantha, Swarna Varsha Gurumoorthy, Krithika S., Roopa S., Sharmili N., Vinaya Skandaprasad.</p>
</div></section>
{faq_section([
    ('When was Divyanjali founded?', 'In 1994, by Dr. S. Divyasena, in CIT Nagar, Chennai.'),
    ('Is Divyanjali a registered trust?', 'Yes. Divyanjali was registered as a Trust in 2011.'),
    ('Who teaches the classes?', 'Dr. S. Divyasena leads the teaching, with Sri B.P. Haribabu for laya and the Divyanjali faculty listed above.'),
], alt=True)}
{cta('Come and watch a class', 'See how we teach before you join.', 'Ask about classes', '/learn#enquire', 'Hello Divyanjali, can I come and watch a class?')}
''')

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
    tabs = [('profile', 'Profile'), ('lineage', 'Gurus'), ('education', 'Education'), ('work', 'Work'), ('stage', 'On stage'), ('media', 'Media'), ('words', 'In her words'), ('peers', 'Peers')]
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
  <h3 class="bio-h3">Publications and resources</h3>
  <div class="edu">{''.join(f'<div class="edu-c reveal"><small>{e(k)}</small><b>{e(t)}</b><span>{e(d)}</span></div>' for k, t, d in works)}</div>
</div></section>

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

def haribabu():
    return page('/haribabu', 'Sri B.P. Haribabu · Mridangam and rhythm, Divyanjali', 'Sri B.P. Haribabu: mridangam artist, nattuvanar and rhythm composer, Vaadhya Visharadha, over 85 tours abroad.', f'''
{crumbs(('About', '/about'), ('Sri B.P. Haribabu', None))}
<section style="padding-top:28px"><div class="wrap hero2">
  <div class="stack"><p class="eyebrow">Secretary · Trustee</p><h1>Sri B.P. Haribabu</h1><p class="lead">Mridangam artist, nattuvanar and rhythm composer who built Divyanjali with Dr. S. Divyasena. He teaches laya as a subject of its own.</p>
  <div class="row"><a class="btn" href="/book?type=Performance+booking">Book him to accompany</a><a class="btn-o" href="/learn">Learn laya</a></div></div>
  {ph('haribabu-portrait.jpg', 'Sri B.P. Haribabu with mridangam', '1200×1500', 'tall')}
</div></section>
<section class="alt" style="padding-block:40px"><div class="wrap">{stats([(25, '+', 'years accompanying dance'), (85, '+', 'tours abroad since 1993'), (20, '', 'countries')])}</div></section>
<section><div class="wrap two">
  <div class="stack">{head('Training', 'Gurus and title')}<div class="prose"><p>A versatile mridangam exponent, Sri B.P. Haribabu trained under the exemplary gurus 'Kalaimamani' Sri V.P. Ramadoss and 'Kalaimamani' Sri Thiruvaroor Bhakthavatchalam at the Tamil Nadu Government Music College. He was conferred the title 'Vaadhya Visharadha' for his mastery of the art.</p>
  <p>Besides the mridangam, he is equally proficient in pakhawaj, nattuvangam and rhythm composition. A specialist in playing for dance concerts, he has accompanied artists for over 25 years and has worked with major dance companies in the USA.</p></div></div>
  {yt(HOME_VIDEO, 'Rhythm on stage')}
</div></section>
<section class="alt"><div class="wrap">{head('Rhythm work', 'Compositions and productions')}
  <div class="tiles">
    <a class="tile" href="/productions/laya-thrayam"><span class="meta">Production · 2012</span><h3>Laya Thrayam</h3><p class="muted">Tala and swara segment with Sri Srikanth Gopalakrishnan</p></a>
    <div class="tile"><span class="meta">Teaching</span><h3>Laya for dancers</h3><p class="muted">Rhythm taught as its own subject to every Divyanjali student</p></div>
    <div class="tile"><span class="meta">Accompaniment</span><h3>Mridangam and nattuvangam</h3><p class="muted">For solo recitals, arangetrams and productions</p></div>
  </div></div></section>
{faq_section([
    ('Can Sri Haribabu accompany our performance?', 'Yes. Send the date and venue through <a href="/book">Book and Enquire</a>.'),
    ('Does he teach rhythm to dancers?', 'Yes. Laya, rhythm, is taught as a subject of its own at Divyanjali.'),
    ('What is nattuvangam?', 'Nattuvangam is the art of conducting a Bharatanatyam performance with cymbals, reciting the rhythmic syllables that the dancer follows.'),
])}
{cta('Book Sri Haribabu', 'Mridangam and nattuvangam for performances and arangetrams.', 'Send an enquiry', '/book?type=Performance+booking')}
''')

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
    return (f'<a class="stc reveal" href="/students/{p["slug"]}" data-cat="{"|".join(tags)}" data-name="{e(p["display"].lower())}" style="--i:{i % 6}">'
            f'{st_face(p)}<b>{e(p["display"])}</b><small>{e(tags[0] if tags[0] != "Students" else "Student")}</small>'
            f'<span class="stc-one">{e(p["items"][0][:90])}{"…" if len(p["items"][0]) > 90 else ""}</span></a>')

def accolades():
    chips = ['All', 'Faculty', 'Students', 'Alumni', 'Doordarshan graded', 'Scholarship', 'Performed abroad', 'Runs a school']
    return page('/accolades', "Student's Accolades · Divyanjali", 'Faculty, students and alumni of Divyanjali: Doordarshan graded artists, scholarship holders, prize winners and teachers. Each dancer has a page of their own.', f'''
<section class="acc-hero"><div class="wrap">
  <h1>Student's Accolades</h1>
  <p class="lead">The faculty, students and alumni of Divyanjali, with every award listed in the Souvenir 2026. Tap a dancer to open their page, share it, or save it as a one-page résumé.</p>
  <div class="acc-groups"><a href="#studentGrid" data-jump="Faculty">Faculty</a><a href="#studentGrid" data-jump="Students">Students</a><a href="#studentGrid" data-jump="Alumni">Alumni</a></div>
</div></section>
<section class="alt acc-list"><div class="wrap">
  <div class="acc-tools">
    <div class="chipbar" data-filter="#studentGrid" data-count="#accCount">{''.join(f'<button class="chip" type="button" data-f="{f}" aria-pressed="{str(f == "All").lower()}">{f}</button>' for f in chips)}</div>
    <label class="acc-search"><span class="sr">Find a dancer</span><input type="search" id="accSearch" placeholder="Find a dancer by name" autocomplete="off"></label>
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
<section><div class="wrap">
  <div class="sec-head"><div><h2>Messages from fellow artists</h2></div></div>
  <div class="msgs">{msgs}</div>
  <p class="muted" style="margin-top:14px">More messages follow on pages 17 to 38 of the souvenir.</p>
</div></section>
<section class="alt"><div class="wrap">{head('Timeline', 'The years, one by one')}
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
<section><div class="wrap two">
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

def choreographies():
    dated = sorted([p for p in PRODUCTIONS if p['year']], key=lambda p: p['year'])
    years = {}
    for p in dated: years.setdefault(p['year'], []).append(p)
    def yearcard(y):
        items = ''.join(f'<p><b>{e(p["title"])}</b> · {e(p["line"])}</p>' for p in years[y])
        if y == '2015': items += '<p><b>Chennai floods</b> · the studio under seven feet of water</p>'
        return e(f'<span class="meta">{y}</span>{items}')
    track = ''.join(f'<button type="button" data-y="{y}" data-html="{yearcard(y)}" aria-pressed="{str(y == "2015").lower()}">{y}</button>' for y in years)
    first = html.unescape(yearcard('2015'))
    return page('/choreographies', 'Enchanting Choreographies · Divyanjali productions', 'Bharatanatyam productions by Dr. S. Divyasena from Tamil, Sanskrit and Telugu literature, presented across India and abroad.', f'''
{crumbs(('Choreographies', None))}
<section style="padding-top:28px"><div class="wrap hero2">
  <div class="stack"><p class="eyebrow">Productions</p><h1>Enchanting Choreographies</h1><p class="lead">Bharatanatyam productions from Tamil, Sanskrit and Telugu literature, presented across India and abroad.</p><div class="row"><a class="btn" href="/book?type=Performance+booking">Plan a performance</a><a class="btn-o" href="#all">Browse all</a></div></div>
  {yt('https://www.youtube.com/watch?v=So5SO_M4zZ8', 'Showreel · Dasavatharam')}
</div></section>
<section class="alt" style="padding-block:40px"><div class="wrap">{stats([(len(PRODUCTIONS), '', 'productions'), (len(dated), '', 'dated, 2012–2026'), (13, '', 'stages, Andal Vaibhavam'), (2, '', 'government grants'), (7, '', 'countries')])}</div></section>
<section><div class="wrap">{head('Year track', 'The journey, year by year')}
  <div class="track" data-track="#trackCard">{track}</div>
  <div class="trackcard" id="trackCard">{first}</div></div></section>
<section class="alt" id="all"><div class="wrap">{head('All productions', 'Choose a theme', '<span class="muted" id="prodCount">Showing ' + str(len(PRODUCTIONS)) + '</span>')}
  <div class="chipbar" data-filter="#prodGrid" data-count="#prodCount" style="margin-bottom:20px">{''.join(f'<button class="chip" type="button" data-f="{f}" aria-pressed="{str(f == "All").lower()}">{f}</button>' for f in ['All'] + THEMES)}</div>
  <div class="tiles" id="prodGrid">{''.join(prod_card(p) for p in PRODUCTIONS)}</div></div></section>
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

def production(p):
    others = [x for x in PRODUCTIONS if x['slug'] and x['slug'] != p['slug']][:3]
    credits = ''.join(f'<div><span>{e(k)}</span><b>{e(v)}</b></div>' for k, v in p['credits'])
    video = yt(p['video'], p['title']) if p.get('video') else f'<a class="ig" href="https://www.youtube.com/channel/UCLPvhdH5qXt0R4IyDt1eSHg" target="_blank" rel="noopener" style="aspect-ratio:16/9"><b>Video coming soon · our YouTube channel ›</b></a>'
    return page('/productions/' + p['slug'], f"{p['title']} · Divyanjali production", (p['story'][:150] + '…'), f'''
{crumbs(('Choreographies', '/choreographies'), (p['title'], None))}
<div class="prod-hero" style="margin-top:12px">{ph(f"prod-{p['slug']}.jpg", 'poster or stage still · ' + p['title'], '2100×900')}</div>
<section class="band" style="padding:0"><div class="wrap"><div class="stack" style="gap:8px"><div class="row" style="gap:6px">{''.join(f'<span class="badge tag">{e(c)}</span>' for c in p['cats'])}</div><h1>{e(p['title'])}</h1><p>{e(p['line'])}</p></div>
  <div class="row"><a class="btn" href="/book?type=Performance+booking&amp;production={e(p['title'])}">Plan this production</a></div></div></section>
<section><div class="wrap two">
  <div class="stack">{head('The story', 'What the audience sees')}<p style="font-size:1.08rem">{e(p['story'])}</p></div>
  <div class="facts"><div><span>Year</span><b>{e(p['year'] or 'Repertoire')}</b></div>{credits}<div><span>Music</span><b>Live or recorded</b></div><div><span>Suits</span><b>{e(p['suits'])}</b></div><div><span>Duration</span><b>{todo('Add')}</b></div></div>
</div></section>
<section class="alt"><div class="wrap">{head('Watch', 'On stage')}
  <div class="vids">{video}</div>
  <div class="tiles" data-gallery style="margin-top:20px">{''.join(ph(f"prod-{p['slug']}-{i}.jpg", f"{p['title']} still {i}", '1200×900') for i in range(1, 5))}</div></div></section>
<section><div class="wrap">{head('More productions', 'Keep exploring', '<a class="btn-o" href="/choreographies#all">All productions</a>')}
  <div class="tiles">{''.join(prod_card(x) for x in others)}</div></div></section>
{cta(f"Stage {e(p['title'])} at your festival", 'Tell us the date, venue and audience. We reply on WhatsApp within 24 hours.', 'Plan this production', f"/book?type=Performance+booking&amp;production={e(p['title'])}")}
''')

def learn():
    return page('/learn', 'Learn Bharatanatyam in Chennai and online · Divyanjali', 'Bharatanatyam classes for children, teens and adults in CIT Nagar, Chennai, and live online classes from Chennai for students abroad.', f'''
{crumbs(('Learn', None))}
<section style="padding-top:28px"><div class="wrap hero2">
  <div class="stack"><p class="eyebrow">Classes</p><h1>Learn Bharatanatyam in Chennai and online</h1><p class="lead">Classes for children, teens and adults in CIT Nagar, and live online classes from Chennai for students abroad.</p><div class="row"><a class="btn" href="#enquire">Ask about classes</a><a class="btn-o" data-wa="Hello Divyanjali, I would like to know about Bharatanatyam classes." href="#">WhatsApp us</a></div></div>
  {ph('learn-hero.jpg', 'a class in progress', '1600×1200')}
</div></section>
<section class="alt" id="paths"><div class="wrap">{head('Choose your path', 'Classes for every age')}
  <div class="tiles">
    <div class="tile">{ph('learn-children.jpg', "children's batch", '1200×900')}<h3>Children</h3><p class="muted">From {todo('youngest age')} · CIT Nagar</p></div>
    <div class="tile">{ph('learn-adults.jpg', 'teens and adults batch', '1200×900')}<h3>Teens and adults</h3><p class="muted">Beginners and returning dancers</p></div>
    <div class="tile">{ph('learn-online.jpg', 'online class on a laptop', '1200×900')}<h3>Online, from abroad</h3><p class="muted">Live from Chennai, in your time zone</p></div>
  </div></div></section>
<section><div class="wrap">{head('The path', 'From first steps to arangetram')}
  <ol class="steps5"><li><b>Adavus</b><span class="muted">The basic steps and postures</span></li><li><b>First items</b><span class="muted">Alarippu, jathiswaram</span></li><li><b>Margam</b><span class="muted">Varnam, padams, thillana</span></li><li><b>Abhinaya and laya</b><span class="muted">Expression and rhythm in depth</span></li><li><b>Arangetram</b><span class="muted">The first full solo recital</span></li></ol>
  <p class="muted" style="margin-top:12px">Names and durations of the levels: {todo('confirm with Dr. Divyasena')}</p></div></section>
<section class="alt"><div class="wrap">{head('Beyond steps', 'What makes a complete dancer')}
  <div class="tiles">
    <a class="tile" href="/haribabu"><h3>Laya with Sri B.P. Haribabu</h3><p class="muted">Rhythm as its own subject</p></a>
    <div class="tile"><h3>Theory</h3><p class="muted">Natya Shastra, mudras and rasas, from our published syllabus</p></div>
    <a class="tile" href="/natya-iq"><h3>Practice at home</h3><p class="muted">Natya IQ games and the Nrithyaharam adavu CD</p></a>
  </div></div></section>
<section><div class="wrap">{head('Batches', 'Days and timings')}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Batch</th><th>Days</th><th>Time</th><th>Where</th></tr></thead><tbody>
    <tr><td>Children</td><td>{todo('Days')}</td><td>{todo('Time')}</td><td>CIT Nagar</td></tr>
    <tr><td>Teens and adults</td><td>{todo('Days')}</td><td>{todo('Time')}</td><td>CIT Nagar</td></tr>
    <tr><td>Online</td><td>{todo('Days')}</td><td>{todo('Time, IST and local')}</td><td>Online</td></tr>
  </tbody></table></div></div></section>
<section class="alt"><div class="wrap">{head('Teachers', 'Faculty')}
  <div class="people">{''.join(f'<div>{ph(f, n, "800×1000", "tall")}<b>{n}</b></div>' for f, n in [('founder-divyasena.jpg', 'Dr. S. Divyasena'), ('founder-haribabu.jpg', 'Sri B.P. Haribabu'), ('faculty-aiswarya.jpg', 'Aiswarya Ramanan'), ('faculty-mahati.jpg', 'S. Mahati')])}</div></div></section>
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
''')

def book():
    return page('/book', 'Book and Enquire · Divyanjali', 'Book a Divyanjali performance or production, ask about classes, or collaborate. We reply on WhatsApp within 24 hours.', f'''
{crumbs(('Book and Enquire', None))}
<section style="padding-top:28px"><div class="wrap stack"><p class="eyebrow">Book and Enquire</p><h1>Book a performance or ask about classes</h1><p class="lead">One page for every enquiry. We reply on WhatsApp within 24 hours.</p>
  <div class="chipbar"><button class="chip" type="button" data-settype="Performance booking" aria-pressed="true">Book a performance</button><button class="chip" type="button" data-settype="Classes for a student" aria-pressed="false">Ask about classes</button><button class="chip" type="button" data-settype="Workshop or lecture demonstration" aria-pressed="false">Workshop</button><button class="chip" type="button" data-settype="Collaboration" aria-pressed="false">Collaborate</button></div></div></section>
<section class="alt"><div class="wrap">{head('Who we perform for', 'Stages we bring dance to', '<a class="btn-o" href="/choreographies">See the productions</a>')}
  <div class="tiles">
    <div class="tile">{ph('book-festival.jpg', 'festival stage', '1200×900')}<h3>Festivals and sabhas</h3><p class="muted">Margazhi, Navaratri, music seasons</p></div>
    <div class="tile">{ph('book-temple.jpg', 'temple performance', '1200×900')}<h3>Temples</h3><p class="muted">Utsavams and special days</p></div>
    <div class="tile">{ph('book-cultural.jpg', 'cultural body event', '1200×900')}<h3>Cultural bodies</h3><p class="muted">In India and abroad</p></div>
    <div class="tile">{ph('book-events.jpg', 'school or corporate event', '1200×900')}<h3>Events and institutions</h3><p class="muted">Schools, colleges, corporate events {todo('confirm')}</p></div>
  </div></div></section>
<section><div class="wrap two">
  <div class="stack"><p class="eyebrow">Enquiry</p><h2>Tell us about the occasion</h2><p class="muted">Date, venue, audience and theme help us suggest the right production.</p></div>
  <form class="f box" data-enquiry="Performance booking" novalidate>
    <label class="l">I'm asking about<select name="enquiry_type"><option>Performance booking</option><option>Workshop or lecture demonstration</option><option>Classes for a student</option><option>Collaboration</option><option>Something else</option></select></label>
    <div class="fr"><label class="l">Your name<input name="name" required autocomplete="name"></label><label class="l">Organisation (optional)<input name="organisation"></label></div>
    <div class="fr"><label class="l">WhatsApp, with country code<input name="whatsapp" required inputmode="tel" placeholder="+91"></label><label class="l">Email (optional)<input name="email" type="email"></label></div>
    <div class="fr"><label class="l">Event date (optional)<input name="date_needed" type="date"></label><label class="l">City and venue<input name="venue" data-extra="City and venue"></label></div>
    <div class="fr"><label class="l">Occasion<select name="occasion" data-extra="Occasion"><option>Festival or sabha</option><option>Temple</option><option>Cultural body</option><option>Event</option><option>Workshop</option></select></label>
    <label class="l">Production, if known<select name="production" data-extra="Production"><option>Suggest one for us</option>{''.join(f'<option>{e(p["title"])}</option>' for p in PRODUCTIONS)}</select></label></div>
    <label class="l">Audience size and anything else<textarea name="message"></textarea></label>
    <input class="hp" tabindex="-1" autocomplete="off" name="website" aria-hidden="true">
    <div class="row"><button class="btn" type="submit">Send enquiry</button></div><div class="msg" role="status"></div>
  </form></div></section>
<section class="alt"><div class="wrap">{head('Contact', 'Other ways to reach us')}
  <div class="tiles">
    <a class="tile" data-wa="Hello Divyanjali" href="#"><span class="meta">WhatsApp</span><h3>+91 90000 00000</h3><p class="muted">{todo('real number')}</p></a>
    <div class="tile"><span class="meta">Call</span><h3>{todo('Number')}</h3></div>
    <div class="tile"><span class="meta">Email</span><h3>{todo('Email')}</h3></div>
    <a class="tile" href="https://maps.google.com/?q=CIT+Nagar+Chennai" target="_blank" rel="noopener"><span class="meta">Visit</span><h3>CIT Nagar, Chennai</h3><p class="muted">{todo('Full address')} · Open in Google Maps</p></a>
  </div></div></section>
{faq_section([
    ('How far ahead should we book?', 'As early as possible, especially for the Margazhi Season. Two to three months ahead is ideal for a production.'),
    ('Can a production be shorter?', 'Yes, most productions can be adapted to your time slot.'),
    ('Live or recorded music?', 'Both are possible. Live orchestra details are planned with you.'),
    ('Do you travel abroad?', 'Yes. Divyanjali has performed in the USA, Thailand, Singapore, the UK, Australia and Sri Lanka.'),
])}
''')

def gallery():
    photos = [('Productions', 'Productions'), ('Classes', 'Classes'), ('Arangetrams', 'Arangetrams'), ('Season', 'Season'), ('30 Years', '30 Years')]
    tiles = ''.join(f'<div data-cat="{c}">{ph(f"gallery-{i + 1:02d}.jpg", f"{c} photo {i // 5 + 1}", "1600×1200")}</div>' for i, (c, _) in enumerate(photos * 4))
    return page('/gallery', 'Gallery and Videos · Divyanjali', 'Photos and videos of Divyanjali productions, classes, arangetrams and the Dance Season.', f'''
{crumbs(('Gallery and Videos', None))}
<section style="padding-top:28px"><div class="wrap stack"><p class="eyebrow">Gallery</p><h1>Gallery and Videos</h1><p class="lead">Tap a photo to open it full size. Videos play right here.</p>
  <div class="chipbar" data-filter="#mediaAll">{''.join(f'<button class="chip" type="button" data-f="{f}" aria-pressed="{str(f == "All").lower()}">{f}</button>' for f in ['All', 'Productions', 'Classes', 'Arangetrams', 'Season', '30 Years', 'Videos'])}</div></div></section>
<div id="mediaAll">
<section class="alt" style="padding-top:32px"><div class="wrap">{head('Videos', 'Watch')}<div class="vids" id="ytList"></div></div></section>
<section><div class="wrap">{head('Photos', 'From our stage')}<div class="tiles" data-gallery>{tiles}</div></div></section>
</div>
<section class="alt"><div class="wrap">{head('Instagram', 'Reels and posts', '<a class="btn-o" href="https://www.instagram.com/divyanjalidance/" target="_blank" rel="noopener">Follow on Instagram</a>')}<div class="tiles" id="igList"></div></div></section>
''')

def media():
    kit = [('Fact sheet', 'PDF · one page'), ('Bios', 'Short and long · both founders'), ('Photos', 'High resolution, with credits'), ('Logos', 'Official and 30-year'), ('Souvenir 2026', '30-year celebration booklet · PDF')]
    return page('/media', 'Media Room · Divyanjali', 'Press kit, photos, logos and media contact for Divyanjali, Chennai.', f'''
{crumbs(('Media Room', None))}
<section style="padding-top:28px"><div class="wrap stack"><p class="eyebrow">Press</p><h1>Media Room</h1><p class="lead">For journalists, presenters and festival curators: facts, photos and contacts in one place.</p></div></section>
<section class="alt"><div class="wrap">{head('Press kit', 'Downloads')}
  <div class="tiles">{''.join(f'<div class="tile"><span class="meta">{e(b)}</span><h3>{e(t)}</h3><a class="btn-o" href="/assets/logo-full.webp" download style="align-self:flex-start">Download</a></div>' if t == 'Logos' else f'<div class="tile"><span class="meta">{e(b)}</span><h3>{e(t)}</h3><span class="muted">{todo("file to upload")}</span></div>' for t, b in kit)}</div></div></section>
<section><div class="wrap">{head('In the press', 'Coverage')}
  <ol class="tl"><li><b>The Hindu</b><span>Pannum Bharathamum · {todo('date and link')}</span></li><li><b>Mylapore Times</b><span>Divyanjali productions and events · <a href="https://www.mylaporetimes.com/tag/divyasena/" target="_blank" rel="noopener">Read</a></span></li><li><b>Narthaki</b><span>Reviews of Divyanjali performances · <a href="https://narthaki.com/info/rev08/rev596.html" target="_blank" rel="noopener">Read</a></span></li></ol></div></section>
<section class="alt"><div class="wrap stack"><p class="eyebrow">Media contact</p><h2>{todo('Contact name')}</h2><p>{todo('Phone')} · {todo('Email')}</p><p class="muted">We answer media requests within one working day.</p></div></section>
''')

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
