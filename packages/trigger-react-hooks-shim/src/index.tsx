'use client';

import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from 'react';

/**
 * Minimal @trigger.dev/react-hooks replacement. `useRealtimeRun` / `useRun`
 * poll `${baseURL}/api/trigger/runs/:runId` (served by apps/app with the
 * user's session) every 2s until the run reaches a terminal status.
 */
export interface RealtimeRun<TTask = unknown> {
  id: string;
  taskIdentifier: string;
  status: string;
  payload?: unknown;
  output?: TTask extends { __output?: infer O } ? O : unknown;
  metadata?: Record<string, unknown>;
  error?: { message: string } | null;
  isCompleted: boolean;
  isSuccess: boolean;
  isFailed: boolean;
  createdAt?: string;
  finishedAt?: string;
}

interface AuthContextValue {
  accessToken?: string;
  baseURL?: string;
}

export const TriggerAuthContext = createContext<AuthContextValue>({});

export function TriggerProvider({
  children,
  ...value
}: AuthContextValue & { children: ReactNode }) {
  return <TriggerAuthContext.Provider value={value}>{children}</TriggerAuthContext.Provider>;
}

interface Options {
  accessToken?: string;
  baseURL?: string;
  enabled?: boolean;
  pollIntervalMs?: number;
  /** alias of pollIntervalMs (upstream name) */
  refreshInterval?: number;
  onComplete?: (run: any, error?: Error) => void;
}

const TERMINAL = new Set(['COMPLETED', 'FAILED', 'CANCELED', 'CRASHED', 'TIMED_OUT']);

export function useRealtimeRun<TTask = unknown>(runId?: string, options: Options = {}) {
  const ctx = useContext(TriggerAuthContext);
  const [run, setRun] = useState<RealtimeRun<TTask> | undefined>(undefined);
  const [error, setError] = useState<Error | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(Boolean(runId));
  const onCompleteRef = useRef(options.onComplete);
  onCompleteRef.current = options.onComplete;
  const enabled = options.enabled ?? true;
  const interval = options.pollIntervalMs ?? options.refreshInterval ?? 2000;
  const base = (options.baseURL ?? ctx.baseURL ?? '').replace(/\/$/, '');

  useEffect(() => {
    if (!runId || !enabled) return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;

    const tick = async () => {
      try {
        const res = await fetch(`${base}/api/trigger/runs/${encodeURIComponent(runId)}`, {
          credentials: 'include',
        });
        if (!res.ok) throw new Error(`run ${runId}: HTTP ${res.status}`);
        const data = (await res.json()) as RealtimeRun<TTask>;
        if (cancelled) return;
        setRun(data);
        setError(undefined);
        setIsLoading(false);
        if (TERMINAL.has(data.status)) {
          onCompleteRef.current?.(data as RealtimeRun);
          return;
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err : new Error(String(err)));
          setIsLoading(false);
        }
      }
      timer = setTimeout(tick, interval);
    };
    void tick();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [runId, enabled, interval, base]);

  return { run, error, isLoading, stop: () => undefined };
}

export const useRun = useRealtimeRun;

export function useRealtimeRunsWithTag() {
  return { runs: [] as RealtimeRun[], error: undefined };
}

export function useRealtimeBatch() {
  return { runs: [] as RealtimeRun[], error: undefined };
}

export function useTaskTrigger() {
  throw new Error(
    'useTaskTrigger is not supported by the self-hosted shim; trigger tasks server-side.',
  );
}
