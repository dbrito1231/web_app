const API_BASE =
  import.meta.env.VITE_API_BASE?.replace(/\/$/, '') ?? 'http://127.0.0.1:8000';

function csrfToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : null;
}

async function request<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const headers = new Headers(init.headers);
  if (!headers.has('Content-Type') && init.body) {
    headers.set('Content-Type', 'application/json');
  }
  const method = (init.method ?? 'GET').toUpperCase();
  if (method !== 'GET' && method !== 'HEAD') {
    const token = csrfToken();
    if (token) {
      headers.set('X-CSRFToken', token);
    }
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    credentials: 'include',
    headers,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const err = (await response.json()) as { error?: string };
      if (err.error) detail = err.error;
    } catch {
      if (response.status === 403) {
        detail =
          "Your answer couldn't be saved — the app's server refused the request";
      }
    }
    throw new Error(detail || `HTTP ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export async function ensureSession(): Promise<void> {
  await request<{ status: string }>('/api/health');
}

export const api = {
  health: () => request<{ status: string }>('/api/health'),
  contentSummary: () => request<import('../types').ContentSummary>('/api/content/summary'),
  questionCatalog: () =>
    request<{ questions: import('../types').QuestionCatalogRow[] }>('/api/content/catalog'),
  lesson: (id: string) => request<import('../types').Lesson>(`/api/lessons/${id}`),
  question: (id: string) => request<import('../types').Question>(`/api/questions/${id}`),
  submitAttempt: (body: {
    questionId: string;
    selectedIds: string[];
    mode: 'practice' | 'exam';
    assisted?: boolean;
    presentedOrder?: string[];
  }) =>
    request<import('../types').AttemptResult>('/api/attempts', {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  lab: (id: string, reveal = false) =>
    request<import('../types').Lab>(
      `/api/labs/${encodeURIComponent(id)}${reveal ? '?reveal=1' : ''}`,
    ),
  labCheckpoint: (labId: string, checkpointId: string, status: string) =>
    request('/api/labs/' + encodeURIComponent(labId) + '/checkpoints', {
      method: 'POST',
      body: JSON.stringify({ checkpointId, status }),
    }),
  progress: () => request<import('../types').ProgressSnapshot>('/api/progress'),
  exportProgress: () => request<Record<string, unknown>>('/api/export', { method: 'POST' }),
  importProgress: (payload: unknown) =>
    request<{ ok: boolean }>('/api/import', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  resetProgress: () =>
    request<{ ok: boolean }>('/api/reset', {
      method: 'POST',
      body: JSON.stringify({ confirm: 'RESET' }),
    }),
  readiness: () => request<import('../types').ReadinessPayload>('/api/metrics/readiness'),
  coverage: () => request<import('../types').CoveragePayload>('/api/coverage'),
};
