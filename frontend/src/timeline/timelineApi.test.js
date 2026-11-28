import { describe, expect, it } from 'vitest'
import { normalizeTimelineResponse } from './timelineApi.js'

describe('normalizeTimelineResponse', () => {
  it('combines decisions, pull requests, and top-level links', () => {
    const events = normalizeTimelineResponse({
      decisions: [
        {
          id: 'decision:1',
          title: 'Choose SQLite',
          date: '2026-11-20T09:00:00Z',
          author: 'iris2617',
        },
      ],
      pull_requests: [
        {
          id: 'pr:14',
          number: 14,
          title: 'Add schema',
          created_at: '2026-11-21T09:00:00Z',
          author: { login: 'iris2617' },
        },
      ],
      links: [
        {
          id: 3,
          decision_id: 'decision:1',
          pull_request_id: 'pr:14',
          pr_number: 14,
          title: 'Add schema',
          status: 'confirmed',
        },
      ],
    })

    expect(events).toHaveLength(2)
    expect(events[0]).toMatchObject({
      id: 'pr:14',
      type: 'pull_request',
      author: 'iris2617',
    })
    expect(events[1].linkedPullRequests[0]).toMatchObject({
      pullRequestId: 'pr:14',
      status: 'confirmed',
    })
  })

  it('accepts an items response and sorts it newest first', () => {
    const events = normalizeTimelineResponse({
      items: [
        {
          id: 'decision:old',
          event_type: 'decision',
          title: 'Old decision',
          occurred_at: '2026-09-01T00:00:00Z',
        },
        {
          id: 'pr:new',
          event_type: 'pr',
          title: 'New PR',
          occurred_at: '2026-11-01T00:00:00Z',
        },
      ],
    })

    expect(events.map((event) => event.id)).toEqual(['pr:new', 'decision:old'])
    expect(events[0].type).toBe('pull_request')
  })
})

