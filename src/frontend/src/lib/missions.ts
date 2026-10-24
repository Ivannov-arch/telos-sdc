import type { MissionId } from "./api";

export interface Mission {
  id: MissionId;
  code: string;
  title: string;
  crisis: string;
  sdg: string;
  sdgGoal: number;
  pitch: string;
}

/** The three SDG-linked crisis missions offered by the simulation. */
export const MISSIONS: Mission[] = [
  { id: "A", code: "MISSION A", title: "Supply Under Pressure", crisis: "Food supply chain collapse in Southeast Asia", sdg: "SDG 2 · Zero Hunger", sdgGoal: 2, pitch: "Four routes, a limited budget, and millions at risk. Decide how food moves." },
  { id: "B", code: "MISSION B", title: "The Credit Algorithm", crisis: "A biased credit-scoring AI is denying loans", sdg: "SDG 10 · Reduced Inequalities", sdgGoal: 10, pitch: "Regulators are watching. Decide how to fix a system that treated people unfairly." },
  { id: "C", code: "MISSION C", title: "Grid Failure", crisis: "A green energy grid fails at peak demand", sdg: "SDG 7 · Clean Energy", sdgGoal: 7, pitch: "Hospitals and 2.3 million homes are in the dark. Decide how to bring power back." },
];

export function missionById(id: string | undefined | null): Mission | undefined {
  return MISSIONS.find((m) => m.id === id);
}

export const ROUND_LABELS = ["Set your strategy", "AI recommends", "The AI shock", "Final decision"] as const;

export const INDICATOR_LABELS: Record<string, { label: string; question: string }> = {
  calibrated_ai_trust: { label: "Calibrated AI trust", question: "Did you adjust how much you relied on the AI based on the evidence?" },
  critical_verification: { label: "Critical verification", question: "Did you check the relevant data before deciding?" },
  decision_quality: { label: "Decision quality", question: "Did your final decision meet the mission’s objectives within its limits?" },
  adaptability: { label: "Adaptability", question: "Did you revise your strategy after the shock?" },
};
