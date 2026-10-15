-- Divyanjali Events · Supabase setup
-- Paste all of this into Supabase > SQL Editor > New query, then press Run. Safe to run again.

-- 1. Events: one row per event. Only Published rows are visible to the website.
create table if not exists events (
  event_code     text primary key,                 -- e.g. DV-261108-RECITAL, used in the share link
  status         text not null default 'Draft' check (status in ('Draft','Published','Cancelled')),
  date           date not null,
  start_time     time not null,                    -- a real time type: no 7:21 AM style shifts
  duration       text default '2 hrs',
  title          text not null,
  type           text default 'Performance' check (type in ('Performance','Arangetram','Workshop','Festival')),
  format         text default 'Solo' check (format in ('Solo','Group')),
  mode           text default 'In person' check (mode in ('In person','Online','Hybrid')),
  lead_artist    text, guru text, dancers text, orchestra text,
  music          text default 'Live' check (music in ('Live','Recorded')),
  venue_name     text, venue_address text, maps_link text,
  entry          text default 'Free', ticket_link text,
  presented_by   text default 'Divyanjali', sponsor text,
  why_attend     text, invite_message text, about text,
  poster         text,                             -- file name in the "posters" storage bucket, e.g. andal-2026.jpg
  photos_link    text, video_link text,
  created_at     timestamptz default now(),
  updated_at     timestamptz default now()
);

-- Two events cannot share the same date, time and venue (in person or hybrid).
create unique index if not exists events_no_clash
  on events (date, start_time, lower(venue_name))
  where status <> 'Cancelled' and mode <> 'Online';

-- 2. Private details: never readable from the website.
create table if not exists event_private (
  event_code text primary key references events(event_code) on update cascade on delete cascade,
  online_join_link text, contact_person text, contact_phone text, notes text
);

-- 3. Wishes and feedback from event pages.
create table if not exists responses (
  id          bigint generated always as identity primary key,
  created_at  timestamptz default now(),
  event_code  text references events(event_code) on update cascade,
  kind        text check (kind in ('Wish','Feedback','Other')),
  name        text not null check (length(name) between 1 and 80),
  city        text check (length(city) <= 80),
  rating      int check (rating between 1 and 5),
  message     text not null check (length(message) between 1 and 2000),
  show_public boolean default false,
  approved    boolean default false,               -- the team ticks this before a message appears on the page
  notes       text
);

-- 4. Enquiries: bookings, workshops, classes.
create table if not exists enquiries (
  id              bigint generated always as identity primary key,
  created_at      timestamptz default now(),
  enquiry_type    text, from_event_code text,
  name            text not null check (length(name) between 1 and 80),
  organisation    text, whatsapp text not null check (length(whatsapp) between 8 and 20),
  email           text, date_needed date,
  message         text check (length(message) <= 2000),
  status          text default 'New' check (status in ('New','Contacted','Won','Lost')),
  notes           text
);

-- 5. Season slots and artist applications.
create table if not exists slots (
  slot_id        text primary key,                 -- e.g. S-261114-1700
  date           date not null, start_time time not null, end_time time,
  venue_name     text, venue_address text, maps_link text,
  slot_for       text default 'Solo or group' check (slot_for in ('Solo','Group','Solo or group')),
  status         text default 'Open' check (status in ('Open','Held','Booked','Closed')),
  application_id bigint
);
create table if not exists applications (
  id          bigint generated always as identity primary key,
  created_at  timestamptz default now(),
  slot_id     text references slots(slot_id),
  artist_name text not null, format text, dancers text, guru text, programme text, music text,
  whatsapp    text not null, email text, city text, video_link text, message text,
  status      text default 'Pending' check (status in ('Pending','Approved','Rejected')),
  event_code  text, notes text
);

-- 6. Who can do what. RLS on = nothing is allowed unless a policy says so.
alter table events        enable row level security;
alter table event_private enable row level security;
alter table responses     enable row level security;
alter table enquiries     enable row level security;
alter table slots         enable row level security;
alter table applications  enable row level security;

drop policy if exists "public reads published events" on events;
create policy "public reads published events" on events for select to anon using (status = 'Published');

drop policy if exists "public reads open slots" on slots;
create policy "public reads open slots" on slots for select to anon using (status = 'Open' and date >= current_date);

drop policy if exists "public sends wishes" on responses;
create policy "public sends wishes" on responses for insert to anon with check (approved = false);

drop policy if exists "public sends enquiries" on enquiries;
create policy "public sends enquiries" on enquiries for insert to anon with check (status = 'New');
-- No select policies on responses, enquiries, event_private or applications: visitors can send, never read.

-- Approved public wishes, without private columns.
create or replace view public_wishes with (security_invoker = false) as
  select event_code, kind, name, city, message, created_at
  from responses where approved and show_public;
grant select on public_wishes to anon;

-- 7. Requesting a slot: one step that locks the slot, so two artists can never hold the same one.
create or replace function request_slot(p_slot text, p_artist text, p_whatsapp text, p_format text default null,
  p_dancers text default null, p_guru text default null, p_programme text default null, p_music text default null,
  p_email text default null, p_city text default null, p_video text default null, p_message text default null)
returns json language plpgsql security definer set search_path = public as $$
declare s slots; new_id bigint;
begin
  if coalesce(trim(p_artist), '') = '' or length(regexp_replace(coalesce(p_whatsapp, ''), '\D', '', 'g')) < 10 then
    return json_build_object('ok', false, 'error', 'Name and a full WhatsApp number are required');
  end if;
  select * into s from slots where slot_id = p_slot for update;   -- waits if someone else is booking this slot
  if not found or s.status <> 'Open' then
    return json_build_object('ok', false, 'taken', true, 'error', 'Sorry, someone just took this slot. Please pick another.');
  end if;
  insert into applications (slot_id, artist_name, whatsapp, format, dancers, guru, programme, music, email, city, video_link, message)
  values (p_slot, left(p_artist, 80), left(p_whatsapp, 20), p_format, p_dancers, p_guru, left(p_programme, 1500), p_music, p_email, p_city, p_video, left(p_message, 1500))
  returning id into new_id;
  update slots set status = 'Held', application_id = new_id where slot_id = p_slot;
  return json_build_object('ok', true, 'application_id', new_id);
end $$;
grant execute on function request_slot to anon;

-- Approve or reject in the Applications table: the slot follows automatically.
create or replace function sync_slot() returns trigger language plpgsql as $$
begin
  if new.status = 'Approved' then update slots set status = 'Booked', application_id = new.id where slot_id = new.slot_id;
  elsif new.status = 'Rejected' then update slots set status = 'Open', application_id = null where slot_id = new.slot_id and application_id = new.id;
  end if;
  return new;
end $$;
drop trigger if exists applications_sync_slot on applications;
create trigger applications_sync_slot after update of status on applications for each row execute function sync_slot();

-- 8. Posters: a public storage bucket. Anyone can view a poster; only the team (signed in to Supabase) can upload.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('posters', 'posters', true, 1048576, array['image/jpeg','image/png','image/webp'])
on conflict (id) do update set public = true, file_size_limit = 1048576, allowed_mime_types = array['image/jpeg','image/png','image/webp'];
