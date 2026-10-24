"use client";

import { useSyncExternalStore } from "react";
import type { MissionId } from "./api";

/** A game session this browser has started. Sessions live on the server; we only remember their ids. */
export interface SavedSession {
  id: string;
  mission: MissionId;
  startedAt: string;
  skills: string[];
}

const KEY = "aiversecity.sessions";
const subscribers = new Set<() => void>();
let cache: { raw: string | null; list: SavedSession[] } = { raw: null, list: [] };
const EMPTY: SavedSession[] = [];

function read(): SavedSession[] {
  let raw: string | null = null;
  try { raw = localStorage.getItem(KEY); } catch { return cache.list; }
  if (raw === cache.raw) return cache.list;
  let list: SavedSession[] = [];
  try { const parsed = raw ? JSON.parse(raw) : []; if (Array.isArray(parsed)) list = parsed; } catch { /* corrupt entry: start fresh */ }
  cache = { raw, list };
  return list;
}

export function saveSession(session: SavedSession) {
  const next = [session, ...read().filter((s) => s.id !== session.id)].slice(0, 20);
  const raw = JSON.stringify(next);
  try { localStorage.setItem(KEY, raw); } catch { /* storage unavailable: session still works via its URL */ }
  cache = { raw, list: next };
  subscribers.forEach((cb) => cb());
}

function subscribe(cb: () => void) {
  subscribers.add(cb);
  window.addEventListener("storage", cb);
  return () => { subscribers.delete(cb); window.removeEventListener("storage", cb); };
}

export function useSavedSessions(): SavedSession[] {
  return useSyncExternalStore(subscribe, read, () => EMPTY);
}
