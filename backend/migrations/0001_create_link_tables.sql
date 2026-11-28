-- §8: decisions and PRs are loaded from GitHub. Only their identifiers are stored.
CREATE TABLE link (
    id          INTEGER PRIMARY KEY,
    decision_id TEXT NOT NULL,
    pr_number   INTEGER NOT NULL CHECK (typeof(pr_number) = 'integer' AND pr_number > 0),
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'confirmed', 'disputed', 'withdrawn')),
    created_by  TEXT NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at  DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- F4/F8: withdrawing a link releases the pair without deleting its history.
CREATE UNIQUE INDEX uq_link_active_pair ON link (decision_id, pr_number)
WHERE status <> 'withdrawn';

CREATE TABLE link_event (
    id      INTEGER PRIMARY KEY,
    link_id INTEGER NOT NULL REFERENCES link(id) ON DELETE RESTRICT,
    actor   TEXT NOT NULL,
    action  TEXT NOT NULL CHECK (action IN ('create', 'confirm', 'dispute', 'respond', 'withdraw')),
    comment TEXT,
    at      DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX ix_link_event_link_id ON link_event (link_id);
