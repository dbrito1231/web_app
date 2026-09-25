import { useEffect, useRef, type KeyboardEvent } from 'react';
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
  const headerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const el = headerRef.current;
    if (!el) return;
    const setVar = () => {
      document.documentElement.style.setProperty('--header-h', `${el.offsetHeight}px`);
    };
    setVar();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(setVar);
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const onTabKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    let next = index;
    if (event.key === 'ArrowRight') next = (index + 1) % TABS.length;
    else if (event.key === 'ArrowLeft') next = (index - 1 + TABS.length) % TABS.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = TABS.length - 1;
    else return;
    event.preventDefault();
    const id = TABS[next].id;
    onTabChange(id);
    document.getElementById(`tab-${id}`)?.focus();
  };

  return (
    <header className="top" ref={headerRef}>
      <a href="#main" className="skip-link">
        Skip to main content
      </a>
      <div className="top-in">
        <div className="brand">
          <h1>AWS + Terraform Workbook</h1>
          <span className="code">SAA-C03 + 004</span>
        </div>
        <nav className="tabs" role="tablist" aria-label="Views">
          {TABS.map((tab, index) => (
            <button
              key={tab.id}
              type="button"
              id={`tab-${tab.id}`}
              role="tab"
              data-view={tab.view}
              aria-selected={activeTab === tab.id}
              aria-controls="main"
              tabIndex={activeTab === tab.id ? 0 : -1}
              onClick={() => onTabChange(tab.id)}
              onKeyDown={(event) => onTabKeyDown(event, index)}
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
