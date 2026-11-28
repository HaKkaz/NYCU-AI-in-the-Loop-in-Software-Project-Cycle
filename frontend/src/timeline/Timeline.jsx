const typeLabels = {
  decision: 'Decision',
  pull_request: 'Pull request',
}

const typeIcons = {
  decision: 'D',
  pull_request: 'PR',
}

function formatDate(value) {
  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

export default function Timeline({ events, selectedId, onSelect }) {
  if (events.length === 0) {
    return (
      <div className="empty-state" role="status">
        <div className="empty-state__mark">0</div>
        <h2>No matching events</h2>
        <p>Try a different search or event filter.</p>
      </div>
    )
  }

  return (
    <ol className="timeline" aria-label="Project history events">
      {events.map((event) => {
        const isSelected = event.id === selectedId
        return (
          <li className={`timeline__item timeline__item--${event.type}`} key={event.id}>
            <span className="timeline__rail" aria-hidden="true" />
            <button
              className={`event-card${isSelected ? ' event-card--selected' : ''}`}
              type="button"
              aria-pressed={isSelected}
              onClick={() => onSelect(event.id)}
            >
              <span className={`event-card__icon event-card__icon--${event.type}`}>
                {typeIcons[event.type]}
              </span>
              <span className="event-card__body">
                <span className="event-card__eyebrow">
                  <span>{typeLabels[event.type]}</span>
                  <time dateTime={event.occurredAt}>{formatDate(event.occurredAt)}</time>
                </span>
                <strong>{event.title}</strong>
                <span className="event-card__summary">
                  {event.summary || 'No additional description.'}
                </span>
                <span className="event-card__meta">
                  <span>by {event.author}</span>
                  {event.linkedPullRequests.length > 0 && (
                    <span className="link-count">
                      {event.linkedPullRequests.length} linked PR
                      {event.linkedPullRequests.length === 1 ? '' : 's'}
                    </span>
                  )}
                </span>
              </span>
            </button>
          </li>
        )
      })}
    </ol>
  )
}

