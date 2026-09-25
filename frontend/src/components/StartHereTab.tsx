import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { ExerciseIndexRow, LabIndexRow, Lesson, ReadinessPayload } from '../types';
import { MarkdownBody } from '../utils/markdown';

interface StartHereTabProps {
  readiness: ReadinessPayload | null;
  onReload: () => void;
}

function RelatedPractice({
  objectiveIds,
  labs,
  exercises,
}: {
  objectiveIds: string[];
  labs: LabIndexRow[];
  exercises: ExerciseIndexRow[];
}) {
  const objectives = new Set(objectiveIds);
  const relatedLabs = labs.filter((lab) => lab.objectiveIds.some((id) => objectives.has(id)));
  const relatedExercises = exercises.filter((item) =>
    item.objectiveIds.some((id) => objectives.has(id)),
  );
  if (relatedLabs.length === 0 && relatedExercises.length === 0) return null;
  return (
    <>
      {relatedLabs.length > 0 && (
        <>
          <h3>Labs for this lesson</h3>
          <ul>
            {relatedLabs.map((lab) => (
              <li key={lab.id}>
                <a href={`/labs?lab=${encodeURIComponent(lab.id)}`}>{lab.title}</a>
              </li>
            ))}
          </ul>
        </>
      )}
      {relatedExercises.length > 0 && (
        <>
          <h3>Design exercises for this lesson</h3>
          <ul>
            {relatedExercises.map((item) => (
              <li key={item.id}>
                <strong>{item.title}</strong>
                {item.scenario ? <p>{item.scenario}</p> : null}
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}

export function StartHereTab({ readiness, onReload }: StartHereTabProps) {
  const [lessonIndex, setLessonIndex] = useState<Array<{ id: string; title: string }>>([
    { id: 'a0-lab-safety', title: 'A0 — Lab safety' },
  ]);
  const [labIndex, setLabIndex] = useState<LabIndexRow[]>([]);
  const [exerciseIndex, setExerciseIndex] = useState<ExerciseIndexRow[]>([]);
  const [lessonId, setLessonId] = useState(
    () => new URLSearchParams(window.location.search).get('lesson') || 'a0-lab-safety',
  );
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [importText, setImportText] = useState('');
  const [resetText, setResetText] = useState('');
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [payload, summary] = await Promise.all([
          api.lesson(lessonId),
          api.contentSummary(),
        ]);
        if (!cancelled) {
          setLesson(payload);
          if (summary.lessonIndex?.length) setLessonIndex(summary.lessonIndex);
          else if (summary.lessons.length) {
            setLessonIndex(summary.lessons.map((id) => ({ id, title: id })));
          }
          setLabIndex(summary.labIndex ?? []);
          setExerciseIndex(summary.exerciseIndex ?? []);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : 'Could not load A0 lesson');
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [lessonId]);

  const exportProgress = async () => {
    setMessage(null);
    try {
      const data = await api.exportProgress();
      const text = JSON.stringify(data, null, 2);
      setImportText(text);
      const blob = new Blob([text], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'workbook-progress.json';
      a.rel = 'noopener noreferrer';
      a.click();
      URL.revokeObjectURL(url);
      setMessage('Exported workbook-progress.json (also shown below)');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Export failed');
    }
  };

  const importProgress = async () => {
    setMessage(null);
    setError(null);
    try {
      const payload = JSON.parse(importText) as unknown;
      await api.importProgress(payload);
      setMessage('Import completed');
      onReload();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Import failed');
    }
  };

  const resetProgress = async () => {
    setMessage(null);
    setError(null);
    if (resetText !== 'RESET') {
      setError('Type RESET to confirm');
      return;
    }
    try {
      await api.resetProgress();
      setResetText('');
      setMessage('Progress reset');
      onReload();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Reset failed');
    }
  };

  const renderTrack = (label: string, track: ReadinessPayload['aws']) => (
    <div className="readiness-card" key={label}>
      <h3>{label}</h3>
      {track.status === 'insufficient_evidence' ? (
        <>
          <p className="insufficient">{track.message ?? 'Insufficient evidence'}</p>
          <p>
            First-attempt exam items: {track.firstAttemptCount ?? 0}
            {track.missingPerBucket && Object.keys(track.missingPerBucket).length > 0 && (
              <>
                {' '}
                · Missing per bucket:{' '}
                {Object.entries(track.missingPerBucket)
                  .map(([k, v]) => `${k}: need ${v} more`)
                  .join('; ')}
              </>
            )}
          </p>
        </>
      ) : (
        <>
          <p className="readiness-score">{track.readiness}%</p>
          <p className="readiness-caption">{track.caption}</p>
        </>
      )}
    </div>
  );

  return (
    <div className="shell shell-tab">
      <aside className="side" aria-label="Start here nav">
        <button type="button" className="side-all sel">
          Setup & progress
        </button>
        <div className="dom" style={DOMAIN_STYLE_D1}>
          <button type="button" className="dom-h sel">
            <span className="dnum">0.0</span>
            <span className="dname">Lab safety</span>
            <span className="dw tnum">A0</span>
          </button>
        </div>
      </aside>

      <div className="main">
        <div className="prose">
          <div className="eyebrow">AWS SAA-C03 · Terraform Associate 004</div>
          <h2 style={{ fontSize: 30, marginTop: 6 }}>Learn it by building it</h2>
          <p>
            Guided and unguided labs you run in your own AWS account, plus MC/MR exam drills. Agents
            never create, change, or delete anything in AWS — you are the only actor.
          </p>

          <div className="facts">
            <div>
              <b className="tnum">SAA-C03</b>
              <span>189 atomic objectives</span>
            </div>
            <div>
              <b className="tnum">004</b>
              <span>Terraform lettered objectives</span>
            </div>
            <div>
              <b className="tnum">321+</b>
              <span>MC/MR drill bank floor</span>
            </div>
            <div>
              <b className="tnum">21+21</b>
              <span>Guided + unguided labs</span>
            </div>
            <div>
              <b className="tnum">$10</b>
              <span>Warning, not a hard stop</span>
            </div>
            <div>
              <b className="tnum">127.0.0.1</b>
              <span>Local app only</span>
            </div>
          </div>

          <h3>Domain weights → where lab hours should go</h3>
          <div className="weights">
            <div style={{ ['--w' as string]: 30, ['--dc' as string]: 'var(--d2)' }}>1.0 30%</div>
            <div style={{ ['--w' as string]: 26, ['--dc' as string]: 'var(--d3)' }}>2.0 26%</div>
            <div style={{ ['--w' as string]: 24, ['--dc' as string]: 'var(--d4)' }}>3.0 24%</div>
            <div style={{ ['--w' as string]: 20, ['--dc' as string]: 'var(--d5)' }}>4.0 20%</div>
          </div>
          <p className="eyebrow" style={{ marginTop: 4 }}>
            Then Terraform modules T1–T4 after the AWS path.
          </p>

          <h3>How to use this workbook</h3>
          <ol>
            <li>Finish GL-01 on the Labs tab: identity, MFA, alert-only budget, tags.</li>
            <li>Work one module at a time. Tick steps as you go; progress saves in SQLite.</li>
            <li>Use Exam drills for MC/MR practice; readiness stays “insufficient evidence” until thresholds.</li>
            <li>Use Coverage to find SAA bullets still marked missing.</li>
            <li>Tear down every lab. Stop charges stays visible without opening gated solutions.</li>
          </ol>

          <div className="note warn">
            <b>Rules of engagement</b>
            You run AWS CLI and Terraform in your own terminal. Free Tier is never assumed. Type{' '}
            <code>I ACCEPT THE COST RISK</code> before create/apply on hourly labs. Agents never
            touch AWS.
          </div>
        </div>

        <div className="prose" style={{ marginTop: 22 }}>
          <h2>{lesson?.title ?? 'A0 — Lab safety'}</h2>
          <label className="lesson-picker">
            Lesson
            <select value={lessonId} onChange={(e) => setLessonId(e.target.value)}>
              {lessonIndex.map((row) => (
                <option key={row.id} value={row.id}>
                  {row.title}
                </option>
              ))}
            </select>
          </label>
          {lesson?.bodyMarkdown && <MarkdownBody source={lesson.bodyMarkdown} />}
          {lesson?.drillIds && lesson.drillIds.length > 0 && (
            <>
              <h3>Drills for this lesson</h3>
              <ul>
                {lesson.drillIds.map((id) => (
                  <li key={id}>
                    <a href={`/exam?q=${encodeURIComponent(id)}`}>{id}</a>
                  </li>
                ))}
              </ul>
            </>
          )}
          {lesson && (
            <RelatedPractice
              objectiveIds={lesson.objectiveIds ?? []}
              labs={labIndex}
              exercises={exerciseIndex}
            />
          )}
          {!lesson && !error && <p>Loading lesson…</p>}
        </div>

        <div className="prose" style={{ marginTop: 22 }}>
          <h2>Your readiness</h2>
          <p>
            Scores stay hidden until enough first-attempt exam-mode items exist. This is not a pass
            probability.
          </p>
          <div className="readiness-grid">
            {readiness && renderTrack('AWS (SAA-C03)', readiness.aws)}
            {readiness && renderTrack('Terraform (004)', readiness.terraform)}
            {!readiness && <p>Loading readiness…</p>}
          </div>
        </div>

        <div className="prose" style={{ marginTop: 22 }}>
          <h2>Your progress</h2>
          <p className="threat-copy">
            Another process on this PC could call the Django port on 127.0.0.1. Answer keys exist in
            content JSON and SQLite — not in this React bundle.
          </p>
          <p>
            To move progress to another browser, copy the text below and paste it into Import there.
          </p>
          <textarea
            className="io"
            id="io"
            spellCheck={false}
            aria-label="Progress export"
            value={importText}
            onChange={(e) => setImportText(e.target.value)}
            placeholder="Export fills this box, or paste a workbook-progress.json here to import."
          />
          <div className="labfoot">
            <button type="button" className="btn" onClick={() => void exportProgress()}>
              Copy / export progress
            </button>
            <button type="button" className="btn primary" onClick={() => void importProgress()}>
              Import pasted progress
            </button>
          </div>
          <label htmlFor="reset-confirm" className="blk-h">
            Type RESET to confirm reset
          </label>
          <input
            id="reset-confirm"
            type="text"
            value={resetText}
            onChange={(e) => setResetText(e.target.value)}
            autoComplete="off"
            style={{
              width: '100%',
              padding: '7px 10px',
              border: '1px solid var(--rule-strong)',
              borderRadius: 5,
            }}
          />
          <button
            type="button"
            className="btn"
            style={{ marginTop: 8 }}
            onClick={() => void resetProgress()}
          >
            Reset all progress
          </button>

          {message && (
            <p className="success-msg" role="status">
              {message}
            </p>
          )}
          {error && (
            <p className="inline-error" role="alert">
              {error}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

const DOMAIN_STYLE_D1 = {
  ['--dc' as string]: 'var(--d1)',
  ['--dsoft' as string]: 'var(--d1-soft)',
  ['--mc' as string]: 'var(--d1)',
};
