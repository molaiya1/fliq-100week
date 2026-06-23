-- ============================================================
-- The $100 Week™ — FLIQ Score Database Setup
-- Run this ONCE in Supabase → SQL Editor → New Query → Run
-- Project: fikdyraqugzstigmzufz (WealthWise Kids)
-- ============================================================

-- Step 1: Make sure UUID generation is available
create extension if not exists "uuid-ossp";

-- Step 2: Create the FLIQ scores table
create table if not exists fliq_scores (
  id              uuid default uuid_generate_v4() primary key,
  created_at      timestamptz default now(),

  -- Session identity (fully anonymous — no names, no emails)
  cohort_id       text,           -- UUID from the Railway API (teacher's class)
  adventure_code  text,           -- student's self-chosen 4-digit PIN
  session_id      text,           -- Railway session ID

  -- Profile result
  band            text not null default 'builder',   -- explorer | builder | strategist
  profile_label   text,           -- Financial Starter → Exceptional
  fliq_score      integer,        -- 0–100

  -- Balance outcome
  balance_final   integer,        -- ending dollar balance
  balance_start   integer,        -- starting dollar balance

  -- Trait scores (0, 1, or 2)
  trait_ic        text,           -- Impulse Control label
  trait_ic_score  integer,
  trait_po        text,           -- Planning label
  trait_po_score  integer,
  trait_ra        text,           -- Risk Awareness label
  trait_ra_score  integer,
  trait_rb        text,           -- Recovery label
  trait_rb_score  integer,

  -- Full choice history
  history         jsonb default '[]'::jsonb,

  sim_version     text default '1.0'
);

-- Step 3: Unique index so students can retake without creating duplicate rows
create unique index if not exists fliq_scores_cohort_code_idx
  on fliq_scores (cohort_id, adventure_code)
  where cohort_id is not null and adventure_code is not null;

-- Step 4: Row Level Security (keeps the table protected)
alter table fliq_scores enable row level security;

-- Step 5: Allow students to submit their scores (anonymous inserts)
create policy "students_can_submit"
  on fliq_scores for insert
  to anon
  with check (true);

-- Step 6: Allow the facilitator dashboard to read results
create policy "facilitators_can_read"
  on fliq_scores for select
  to anon
  using (true);

-- ============================================================
-- Done. The sim will now write scores here automatically.
-- ============================================================
