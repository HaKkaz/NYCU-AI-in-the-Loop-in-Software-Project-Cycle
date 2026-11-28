-- F9: one creation per link. If legacy data has duplicates, fail the upgrade
-- without discarding any history. The runner reports the integrity error.
CREATE UNIQUE INDEX uq_link_event_create ON link_event (link_id)
WHERE action = 'create';

-- A missing creation can be recovered from the link itself. Keep every existing
-- event (including its actor, timestamp, and optional comment) intact.
INSERT INTO link_event (link_id, actor, action, at)
SELECT link.id, link.created_by, 'create', link.created_at
FROM link
WHERE NOT EXISTS (
    SELECT 1 FROM link_event
    WHERE link_event.link_id = link.id AND link_event.action = 'create'
);

-- Preserve a timestamp supplied by the backend in the same UPDATE. Otherwise,
-- set updated_at when the stored status actually changes.
CREATE TRIGGER link_status_updated_at
AFTER UPDATE OF status ON link
WHEN NEW.status <> OLD.status AND NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE link
    SET updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
    WHERE id = NEW.id;
END;
