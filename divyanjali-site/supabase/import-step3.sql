-- STEP 3 of 3: copy the imported rows into "events", converting dates and times. Safe to run again (updates existing codes).
insert into events (event_code, status, date, start_time, duration, title, type, format, mode, lead_artist, guru, dancers,
  orchestra, music, venue_name, venue_address, maps_link, entry, ticket_link, presented_by, sponsor, why_attend,
  invite_message, about, poster_link, photos_link, video_link)
select
  trim(event_code),
  coalesce(nullif(trim(status), ''), 'Draft'),
  case when trim(date) ~ '^\d{4}-\d{2}-\d{2}$' then trim(date)::date
       when trim(date) ~ '^\d{1,2}/\d{1,2}/\d{4}$' then to_date(trim(date), 'DD/MM/YYYY')
       else to_date(trim(date), 'DD Mon YYYY') end,                                        -- 15 Nov 2026, 15/11/2026 or 2026-11-15
  case when trim(start_time) ~* '[ap]\.?m' then to_timestamp(upper(replace(trim(start_time), '.', '')), 'HH12:MI AM')::time
       else trim(start_time)::time end,                                                     -- 6:00 PM or 18:00
  nullif(trim(duration), ''), trim(title),
  coalesce(nullif(trim(type), ''), 'Performance'), coalesce(nullif(trim(format), ''), 'Solo'),
  coalesce(nullif(trim(mode), ''), 'In person'),
  nullif(trim(lead_artist), ''), nullif(trim(guru), ''), nullif(trim(dancers), ''), nullif(trim(orchestra), ''),
  coalesce(nullif(trim(music), ''), 'Live'),
  nullif(trim(venue_name), ''), nullif(trim(venue_address), ''), nullif(trim(maps_link), ''),
  coalesce(nullif(trim(entry), ''), 'Free'), nullif(trim(ticket_link), ''),
  coalesce(nullif(trim(presented_by), ''), 'Divyanjali'), nullif(trim(sponsor), ''),
  nullif(trim(why_attend), ''), nullif(trim(invite_message), ''), nullif(trim(about), ''),
  -- a photo link pasted into photo_check by mistake is used as the poster too
  coalesce(nullif(trim(poster_link), ''), case when trim(photo_check) ~* '^https?://' then trim(photo_check) end),
  nullif(trim(photos_link), ''), nullif(trim(video_link), '')
from events_import
where coalesce(trim(event_code), '') <> '' and coalesce(trim(date), '') <> '' and coalesce(trim(title), '') <> ''
on conflict (event_code) do update set
  status = excluded.status, date = excluded.date, start_time = excluded.start_time, duration = excluded.duration,
  title = excluded.title, type = excluded.type, format = excluded.format, mode = excluded.mode,
  lead_artist = excluded.lead_artist, guru = excluded.guru, dancers = excluded.dancers, orchestra = excluded.orchestra,
  music = excluded.music, venue_name = excluded.venue_name, venue_address = excluded.venue_address,
  maps_link = excluded.maps_link, entry = excluded.entry, ticket_link = excluded.ticket_link,
  presented_by = excluded.presented_by, sponsor = excluded.sponsor, why_attend = excluded.why_attend,
  invite_message = excluded.invite_message, about = excluded.about, poster_link = excluded.poster_link,
  photos_link = excluded.photos_link, video_link = excluded.video_link, updated_at = now();

-- Check: every event, with its date and time as stored.
select event_code, status, date, start_time, title, venue_name, poster_link is not null as has_photo from events order by date, start_time;
