export const mockTimelineResponse = {
  items: [
    {
      id: 'decision:web-architecture',
      event_type: 'decision',
      title: 'Use a separated web architecture',
      description:
        'Build the dashboard with a Python API, SQLite persistence, and a React interface.',
      occurred_at: '2026-11-28T13:00:00Z',
      author: 'Group 13',
      source_label: 'DECISIONS.md',
      linked_pull_requests: [
        {
          id: 'link:11',
          pull_request_id: 'pr:11',
          number: 11,
          title: 'Complete Week 12 recovery artifacts',
          url: 'https://github.com/HaKkaz/NYCU-AI-in-the-Loop-in-Software-Project-Cycle/pull/11',
          status: 'confirmed',
        },
      ],
    },
    {
      id: 'pr:11',
      event_type: 'pull_request',
      title: 'Complete Week 12 recovery artifacts',
      description:
        'Makes the project direction, evaluation plan, and collaboration evidence visible.',
      occurred_at: '2026-11-25T09:31:11Z',
      author: 'u7chi',
      source_url:
        'https://github.com/HaKkaz/NYCU-AI-in-the-Loop-in-Software-Project-Cycle/pull/11',
    },
    {
      id: 'decision:initial-direction',
      event_type: 'decision',
      title: 'Explore a project-history dashboard',
      description:
        'Combine implementation history with human-authored decisions so teammates can recover context faster.',
      occurred_at: '2026-09-21T03:46:09Z',
      author: 'HaKkaz',
      source_label: 'DECISIONS.md',
      linked_pull_requests: [],
    },
    {
      id: 'pr:6',
      event_type: 'pull_request',
      title: 'Update the evaluation plan',
      description:
        'Adds the proposed comparison between normal repository navigation and the dashboard.',
      occurred_at: '2026-09-24T09:57:48Z',
      author: 'milktea7654',
      source_url:
        'https://github.com/HaKkaz/NYCU-AI-in-the-Loop-in-Software-Project-Cycle/pull/6',
    },
  ],
}

