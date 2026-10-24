"use client";

import Link from "next/link";
import { useCallback } from "react";
import { useParams } from "next/navigation";
import { getRoleMatches, type RoleMatch } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Icon, Loading, Meter, PageIntro } from "@/components/ui";

function RoleCard({ role, sessionId }: { role: RoleMatch; sessionId: string }) {
  const b = role.score_breakdown;
  return <section className="panel match-card reveal">
    <div className="match-head"><div><div className="eyebrow" style={{ color: "var(--muted)" }}>RANK {role.rank} · {role.esco_id}</div><h2>{role.title}</h2></div><div className="score">{Math.round(role.match_score * 100)}<small>% fit</small></div></div>
    <p style={{ marginTop: 12 }}>{role.description}</p>
    <div className="breakdown">{[["Behavioural evidence", b.behavioral_score], ["Your stated skills", b.profile_score], ["Mission fit", Math.min(1, b.mission_bonus * 10)]].map(([label, v]) => <div key={label as string}><div className="meta-row"><span>{label}</span><span>{Math.round((v as number) * 100)}%</span></div><Meter value={v as number} /></div>)}</div>
    <p className="notice" style={{ margin: "0 0 22px" }}>{role.reasoning}</p>
    {role.skills_possessed.length > 0 && <><div className="eyebrow" style={{ color: "var(--muted)", marginBottom: 10 }}>SKILLS YOU ALREADY BRING</div><div className="pills" style={{ marginBottom: 22 }}>{role.skills_possessed.map((s) => <span key={s} className="pill accent">{s}</span>)}</div></>}
    <div className="sg-heading"><div className="eyebrow" style={{ color: "var(--muted)" }}>SKILLS TO BUILD</div></div>
    <ul className="sg-list" style={{ marginTop: 10 }}>{role.skill_gaps.map((g) => <li key={g.esco_id}><div className="sg-link"><span className="sg-skill">{g.skill}<small>{g.type}</small></span><span className="sg-urgency" data-priority={g.urgency}>{g.urgency}</span></div></li>)}</ul>
    {role.sdg_alignment.map((s) => <div className="sdg-entry" key={s.sdg_goal}><h3>SDG {s.sdg_goal} · {s.sdg_name}</h3><p>{s.impact_reasoning}</p><small>Source: {s.source}</small></div>)}
    <div className="actions"><Link className="btn" href={`/play/${encodeURIComponent(sessionId)}/pathway/${encodeURIComponent(role.id)}`}>Build my reskilling path<Icon size={15} /></Link></div>
  </section>;
}

export default function RolesPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const res = useResource(useCallback(() => getRoleMatches(sessionId), [sessionId]));
  const back = `/play/${encodeURIComponent(sessionId)}/report`;
  return <>
    <PageIntro eyebrow="FUTURE SKILLS RADAR" title="Roles your decisions point toward." description="Three roles ranked by what we observed, what you told us, and the crisis you chose."><Link className="btn secondary" href={back}><Icon name="back" size={15} />Back to your report</Link></PageIntro>
    {res.loading ? <Loading label="Matching your behaviour to roles…" /> : res.error || !res.data ? <ErrorState message={res.error ?? "No role matches are available yet."} retry={res.retry} /> : <>
      {res.data.roles.map((role) => <RoleCard key={role.id} role={role} sessionId={sessionId} />)}
      <p className="notice">{res.data.guardrail} Source: {res.data.data_source} ({res.data.data_date}).</p>
    </>}
  </>;
}
