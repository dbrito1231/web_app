import type { HeaderStats, TabId } from '../types';

const TABS: { id: TabId; label: string; view: string }[] = [
  { id: 'labs', label: 'Labs', view: 'labs' },
  { id: 'exam', label: 'Exam drills', view: 'pbq' },
  { id: 'coverage', label: 'Coverage', view: 'coverage' },
  { id: 'start', label: 'Start here', view: 'setup' },
];

interface HeaderProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
  stats: HeaderStats;
}

export function Header({ activeTab, onTabChange, stats }: HeaderProps) {
  return (
    <header className="top">
      <a href="#main" className="skip-link">
        Skip to main content
      </a>
      <div className="top-in">
        <div className="brand">
          <h1>AWS + Terraform Workbook</h1>
          <span className="code">SAA-C03 + 004</span>
        </div>
        <nav className="tabs" role="tablist" aria-label="Views">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              id={`tab-${tab.id}`}
              role="tab"
              data-view={tab.view}
              aria-selected={activeTab === tab.id}
              aria-controls="main"
              onClick={() => onTabChange(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </nav>
        <div className="overall">
          <span className="sync on" id="sync">
            Saved in this browser
          </span>
          <span className="big tnum" id="ovPct">
            {stats.progressPercent}%
          </span>
          <span className="num tnum" id="ovNum">
            {stats.stepsCompleted} / {stats.stepsTotal} steps · {stats.labsCompleted} of{' '}
            {stats.labsTotal} labs done
          </span>
        </div>
      </div>
      <div className="domstrip" aria-hidden="true">
        <span style={{ ['--w' as string]: 20, background: 'var(--d1)' }} />
        <span style={{ ['--w' as string]: 20, background: 'var(--d2)' }} />
        <span style={{ ['--w' as string]: 20, background: 'var(--d3)' }} />
        <span style={{ ['--w' as string]: 15, background: 'var(--d4)' }} />
        <span style={{ ['--w' as string]: 15, background: 'var(--d5)' }} />
        <span style={{ ['--w' as string]: 10, background: 'var(--d6)' }} />
      </div>
    </header>
  );
}
