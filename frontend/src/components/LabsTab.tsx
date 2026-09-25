import { useMemo, useState } from 'react';
import { CURRICULUM, DOMAIN_STYLE } from '../data/curriculum';
import type { ContentSummary, Lab, ProgressSnapshot } from '../types';
import { computeHeaderStats, labStepProgress } from '../utils/progress';
import { LabCard } from './LabCard';

interface LabsTabProps {
  summary: ContentSummary;
  labsById: Map<string, Lab>;
  progress: ProgressSnapshot;
  onProgressChange: () => void;
  onSelectSetupLab: () => void;
}

type DifficultyFilter = '' | 'foundation' | 'applied' | 'tradeoff';
type StatusFilter = '' | 'not-started' | 'in-progress' | 'complete';

export function LabsTab({
  summary,
  labsById,
  progress,
  onProgressChange,
  onSelectSetupLab,
}: LabsTabProps) {
  const available = useMemo(() => new Set(summary.labs), [summary.labs]);
  const stats = computeHeaderStats(labsById, progress);

  const [mainQuery, setMainQuery] = useState('');
  const [difficulty, setDifficulty] = useState<DifficultyFilter>('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('');
  const [selectedModId, setSelectedModId] = useState<string | null>(null);
  const [selectedGroupId, setSelectedGroupId] = useState<string | null>(null);

  const totalCatalogLabs = useMemo(
    () =>
      CURRICULUM.reduce(
        (n, mod) => n + mod.groups.reduce((g, grp) => g + grp.labs.length, 0),
        0,
      ),
    [],
  );

  const moduleProgress = (modId: string) => {
    let done = 0;
    let total = 0;
    const mod = CURRICULUM.find((m) => m.id === modId);
    if (!mod) return { done, total, pct: 0 };
    for (const group of mod.groups) {
      for (const ref of group.labs) {
        if (!available.has(ref.id)) continue;
        const lab = labsById.get(ref.id);
        if (!lab) continue;
        total += 1;
        if (labStepProgress(lab, progress).status === 'complete') done += 1;
      }
    }
    return { done, total, pct: total ? Math.round((done / total) * 100) : 0 };
  };

  const groupDoneTotal = (groupId: string) => {
    let done = 0;
    let total = 0;
    for (const mod of CURRICULUM) {
      for (const group of mod.groups) {
        if (group.id !== groupId) continue;
        for (const ref of group.labs) {
          if (!available.has(ref.id)) continue;
          const lab = labsById.get(ref.id);
          if (!lab) continue;
          total += 1;
          if (labStepProgress(lab, progress).status === 'complete') done += 1;
        }
      }
    }
    return { done, total };
  };

  const sections = useMemo(() => {
    const q = mainQuery.trim().toLowerCase();
    return CURRICULUM.flatMap((mod) => {
      if (selectedModId && mod.id !== selectedModId) return [];
      return mod.groups
        .filter((g) => !selectedGroupId || g.id === selectedGroupId)
        .map((group) => {
          const labs = group.labs.filter((ref) => {
            if (!available.has(ref.id)) return false;
            const lab = labsById.get(ref.id);
            if (!lab) return false;
            if (difficulty && (lab.difficulty ?? 'applied') !== difficulty) return false;
            const st = labStepProgress(lab, progress).status;
            if (statusFilter && st !== statusFilter) return false;
            if (!q) return true;
            return (
              ref.title.toLowerCase().includes(q) ||
              ref.chip.toLowerCase().includes(q) ||
              lab.title.toLowerCase().includes(q)
            );
          });
          return { mod, group, labs };
        })
        .filter((s) => s.labs.length > 0 || (!q && !difficulty && !statusFilter));
    });
  }, [
    available,
    labsById,
    mainQuery,
    difficulty,
    statusFilter,
    progress,
    selectedModId,
    selectedGroupId,
  ]);

  const shown = sections.reduce((n, s) => n + s.labs.length, 0);

  return (
    <div className="shell shell-tab">
      <aside className="side" id="side" aria-label="Domains and topics">
        <button
          type="button"
          className={`side-all ${!selectedModId && !selectedGroupId ? 'sel' : ''}`}
          onClick={() => {
            setSelectedModId(null);
            setSelectedGroupId(null);
          }}
        >
          All {totalCatalogLabs} labs <span className="count">· {stats.progressPercent}%</span>
        </button>
        {CURRICULUM.map((mod) => {
          const mp = moduleProgress(mod.id);
          return (
            <div className="dom" key={mod.id} style={DOMAIN_STYLE[mod.color]}>
              <button
                type="button"
                className={`dom-h ${selectedModId === mod.id && !selectedGroupId ? 'sel' : ''}`}
                onClick={() => {
                  setSelectedModId(mod.id);
                  setSelectedGroupId(null);
                }}
              >
                <span className="dnum">{mod.pill}</span>
                <span className="dname">{mod.title}</span>
                <span className="dw tnum">
                  {mod.weight ? `${mod.weight}% · ` : ''}
                  {mp.pct}%
                </span>
              </button>
              <div className="meter">
                <i style={{ width: `${mp.pct}%` }} />
              </div>
              <ul className="objs">
                {mod.groups.map((group) => {
                  const gt = groupDoneTotal(group.id);
                  return (
                    <li key={group.id}>
                      <button
                        type="button"
                        className={selectedGroupId === group.id ? 'sel' : ''}
                        onClick={() => {
                          setSelectedModId(mod.id);
                          setSelectedGroupId(group.id);
                        }}
                      >
                        <span className="on">{group.id.replace(/^[A-Z]/, '')}</span>
                        <span>{group.title}</span>
                        <span className="oc tnum">
                          {gt.done}/{gt.total || group.labs.length}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </aside>

      <div className="main labs-main">
        <div className="filters">
          <input
            type="search"
            id="q"
            aria-label="Search labs"
            placeholder="Search labs, tools, topics (e.g. IAM, NAT, Terraform state)"
            value={mainQuery}
            onChange={(e) => setMainQuery(e.target.value)}
          />
          <select
            id="fdiff"
            aria-label="Difficulty"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value as DifficultyFilter)}
          >
            <option value="">Any difficulty</option>
            <option value="foundation">● Foundation</option>
            <option value="applied">●● Practitioner</option>
            <option value="tradeoff">●●● Advanced</option>
          </select>
          <select
            id="fstat"
            aria-label="Status"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
          >
            <option value="">Any status</option>
            <option value="not-started">Not started</option>
            <option value="in-progress">In progress</option>
            <option value="complete">Done</option>
          </select>
          <span className="count tnum">{shown} shown</span>
        </div>

        <div className="note warn" style={{ maxWidth: 'none' }}>
          <b>First time here?</b>
          Complete{' '}
          <button type="button" className="linkish" onClick={onSelectSetupLab}>
            GL-01 — identity, budget, and preflight
          </button>{' '}
          before starting. Agents never create anything in AWS — you run the commands.
        </div>

        {sections.map(({ mod, group, labs }) => {
          const gp = groupDoneTotal(group.id);
          const pct = gp.total ? Math.round((100 * gp.done) / gp.total) : 0;
          return (
            <section className="objsec" key={group.id} style={DOMAIN_STYLE[mod.color]}>
              <div className="objsec-h">
                <span className="on">{group.id}</span>
                <h2>{group.title}</h2>
                <span className="meta tnum">
                  {labs.length} labs · {pct}%
                </span>
              </div>
              {labs.map((ref) => {
                const lab = labsById.get(ref.id);
                if (!lab) return null;
                return (
                  <LabCard
                    key={ref.id}
                    lab={lab}
                    chip={ref.chip}
                    domainStyle={DOMAIN_STYLE[mod.color]}
                    progress={progress}
                    onProgressChange={onProgressChange}
                  />
                );
              })}
            </section>
          );
        })}

        {sections.length === 0 && <div className="empty">No labs match these filters.</div>}
      </div>
    </div>
  );
}
