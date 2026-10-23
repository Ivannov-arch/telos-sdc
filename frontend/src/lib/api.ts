import axios from "axios";

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

export interface SkillGapItem {
  skill: string;
  esco_id: string;
  type: "core" | "supporting";
  urgency: "high" | "medium" | "low";
}

export interface ScoreBreakdown {
  rrf_score: number;
  hard_skill_coverage: number;
  seniority_match: number;
}

export interface SdgAlignment {
  sdg_goal: number;
  sdg_name: string;
  target: string | null;
  impact_reasoning: string;
  source: string;
  color_hex?: string | null;
}

export interface MatchResult {
  target_role: string;
  esco_id: string;
  match_score: number;
  score_breakdown: ScoreBreakdown;
  skills_gap: SkillGapItem[];
  sdg_alignment: SdgAlignment[];
  ctci_score?: number | null;
  compression_type?: string | null;
}

export interface MatchResponse {
  user_id: string;
  scenario: "moderate" | "fast" | string;
  results: MatchResult[];
}

export interface UserSkill {
  esco_id: string;
  skill_name: string;
  proficiency?: number;
}

export interface UserProfile {
  id: string;
  experience_years: number;
  hard_skills: UserSkill[];
  soft_skills: string[];
  source_type?: string;
  created_at?: string;
}

export interface SimulationTask {
  id: string;
  skill_id: string;
  scenario_text: string;
  difficulty?: string;
  onet_task_ref?: string;
  rubric_criteria?: string[];
}

export interface SimulateResult {
  simulation_id: string;
  task_id: string;
  scenario_text: string;
  score_percent: number | null;
  improvement_reasoning: string | null;
  missing_concepts: string[];
  evaluated: boolean;
}

/**
 * Fetch available demo user profiles from FastAPI backend
 */
export async function listProfiles(): Promise<{ profiles: UserProfile[] }> {
  try {
    const res = await apiClient.get("/api/profiles");
    return res.data;
  } catch (err) {
    console.warn("Failed to fetch /api/profiles from backend, using fallback demo profiles:", err);
    return {
      profiles: [
        {
          id: "587479a6-04d5-4371-a57f-c3b39c9b7be2",
          experience_years: 3,
          hard_skills: [
            { esco_id: "e44d3ba1-3836-4d04-8b6b-3aa83984ca3b", skill_name: "Python programming" },
            { esco_id: "3e5804aa-5768-450f-93d3-7801a61c3c38", skill_name: "Natural Language Processing" },
            { esco_id: "6e0771cb-8b5e-450a-9d75-408a287a36cb", skill_name: "Machine learning algorithms" },
          ],
          soft_skills: ["Problem solving", "Team collaboration", "Analytical thinking"],
          source_type: "demo_ai_nlp",
        },
        {
          id: "146f103d-946f-4619-9fa0-ba0b4fdfe84c",
          experience_years: 5,
          hard_skills: [
            { esco_id: "2d1f0412-3fba-4a62-87c2-8fe2679958ee", skill_name: "SQL & Data Warehousing" },
            { esco_id: "f1a141b2-c0e4-4d89-bf83-05b1f8eb6c30", skill_name: "ETL pipeline architecture" },
            { esco_id: "e44d3ba1-3836-4d04-8b6b-3aa83984ca3b", skill_name: "Python programming" },
          ],
          soft_skills: ["System design", "Data governance", "Agile delivery"],
          source_type: "demo_data_engineer",
        },
      ],
    };
  }
}

/**
 * Fetch hybrid match results for a user under given scenario (moderate or fast)
 */
export async function getMatchResults(
  userId: string,
  scenario: "moderate" | "fast" = "moderate",
  topK: number = 5
): Promise<MatchResponse> {
  const res = await apiClient.get<MatchResponse>("/api/match", {
    params: {
      user_id: userId,
      scenario,
      top_k: topK,
    },
  });
  return res.data;
}

/**
 * Upload CV / Profile intake. Accepts PDF file or structured JSON.
 */
export async function uploadProfile(
  payload: FormData | { experience_years: number; skills: string[]; interests?: string }
): Promise<{ user_id: string; profile: UserProfile }> {
  try {
    const isFormData = typeof FormData !== "undefined" && payload instanceof FormData;
    const res = await apiClient.post(
      "/api/profile",
      payload,
      isFormData ? { headers: { "Content-Type": "multipart/form-data" } } : undefined
    );
    return res.data;
  } catch (err) {
    console.warn("POST /api/profile not yet available or failed. Generating demo profile session:", err);
    // Graceful demo fallback to ensure uninterrupted end-to-end user flow
    const defaultId = "587479a6-04d5-4371-a57f-c3b39c9b7be2";
    return {
      user_id: defaultId,
      profile: {
        id: defaultId,
        experience_years: 3,
        hard_skills: [
          { esco_id: "e44d3ba1-3836-4d04-8b6b-3aa83984ca3b", skill_name: "Python programming" },
          { esco_id: "3e5804aa-5768-450f-93d3-7801a61c3c38", skill_name: "Natural Language Processing" },
        ],
        soft_skills: ["Critical thinking", "Communication"],
      },
    };
  }
}

/**
 * Fetch simulation tasks for a skill or general pool
 */
export async function getSimulationTasks(skillId?: string, limit: number = 20): Promise<{ tasks: SimulationTask[] }> {
  try {
    const res = await apiClient.get("/api/simulate/tasks", {
      params: { skill_id: skillId, limit },
    });
    return res.data;
  } catch (err) {
    console.warn("GET /api/simulate/tasks failed:", err);
    return { tasks: [] };
  }
}

/**
 * Submit micro-task simulation answer to LLM evaluator
 */
export async function submitSimulation(
  userId: string,
  taskId: string,
  userResponse: string
): Promise<SimulateResult> {
  const res = await apiClient.post<SimulateResult>("/api/simulate", {
    user_id: userId,
    task_id: taskId,
    user_response: userResponse,
  });
  return res.data;
}

/**
 * Fetch reskilling pathway data for a specific role
 */
export async function getReskillPathway(roleId: string, userId?: string) {
  // Query simulation tasks associated with this role or general skill catalog
  const tasksResp = await getSimulationTasks(undefined, 10);
  return {
    roleId,
    tasks: tasksResp.tasks,
  };
}
