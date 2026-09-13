-- Synthetic P0 transaction probe. Not a complete NEKI migration or production grant set.
create table streams (
  namespace text not null,
  id uuid not null,
  state_value integer not null default 0,
  version bigint not null default 0 check (version >= 0),
  event_sequence bigint not null default 0 check (event_sequence >= 0),
  primary key (namespace, id)
);
create table dispatch_cursors (
  namespace text not null,
  stream_id uuid not null,
  last_sequence bigint not null default 0 check (last_sequence >= 0),
  failures integer not null default 0 check (failures between 0 and 8),
  blocked boolean not null default false,
  next_attempt_at timestamptz not null default '-infinity',
  primary key (namespace, stream_id),
  foreign key (namespace, stream_id) references streams(namespace, id)
);
create table events (
  id uuid primary key,
  namespace text not null,
  stream_id uuid not null,
  sequence bigint not null check (sequence > 0),
  aggregate_version bigint not null check (aggregate_version > 0),
  event_type text not null check (event_type = 'ProbeChanged.v1'),
  payload jsonb not null check (jsonb_typeof(payload) = 'object'),
  required_handlers text[] not null,
  occurred_at timestamptz not null default clock_timestamp(),
  correlation_id uuid not null,
  causation_id uuid not null,
  unique (namespace, stream_id, sequence),
  foreign key (namespace, stream_id) references streams(namespace, id)
);
create table effects (
  event_id uuid primary key references events(id),
  delta integer not null
);
create table handler_receipts (
  event_id uuid not null references events(id),
  handler text not null,
  processed_at timestamptz not null default clock_timestamp(),
  primary key (event_id, handler)
);
create table failed_attempts (
  id bigint generated always as identity primary key,
  event_id uuid not null references events(id),
  attempt_in_cycle integer not null check (attempt_in_cycle between 1 and 8),
  failure_code text not null,
  at timestamptz not null
);
create table dead_letters (
  id bigint generated always as identity primary key,
  event_id uuid not null references events(id),
  failure_code text not null,
  at timestamptz not null
);
create table replay_audit (
  id bigint generated always as identity primary key,
  event_id uuid not null references events(id),
  reason text not null check (length(trim(reason)) > 0),
  at timestamptz not null default clock_timestamp()
);
create function deny_event_rewrite() returns trigger language plpgsql as $$
begin
  raise exception 'Outbox evidence is immutable' using errcode = '23514';
end $$;
create trigger events_immutable before update or delete on events
  for each row execute function deny_event_rewrite();
create trigger failed_attempts_immutable before update or delete on failed_attempts
  for each row execute function deny_event_rewrite();
create trigger replay_audit_immutable before update or delete on replay_audit
  for each row execute function deny_event_rewrite();
