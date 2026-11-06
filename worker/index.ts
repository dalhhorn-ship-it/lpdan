// Cloudflare Worker entry (danfactory scaffold).
// /version proves which commit is live (deploy-watcher); /health is a cheap smoke check.
// Everything else is served from static assets (your built app).
interface Env {
  ASSETS?: { fetch(request: Request): Promise<Response> };
  GIT_SHA?: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { pathname } = new URL(request.url);
    if (pathname === "/version") {
      return Response.json({ sha: env.GIT_SHA ?? "dev" }, { headers: { "cache-control": "no-store" } });
    }
    if (pathname === "/health") {
      return new Response("ok", { headers: { "cache-control": "no-store" } });
    }
    return env.ASSETS ? env.ASSETS.fetch(request) : new Response("Not found", { status: 404 });
  },
};
