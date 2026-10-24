"use client";

import Link from "next/link";
import { useCallback, useState } from "react";
import { useParams } from "next/navigation";
import { getPathway, type PathwayScenario } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Icon, Loading, PageIntro } from "@/components/ui";

export default function PathwayPage() {
  const { sessionId, roleId } = useParams<{ sessionId: string; roleId: string }>();
  const [scenario, setScenario] = useState<PathwayScenario>("moderate");
  const res = useResource(useCallback(() => getPathway(roleId, sessionId, scenario), [roleId, sessionId, scenario]));
  const total = res.data?.steps.reduce((sum, s) => sum + s.time_estimate_weeks, 0) ?? 0;
  return <>
    <PageIntro eyebrow="YOUR RESKILLING PATH" title={res.data ? `Your path to ${res.data.role_title}.` : "Your reskilling path."} description="Step-by-step, built from the skill gaps we found. Time estimates are estimates, not predictions."><Link className="btn secondary" href={`/play/${encodeURIComponent(sessionId)}/roles`}><Icon name="back" size={15} />All role matches</Link></PageIntro>
    <div className="controls"><div className="field"><span className="eyebrow" style={{ color: "var(--muted)" }}>AI ADOPTION SCENARIO</span><div className="tabs" role="tablist" aria-label="AI adoption scenario">{(["moderate", "rapid"] as const).map((s) => <button key={s} type="button" role="tab" aria-selected={scenario === s} className={scenario === s ? "selected" : ""} onClick={() => setScenario(s)}>{s === "moderate" ? "Moderate AI adoption" : "Rapid AI adoption"}</button>)}</div></div></div>
    {res.loading ? <Loading label="Charting your path…" /> : res.error || !res.data ? <ErrorState message={res.error ?? "No pathway is available."} retry={res.retry} /> : <>
      <div className="meta-row" style={{ marginBottom: 14 }}><span className="eyebrow">{res.data.steps.length} STEPS</span><span className="pill">≈ {total} WEEKS IN TOTAL (ESTIMATE)</span></div>
      <ol className="path-list stagger">{res.data.steps.map((step) => <li key={step.step} className="path-step"><div className="path-num">{String(step.step).padStart(2, "0")}</div><div className="path-body">
        <div className="pills" style={{ marginBottom: 10 }}><span className="pill">{step.type}</span><span className="sg-urgency" data-priority={step.urgency}>{step.urgency}</span><span className="pill">~{step.time_estimate_weeks} wk</span></div>
        <h3>{step.skill}</h3>
        {step.sources.length > 0 && <ul className="path-sources">{step.sources.map((src) => <li key={src.url}><a href={src.url} target="_blank" rel="noopener noreferrer">{src.title}<Icon name="arrow" size={13} /></a></li>)}</ul>}
        {step.sdg && <div className="sdg-entry"><h3>SDG {step.sdg.sdg_goal} · {step.sdg.sdg_name}</h3><p>{step.sdg.rationale}</p></div>}
      </div></li>)}</ol>
    </>}
  </>;
}
