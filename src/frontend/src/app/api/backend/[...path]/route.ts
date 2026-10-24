/**
 * Server-side proxy to the FastAPI backend.
 *
 * The backend's /api/* routes require a trusted-operator bearer token
 * (API_ACCESS_TOKEN). That token must never reach the browser, so every
 * frontend request goes through this handler, which attaches it on the server.
 *
 *   GET  /api/backend/profiles            -> GET  {BACKEND_URL}/api/profiles
 *   POST /api/backend/profile             -> POST {BACKEND_URL}/api/profile
 *   GET  /api/backend/match?user_id=...   -> GET  {BACKEND_URL}/api/match?user_id=...
 */

import type { NextRequest } from "next/server";

const BACKEND_URL = (process.env.BACKEND_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");

async function proxy(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
): Promise<Response> {
  const token = process.env.API_ACCESS_TOKEN;
  if (!token) {
    return Response.json(
      { detail: "The server is missing API_ACCESS_TOKEN, so the data API is unavailable." },
      { status: 503 },
    );
  }

  const { path } = await params;
  const target = new URL(`${BACKEND_URL}/api/${path.map(encodeURIComponent).join("/")}`);
  target.search = request.nextUrl.search;

  const headers = new Headers();
  headers.set("Authorization", `Bearer ${token}`);
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("content-type", contentType);
  headers.set("accept", "application/json");

  const hasBody = request.method !== "GET" && request.method !== "HEAD";

  let upstream: Response;
  try {
    upstream = await fetch(target, {
      method: request.method,
      headers,
      body: hasBody ? await request.arrayBuffer() : undefined,
      cache: "no-store",
      redirect: "manual",
    });
  } catch {
    return Response.json(
      { detail: "The backend API is not reachable. Make sure the Backend API workflow is running." },
      { status: 502 },
    );
  }

  const responseHeaders = new Headers();
  const upstreamType = upstream.headers.get("content-type");
  if (upstreamType) responseHeaders.set("content-type", upstreamType);
  responseHeaders.set("cache-control", "no-store");

  return new Response(upstream.body, { status: upstream.status, headers: responseHeaders });
}

export { proxy as GET, proxy as POST, proxy as PUT, proxy as PATCH, proxy as DELETE };
