-- Run this in your Supabase SQL Editor to set up the database

create table items (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  emoji text default '🥬',
  quantity text not null,
  from_name text not null,
  pickup_note text,
  is_taken boolean default false,
  taken_at timestamptz,
  created_at timestamptz default now()
);

-- Enable realtime for the items table
alter publication supabase_realtime add table items;

-- Allow anonymous access (no auth required)
alter table items enable row level security;

create policy "Allow anonymous read" on items
  for select using (true);

create policy "Allow anonymous insert" on items
  for insert with check (true);

create policy "Allow anonymous update" on items
  for update using (true);
