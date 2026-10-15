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
    return '<div class="stats">' + ''.join(f'<div class="stat reveal"><b data-count="{n}" data-plus="{p}">{n}{p}</b><span>{e(l)}</span></div>' for n, p, l in items) + '</div>'

# ---------------------------------------------------------------- layout
NAV = [('About', '/about'), ('Choreographies', '/choreographies'), ('Learn', '/learn'), ('Natya IQ', '/natya-iq'), ('Calendar', '/events')]
MENU = [('Home', '/'), ('About Divyanjali', '/about'), ('Dr. S. Divyasena', '/divyasena'), ('Sri B.P. Haribabu', '/haribabu'), ('30 Years', '/30-years'),
        ("Student's Accolades", '/accolades'), ('Choreographies', '/choreographies'), ('Learn', '/learn'), ('Events calendar', '/events'),
        ('Gallery and Videos', '/gallery'), ('Natya IQ', '/natya-iq'), ('Media Room', '/media'), ('Store', '/store'), ('Book and Enquire', '/book')]

def header(path):
    cur = lambda h: ' aria-current="page"' if h == path or (h != '/' and path.startswith(h + '/')) else ''
    nav = ''.join(f'<a class="{"navcal" if h == "/events" else "hide-m"}" href="{h}"{cur(h)}>{t}</a>' for t, h in NAV)
    menu = ''.join(f'<a href="{h}"{cur(h)}>{t}</a>' for t, h in MENU)
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

def home():
    feat = [p for p in PRODUCTIONS if p['slug'] in ('hanumath-margam', 'andal-vaibhavam', 'thirumurugaatrupadai', 'dasavatharam')]
    def bento(p, i):
        img = ph(f"prod-{p['slug']}.jpg", f"poster · {p['title']}", '1500×900' if i else '1200×1500', '' if i else 'tall')
        return f'<a class="bento-i{" big" if i == 0 else ""} reveal" href="/productions/{p["slug"]}">{img}<span class="bento-t"><small>{e(p["year"])} · {e(p["cats"][0])}</small><b>{e(p["title"])}</b></span></a>'
    classes = [('01', 'Children', f'From {todo("youngest age")} · weekday and weekend batches in CIT Nagar', 'learn-children.jpg'),
               ('02', 'Teens and adults', 'Beginners, and dancers coming back after a break', 'learn-adults.jpg'),
               ('03', 'Online, from abroad', 'Live classes from Chennai, set to your time zone', 'learn-online.jpg')]
    rows = ''.join(f'<a class="crow reveal" href="/learn#paths"><span class="cn">{n}</span><span class="ct"><b>{t}</b><span class="muted">{d}</span></span>{ph(f, t + " class", "800×600")}<span class="ca" aria-hidden="true">→</span></a>' for n, t, d, f in classes)
    return page('/', 'Divyanjali · Bharatanatyam school in Chennai since 1994',
        'Divyanjali, the Bharatanatyam school of Dr. S. Divyasena and Sri B.P. Haribabu in CIT Nagar, Chennai. See the season calendar of performances, workshops and arangetrams.', f'''
<section class="hc">
  <div class="wrap hc-grid">
    <div class="hc-copy">
      <p class="kicker">Divyanjali · Bharatanatyam since 1994 · Chennai</p>
      <h1>Every performance of the season, <em>on one calendar.</em></h1>
      <p class="lead">Recitals, workshops and arangetrams by Dr. S. Divyasena, Sri B.P. Haribabu and their students. Tap a date to see what is on, then add it to your phone in one tap.</p>
      <div class="next" id="nextUp" aria-live="polite">
        <div class="next-skel"><span></span><span></span><span></span></div>
      </div>
    </div>
    <div class="cal" id="homeCal" aria-label="Season calendar">
      <div class="cal-top">
        <button class="cal-arr" type="button" data-cal="-1" aria-label="Previous month">‹</button>
        <h2 class="cal-m" id="calMonth">Season calendar</h2>
        <button class="cal-arr" type="button" data-cal="1" aria-label="Next month">›</button>
      </div>
      <div class="cal-dow" aria-hidden="true"><span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span></div>
      <div class="cal-days" id="calDays" role="grid"></div>
      <div class="cal-list" id="calList"><div class="cal-skel"></div><div class="cal-skel"></div></div>
      <div class="cal-foot"><a class="btn" href="/events">Open full calendar</a><a class="btn-o" href="#follow">Subscribe</a></div>
    </div>
  </div>
</section>
<section class="strip-sec">
  <div class="wrap sec-head"><div><h2>The season, poster by poster</h2></div>
    <div class="strip-nav"><button class="cal-arr" type="button" data-strip="-1" aria-label="Scroll back">‹</button><button class="cal-arr" type="button" data-strip="1" aria-label="Scroll on">›</button></div></div>
  <div class="strip" id="seasonStrip"><div class="strip-card skel"></div><div class="strip-card skel"></div><div class="strip-card skel"></div></div>
</section>
<section class="follow" id="follow"><div class="wrap follow-in">
  <div class="stack" style="gap:8px"><h2>Never miss a performance</h2><p class="muted">Subscribe once. New dates from Divyanjali appear in your own calendar, with venue and timing, as soon as we add them.</p></div>
  <div class="row"><a class="btn" id="subG" href="/events#subscribe" target="_blank" rel="noopener">Google Calendar</a><a class="btn-o" id="subA" href="/calendar.ics">Apple and Outlook</a><a class="btn-o" data-wa="Hello Divyanjali, please add me to your events list on WhatsApp." href="#">WhatsApp updates</a></div>
</div></section>
<section class="stage"><div class="wrap stage-grid">
  <div class="stage-v">{yt(HOME_VIDEO, 'Watch Divyanjali on stage', 12)}</div>
  <div class="stack stage-c">
    <h2>The dancer is the dance.</h2>
    <p class="muted">Thirty years of classes, productions and arangetrams, from CIT Nagar to stages in some twenty countries.</p>
    {stats([(30, '', 'years of teaching'), (71, '', 'arangetrams'), (300, '+', 'dancers trained'), (len(PRODUCTIONS), '', 'productions')])}
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
<section class="alt"><div class="wrap learn-grid">
  <div class="stack" style="gap:12px"><h2>Find your class</h2><p class="muted">Technique, abhinaya, laya and theory, taught in small batches. Start with a trial class.</p><a class="btn" href="/learn#enquire" style="align-self:flex-start">Ask about classes</a></div>
  <div class="crows">{rows}</div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><h2>71 arangetrams. Stages from Chennai to the world.</h2><p class="muted">Scholarship holders, Doordarshan graded artists and teachers with their own schools in India, the USA, the UK and Singapore.</p><a class="btn-o" href="/accolades" style="align-self:flex-start">Student's Accolades</a></div>
  <div class="tiles" data-gallery>{ph('home-students-1.jpg', 'students on stage', '1000×1250', 'tall')}{ph('home-students-2.jpg', 'arangetram moment', '1000×1250', 'tall')}</div>
</div></section>
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
    return page('/divyasena', 'Dr. S. Divyasena · Bharatanatyam guru, Divyanjali', 'Natyacharya Dr. S. Divyasena: dancer, choreographer and nattuvanar, founder of Divyanjali, Doordarshan A grade artist.', f'''
{crumbs(('About', '/about'), ('Dr. S. Divyasena', None))}
<section style="padding-top:28px"><div class="wrap hero2">
  {ph('divyasena-portrait.jpg', 'Dr. S. Divyasena, portrait', '1200×1500', 'tall')}
  <div class="stack"><p class="eyebrow">Founder · Natyacharya</p><h1>Dr. S. Divyasena</h1><p class="lead">Dancer, choreographer and nattuvanar. Founder of Divyanjali in 1994. Doctorate in Bharatanatyam. Doordarshan A grade artist. Honoured as Nrithya Kala Sagaram.</p>
  <div class="row"><a class="btn" href="/book?type=Performance+booking">Invite her to perform</a><a class="btn-o" href="/learn">Learn with her</a></div></div>
</div></section>
<section class="alt"><div class="wrap two">
  <div class="stack">{head('Training', 'Her gurus')}
  <div class="prose"><p>Dr. S. Divyasena trained in the preliminaries of Bharatanatyam under Smt. Saroja Rani and made her stage debut with her arangetram in 1985. She continued her rigorous training under 'Yuva Kala Bharathi' Sri J. Suryanarayana Murthy, and trained in abhinaya under 'Padma Bhushan' Late Smt. Kalanidhi Narayanan.</p>
  <p>As part of her own learning she has also trained in Kuchipudi, at the Kuchipudi Arts Academy founded by 'Padma Bhushan' Dr. Vempati Chinna Satyam, and later under Sri Jai Kishore Mosalikanti. She learnt nattuvangam, the art of wielding the cymbals, from Sri B.P. Haribabu. At Divyanjali, she teaches Bharatanatyam.</p></div></div>
  <ol class="tl"><li><b>1985</b><span>Arangetram</span></li><li><b>Gurus</b><span>Smt. Saroja Rani · Sri J. Suryanarayana Murthy · Smt. Kalanidhi Narayanan (abhinaya)</span></li><li><b>Nattuvangam</b><span>Sri B.P. Haribabu</span></li><li><b>1994</b><span>Founded Divyanjali</span></li></ol>
</div></section>
<section><div class="wrap">{head('Education and honours', 'Scholar and artist')}
  <div class="tiles">
    <div class="tile"><span class="meta">Doctorate</span><h3>Bharatanatyam</h3><p class="muted">Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya, under the guidance of Dr. Ambika Kameshwar</p></div>
    <div class="tile"><span class="meta">Master's</span><h3>Kuchipudi</h3><p class="muted">Postgraduate study, part of her own training</p></div>
    <div class="tile"><span class="meta">Bachelor's</span><h3>Music</h3><p class="muted">Carnatic music</p></div>
    <div class="tile"><span class="meta">Doordarshan</span><h3>A grade artist</h3><p class="muted">National broadcaster grading</p></div>
    <div class="tile"><span class="meta">Title</span><h3>Nrithya Kala Sagaram</h3><p class="muted">{todo('Given by, year')}</p></div>
    <div class="tile"><span class="meta">Service</span><h3>Prayathnam</h3><p class="muted">Secretary of the forum for young classical dance teachers</p></div>
  </div></div></section>
<section class="alt"><div class="wrap">{head('On stage and screen', 'Productions and television', '<a class="btn-o" href="/choreographies">See the productions</a>')}
  <div class="vids">{yt('https://www.youtube.com/watch?v=So5SO_M4zZ8', 'Dasavatharam')}{yt(HOME_VIDEO, 'Divyanjali on stage')}</div>
  <div class="tiles" style="margin-top:24px">
    <div class="tile"><span class="meta">Jaya TV</span><h3>Judge and interview</h3><p class="muted">Judge for the dance show Takadimi Tha, and an interview</p></div>
    <div class="tile"><span class="meta">Raj TV</span><h3>Judge</h3><p class="muted">Aaseervath 'Abhinaya'</p></div>
    <div class="tile"><span class="meta">Sun TV · Makkal TV · Podhigai</span><h3>Performances</h3><p class="muted">Televised dance performances</p></div>
  </div></div></section>
{faq_section([
    ('Where did Dr. Divyasena train?', 'Under Smt. Saroja Rani, Sri J. Suryanarayana Murthy and, for abhinaya, Smt. Kalanidhi Narayanan. She holds a doctorate in Bharatanatyam.'),
    ('Does Divyanjali teach Kuchipudi?', 'No. Dr. Divyasena trained in Kuchipudi as part of her own learning, and it informs her work, but Divyanjali teaches Bharatanatyam.'),
    ('Can we invite her for a workshop or lecture demonstration?', 'Yes. Send the details through <a href="/book?type=Workshop+or+lecture+demonstration">Book and Enquire</a>.'),
])}
{cta('Invite Dr. Divyasena', 'For performances, workshops and lecture demonstrations.', 'Send an enquiry', '/book?type=Workshop+or+lecture+demonstration')}
''')

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

def thirty():
    return page('/30-years', '30 Years of Divyanjali', 'Three decades of a divine offering: a class that became a trust, a flood that took everything, and the students who carried the school forward.', f'''
{crumbs(('About', '/about'), ('30 Years', None))}
<section style="padding-top:28px"><div class="wrap hero2">
  <div class="stack"><p class="eyebrow">1994–2024</p><h1>Three decades of a divine offering</h1><p class="lead">A small class that grew into a trust, a flood that took everything, and the students who carried the school forward.</p></div>
  <figure class="ph sq" style="background:#FFFFFF"><img src="/assets/logo-full.webp" alt="Divyanjali 30 years logo" style="object-fit:contain;padding:12%;cursor:default"></figure>
</div></section>
<section class="alt" style="padding-block:40px"><div class="wrap">{stats([(1994, '', 'founded'), (71, '', 'arangetrams'), (300, '+', 'dancers trained'), (150, '+', 'books in the rebuilt library')])}</div></section>
<section><div class="wrap">{head('Timeline', 'The years, one by one')}
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
<section class="alt"><div class="wrap two">
  <div class="stack">{head('2015', 'The flood, and the way back')}<div class="prose"><p>In the 2015 Chennai floods the workspace stood under seven feet of water. Choreographies in digital format, library books and musical instruments, the school's treasures, were lost.</p>
  <p>Divyanjali did not lose hope. It came back with the help of many institutions and legends: Smt. Chithra Visweswaran through ABHAI, the Music Academy, Narada Gana Sabha, Sri Nellai Kannan, Sri C.V. Chandrasekar, the core members of Prayathnam, Smt. Vasanthalakshmi Narasimhachari and Sri Jaikishore Mosalikanti, and others who asked not to be named. Today the library holds over 150 books, contributed by Smt. Nandini Ramani.</p></div></div>
  <div class="tiles" data-gallery>{ph('flood-before.jpg', 'the workspace after the flood', '1200×900')}{ph('flood-after.jpg', 'the rebuilt library', '1200×900')}</div>
</div></section>
<section><div class="wrap">{head('Messages', 'From fellow artists')}
  <div class="quotes">{''.join(f'<blockquote><p>“{todo("Quote from the Souvenir")}”</p><cite>{todo("Artist name")}</cite></blockquote>' for _ in range(3))}</div></div></section>
<section class="alt"><div class="wrap">{head('Celebration', 'Gallery', '<a class="btn-o" href="/gallery">See all photos</a>')}
  <div class="tiles" data-gallery>{''.join(ph(f'30y-{i}.jpg', f'30 years celebration {i}', '1200×900') for i in range(1, 7))}</div></div></section>
{faq_section([
    ('When did Divyanjali complete 30 years?', 'In 2024. The school was founded in 1994.'),
    ('What happened in the 2015 floods?', 'The workspace was under seven feet of water and the library, instruments and recordings were lost. Friends and institutions helped the school rebuild.'),
    ('How many arangetrams has Divyanjali conducted?', 'Seventy-one, including one abroad. The 50th was in 2015 and the 60th in 2019.'),
])}
{cta('Be part of the next chapter', 'Join a class, or bring a production to your stage.', 'Join a class', '/learn')}
''')

def accolades():
    students = [('student-shabin.jpg', 'Dr. Shabin Bright', 'Disciple of Dr. S. Divyasena', 'Teaching abroad|Awards', 'Solo recitals across India, including Navaratri Nayanotsava, Bengaluru')]
    students += [(f'student-{i}.jpg', '[Student name]', 'Arangetram [year]', ['Awards', 'Scholarships', 'Doordarshan graded', 'Teaching abroad'][i % 4], 'Top two achievements') for i in range(1, 8)]
    cards = ''.join(f'<div class="tile" data-cat="{c}">{ph(f, n, "800×1000", "tall")}<span class="meta">{e(s)}</span><h3>{e(n)}</h3><p class="muted">{e(a)}</p></div>' for f, n, s, c, a in students)
    return page('/accolades', "Student's Accolades · Divyanjali", 'Dancers trained at Divyanjali: 71 arangetrams, national scholarships, Doordarshan graded artists and teachers in India and abroad.', f'''
{crumbs(('About', '/about'), ("Student's Accolades", None))}
<section style="padding-top:28px"><div class="wrap stack"><p class="eyebrow">Our students</p><h1>Student's Accolades</h1><p class="lead">Dancers trained at Divyanjali, on stages from Chennai sabhas to festivals abroad, and teaching in India and around the world.</p>
{stats([(71, '', 'arangetrams'), (300, '+', 'dancers trained'), (3, '', 'national scholarships'), (4, '', 'countries with alumni schools')])}</div></section>
<section class="alt"><div class="wrap">{head('Featured', 'Students')}
  <div class="chipbar" data-filter="#studentGrid" style="margin-bottom:20px">{''.join(f'<button class="chip" type="button" data-f="{f}" aria-pressed="{str(f == "All").lower()}">{f}</button>' for f in ['All', 'Awards', 'Scholarships', 'Doordarshan graded', 'Teaching abroad'])}</div>
  <div class="people" id="studentGrid" data-gallery>{cards}</div></div></section>
<section><div class="wrap two">
  <div class="stack">{head('Alumni', 'Students who started schools')}<ol class="tl"><li><b>Kala Roopam</b><span>Dr. S. Roopa</span></li><li><b>Shiva Nrittam</b><span>Sumodh</span></li><li><b>Ananda Natyakshethra</b><span>Anandaraj A., Thiruverkadu</span></li></ol><p class="muted">Senior students also teach at leading institutions and run schools in the USA, the UK and Singapore: {todo('names to confirm')}.</p></div>
  <div class="stack">{head('Recognition', 'Scholarships and prizes')}<ul class="list">
    <li>CCRT Scholarship, Government of India</li><li>Bharat Kalachar Scholarship</li><li>Iyal Isai Nataka Mandram Scholarship</li>
    <li>Prizes at the Cleveland Thyagaraja Festival, Ohio, USA</li><li>All India Dance Festival, Kalamandir College of Fine Arts, Kannur</li>
    <li>Nrithyathi Kalakshetram, Raipur · Navya Nataka Samiti, Hyderabad · Akhil Bharatiya Sanskrutik Sangh, Pune</li>
    <li>Natyarangam and Spirit of Youth competitions, Music Academy, Chennai</li>
    <li>Dr. Padma Subramanian Endowment Award · VDS Best Dancer · Indian Fine Arts Best Dancer · Nalanda Nritya Nipuna</li>
    <li>Students with a master's in Bharatanatyam, and Doordarshan B grade artists</li></ul></div>
</div></section>
<section class="alt"><div class="wrap">{head('Big stages', 'Moments')}
  <div class="tiles" data-gallery>{ph('stage-1.jpg', 'a national stage', '1200×900')}{ph('stage-2.jpg', 'performing abroad', '1200×900')}{ph('stage-3.jpg', 'festival performance', '1200×900')}</div></div></section>
{cta('Your child could be next', 'Classes for children from their first steps to arangetram.', 'Ask about classes', '/learn#enquire')}
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
