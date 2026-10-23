/**
 * Typed client for the Aiversecity backend, called from the browser through
 * the Next.js proxy at /api/backend/* (see src/app/api/backend/[...path]/route.ts).
 *
 * Every function throws an ApiError with the backend's `detail` message when
 * the request fails, so UI code can show the real reason instead of a generic one.
 */

// ── Types (mirror the FastAPI response models) ─────────────────────────────

export interface SkillEntry {
  skill_name: string;
  label: string | null;
  esco_id: string | null;
  confidence_score: number;
}

export interface UserProfile {
  id: string;
  hard_skills: SkillEntry[];
  soft_skills: SkillEntry[];
  experience_years: number;
  source_type: "pdf" | "form";
  has_dense_vector: boolean;
  message: string;
}

export interface ProfileSummary {
  id: string;
  experience_years: number;
  hard_skills: SkillEntry[];
  soft_skills: SkillEntry[];
  source_type: "pdf" | "form";
  created_at: string;
}

export interface ProfileFormInput {
  hard_skills: string[];
  soft_skills: string[];
  experience_years: number;
  raw_text?: string | null;
}

export interface ScoreBreakdown {
  rrf_score: number;
  hard_skill_coverage: number;
  seniority_match: number;
}

export interface SkillGapItem {
  skill: string;
  esco_id: string;
  type: string;
  urgency: string;
}

export interface SdgAlignment {
  sdg_goal: number;
  sdg_name: string;
  target: string | null;
  impact_reasoning: string;
  source: string;
  color_hex: string | null;
}

export interface MatchResult {
  target_role: string;
  esco_id: string;
  match_score: number;
  score_breakdown: ScoreBreakdown;
  skills_gap: SkillGapItem[];
  sdg_alignment: SdgAlignment[];
  ctci_score: number | null;
  compression_type: string | null;
}

export type MatchScenario = "moderate" | "fast";

export interface MatchResponse {
  user_id: string;
  scenario: MatchScenario;
  results: MatchResult[];
}

export interface SimulationTask {
  id: string;
  skill_id: string;
  skill_name: string;
  scenario_text: string;
  rubric_criteria: string[];
  difficulty: string;
  onet_task_ref: string | null;
}

export interface SimulateResult {
  simulation_id: string;
  task_id: string;
  scenario_text: string;
  score_percent: number;
  improvement_reasoning: string;
  missing_concepts: string[];
  evaluated: boolean;
}

export interface SimulationHistoryItem {
  id: string;
  task_id: string;
  user_response: string;
  score_percent: number;
  improvement_reasoning: string;
  missing_concepts: string[];
  evaluated_at: string | null;
  created_at: string;
  simulation_tasks: { skill_id: string; scenario_text: string; difficulty: string } | null;
}

// ── Error handling ─────────────────────────────────────────────────────────

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api/backend/${path}`, { ...init, cache: "no-store" });
  if (!res.ok) {
    let message = `Request failed with status ${res.status}`;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") message = body.detail;
      else if (Array.isArray(body?.detail)) message = body.detail.map((d: { msg?: string }) => d.msg ?? "").join("; ");
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(res.status, message);
  }
  return (await res.json()) as T;
}

// ── Profiles (Feature 1) ───────────────────────────────────────────────────

export function listProfiles() {
  return request<{ profiles: ProfileSummary[] }>("profiles");
}

export function getProfile(userId: string) {
  return request<UserProfile>(`profile/${encodeURIComponent(userId)}`);
}

export function createProfileFromForm(input: ProfileFormInput) {
  return request<UserProfile>("profile", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(input),
  });
}

export function createProfileFromPdf(file: File) {
  const form = new FormData();
  form.append("file", file);
  return request<UserProfile>("profile/upload", { method: "POST", body: form });
}

// ── Matching (Feature 3) ───────────────────────────────────────────────────

export function getMatches(userId: string, scenario: MatchScenario = "moderate", topK = 5) {
  const qs = new URLSearchParams({ user_id: userId, scenario, top_k: String(topK) });
  return request<MatchResponse>(`match?${qs}`);
}

// ── Simulation (Feature 4) ─────────────────────────────────────────────────

export function listSimulationTasks(skillId?: string, limit = 20) {
  const qs = new URLSearchParams({ limit: String(limit) });
  if (skillId) qs.set("skill_id", skillId);
  return request<{ tasks: SimulationTask[]; count: number }>(`simulate/tasks?${qs}`);
}

export function submitSimulation(userId: string, taskId: string, userResponse: string) {
  return request<SimulateResult>("simulate", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ user_id: userId, task_id: taskId, user_response: userResponse }),
  });
}

export function getSimulationHistory(userId: string) {
  return request<{ history: SimulationHistoryItem[]; total_attempts: number }>(
    `simulate/history?${new URLSearchParams({ user_id: userId })}`,
  );
}
