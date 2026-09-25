import type { HeaderStats, Lab, LabIndexRow, LabStep, ProgressSnapshot } from '../types';

export function checkpointMap(progress: ProgressSnapshot): Map<string, string> {
  const map = new Map<string, string>();
  for (const row of progress.labCheckpoints) {
    map.set(`${row.lab_id}:${row.checkpoint_id}`, row.status);
  }
  return map;
}

export function labChecklist(lab: Lab): LabStep[] {
  if (lab.steps && lab.steps.length > 0) return lab.steps;
  return (lab.acceptanceCriteria ?? []).map((text, index) => ({
    id: `c${String(index + 1).padStart(2, '0')}`,
    title: text,
  }));
}

export function labStepProgress(
  lab: Lab,
  progress: ProgressSnapshot,
): { completed: number; total: number; status: 'not-started' | 'in-progress' | 'complete' } {
  const steps = labChecklist(lab);
  const map = checkpointMap(progress);
  let completed = 0;
  for (const step of steps) {
    if (map.get(`${lab.id}:${step.id}`) === 'self-reported') {
      completed += 1;
    }
  }
  const total = steps.length;
  let status: 'not-started' | 'in-progress' | 'complete' = 'not-started';
  if (total > 0 && completed >= total) status = 'complete';
  else if (completed > 0) status = 'in-progress';
  return { completed, total, status };
}

export function computeHeaderStatsFromIndex(
  labs: LabIndexRow[],
  progress: ProgressSnapshot,
): HeaderStats {
  const map = checkpointMap(progress);
  let stepsCompleted = 0;
  let stepsTotal = 0;
  let labsCompleted = 0;
  for (const lab of labs) {
    const completed = lab.stepIds.filter(
      (stepId) => map.get(`${lab.id}:${stepId}`) === 'self-reported',
    ).length;
    stepsCompleted += completed;
    stepsTotal += lab.stepIds.length;
    if (lab.stepIds.length > 0 && completed >= lab.stepIds.length) labsCompleted += 1;
  }
  const progressPercent =
    stepsTotal > 0 ? Math.round((stepsCompleted / stepsTotal) * 100) : 0;
  return {
    progressPercent,
    stepsCompleted,
    stepsTotal,
    labsCompleted,
    labsTotal: labs.length,
  };
}

export function computeHeaderStats(
  labsById: Map<string, Lab>,
  progress: ProgressSnapshot,
): HeaderStats {
  let stepsCompleted = 0;
  let stepsTotal = 0;
  let labsCompleted = 0;
  const labsTotal = labsById.size;

  for (const lab of labsById.values()) {
    const { completed, total, status } = labStepProgress(lab, progress);
    stepsCompleted += completed;
    stepsTotal += total;
    if (status === 'complete') labsCompleted += 1;
  }

  const progressPercent =
    stepsTotal > 0 ? Math.round((stepsCompleted / stepsTotal) * 100) : 0;

  return { progressPercent, stepsCompleted, stepsTotal, labsCompleted, labsTotal };
}

export function shuffle<T>(items: T[]): T[] {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}
