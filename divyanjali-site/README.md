# Divyanjali Events · Phase 0

One fast page (`index.html`, about 55 KB, no framework) with:

- Home: next event, upcoming events, month calendar with quick view, past events, "coming soon" cards, enquiry form
- A shareable page for every event: `divyanjalidance.com/e/EVENT-CODE`
- Wishes and feedback, and enquiries, saved to Google Sheets

Until the Google Sheet is connected, the page shows demo events with a yellow "Demo data" bar.

---

## 1. Google Sheet (10 minutes)

1. Use the institution's Google account, not a personal one. Create a new Google Sheet named **Divyanjali Website**.
2. **Extensions > Apps Script**. Delete what is there, paste all of `apps-script/Code.gs`, and save.
3. In the script editor, choose `setup` in the function list and press **Run**. Allow the permissions.
   This creates five tabs, the drop-down lists, the red warnings and one sample row:

| Tab | Who uses it | Public? |
|---|---|---|
| **Events** | The team adds one row per event | Only rows with status **Published** are read by the site |
| **Private** | Join links for online events, contact people | Never read by the site |
| **Responses** | Wishes and feedback from event pages (one tab, tagged by event code and date) | Private. Only rows you mark **approved = Yes** and the visitor allowed are shown |
| **Enquiries** | Performance bookings, workshops, class enquiries | Private |
| **Settings** | Admin email for alerts, WhatsApp number, drop-down lists | Private |

4. In **Settings**, put the admin email in `admin_email` to get an email for every new wish or enquiry.
5. **Deploy > New deployment > Web app**. Execute as **Me**, access **Anyone**. Copy the URL ending in `/exec`.
6. Open `index.html`, find `CONFIG` near the bottom, and paste that URL into `SCRIPT_URL`. Also set `WHATSAPP`, `ADDRESS` and the social links.

Changing the script later: **Deploy > Manage deployments > Edit > New version**. Do not create a new deployment, or the URL changes and the site stops saving forms.

## 2. Put it online (free)

**Recommended: Cloudflare Pages**
1. Put the `divyanjali-site` folder in a GitHub repository (this one works).
2. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git > choose the repo. Build command: none. Output folder: `divyanjali-site`.
3. You get `something.pages.dev` at once. Add `divyanjalidance.com` under Custom domains, then point the domain's DNS at Cloudflare (GoDaddy > Nameservers).
4. The `_redirects` file makes `/e/EVENT-CODE` links open the event page.

**Quick alternative: GitHub Pages.** It works the same, but set `PRETTY_LINKS: false` in `CONFIG`, so links look like `divyanjalidance.com/?e=EVENT-CODE`.

**WhatsApp preview cards (Phase 1, included):** on Cloudflare Pages, `_worker.js` gives every `/e/EVENT-CODE` link its own preview card with the event's poster, title, date and venue. Nothing to set up. If you change the Apps Script link, update `SCRIPT_URL` at the top of `_worker.js` too.

Test a card: paste an event link into WhatsApp (to yourself). If an old preview shows, add `?v=2` to the end of the link once, because WhatsApp remembers previews.

**Connect divyanjalidance.com:** Cloudflare Pages > your project > Custom domains > Set up a domain > `divyanjalidance.com`. Cloudflare shows the DNS records or nameservers to set at GoDaddy. Add `www.divyanjalidance.com` the same way.

## 3. Rules for the team (keep this page)

1. **Add an event:** fill a new row in **Events**. The event code fills itself in once date and title are entered. Set **status = Published** when it is ready. It appears on the site within a minute.
2. **Never change** the heading row, or an event code that has already been shared. Old links would break.
3. **Posters:** upload a JPG to the shared Drive folder, about 1200 px wide and under 300 KB. Set it to *Anyone with the link can view*. Paste the link in `poster_link`. Then use the menu **Divyanjali > Check photo links**.
4. **Red rows** mean a duplicate code or two events at the same date, time and venue. Fix them before publishing.
5. **Orchestra** is written as `Role: Name; Role: Name`. **Dancers** for group events are separated by commas.
6. **Wishes:** read them in **Responses**. Set `approved = Yes` only for messages that can appear on the event page.
7. **Online join links** go in the **Private** tab, never in Events.

## 4. How people use it

- Families copy the event link into their WhatsApp invitation and Instagram story (link sticker).
- The event page has Add to Google Calendar, Apple or Outlook calendar, Share (phone share sheet, WhatsApp, Facebook, X, LinkedIn, Telegram, Email, Copy link), Send a wish, Book us and Reach us on WhatsApp.
- Past events stay online with photos and video links, so every event builds the record. The full archive is at `divyanjalidance.com/#archive`, grouped by year, with a search box and type filters.

## Files

- `index.html`: the whole site (HTML, CSS, JS in one file)
- `apps-script/Code.gs`: the Google Sheet backend
- `_redirects`: pretty event links on Cloudflare Pages
