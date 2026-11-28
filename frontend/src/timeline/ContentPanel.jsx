const typeLabels = {
  decision: 'Decision record',
  pull_request: 'Pull request',
}

function formatDate(value) {
  return new Intl.DateTimeFormat('en', {
    dateStyle: 'long',
    timeStyle: 'short',
  }).format(new Date(value))
}

function StatusPill({ status }) {
  const label = status.replaceAll('_', ' ')
  return <span className={`status-pill status-pill--${status}`}>{label}</span>
}

export default function ContentPanel({ event }) {
  if (!event) {
    return (
      <aside className="content-panel content-panel--empty">
        <span className="content-panel__empty-icon">↖</span>
        <h2>Select an event</h2>
        <p>Choose a decision or pull request to inspect its context.</p>
      </aside>
    )
  }

  return (
    <aside className="content-panel" aria-label="Selected event details">
      <div className="content-panel__type">{typeLabels[event.type]}</div>
      <h2>{event.title}</h2>
      <div className="content-panel__facts">
        <span>{event.author}</span>
        <span aria-hidden="true">·</span>
        <time dateTime={event.occurredAt}>{formatDate(event.occurredAt)}</time>
      </div>

      <p className="content-panel__summary">
        {event.summary || 'No additional description was provided.'}
      </p>

      {event.sourceUrl ? (
        <a className="source-link" href={event.sourceUrl} target="_blank" rel="noreferrer">
          {event.sourceLabel}
          <span aria-hidden="true">↗</span>
        </a>
      ) : (
        <div className="source-label">Source: {event.sourceLabel}</div>
      )}

      {event.type === 'decision' && (
        <section className="related-section" aria-labelledby="related-title">
          <div className="related-section__heading">
            <h3 id="related-title">Related pull requests</h3>
            <span>{event.linkedPullRequests.length}</span>
          </div>

          {event.linkedPullRequests.length === 0 ? (
            <p className="related-section__empty">
              No implementation has been linked to this decision yet.
            </p>
          ) : (
            <ul className="related-list">
              {event.linkedPullRequests.map((pullRequest) => (
                <li key={pullRequest.id || pullRequest.pullRequestId}>
                  <div>
                    <span className="related-list__number">
                      {pullRequest.number ? `#${pullRequest.number}` : 'PR'}
                    </span>
                    {pullRequest.url ? (
                      <a href={pullRequest.url} target="_blank" rel="noreferrer">
                        {pullRequest.title}
                      </a>
                    ) : (
                      <span>{pullRequest.title}</span>
                    )}
                  </div>
                  <StatusPill status={pullRequest.status} />
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </aside>
  )
}

