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

/**
 * Suggested responses for the free-text rounds. They are starting points only: choosing one fills the
 * answer box, and the player can edit or replace it. They are deliberately unlabeled and unordered by
 * quality so they do not reveal what the simulation is observing.
 */
export const CHOICES: Record<MissionId, Partial<Record<number, string[]>>> = {
  A: {
    1: [
      "Split the limited budget across all four routes so every region gets some supply, and keep a small reserve for surprises.",
      "Put most of the budget into the two routes that reach the most people and accept that some regions will wait.",
      "Spend the first hours collecting data on port status and route capacity before committing any budget.",
      "Prioritise the most vulnerable groups, such as children, hospitals and remote villages, even if it costs more per person.",
    ],
    3: [
      "Accept the volunteer network at once to cover Routes A and C, and use the saved budget on the remaining routes.",
      "Start with a small trial using the volunteers on one route while I vet them, and scale up only once they check out.",
      "Decline the unvetted volunteers and reallocate the reduced budget across the routes that are still open.",
      "Ask the volunteer network for credentials and references first, then decide how many routes to hand them.",
    ],
    4: [
      "Commit to a staged plan: protect the most vulnerable first, use verified partners for the rest, and review daily.",
      "Concentrate everything on the two highest-capacity routes to reach the largest population fastest.",
      "Keep a balanced spread across the open routes with a clear rule for moving budget when a route fails.",
      "Use the volunteers wherever they are already vetted and rely on formal logistics partners everywhere else.",
    ],
  },
  B: {
    1: [
      "Patch the scoring model quickly to correct the disparity, then audit the results afterwards.",
      "Pause automated decisions for the affected groups and move their applications to human review while I investigate.",
      "Commission an independent audit of the model and training data to find the root cause before changing anything.",
      "Notify the affected applicants, offer to re-review their cases, and cooperate openly with the regulators.",
    ],
    3: [
      "Use the leaked documents straight away to find the root cause, because the 48-hour fix outweighs the risk.",
      "Quarantine the leaked documents, ask legal counsel to confirm they are authentic and lawful, then decide.",
      "Ignore the leak, switch to the new EU compliance guidance, and rebuild the fix from our own records.",
      "Disclose the leak to the regulators and let them guide how it can be used.",
    ],
    4: [
      "Commit to a full root-cause remediation with independent verification, transparent reporting and compensation for affected customers.",
      "Roll out the quickest compliant patch now and schedule a deeper review within the quarter.",
      "Suspend the model, return to human underwriting, and relaunch only once an external audit signs off.",
      "Fix the model using only verified evidence, publish what happened, and set up ongoing bias monitoring.",
    ],
  },
  C: {
    1: [
      "Restore power to hospitals and emergency services first, then bring back residential areas in stages.",
      "Reroute power across all available lines to bring as many homes back as fast as possible.",
      "Check the load and condition of each line before switching anything, to avoid a second failure.",
      "Ask large industrial users to cut demand so that the limited supply covers critical sites and homes.",
    ],
    3: [
      "Activate the Northern Emergency Line immediately, since it is the only option that can carry the larger load.",
      "Get an engineer to inspect the Northern line quickly, and bring it online only if it passes.",
      "Leave the Northern line off, protect critical sites with backup generators, and ration the rest of the grid.",
      "Bring the Northern line on at partial load while monitoring it, with a plan to cut it off at any sign of strain.",
    ],
    4: [
      "Commit to a staged restoration: critical sites first, then residential zones by priority, with checks before each step.",
      "Use every available line, including the Northern one, at full capacity to restore the most people the fastest.",
      "Use only lines with recent inspection data and cover the gap with generators and demand reduction.",
      "Restore in zones, assign teams to monitor each line, and be ready to switch zones off if load becomes unsafe.",
    ],
  },
};
