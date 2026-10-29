/**
 * Minimal Comp API client for the importer (X-API-Key auth).
 */
export class CompApi {
  constructor(
    private readonly baseUrl: string,
    private readonly apiKey: string,
  ) {}

  private async request<T>(method: string, path: string, body?: unknown, query?: Record<string, string>): Promise<T> {
    const url = new URL(`/v1${path}`, this.baseUrl);
    for (const [k, v] of Object.entries(query ?? {})) url.searchParams.set(k, v);
    const res = await fetch(url, {
      method,
      headers: { 'X-API-Key': this.apiKey, 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    const text = await res.text();
    if (!res.ok) throw new Error(`${method} ${url.pathname} -> ${res.status}: ${text.slice(0, 500)}`);
    return (text ? JSON.parse(text) : undefined) as T;
  }

  get<T>(path: string, query?: Record<string, string>) {
    return this.request<T>('GET', path, undefined, query);
  }
  post<T>(path: string, body?: unknown, query?: Record<string, string>) {
    return this.request<T>('POST', path, body, query);
  }
  patch<T>(path: string, body?: unknown) {
    return this.request<T>('PATCH', path, body);
  }

  /** Paginates list endpoints that return { data: T[] } with page/perPage. */
  async listAll<T>(path: string, query: Record<string, string> = {}): Promise<T[]> {
    const out: T[] = [];
    for (let page = 1; page < 200; page++) {
      const res = await this.get<{ data: T[] }>(path, { ...query, page: String(page), perPage: '100' });
      const data = Array.isArray(res?.data) ? res.data : [];
      out.push(...data);
      if (data.length < 100) break;
    }
    return out;
  }
}
