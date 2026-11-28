import { useEffect, useMemo, useState } from 'react'
import ContentPanel from './timeline/ContentPanel.jsx'
import Timeline from './timeline/Timeline.jsx'
import { useTimeline } from './timeline/useTimeline.js'

const filters = [
  { value: 'all', label: 'All events' },
  { value: 'decision', label: 'Decisions' },
  { value: 'pull_request', label: 'Pull requests' },
]

function formatUpdatedAt(value) {
  if (!value) return 'Waiting for first sync'
  return `Updated ${new Intl.DateTimeFormat('en', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(value)}`
}

export default function App() {
  const { events, error, isLoading, isRefreshing, lastUpdatedAt, refresh } =
    useTimeline()
  const [activeFilter, setActiveFilter] = useState('all')
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState(null)

  const filteredEvents = useMemo(() => {
    const normalizedQuery = query.trim().toLocaleLowerCase()
    return events.filter((event) => {
      const matchesType = activeFilter === 'all' || event.type === activeFilter
      const matchesQuery =
        normalizedQuery.length === 0 ||
        `${event.title} ${event.summary} ${event.author}`
          .toLocaleLowerCase()
          .includes(normalizedQuery)
      return matchesType && matchesQuery
    })
  }, [activeFilter, events, query])

  useEffect(() => {
    if (filteredEvents.length === 0) {
      setSelectedId(null)
      return
    }

    if (!filteredEvents.some((event) => event.id === selectedId)) {
      setSelectedId(filteredEvents[0].id)
    }
  }, [filteredEvents, selectedId])

  const selectedEvent =
    filteredEvents.find((event) => event.id === selectedId) ?? null
  const decisionCount = events.filter((event) => event.type === 'decision').length
  const pullRequestCount = events.filter(
    (event) => event.type === 'pull_request',
  ).length
  const linkCount = events.reduce(
    (total, event) => total + event.linkedPullRequests.length,
    0,
  )

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Project Trace home">
          <span className="brand__mark" aria-hidden="true">
            PT
          </span>
          <span>
            <strong>Project Trace</strong>
            <small>History, with the why attached.</small>
          </span>
        </a>
        <div className="sync-state" aria-live="polite">
          <span className={isRefreshing ? 'sync-dot sync-dot--active' : 'sync-dot'} />
          <span>{isRefreshing ? 'Syncing timeline…' : formatUpdatedAt(lastUpdatedAt)}</span>
          <button type="button" onClick={refresh} disabled={isLoading || isRefreshing}>
            Refresh
          </button>
        </div>
      </header>

      <main id="top">
        <section className="hero">
          <div>
            <span className="hero__kicker">Group 13 · Project history</span>
            <h1>See what changed.<br />Understand why.</h1>
            <p>
              Decisions and pull requests in one shared timeline, so context does not
              disappear between files and tabs.
            </p>
          </div>
          <dl className="stats" aria-label="Timeline summary">
            <div>
              <dt>Decisions</dt>
              <dd>{decisionCount}</dd>
            </div>
            <div>
              <dt>Pull requests</dt>
              <dd>{pullRequestCount}</dd>
            </div>
            <div>
              <dt>Links</dt>
              <dd>{linkCount}</dd>
            </div>
          </dl>
        </section>

        <section className="workspace" aria-labelledby="workspace-title">
          <div className="workspace__header">
            <div>
              <span className="section-label">Timeline</span>
              <h2 id="workspace-title">Project activity</h2>
            </div>
            <label className="search-field">
              <span className="sr-only">Search timeline</span>
              <span aria-hidden="true">⌕</span>
              <input
                type="search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search title, context, or author"
              />
            </label>
          </div>

          <div className="filter-row" aria-label="Filter timeline">
            {filters.map((filter) => (
              <button
                type="button"
                className={activeFilter === filter.value ? 'filter-chip filter-chip--active' : 'filter-chip'}
                aria-pressed={activeFilter === filter.value}
                onClick={() => setActiveFilter(filter.value)}
                key={filter.value}
              >
                {filter.label}
              </button>
            ))}
          </div>

          {error && (
            <div className="error-banner" role="alert">
              <span>{error}</span>
              <button type="button" onClick={refresh}>Try again</button>
            </div>
          )}

          <div className="workspace__grid">
            <div className="timeline-pane">
              {isLoading ? (
                <div className="loading-state" role="status">
                  <span className="loader" aria-hidden="true" />
                  <span>Loading project history…</span>
                </div>
              ) : (
                <Timeline
                  events={filteredEvents}
                  selectedId={selectedId}
                  onSelect={setSelectedId}
                />
              )}
            </div>
            <ContentPanel event={selectedEvent} />
          </div>
        </section>
      </main>
    </div>
  )
}

