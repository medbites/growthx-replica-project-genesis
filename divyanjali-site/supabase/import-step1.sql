-- STEP 1 of 3: a holding table that accepts the Google Sheet CSV exactly as exported (every column as text).
-- Run this, then import the CSV into the table "events_import" (Table Editor > events_import > Insert > Import data from CSV).
alter table events add column if not exists poster_link text;   -- keeps Google Drive photo links working

drop table if exists events_import;
create table events_import (
  event_code text, status text, date text, start_time text, duration text, title text, type text, format text, mode text,
  lead_artist text, guru text, dancers text, orchestra text, music text, venue_name text, venue_address text, maps_link text,
  entry text, ticket_link text, presented_by text, sponsor text, why_attend text, invite_message text, about text,
  poster_link text, photos_link text, video_link text, photo_check text
);
