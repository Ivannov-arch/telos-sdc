"use client";

import Link from "next/link";
import { useCallback } from "react";
import { useParams } from "next/navigation";
import { getReport, type BehavioralReport } from "@/lib/api";
import { INDICATOR_LABELS, missionById } from "@/lib/missions";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Icon, Loading } from "@/components/ui";

function indicatorState(key: string, value: unknown): { ok: boolean; text: string } {
  const v = value as { observed?: boolean; met_objectives?: boolean; evidence?: string; note?: string };
  return { ok: key === "decision_quality" ? !!v.met_objectives : !!v.observed, text: (key === "decision_quality" ? v.note : v.evidence) ?? "" };
}

function Report({ report, sessionId }: { report: BehavioralReport; sessionId: string }) {
  const m = missionById(report.mission);
  const gap = report.self_vs_observed_gap;
  const keys = ["calibrated_ai_trust", "critical_verification", "decision_quality", "adaptability"] as const;
  const base = `/play/${encodeURIComponent(sessionId)}`;
  return <>
    <section className="reveal-hero reveal">
      <div className="eyebrow"><span className="status-dot" style={{ background: "var(--lime)" }} /> THE REVEAL · {m?.code ?? "SIMULATION COMPLETE"}</div>
      <h1>That simulation was a <em>skill-sensing tool.</em></h1>
      <p>Based on how you made decisions, here is what we observed. You didn’t know what was being measured, which is why it shows how you actually decide.</p>
      <div className="actions"><Link className="btn lime" href={`${base}/roles`}>See roles that fit you<Icon size={16} /></Link><Link className="text-link" href="/play">Play another mission<Icon size={14} /></Link></div>
    </section>
    <div className="section-header"><div><div className="eyebrow" style={{ color: "var(--muted)" }}>WHAT WE OBSERVED</div><h2>Four signals from your decisions.</h2></div>{report.indicators._evaluated_by && <span className="pill">{report.indicators._evaluated_by.replace(/_/g, " ")}</span>}</div>
    <div className="indicator-grid stagger">{keys.map((key) => {
      const info = INDICATOR_LABELS[key]; const st = indicatorState(key, report.indicators[key]);
      return <section key={key} className={`indicator ${st.ok ? "observed" : "gap"}`}><div className="card-top"><span className="pill">{st.ok ? "OBSERVED" : "TO DEVELOP"}</span><span className="indicator-mark" aria-hidden="true">{st.ok ? <Icon name="check" size={15} /> : <Icon name="plus" size={15} />}</span></div><h3>{info.label}</h3><p className="indicator-q">{info.question}</p><p>{st.text}</p></section>;
    })}</div>
    <div className="two-col" style={{ marginTop: 20 }}>
      <section className="panel"><div className="eyebrow" style={{ color: "var(--muted)", marginBottom: 10 }}>WHAT YOU SAID VS. WHAT YOU DID</div><h2>Your claimed skills, next to your behaviour.</h2>
        <div className="gap-cols"><div><small className="gap-title">YOU TOLD US</small><div className="pills">{gap.claimed_skills.length ? gap.claimed_skills.map((s) => <span key={s} className="pill">{s}</span>) : <span className="helper">No skills listed.</span>}</div></div>
          <div><small className="gap-title">WE SAW STRENGTH IN</small><div className="pills">{gap.observed_strengths.length ? gap.observed_strengths.map((s) => <span key={s} className="pill accent">{s}</span>) : <span className="helper">Nothing flagged this time.</span>}</div></div>
          <div><small className="gap-title">AREAS TO DEVELOP</small><div className="pills">{gap.observed_gaps.length ? gap.observed_gaps.map((s) => <span key={s} className="pill">{s}</span>) : <span className="helper">No gaps flagged.</span>}</div></div></div>
        {gap.note && <p style={{ marginTop: 22, fontSize: 13 }}>{gap.note}</p>}
      </section>
      <aside className="stack"><section className="panel" style={{ background: "var(--featured-bg)" }}><Icon name="target" size={22} /><h3 style={{ margin: "13px 0 8px", fontSize: 17, fontWeight: 500 }}>What’s next</h3><p style={{ fontSize: 12 }}>Your behaviour, your skills and your mission choice are combined to find roles that fit, then a reskilling path for each.</p><div className="actions"><Link className="btn" href={`${base}/roles`}>Open role matches<Icon size={15} /></Link></div></section>
        <p className="notice" style={{ margin: 0 }}>{report.limitation_notice}</p></aside>
    </div>
  </>;
}

export default function ReportPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const res = useResource(useCallback(() => getReport(sessionId), [sessionId]));
  if (res.loading) return <Loading label="Reading what your decisions showed…" />;
  if (res.error || !res.data) return <><ErrorState message={res.error ?? "No report is available yet."} retry={res.retry} /><Link className="text-link" href={`/play/${encodeURIComponent(sessionId)}`}><Icon name="back" size={15} />Back to the simulation</Link></>;
  return <Report report={res.data} sessionId={sessionId} />;
}
