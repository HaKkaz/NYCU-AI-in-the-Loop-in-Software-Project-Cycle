import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import Timeline from './Timeline.jsx'

const events = [
  {
    id: 'decision:1',
    type: 'decision',
    title: 'Choose SQLite',
    summary: 'Keep local setup simple.',
    occurredAt: '2026-11-28T13:00:00Z',
    author: 'iris2617',
    linkedPullRequests: [],
  },
]

describe('Timeline', () => {
  it('renders events and reports selection', async () => {
    const user = userEvent.setup()
    const onSelect = vi.fn()
    render(<Timeline events={events} selectedId={null} onSelect={onSelect} />)

    await user.click(screen.getByRole('button', { name: /choose sqlite/i }))

    expect(onSelect).toHaveBeenCalledWith('decision:1')
    expect(screen.getByText('Keep local setup simple.')).toBeInTheDocument()
  })

  it('shows an empty state when filters match nothing', () => {
    render(<Timeline events={[]} selectedId={null} onSelect={() => {}} />)

    expect(screen.getByRole('status')).toHaveTextContent('No matching events')
  })
})
