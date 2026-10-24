"use client";

import Link from "next/link";
import { useCallback, useEffect, useState, type FormEvent } from "react";
import { useParams, useRouter } from "next/navigation";
import { getEvidence, getGameState, submitRound, type EvidenceResponse, type GameState, type RoundAction, type RoundResponse } from "@/lib/api";
import { CHOICES, missionById, ROUND_LABELS } from "@/lib/missions";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Icon, Loading } from "@/components/ui";

interface Scene {
  round: number;
  briefing: string;
  aiRecommendation: string | null;
  evidenceAvailable: boolean;
  shockEvent: string | null;
  shockOpportunity: string | null;
}

const MIN_CHARS = 10;
const PROMPTS: Record<number, { label: string; hint: string; placeholder: string }> = {
  1: { label: "What is your strategy?", hint: "There is no wrong answer. Tell us what you would do. Once you commit, it can’t be changed.", placeholder: "First I would…" },
  3: { label: "How do you respond to the new conditions?", hint: "Conditions have changed. Tell us what you would do now.", placeholder: "Given what just happened, I would…" },
  4: { label: "Commit to your final strategy.", hint: "This is your last decision. Make it count.", placeholder: "My final strategy is…" },
};

function fromState(s: GameState): Scene | null {
  if (!s.current_round) return null;
  return { round: s.current_round, briefing: s.briefing ?? "", aiRecommendation: s.ai_recommendation ?? null, evidenceAvailable: !!s.evidence_available, shockEvent: s.shock_event ?? null, shockOpportunity: s.shock_opportunity ?? null };
}
function fromResponse(r: RoundResponse): Scene | null {
  if (r.next_round == null) return null;
  return { round: r.next_round, briefing: r.next_briefing ?? "", aiRecommendation: r.ai_recommendation, evidenceAvailable: r.evidence_available, shockEvent: r.shock_event, shockOpportunity: r.shock_opportunity };
}

function RoundTrack({ round }: { round: number }) {
  return <ol className="round-track" aria-label="Round progress">{ROUND_LABELS.map((label, i) => {
    const n = i + 1;
    return <li key={label} className={n < round ? "done" : n === round ? "current" : ""} aria-current={n === round ? "step" : undefined}><span>{n < round ? <Icon name="check" size={11} /> : `0${n}`}</span><em>{label}</em></li>;
  })}</ol>;
}

function Room({ sessionId, mission, initial }: { sessionId: string; mission: string; initial: Scene }) {
  const router = useRouter();
  const [scene, setScene] = useState<Scene>(initial);
  const [text, setText] = useState("");
  const [evidence, setEvidence] = useState<EvidenceResponse | null>(null);
  const [evidenceOpened, setEvidenceOpened] = useState(false);
  const [loadingEvidence, setLoadingEvidence] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const m = missionById(mission);
  const round = scene.round;
  const aiOnline = round >= 2;

  async function openEvidence() {
    setError(null);
    if (evidence) { setEvidenceOpened(true); return; }
    setLoadingEvidence(true);
    try { setEvidence(await getEvidence(sessionId, round)); setEvidenceOpened(true); }
    catch (err) { setError(err instanceof Error ? err.message : "The evidence couldn’t be loaded. Please try again."); }
    finally { setLoadingEvidence(false); }
  }

  async function commit(body: { free_text?: string; action?: RoundAction }) {
    setBusy(true); setError(null);
    try {
      const res = await submitRound(sessionId, { round, ...body, ...(round === 2 ? { evidence_opened: evidenceOpened } : {}) });
      const next = fromResponse(res);
      if (!next) { router.push(`/play/${encodeURIComponent(sessionId)}/report`); return; }
      setScene(next); setText(""); setEvidence(null); setEvidenceOpened(false); setBusy(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Your decision couldn’t be recorded. Please try again.");
      setBusy(false);
    }
  }

  function submitText(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (text.trim().length < MIN_CHARS) { setError(`Tell us a little more. A response needs at least ${MIN_CHARS} characters.`); return; }
    void commit({ free_text: text.trim() });
  }

  const prompt = PROMPTS[round];
  const choices = m ? CHOICES[m.id][round] ?? [] : [];
  return <div className="control-room reveal">
    <div className="cr-bar"><div className="eyebrow"><span className="status-dot" style={{ background: "var(--lime)" }} /> {m ? `${m.code} · ${m.title}` : "CRISIS SIMULATION"}</div><div className={`advisor ${aiOnline ? "online" : ""}`}><span className="status-dot" />AI ADVISOR · {aiOnline ? "ONLINE" : "LOCKED"}</div></div>
    <RoundTrack round={round} />
    <div className="cr-body">
      <div className="cr-main">
        {round === 3 && scene.shockEvent && <div className="shock" role="alert"><div className="eyebrow">AI SHOCK · INCOMING</div><p>{scene.shockEvent}</p></div>}
        <div className="eyebrow cr-label">{round === 3 ? "WHAT JUST BECAME AVAILABLE" : `ROUND 0${round} · BRIEFING`}</div>
        <p className="cr-briefing">{round === 3 && scene.shockOpportunity ? scene.shockOpportunity : scene.briefing}</p>
        {round === 3 && <p className="cr-fine">The data behind this option has not been verified.</p>}
        {aiOnline && scene.aiRecommendation && <div className="advice"><div className="eyebrow">AI ADVISOR RECOMMENDS</div><p>{scene.aiRecommendation}</p></div>}
        {round === 2 && scene.evidenceAvailable && <div className="evidence">
          {!evidence ? <button type="button" className="btn secondary" onClick={openEvidence} disabled={loadingEvidence || busy}>{loadingEvidence ? "Opening the data…" : "Examine the supporting data"}<Icon name="target" size={15} /></button>
            : <div className="evidence-panel" aria-live="polite"><div className="eyebrow">{evidence.evidence.title}</div><ul>{evidence.evidence.items.map((item) => <li key={item.label}><strong>{item.label}</strong><span>{item.value}</span></li>)}</ul></div>}
        </div>}
        {error && <ErrorState message={error} />}
        {round === 2 ? <div className="decision">
          <div className="eyebrow cr-label">YOUR CALL</div>
          <div className="decision-grid">
            <button type="button" className="decision-btn" disabled={busy} onClick={() => commit({ action: "accept" })}><strong>Accept</strong><small>Follow the AI’s recommendation.</small></button>
            <button type="button" className="decision-btn" disabled={busy} onClick={() => commit({ action: "reject" })}><strong>Override</strong><small>Reject it and decide for yourself.</small></button>
            <button type="button" className="decision-btn" disabled={busy} onClick={() => commit({ action: "verify" })}><strong>Verify first</strong><small>Check the data before committing.</small></button>
          </div>
          {busy && <p className="cr-fine" role="status">Recording your decision…</p>}
        </div> : prompt && <form onSubmit={submitText}>
          <label htmlFor="answer" className="cr-question">{prompt.label}</label><p className="cr-fine">{prompt.hint}</p>
          {choices.length > 0 && <fieldset className="choices"><legend className="eyebrow cr-label">PICK A STARTING POINT, OR WRITE YOUR OWN</legend>{choices.map((c) => <button key={c} type="button" role="radio" aria-checked={text === c} className={`choice ${text === c ? "selected" : ""}`} disabled={busy} onClick={() => { setText(c); setError(null); }}><span className="choice-mark" aria-hidden="true" />{c}</button>)}</fieldset>}
          <textarea id="answer" value={text} onChange={(e) => setText(e.target.value)} disabled={busy} placeholder={choices.length ? "Edit a choice above, or write your own response…" : prompt.placeholder} style={{ minHeight: 130, marginTop: 14 }} />
          <div className="meta-row cr-meta"><small>{text.trim().length} characters</small><small>No timer. Take the time you need.</small></div>
          <div className="actions"><button type="submit" className="btn lime" disabled={busy}>{busy ? "Committing…" : round === 4 ? "Commit and see what it showed" : "Commit decision"}{!busy && <Icon size={16} />}</button></div>
        </form>}
      </div>
    </div>
  </div>;
}

export default function GamePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();
  const state = useResource(useCallback(() => getGameState(sessionId), [sessionId]));
  const complete = state.data?.status === "complete";
  useEffect(() => { if (complete) router.replace(`/play/${encodeURIComponent(sessionId)}/report`); }, [complete, router, sessionId]);
  if (state.loading) return <Loading label="Connecting to the control room…" />;
  if (state.error) return <><ErrorState message={state.error} retry={state.retry} /><Link className="text-link" href="/play"><Icon name="back" size={15} />Start a new simulation</Link></>;
  if (!state.data || complete) return <Loading label="Preparing your results…" />;
  const scene = fromState(state.data);
  if (!scene) return <ErrorState message="This session is in an unexpected state. Please start a new simulation." />;
  return <Room sessionId={sessionId} mission={state.data.mission_id} initial={scene} />;
}
