const API_BASE = '/api';

export interface AIQueryResponse {
  query: string;
  success: boolean;
  response: Record<string, unknown> | string;
  reasoning?: string | null;
  confidence?: number | null;
}

export async function queryNutritionAI(query: string): Promise<AIQueryResponse> {
  const res = await fetch(`${API_BASE}/ai/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}
