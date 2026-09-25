import { useCallback, useEffect } from 'react';
import { Navigate, Route, Routes, useNavigate, useParams } from 'react-router-dom';
import { Header } from './components/Header';
import { CoverageTab } from './components/CoverageTab';
import { ExamDrillsTab } from './components/ExamDrillsTab';
import { LabsTab } from './components/LabsTab';
import { StartHereTab } from './components/StartHereTab';
import { useWorkbookBootstrap } from './hooks/useWorkbookBootstrap';
import type { TabId } from './types';

const TAB_PATHS: Record<TabId, string> = {
  labs: '/labs',
  exam: '/exam',
  coverage: '/coverage',
  start: '/start',
};

const PATH_TO_TAB: Record<string, TabId> = {
  labs: 'labs',
  exam: 'exam',
  coverage: 'coverage',
  start: 'start',
};

function WorkbookShell() {
  const { tabSlug } = useParams();
  const navigate = useNavigate();
  const knownTab = tabSlug ? PATH_TO_TAB[tabSlug] : undefined;
  const tab: TabId = knownTab ?? 'labs';

  useEffect(() => {
    if (tabSlug && !knownTab) {
      navigate('/labs', { replace: true });
    }
  }, [tabSlug, knownTab, navigate]);

  const {
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
    notice,
    clearNotice,
    refreshProgress,
    reloadWithNotice,
  } = useWorkbookBootstrap();

  const setTab = useCallback(
    (next: TabId) => {
      navigate(TAB_PATHS[next]);
    },
    [navigate],
  );

  useEffect(() => {
    if (tab === 'labs' && summary) {
      void ensureLabs(summary.labs);
    }
  }, [tab, summary, ensureLabs]);

  const goToGl01 = () => {
    navigate('/labs');
    window.requestAnimationFrame(() => {
      document.querySelector('.labs-main')?.scrollIntoView({ behavior: 'smooth' });
    });
  };

  return (
    <div className="app-shell">
      <Header activeTab={tab} onTabChange={setTab} stats={headerStats} />
      <main
        id="main"
        className="app-main"
        style={{ padding: 0 }}
        role="tabpanel"
        aria-labelledby={`tab-${tab}`}
      >
        {loading && <p className="page-loading">Connecting to local API…</p>}
        {error && (
          <p className="inline-error page-error" role="alert">
            {error}. Start Django on 127.0.0.1:8000, then reload.
          </p>
        )}
        {!loading && summary && (
          <>
            {tab === 'labs' && labLoadError && (
              <p className="inline-error" role="alert">
                {labLoadError}
              </p>
            )}
            {tab === 'labs' && labsLoading && <p className="page-loading">Loading labs…</p>}
            {tab === 'labs' && (
              <LabsTab
                summary={summary}
                labsById={labsById}
                progress={progress}
                onProgressChange={() => void refreshProgress()}
                onSelectSetupLab={goToGl01}
              />
            )}
            {tab === 'exam' && <ExamDrillsTab summary={summary} />}
            {tab === 'coverage' && <CoverageTab />}
            {tab === 'start' && (
              <StartHereTab
                readiness={readiness}
                notice={notice}
                onDismissNotice={clearNotice}
                onReload={(message) => void reloadWithNotice(message)}
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/labs" replace />} />
      <Route path="/:tabSlug" element={<WorkbookShell />} />
      <Route path="*" element={<Navigate to="/labs" replace />} />
    </Routes>
  );
}
