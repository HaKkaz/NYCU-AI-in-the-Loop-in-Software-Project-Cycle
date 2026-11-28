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
    at      DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),

    -- F6/F7: SQLite trim() alone only strips ASCII spaces. Match Python str.strip()
    -- so tabs, newlines, and full-width spaces also count as a blank comment.
    CHECK (
        action NOT IN ('dispute', 'respond') OR (
            comment IS NOT NULL AND trim(comment, char(
                0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x1C, 0x1D, 0x1E, 0x1F, 0x20,
                0x85, 0xA0, 0x1680, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004,
                0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x2028, 0x2029,
                0x202F, 0x205F, 0x3000
            )) <> ''
        )
    )
);

CREATE INDEX ix_link_event_link_id ON link_event (link_id);
