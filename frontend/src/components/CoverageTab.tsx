import { useEffect, useMemo, useState } from 'react';
import { api } from '../api/client';
import { DOMAIN_STYLE } from '../data/curriculum';
import type { CoveragePayload, CoverageRow } from '../types';

const DOMAIN_COLOR: Record<string, keyof typeof DOMAIN_STYLE> = {
  '1': 'd2',
  '2': 'd3',
  '3': 'd4',
  '4': 'd5',
};

export function CoverageTab() {
  const [data, setData] = useState<CoveragePayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [domainFilter, setDomainFilter] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const payload = await api.coverage();
        if (!cancelled) setData(payload);
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : 'Failed to load coverage');
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const rows = useMemo(() => {
    if (!data) return [] as CoverageRow[];
    if (!domainFilter) return data.rows;
    return data.rows.filter((r) => r.domain_id === domainFilter);
  }, [data, domainFilter]);

  const byTask = useMemo(() => {
    const map = new Map<string, CoverageRow[]>();
    for (const row of rows) {
      const list = map.get(row.task_id) ?? [];
      list.push(row);
      map.set(row.task_id, list);
    }
    return [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]));
  }, [rows]);

  const withContent = rows.filter((r) => r.status !== 'missing').length;
  const verified = rows.filter((r) => r.status === 'verified').length;
  const total = data?.total ?? rows.length;

  const domainCounts = useMemo(() => {
    const counts: Record<string, { n: number; done: number }> = {
      '1': { n: 0, done: 0 },
      '2': { n: 0, done: 0 },
      '3': { n: 0, done: 0 },
      '4': { n: 0, done: 0 },
    };
    for (const row of data?.rows ?? []) {
      const d = counts[row.domain_id];
      if (!d) continue;
      d.n += 1;
      if (row.status === 'verified') d.done += 1;
    }
    return counts;
  }, [data]);

  return (
    <div className="shell shell-tab">
      <aside className="side" aria-label="Coverage domains">
        <button
          type="button"
          className={`side-all ${!domainFilter ? 'sel' : ''}`}
          onClick={() => setDomainFilter(null)}
        >
          All objectives <span className="count">{total}</span>
        </button>
        {(['1', '2', '3', '4'] as const).map((d) => {
          const c = domainCounts[d];
          const color = DOMAIN_COLOR[d];
          return (
            <div className="dom" key={d} style={DOMAIN_STYLE[color]}>
              <button
                type="button"
                className={`dom-h ${domainFilter === d ? 'sel' : ''}`}
                onClick={() => setDomainFilter(d)}
              >
                <span className="dnum">{d}.0</span>
                <span className="dname">Domain {d}</span>
                <span className="dw tnum">
                  {c.done}/{c.n}
                </span>
              </button>
              <div className="meter">
                <i style={{ width: c.n ? `${(100 * c.done) / c.n}%` : '0%' }} />
              </div>
            </div>
          );
        })}
      </aside>

      <div className="main">
        <div className="eyebrow">
          Objective bullet → curriculum status. Gaps stay visible until the lesson and drills are reviewed on paper. This is curriculum coverage, not a pass probability or exam readiness.
        </div>
        <div className="covsum">
          <div>
            <b className="tnum">
              {withContent}/{total}
            </b>
            <span>bullets past missing</span>
          </div>
          <div>
            <b className="tnum">
              {verified}/{total}
            </b>
            <span>verified on paper (labs not run in AWS)</span>
          </div>
          <div>
            <b className="tnum">189</b>
            <span>SAA atomic IDs (exact)</span>
          </div>
        </div>

        {error && (
          <p className="inline-error" role="alert">
            {error}
          </p>
        )}

        {byTask.map(([taskId, taskRows]) => {
          const domain = taskRows[0]?.domain_id ?? '1';
          const color = DOMAIN_COLOR[domain] ?? 'd1';
          return (
            <div className="cov-obj" key={taskId} style={DOMAIN_STYLE[color]}>
              <h3>
                <span className="on">{taskId}</span>
                Task {taskId} · {taskRows.length} bullets
              </h3>
              <div className="cov-wrap">
                <table className="cov">
                  <tbody>
                    {taskRows.map((row) => (
                      <tr key={row.objective_id}>
                        <td>
                          <code>{row.objective_id}</code>
                          <div style={{ color: 'var(--muted)', fontSize: 12.5, marginTop: 2 }}>
                            {row.source_text}
                          </div>
                        </td>
                        <td>
                          {row.status === 'missing' ? (
                            <span className="gap">No content yet</span>
                          ) : (
                            <span className={`status-badge status-${row.status}`}>
                              {row.status}
                              {row.practice_mode ? ` · ${row.practice_mode}` : ''}
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
