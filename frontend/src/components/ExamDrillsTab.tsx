import { useEffect, useMemo, useState } from 'react';
import { api } from '../api/client';
import {
  DOMAIN_STYLE,
  EXAM_MODULE_COLOR,
  EXAM_MODULE_LABELS,
  EXAM_MODULE_ORDER,
} from '../data/curriculum';
import type { AttemptResult, ContentSummary, Question } from '../types';
import { shuffle } from '../utils/progress';

interface ExamDrillsTabProps {
  summary: ContentSummary;
}

interface QuestionMeta {
  id: string;
  module: string;
  type: 'mc' | 'mr';
  stem?: string;
}

export function ExamDrillsTab({ summary }: ExamDrillsTabProps) {
  const [catalog, setCatalog] = useState<QuestionMeta[]>([]);
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const [activeQuestionId, setActiveQuestionId] = useState<string | null>(null);
  const [question, setQuestion] = useState<Question | null>(null);
  const [order, setOrder] = useState<string[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [result, setResult] = useState<AttemptResult | null>(null);
  const [bestScores, setBestScores] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const [catalogPayload, progress] = await Promise.all([
        api.questionCatalog(),
        api.progress(),
      ]);
      if (!cancelled) {
        const rows = catalogPayload.questions.map((q) => ({
          id: q.id,
          module: q.module ?? 'A0',
          type: q.type,
          stem: q.stem,
        }));
        rows.sort((a, b) => a.id.localeCompare(b.id));
        setCatalog(rows);
        if (progress.bestByQuestion) setBestScores(progress.bestByQuestion);
        const requested = new URLSearchParams(window.location.search).get('q');
        const pick = rows.find((row) => row.id === requested);
        if (pick) {
          setActiveModule(null);
          setActiveQuestionId(pick.id);
        } else if (rows[0]) {
          setActiveQuestionId(rows[0].id);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [summary.questions]);

  const list = useMemo(
    () => catalog.filter((q) => !activeModule || q.module === activeModule),
    [catalog, activeModule],
  );

  useEffect(() => {
    if (!list.length) {
      setQuestion(null);
      return;
    }
    if (!list.some((q) => q.id === activeQuestionId)) {
      setActiveQuestionId(list[0].id);
    }
  }, [list, activeQuestionId]);

  useEffect(() => {
    if (!activeQuestionId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    setResult(null);
    setSelected(new Set());
    (async () => {
      try {
        const q = await api.question(activeQuestionId);
        if (cancelled) return;
        setQuestion(q);
        setOrder(shuffle(q.choices.map((c) => c.id)));
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : 'Failed to load question');
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [activeQuestionId]);

  const toggleChoice = (id: string) => {
    if (!question || result) return;
    setSelected((prev) => {
      if (question.type === 'mc') return new Set([id]);
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const submit = async () => {
    if (!question) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.submitAttempt({
        questionId: question.id,
        selectedIds: [...selected],
        mode: 'exam',
        assisted: false,
        presentedOrder: order,
      });
      setResult(res);
      const score = res.correct ? 100 : 0;
      setBestScores((prev) => ({
        ...prev,
        [question.id]: Math.max(prev[question.id] ?? 0, score),
      }));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Submit failed');
    } finally {
      setLoading(false);
    }
  };

  const retry = () => {
    setResult(null);
    setSelected(new Set());
    if (question) setOrder(shuffle(question.choices.map((c) => c.id)));
  };

  const selectCount =
    question?.type === 'mr' ? String(question.selectCount ?? 2) : '1';

  const moduleDone = (mod: string) => {
    const qs = catalog.filter((q) => q.module === mod);
    const done = qs.filter((q) => (bestScores[q.id] ?? 0) >= 100).length;
    return { done, total: qs.length };
  };

  return (
    <div className="shell shell-tab">
      <aside className="side" aria-label="Exam drill modules">
        <button
          type="button"
          className={`side-all ${!activeModule ? 'sel' : ''}`}
          onClick={() => setActiveModule(null)}
        >
          All drills <span className="count">{catalog.length}</span>
        </button>
        {EXAM_MODULE_ORDER.map((mod) => {
          const { done, total } = moduleDone(mod);
          const color = EXAM_MODULE_COLOR[mod] ?? 'd1';
          return (
            <div className="dom" key={mod} style={DOMAIN_STYLE[color]}>
              <button
                type="button"
                className={`dom-h ${activeModule === mod ? 'sel' : ''}`}
                onClick={() => setActiveModule(mod)}
              >
                <span className="dnum">{mod}</span>
                <span className="dname">{EXAM_MODULE_LABELS[mod]?.split('—')[1]?.trim() ?? mod}</span>
                <span className="dw tnum">
                  {done}/{total}
                </span>
              </button>
              <div className="meter">
                <i style={{ width: total ? `${(100 * done) / total}%` : '0%' }} />
              </div>
            </div>
          );
        })}
      </aside>

      <div className="main">
        <div className="eyebrow" style={{ marginBottom: 10 }}>
          Exam-style MC and MR drills. Answers are scored when you press Check answers.
        </div>

        {list.length === 0 && (
          <div className="empty">No questions published for this filter yet.</div>
        )}

        {list.length > 0 && (
          <>
            <div className="pbq-grid">
              {list.map((q) => {
                const color = EXAM_MODULE_COLOR[q.module] ?? 'd1';
                const best = bestScores[q.id];
                return (
                  <button
                    key={q.id}
                    type="button"
                    className={`pbq-card ${q.id === activeQuestionId ? 'sel' : ''}`}
                    style={DOMAIN_STYLE[color]}
                    onClick={() => setActiveQuestionId(q.id)}
                  >
                    <span className="eyebrow" style={{ color: 'var(--dc)' }}>
                      {q.module} · {q.type === 'mc' ? 'Multiple choice' : 'Multiple response'}
                    </span>
                    <span className="t">{q.stem?.slice(0, 90) ?? q.id}</span>
                    <span className="m">
                      <span>~5 min</span>
                      <span className="tnum">
                        {best == null ? 'Not tried' : `Best ${best}%`}
                      </span>
                    </span>
                  </button>
                );
              })}
              <button
                type="button"
                className="pbq-card"
                disabled
                title="The 50-question set is in the coverage registry. A timed runner is not in this build."
              >
                <span className="eyebrow">Mock exam</span>
                <span className="t">50-question set (15/13/12/10)</span>
                <span className="m">
                  <span>Set shipped; timed runner not in this build</span>
                  <span className="tnum">Not runnable</span>
                </span>
              </button>
            </div>

            {loading && !question && <p>Loading question…</p>}
            {error && (
              <p className="inline-error" role="alert">
                {error}
              </p>
            )}

            {question && (
              <article
                className="pbq"
                style={DOMAIN_STYLE[EXAM_MODULE_COLOR[question.module ?? 'A0'] ?? 'd1']}
              >
                <div className="eyebrow" style={{ color: 'var(--dc)' }}>
                  Module {question.module ?? 'A0'} ·{' '}
                  {question.type === 'mc' ? 'Multiple choice' : 'Multiple response'}
                </div>
                <h2>{question.id}</h2>
                <div className="prompt">
                  {question.stem}
                  {question.promptNote && (
                    <p style={{ marginTop: 8, color: 'var(--muted)' }}>{question.promptNote}</p>
                  )}
                  <p style={{ marginTop: 6, fontSize: 13, color: 'var(--muted)' }}>
                    Select {selectCount}
                  </p>
                </div>

                <fieldset className="choice-list">
                  <legend className="sr-only">Answer choices</legend>
                  {order.map((choiceId) => {
                    const choice = question.choices.find((c) => c.id === choiceId);
                    if (!choice) return null;
                    const inputType = question.type === 'mc' ? 'radio' : 'checkbox';
                    return (
                      <label key={choice.id} className="choice-row">
                        <input
                          type={inputType}
                          name={`q-${question.id}`}
                          checked={selected.has(choice.id)}
                          disabled={!!result}
                          onChange={() => toggleChoice(choice.id)}
                        />
                        <span>{choice.text}</span>
                      </label>
                    );
                  })}
                </fieldset>

                <div className="score">
                  {!result && (
                    <button
                      type="button"
                      className="btn primary"
                      disabled={selected.size !== Number(selectCount) || loading}
                      onClick={() => void submit()}
                    >
                      Check answers
                    </button>
                  )}
                  {result && (
                    <>
                      <span className="s tnum">{result.correct ? '100%' : '0%'}</span>
                      <span className="why">
                        {result.correct
                          ? 'Clean pass. Move on to the next drill.'
                          : 'Review the explanation, then retry.'}
                      </span>
                      <button type="button" className="btn" onClick={retry}>
                        Retry
                      </button>
                    </>
                  )}
                </div>

                {result && (
                  <div
                    className={`rationale ${result.correct ? 'is-correct' : 'is-wrong'}`}
                    role="status"
                    aria-live="polite"
                  >
                    <p>
                      <strong>{result.correct ? 'Correct' : 'Incorrect'}</strong>
                    </p>
                    <p>{result.rationale}</p>
                    {result.objectiveIds.length > 0 && (
                      <p className="objective-ids">
                        Objectives: {result.objectiveIds.join(', ')}
                      </p>
                    )}
                  </div>
                )}
              </article>
            )}
          </>
        )}
      </div>
    </div>
  );
}
