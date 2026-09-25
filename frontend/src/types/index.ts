export type TabId = 'labs' | 'exam' | 'coverage' | 'start';

export interface LabStep {
  id: string;
  title: string;
  body?: string;
  bullets?: string[];
}

export interface LabCheckpoint {
  id: string;
  label: string;
}

export interface LabTeardown {
  labId?: string;
  regionScope?: string;
  orderedDeletesPowerShell?: string[];
  verification?: string[];
  stillBillingNote?: string;
  recovery?: string;
}

export interface Lab {
  id: string;
  title: string;
  kind?: string;
  difficulty?: string;
  practiceMode?: string;
  estimatedMinutes?: number;
  costSameHour?: string;
  sameHourEstimateUsd?: number;
  forgotten24hEstimateUsd?: number;
  region?: string;
  doneWhen?: string;
  beforeYouStart?: string | string[];
  stopChargesPanel?: string;
  body?: string;
  steps?: LabStep[];
  checkpoints?: LabCheckpoint[];
  teardown?: LabTeardown;
  requiresCostRisk?: boolean;
  scenario?: string;
  acceptanceCriteria?: string[];
  hints?: { level: number; text: string }[];
  rubric?: string[];
}

export interface QuestionChoice {
  id: string;
  text: string;
}

export interface Question {
  id: string;
  type: 'mc' | 'mr';
  stem: string;
  promptNote?: string;
  selectCount?: number;
  choices: QuestionChoice[];
  module?: string;
  difficulty?: string;
  objectiveIds?: string[];
}

export interface AttemptResult {
  correct: boolean;
  rationale: string;
  objectiveIds: string[];
}

export interface ProgressSnapshot {
  attemptCounts: { total: number; examFirstAttempts: number };
  labCheckpoints: Array<{
    lab_id: string;
    checkpoint_id: string;
    status: string;
  }>;
  costEntryCount: number;
  settingsKeys: string[];
  bestByQuestion?: Record<string, number>;
}

export interface LessonIndexRow {
  id: string;
  title: string;
  drillIds?: string[];
  objectiveIds?: string[];
}

export interface LabIndexRow {
  id: string;
  title: string;
  objectiveIds: string[];
  stepIds: string[];
}

export interface ExerciseIndexRow {
  id: string;
  title: string;
  objectiveIds: string[];
  scenario: string;
}

export interface ContentSummary {
  lessons: string[];
  lessonIndex?: LessonIndexRow[];
  questions: string[];
  labs: string[];
  labIndex?: LabIndexRow[];
  exerciseIndex?: ExerciseIndexRow[];
}

export interface QuestionCatalogRow {
  id: string;
  module?: string;
  type: 'mc' | 'mr';
  stem?: string;
  selectCount?: number;
}

export interface CoverageRow {
  objective_id: string;
  task_id: string;
  domain_id: string;
  source_text: string;
  status: string;
  practice_mode: string | null;
}

export interface CoveragePayload {
  schemaVersion: number;
  total: number;
  rows: CoverageRow[];
}

export interface ReadinessTrack {
  status: 'insufficient_evidence' | 'ok';
  message?: string;
  readiness?: number;
  firstAttemptCount?: number;
  missingPerBucket?: Record<string, number>;
  components?: Record<string, unknown>;
  caption?: string;
  groupWeightNote?: string;
}

export interface ReadinessPayload {
  aws: ReadinessTrack;
  terraform: ReadinessTrack;
}

export interface Lesson {
  id: string;
  title: string;
  module?: string;
  bodyMarkdown?: string;
  drillIds?: string[];
  labIds?: string[];
  objectiveIds?: string[];
}

export interface HeaderStats {
  progressPercent: number;
  stepsCompleted: number;
  stepsTotal: number;
  labsCompleted: number;
  labsTotal: number;
}
