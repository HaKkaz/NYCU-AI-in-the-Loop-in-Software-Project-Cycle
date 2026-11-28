import { useCallback, useEffect, useRef, useState } from 'react'
import { getTimeline } from './timelineApi.js'

export const DEFAULT_POLL_INTERVAL = 5_000

export function useTimeline({ pollInterval = DEFAULT_POLL_INTERVAL } = {}) {
  const [events, setEvents] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [error, setError] = useState(null)
  const [lastUpdatedAt, setLastUpdatedAt] = useState(null)
  const controllerRef = useRef(null)
  const hasLoadedRef = useRef(false)

  const loadTimeline = useCallback(async () => {
    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller

    if (hasLoadedRef.current) setIsRefreshing(true)
    else setIsLoading(true)

    try {
      const nextEvents = await getTimeline({ signal: controller.signal })
      setEvents(nextEvents)
      setError(null)
      setLastUpdatedAt(new Date())
      hasLoadedRef.current = true
    } catch (nextError) {
      if (nextError.name !== 'AbortError') {
        setError(nextError.message || 'Unable to load the project timeline.')
      }
    } finally {
      if (controllerRef.current === controller) {
        setIsLoading(false)
        setIsRefreshing(false)
      }
    }
  }, [])

  useEffect(() => {
    loadTimeline()
    const intervalId = window.setInterval(loadTimeline, pollInterval)

    return () => {
      window.clearInterval(intervalId)
      controllerRef.current?.abort()
    }
  }, [loadTimeline, pollInterval])

  return {
    events,
    error,
    isLoading,
    isRefreshing,
    lastUpdatedAt,
    refresh: loadTimeline,
  }
}

