import { useMemo, useState, type CSSProperties } from 'react';
import { api } from '../api/client';
import { HOURLY_COST_RISK_LABS } from '../data/curriculum';
import type { Lab, ProgressSnapshot } from '../types';
import { checkpointMap, labChecklist, labStepProgress } from '../utils/progress';

interface LabCardProps {
  lab: Lab;
  chip: string;
  domainStyle?: CSSProperties;
  defaultOpen?: boolean;
  progress: ProgressSnapshot;
  onProgressChange: () => void;
}

const COST_RISK_PHRASE = 'I ACCEPT THE COST RISK';

function formatSameHourCost(lab: Lab): string {
  if (lab.costSameHour) return lab.costSameHour;
  const usd = lab.sameHourEstimateUsd;
  if (usd === undefined || usd === null) return 'See lab guide';
  if (usd === 0) return '$0';
  const text = usd.toFixed(2).replace(/\.?0+$/, '');
  return `~$${text}`;
}

function difficultyPips(difficulty?: string): string {
  const level =
    difficulty === 'foundation' ? 1 : difficulty === 'tradeoff' || difficulty === 'advanced' ? 3 : 2;
  return '●'.repeat(level) + '○'.repeat(3 - level);
}

function ProgressRing({ pct, done }: { pct: number; done: boolean }) {
  const C = 2 * Math.PI * 10;
  const stroke = done ? 'var(--ok)' : 'var(--dc, var(--accent))';
  return (
    <svg className="ring" viewBox="0 0 26 26" aria-hidden="true">
      <circle cx="13" cy="13" r="10" fill="none" stroke="var(--rule)" strokeWidth="3" />
      <circle
        cx="13"
        cy="13"
        r="10"
        fill="none"
        stroke={stroke}
        strokeWidth="3"
        strokeDasharray={`${C * (pct / 100)} ${C}`}
        transform="rotate(-90 13 13)"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function LabCard({
  lab,
  chip,
  domainStyle,
  defaultOpen = true,
  progress,
  onProgressChange,
}: LabCardProps) {
  const [open, setOpen] = useState(defaultOpen);
  const [costRiskInput, setCostRiskInput] = useState('');
  const [busyId, setBusyId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const map = useMemo(() => checkpointMap(progress), [progress]);
  const stepStats = labStepProgress(lab, progress);
  const hourly = HOURLY_COST_RISK_LABS.has(lab.id);
  const costRiskOk = !hourly || costRiskInput.trim() === COST_RISK_PHRASE;

  const practiceLabel = (lab.practiceMode ?? lab.kind ?? 'guided').replace(/_/g, ' ').toUpperCase();
  const minutes = lab.estimatedMinutes ?? 60;
  const costLabel = formatSameHourCost(lab);

  const doneWhen =
    lab.doneWhen ??
    (lab.checkpoints?.length
      ? lab.checkpoints.map((c) => c.label).join(' ')
      : (lab.teardown?.verification?.join(' ') ??
        'All steps self-reported and teardown complete.'));

  const pillClass =
    stepStats.status === 'complete' ? 'dn' : stepStats.status === 'in-progress' ? 'ip' : 'ns';
  const statusLabel =
    stepStats.status === 'complete'
      ? 'Done'
      : stepStats.status === 'in-progress'
        ? 'In progress'
        : 'Not started';

  const ringPct =
    stepStats.total > 0 ? Math.round((100 * stepStats.completed) / stepStats.total) : 0;
  const checklist = labChecklist(lab);
  const checklistLabel = lab.steps && lab.steps.length > 0 ? 'Steps' : 'Acceptance criteria';
  const beforeItems = Array.isArray(lab.beforeYouStart)
    ? lab.beforeYouStart.filter(Boolean)
    : lab.beforeYouStart
      ? [lab.beforeYouStart]
      : [];

  const toggleStep = async (stepId: string) => {
    const current = map.get(`${lab.id}:${stepId}`);
    const next = current === 'self-reported' ? 'not-started' : 'self-reported';
    if (!costRiskOk && next === 'self-reported') {
      setError(`Type ${COST_RISK_PHRASE} before marking create/apply steps.`);
      return;
    }
    setBusyId(stepId);
    setError(null);
    try {
      await api.labCheckpoint(lab.id, stepId, next);
      await onProgressChange();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Could not save checkpoint');
    } finally {
      setBusyId(null);
    }
  };

  return (
    <article id={`lab-card-${lab.id}`} className={`lab-card ${open ? 'is-open' : ''}`} style={domainStyle}>
      <header
        className="lab-card-head"
        onClick={() => setOpen((v) => !v)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setOpen((v) => !v);
          }
        }}
        role="button"
        tabIndex={0}
        aria-expanded={open}
        aria-label={`${chip} details`}
      >
        <span className="lab-id-chip">{chip}</span>
        <span>
          <span className="lt" style={{ fontWeight: 600, fontSize: 15, display: 'block' }}>
            {lab.title}
          </span>
          <span className="lab-meta">
            <span className="kind">{practiceLabel}</span>
            <span className="diff-pips">{difficultyPips(lab.difficulty)}</span>
            <span>{minutes} min</span>
            <span>
              {stepStats.completed}/{stepStats.total} steps
            </span>
          </span>
        </span>
        <span className="lab-status-ring">
          <span className={`pill ${pillClass}`}>{statusLabel}</span>
          <ProgressRing pct={ringPct} done={stepStats.status === 'complete'} />
        </span>
      </header>

      {open && (
        <div className="lab-card-body">
          <div className="chips">
            <span className="chip cost">Cost: {costLabel}</span>
            {lab.difficulty && <span className="chip">{lab.difficulty}</span>}
            {lab.kind && <span className="chip">{lab.kind}</span>}
          </div>

          {(lab.body || lab.scenario) && <p className="goal">{lab.body || lab.scenario}</p>}

          {beforeItems.length > 0 && (
            <>
              <div className="blk-h">Before you start</div>
              <ul className="stxt" style={{ margin: 0, paddingLeft: 18 }}>
                {beforeItems.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </>
          )}

          {hourly && (
            <section className="cost-risk">
              <label htmlFor={`cost-risk-${lab.id}`}>
                Hourly lab — type <strong>{COST_RISK_PHRASE}</strong> before checking steps
              </label>
              <input
                id={`cost-risk-${lab.id}`}
                type="text"
                value={costRiskInput}
                onChange={(e) => setCostRiskInput(e.target.value)}
                autoComplete="off"
                spellCheck={false}
                onClick={(e) => e.stopPropagation()}
              />
            </section>
          )}

          <div className="blk-h">{checklistLabel}</div>
          <ol className="step-list">
            {checklist.map((step, index) => {
              const checked = map.get(`${lab.id}:${step.id}`) === 'self-reported';
              return (
                <li key={step.id} className={checked ? 'is-done' : ''}>
                  <span className="step-num">{index + 1}</span>
                  <div className="step-text">
                    <button
                      type="button"
                      className="step-check"
                      aria-pressed={checked}
                      disabled={busyId === step.id}
                      onClick={(e) => {
                        e.stopPropagation();
                        void toggleStep(step.id);
                      }}
                    >
                      <strong>{step.title}</strong>
                    </button>
                    {step.bullets && step.bullets.length > 0 ? (
                      <ul className="step-bullets">
                        {step.bullets.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    ) : (
                      step.body && <span className="step-body">{step.body}</span>
                    )}
                  </div>
                </li>
              );
            })}
          </ol>

          {lab.hints && lab.hints.length > 0 && (
            <>
              <div className="blk-h">Hints</div>
              <ul className="stxt" style={{ margin: 0, paddingLeft: 18 }}>
                {lab.hints.map((hint) => (
                  <li key={hint.level}>{hint.text}</li>
                ))}
              </ul>
            </>
          )}

          {lab.rubric && lab.rubric.length > 0 && (
            <>
              <div className="blk-h">Rubric</div>
              <ul className="stxt" style={{ margin: 0, paddingLeft: 18 }}>
                {lab.rubric.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </>
          )}

          <div className="note verify" aria-label="Done when">
            <b>Done when</b>
            {doneWhen}
          </div>

          <section className="stop-charges" aria-label="Stop charges and teardown">
            <h4>Stop charges</h4>
            {lab.stopChargesPanel && <p>{lab.stopChargesPanel}</p>}
            {lab.teardown?.stillBillingNote && (
              <p className="still-billing">{lab.teardown.stillBillingNote}</p>
            )}
            {lab.teardown?.orderedDeletesPowerShell &&
              lab.teardown.orderedDeletesPowerShell.length > 0 && (
                <div className="teardown-block">
                  <h5>Teardown (PowerShell — you run these)</h5>
                  <p className="teardown-scope">
                    Region scope: {lab.teardown.regionScope ?? lab.region ?? 'us-east-1'}. Agents
                    never run these commands.
                  </p>
                  <ol className="teardown-commands">
                    {lab.teardown.orderedDeletesPowerShell.map((cmd) => (
                      <li key={cmd}>
                        <pre className="command-block">
                          <code>{cmd}</code>
                        </pre>
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            {lab.teardown?.verification && lab.teardown.verification.length > 0 && (
              <div className="teardown-block">
                <h5>Post-teardown checks</h5>
                <ul>
                  {lab.teardown.verification.map((check) => (
                    <li key={check}>{check}</li>
                  ))}
                </ul>
              </div>
            )}
            {lab.teardown?.recovery && <p className="still-billing">{lab.teardown.recovery}</p>}
          </section>

          {error && (
            <p className="inline-error" role="alert">
              {error}
            </p>
          )}
        </div>
      )}
    </article>
  );
}
