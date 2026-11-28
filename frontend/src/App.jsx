import { useTimeline } from './timeline/useTimeline.js'

function formatTimestamp(value) {
  return new Intl.DateTimeFormat('en', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export default function App() {
  const { events, error, isLoading, isRefreshing, lastUpdatedAt, refresh } =
    useTimeline()

  return (
    <main className="foundation-shell">
      <header className="foundation-header">
        <div>
          <span className="eyebrow">Group 13 · Frontend foundation</span>
          <h1>Project Trace</h1>
          <p>
            The timeline data client is running. The browsing interface lands in the
            follow-up UI pull request.
          </p>
        </div>
        <button type="button" onClick={refresh} disabled={isLoading || isRefreshing}>
          {isRefreshing ? 'Refreshing…' : 'Refresh timeline'}
        </button>
      </header>

      <section className="foundation-panel" aria-labelledby="timeline-heading">
        <div className="panel-heading">
          <div>
            <span className="sync-dot" aria-hidden="true" />
            <span>
              {lastUpdatedAt
                ? `Updated ${lastUpdatedAt.toLocaleTimeString()}`
                : 'Waiting for first sync'}
            </span>
          </div>
          <strong>{events.length} events</strong>
        </div>

        <h2 id="timeline-heading">Timeline data</h2>

        {error && (
          <div className="error-message" role="alert">
            <span>{error}</span>
            <button type="button" onClick={refresh}>Try again</button>
          </div>
        )}

        {isLoading ? (
          <p role="status">Loading project history…</p>
        ) : (
          <ul className="event-list">
            {events.map((event) => (
              <li key={event.id}>
                <span className={`event-type event-type--${event.type}`}>
                  {event.type === 'decision' ? 'Decision' : 'Pull request'}
                </span>
                <div>
                  <strong>{event.title}</strong>
                  <small>
                    {event.author} · {formatTimestamp(event.occurredAt)}
                  </small>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  )
}

