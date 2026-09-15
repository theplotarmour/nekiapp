"""Versioned event streams and durable dispatch foundation; no synthetic domain effects."""

from alembic import op

revision = "0001_platform"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        create table event_streams (
            aggregate_type text not null, aggregate_id uuid not null,
            last_sequence bigint not null default 0 check (last_sequence >= 0),
            primary key (aggregate_type, aggregate_id)
        );
        create table domain_events (
            id uuid primary key,
            aggregate_type text not null, aggregate_id uuid not null,
            aggregate_sequence bigint not null check (aggregate_sequence > 0),
            aggregate_version bigint not null check (aggregate_version > 0),
            event_type text not null, schema_version integer not null check (schema_version > 0),
            payload jsonb not null check (jsonb_typeof(payload) = 'object'),
            required_handlers jsonb not null check (jsonb_typeof(required_handlers) = 'array'),
            correlation_id uuid not null, causation_id uuid not null, transition_id uuid not null,
            occurred_at timestamptz not null default clock_timestamp(),
            unique (aggregate_type, aggregate_id, aggregate_sequence),
            foreign key (aggregate_type, aggregate_id) references event_streams
        );
        create table aggregate_dispatch_cursors (
            aggregate_type text not null, aggregate_id uuid not null,
            last_sequence bigint not null default 0 check (last_sequence >= 0),
            failures integer not null default 0 check (failures between 0 and 8),
            blocked boolean not null default false,
            next_attempt_at timestamptz not null default '-infinity',
            primary key (aggregate_type, aggregate_id),
            foreign key (aggregate_type, aggregate_id) references event_streams
        );
        create index dispatch_runnable on aggregate_dispatch_cursors(next_attempt_at)
            where not blocked;
        create table event_handler_receipts (
            event_id uuid not null references domain_events,
            handler_name text not null,
            handler_version integer not null check (handler_version > 0),
            processed_at timestamptz not null default clock_timestamp(),
            primary key (event_id, handler_name, handler_version)
        );
        create function prevent_event_rewrite() returns trigger language plpgsql as $$
        begin
            raise exception 'Domain event evidence is immutable' using errcode='23514';
        end $$;
        create trigger domain_events_immutable before update or delete on domain_events
            for each row execute function prevent_event_rewrite();
    """)


def downgrade():
    op.execute("""
        drop table event_handler_receipts;
        drop table aggregate_dispatch_cursors;
        drop table domain_events;
        drop function prevent_event_rewrite();
        drop table event_streams;
    """)
