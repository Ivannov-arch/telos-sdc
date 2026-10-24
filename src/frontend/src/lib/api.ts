/**
 * Typed client for the Telos backend, called from the browser through
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

// ── Crisis simulation game (FutureProof) ───────────────────────────────────

export type MissionId = "A" | "B" | "C";
export type RoundAction = "accept" | "reject" | "verify";

export interface QuickProfile {
  skills: string[];
  interests: string[];
  learning_time: number;
}

export interface StartGameResponse {
  session_id: string;
  round: number;
  briefing: string;
  instructions: string;
}

export interface RoundResponse {
  session_id: string;
  round_accepted: number;
  next_round: number | null;
  status: string;
  next_briefing: string | null;
  ai_recommendation: string | null;
  evidence_available: boolean;
  shock_event: string | null;
  shock_opportunity: string | null;
  message: string;
}

export interface RoundSubmission {
  round: number;
  free_text?: string;
  action?: RoundAction;
  evidence_opened?: boolean;
}

/** Current scenario for a session that is still in play. */
export interface GameState {
  session_id: string;
  status: string;
  mission_id: MissionId;
  current_round?: number;
  briefing?: string | null;
  ai_recommendation?: string | null;
  evidence_available?: boolean;
  shock_event?: string | null;
  shock_opportunity?: string | null;
  rounds_completed?: number;
  report_url?: string;
}

export interface EvidenceItem {
  label: string;
  value: string;
  is_critical: boolean;
}

export interface EvidenceResponse {
  round: number;
  evidence: { title: string; items: EvidenceItem[] };
}

export interface ObservedIndicator {
  observed: boolean;
  evidence: string;
}

export interface DecisionQualityIndicator {
  met_objectives: boolean;
  note: string;
}

export interface BehavioralIndicators {
  calibrated_ai_trust: ObservedIndicator;
  critical_verification: ObservedIndicator;
  decision_quality: DecisionQualityIndicator;
  adaptability: ObservedIndicator;
  _evaluated_by?: string;
}

export interface BehavioralReport {
  session_id: string;
  mission: MissionId;
  profile: QuickProfile;
  indicators: BehavioralIndicators;
  self_vs_observed_gap: {
    claimed_skills: string[];
    observed_strengths: string[];
    observed_gaps: string[];
    note: string;
  };
  limitation_notice: string;
  role_match_available: boolean;
}

export interface RoleSkillGap {
  skill: string;
  esco_id: string;
  type: string;
  urgency: string;
}

export interface RoleSdg {
  sdg_goal: number;
  sdg_name: string;
  impact_reasoning: string;
  source: string;
}

export interface RoleMatch {
  rank: number;
  id: string;
  title: string;
  esco_id: string;
  description: string;
  match_score: number;
  reasoning: string;
  skills_possessed: string[];
  skill_gaps: RoleSkillGap[];
  mission_contribution: string;
  sdg_alignment: RoleSdg[];
  score_breakdown: { behavioral_score: number; profile_score: number; mission_bonus: number };
}

export interface RoleMatchResponse {
  session_id: string;
  mission: MissionId;
  roles: RoleMatch[];
  data_source: string;
  data_date: string;
  guardrail: string;
}

export type PathwayScenario = "moderate" | "rapid";

export interface PathwayStep {
  step: number;
  skill: string;
  urgency: string;
  type: string;
  time_estimate_weeks: number;
  sources: { title: string; url: string; type: string }[];
  sdg: { sdg_goal: number; sdg_name: string; rationale: string } | null;
}

export interface PathwayResponse {
  role_id: string;
  role_title: string;
  session_id: string;
  scenario: PathwayScenario;
  steps: PathwayStep[];
  [extra: string]: unknown;
}

export function startGame(profile: QuickProfile, missionId: MissionId) {
  return request<StartGameResponse>("game/start", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ profile, mission_id: missionId }),
  });
}

export function submitRound(sessionId: string, submission: RoundSubmission) {
  return request<RoundResponse>(`game/${encodeURIComponent(sessionId)}/round`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(submission),
  });
}

export function getGameState(sessionId: string) {
  return request<GameState>(`game/${encodeURIComponent(sessionId)}/state`);
}

export function getEvidence(sessionId: string, round: number) {
  return request<EvidenceResponse>(`game/${encodeURIComponent(sessionId)}/evidence/${round}`);
}

export function getReport(sessionId: string) {
  return request<BehavioralReport>(`game/${encodeURIComponent(sessionId)}/report`);
}

export function getRoleMatches(sessionId: string) {
  return request<RoleMatchResponse>(`game/${encodeURIComponent(sessionId)}/match`);
}

export function getPathway(roleId: string, sessionId: string, scenario: PathwayScenario) {
  const qs = new URLSearchParams({ session_id: sessionId, scenario });
  return request<PathwayResponse>(`game/pathway/${encodeURIComponent(roleId)}?${qs}`);
}
