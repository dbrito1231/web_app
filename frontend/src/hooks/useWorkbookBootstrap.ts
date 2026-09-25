import { useCallback, useEffect, useRef, useState } from 'react';
import { api, ensureSession } from '../api/client';
import type {
  ContentSummary,
  HeaderStats,
  Lab,
  ProgressSnapshot,
  ReadinessPayload,
} from '../types';
import { computeHeaderStatsFromIndex } from '../utils/progress';

const emptyProgress: ProgressSnapshot = {
  attemptCounts: { total: 0, examFirstAttempts: 0 },
  labCheckpoints: [],
  costEntryCount: 0,
  settingsKeys: [],
};

export function useWorkbookBootstrap() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [labLoadError, setLabLoadError] = useState<string | null>(null);
  const [summary, setSummary] = useState<ContentSummary | null>(null);
  const [progress, setProgress] = useState<ProgressSnapshot>(emptyProgress);
  const [readiness, setReadiness] = useState<ReadinessPayload | null>(null);
  const [labsById, setLabsById] = useState<Map<string, Lab>>(new Map());
  const [labsLoading, setLabsLoading] = useState(false);
  const labsStarted = useRef(false);
  const [headerStats, setHeaderStats] = useState<HeaderStats>({
    progressPercent: 0,
    stepsCompleted: 0,
    stepsTotal: 0,
    labsCompleted: 0,
    labsTotal: 0,
  });

  const refreshProgress = useCallback(async () => {
    const snap = await api.progress();
    setProgress(snap);
    return snap;
  }, []);

  const reloadLabs = useCallback(async (labIds: string[]) => {
    const map = new Map<string, Lab>();
    const failed: string[] = [];
    await Promise.all(
      labIds.map(async (id) => {
        try {
          const lab = await api.lab(id);
          map.set(id, lab);
        } catch {
          failed.push(id);
        }
      }),
    );
    setLabsById(map);
    setLabLoadError(
      failed.length
        ? `Could not load ${failed.length} lab${failed.length === 1 ? '' : 's'}: ${failed.slice(0, 3).join(', ')}`
        : null,
    );
    return map;
  }, []);

  const ensureLabs = useCallback(
    async (labIds: string[]) => {
      if (labsStarted.current) return;
      labsStarted.current = true;
      setLabsLoading(true);
      try {
        await reloadLabs(labIds);
      } finally {
        setLabsLoading(false);
      }
    },
    [reloadLabs],
  );

  const bootstrap = useCallback(async () => {
    setLoading(true);
    setError(null);
    labsStarted.current = false;
    setLabsById(new Map());
    try {
      await ensureSession();
      const [sum, prog, ready] = await Promise.all([
        api.contentSummary(),
        api.progress(),
        api.readiness(),
      ]);
      setSummary(sum);
      setProgress(prog);
      setReadiness(ready);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load workbook');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void bootstrap();
  }, [bootstrap]);

  useEffect(() => {
    if (!summary?.labIndex) return;
    setHeaderStats(computeHeaderStatsFromIndex(summary.labIndex, progress));
  }, [summary, progress]);

  const onProgressChange = useCallback(async () => {
    await refreshProgress();
    setReadiness(await api.readiness());
  }, [refreshProgress]);

  return {
    loading,
    error,
    labLoadError,
    labsLoading,
    ensureLabs,
    summary,
    progress,
    readiness,
    labsById,
    headerStats,
    refreshProgress: onProgressChange,
    reload: bootstrap,
  };
}
