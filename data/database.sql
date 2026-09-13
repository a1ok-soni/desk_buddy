
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ
);

CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    role TEXT NOT NULL CHECK (role IN ('system', 'user', 'assistant', 'tool')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID REFERENCES users(id),

    content TEXT NOT NULL,

    memory_type TEXT NOT NULL,
    
    importance REAL DEFAULT 0.5
        CHECK (importance >= 0 AND importance <= 1),

    source TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    last_accessed_at TIMESTAMPTZ
);

CREATE TABLE preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID REFERENCES users(id),

    key TEXT NOT NULL,
    value JSONB NOT NULL,

    confidence REAL DEFAULT 1.0
        CHECK (confidence >= 0 AND confidence <= 1),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(user_id, key)
);

CREATE TABLE reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID REFERENCES users(id),

    title TEXT NOT NULL,
    description TEXT,

    due_at TIMESTAMPTZ NOT NULL,

    completed BOOLEAN DEFAULT FALSE,
    cancelled BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID REFERENCES users(id),

    title TEXT NOT NULL,
    description TEXT,

    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),

    priority INTEGER DEFAULT 3,

    due_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE robot_state (
    id INTEGER PRIMARY KEY DEFAULT 1,

    battery_percent REAL,
    location_x REAL,
    location_y REAL,
    location_z REAL,

    docked BOOLEAN DEFAULT FALSE,

    current_activity TEXT,

    updated_at TIMESTAMPTZ DEFAULT NOW()
);


CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID REFERENCES users(id),

    event_type TEXT NOT NULL,
    description TEXT,

    event_time TIMESTAMPTZ DEFAULT NOW(),

    metadata JSONB
);
