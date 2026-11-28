import { mockTimelineResponse } from './timelineMock.js'

const TIMELINE_ENDPOINT = '/api/timeline'
const MOCK_DELAY_MS = 180

function normalizeType(value) {
  if (value === 'pr' || value === 'pull-request') return 'pull_request'
  if (value === 'pull_request' || value === 'decision') return value
  return 'decision'
}

function normalizeLink(link) {
  return {
    id: String(link.id ?? link.link_id ?? ''),
    pullRequestId: String(
      link.pullRequestId ??
        link.pull_request_id ??
        link.pr_id ??
        link.pull_request?.id ??
        '',
    ),
    number: link.number ?? link.pr_number ?? link.pull_request?.number ?? null,
    title: link.title ?? link.pull_request?.title ?? 'Related pull request',
    url: link.url ?? link.html_url ?? link.pull_request?.url ?? null,
    status: link.status ?? 'pending',
  }
}

function attachTopLevelLinks(items, links = []) {
  const linksByDecision = new Map()

  for (const link of links) {
    const decisionId = String(link.decision_id ?? link.decision?.id ?? '')
    if (!decisionId) continue
    const existing = linksByDecision.get(decisionId) ?? []
    existing.push(normalizeLink(link))
    linksByDecision.set(decisionId, existing)
  }

  return items.map((item) => {
    if (normalizeType(item.event_type ?? item.type) !== 'decision') return item
    const itemId = String(item.id ?? item.decision_id ?? '')
    return {
      ...item,
      linked_pull_requests:
        item.linked_pull_requests ?? item.links ?? linksByDecision.get(itemId) ?? [],
    }
  })
}

function extractItems(payload) {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.items)) return payload.items
  if (Array.isArray(payload?.events)) return payload.events

  const decisions = (payload?.decisions ?? []).map((decision) => ({
    ...decision,
    event_type: 'decision',
  }))
  const pullRequests = (payload?.pull_requests ?? payload?.prs ?? []).map(
    (pullRequest) => ({
      ...pullRequest,
      event_type: 'pull_request',
    }),
  )

  return attachTopLevelLinks([...decisions, ...pullRequests], payload?.links)
}

function normalizeEvent(event, index) {
  const type = normalizeType(event.event_type ?? event.type)
  const occurredAt =
    event.occurred_at ??
    event.merged_at ??
    event.created_at ??
    event.date ??
    new Date(0).toISOString()

  return {
    id: String(event.id ?? event.event_id ?? `${type}:${index}`),
    type,
    title:
      event.title ??
      event.name ??
      (type === 'decision' ? 'Untitled decision' : 'Untitled pull request'),
    summary: event.description ?? event.summary ?? event.body ?? '',
    occurredAt,
    author: event.author?.login ?? event.author ?? event.owner ?? 'Unknown',
    sourceUrl: event.source_url ?? event.html_url ?? event.url ?? null,
    sourceLabel:
      event.source_label ??
      (type === 'decision' ? 'DECISIONS.md' : 'View on GitHub'),
    linkedPullRequests: (
      event.linked_pull_requests ??
      event.links ??
      []
    ).map(normalizeLink),
  }
}

export function normalizeTimelineResponse(payload) {
  return extractItems(payload)
    .map(normalizeEvent)
    .sort((left, right) => {
      return new Date(right.occurredAt) - new Date(left.occurredAt)
    })
}

function waitForMock(signal) {
  return new Promise((resolve, reject) => {
    const timeoutId = window.setTimeout(resolve, MOCK_DELAY_MS)
    signal?.addEventListener(
      'abort',
      () => {
        window.clearTimeout(timeoutId)
        reject(new DOMException('Request aborted', 'AbortError'))
      },
      { once: true },
    )
  })
}

export async function getTimeline({ signal } = {}) {
  if (import.meta.env.VITE_USE_MOCK_API === 'true') {
    await waitForMock(signal)
    return normalizeTimelineResponse(mockTimelineResponse)
  }

  const response = await fetch(TIMELINE_ENDPOINT, {
    headers: { Accept: 'application/json' },
    signal,
  })

  if (!response.ok) {
    const detail = await response.json().catch(() => null)
    throw new Error(detail?.detail ?? `Timeline request failed (${response.status})`)
  }

  return normalizeTimelineResponse(await response.json())
}

