"""Identity, revocable sessions and private profile preferences."""

from alembic import op

revision = "0002_identity"
down_revision = "0001_platform"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE users (
      id uuid PRIMARY KEY, phone_e164 text NOT NULL UNIQUE,
      first_name text, last_name text, impact_statement text NOT NULL DEFAULT '',
      status text NOT NULL DEFAULT 'ACTIVE'
        CHECK (status IN ('ACTIVE','SUSPENDED','DELETION_PENDING')),
      version bigint NOT NULL DEFAULT 1 CHECK (version > 0),
      created_at timestamptz NOT NULL DEFAULT now()
    );
    CREATE TABLE user_roles (
      user_id uuid NOT NULL REFERENCES users(id), role text NOT NULL
        CHECK (role IN ('contributor','volunteer','org_admin','ops_agent','ops_lead',
                       'finance','super_admin')),
      organization_id uuid, granted_by uuid REFERENCES users(id),
      granted_at timestamptz NOT NULL DEFAULT now(),
      CHECK ((role = 'org_admin') = (organization_id IS NOT NULL)),
      UNIQUE NULLS NOT DISTINCT (user_id,role,organization_id)
    );
    CREATE TABLE auth_limits (
      scope text PRIMARY KEY, window_start timestamptz NOT NULL DEFAULT now(),
      requests integer NOT NULL DEFAULT 0 CHECK (requests >= 0),
      next_allowed timestamptz NOT NULL DEFAULT '-infinity',
      locked_until timestamptz NOT NULL DEFAULT '-infinity'
    );
    CREATE TABLE auth_challenges (
      id uuid PRIMARY KEY, phone_e164 text NOT NULL, phone_scope text NOT NULL,
      device_id uuid NOT NULL, client_kind text NOT NULL CHECK(client_kind IN ('mobile','web')),
      code_hash text NOT NULL, expires_at timestamptz NOT NULL,
      attempts integer NOT NULL DEFAULT 0 CHECK(attempts BETWEEN 0 AND 5),
      consumed_at timestamptz, created_at timestamptz NOT NULL DEFAULT now()
    );
    CREATE INDEX auth_challenges_phone ON auth_challenges(phone_scope);
    CREATE TABLE auth_sessions (
      id uuid PRIMARY KEY, user_id uuid NOT NULL REFERENCES users(id),
      device_id uuid NOT NULL, client_kind text NOT NULL CHECK(client_kind IN ('mobile','web')),
      expires_at timestamptz NOT NULL, revoked_at timestamptz,
      version bigint NOT NULL DEFAULT 1 CHECK(version > 0),
      created_at timestamptz NOT NULL DEFAULT now()
    );
    CREATE INDEX auth_sessions_owner ON auth_sessions(user_id);
    CREATE TABLE refresh_tokens (
      token_hash text PRIMARY KEY, session_id uuid NOT NULL REFERENCES auth_sessions(id),
      consumed_at timestamptz, created_at timestamptz NOT NULL DEFAULT now()
    );
    CREATE TABLE privacy_preferences (
      user_id uuid PRIMARY KEY REFERENCES users(id),
      profile_public boolean NOT NULL DEFAULT false,
      contributions_public boolean NOT NULL DEFAULT false,
      impact_sharing boolean NOT NULL DEFAULT false,
      version bigint NOT NULL DEFAULT 1 CHECK(version > 0)
    );
    """)


def downgrade():
    op.execute("""
    DROP TABLE privacy_preferences, refresh_tokens, auth_sessions,
      auth_challenges, auth_limits, user_roles, users;
    """)
