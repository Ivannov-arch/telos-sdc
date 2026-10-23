"use client";

import Link from "next/link";
import { useCallback, useEffect, useId, useState } from "react";
import { useParams } from "next/navigation";
import { getMatches, type MatchScenario, type SkillGapItem } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { useActiveProfile } from "@/components/shell";
import { Empty, ErrorState, Icon, Loading, Meter, PageIntro } from "@/components/ui";

const GAP_PREVIEW_COUNT = 8;
const urgencyOrder: Record<string, number> = {
  critical: 0,
  immediate: 0,
  urgent: 0,
  high: 1,
  medium: 2,
  moderate: 2,
  low: 3,
};

function SkillsGapList({ gaps, profileId }: { gaps: SkillGapItem[]; profileId: string }) {
  const [expanded, setExpanded] = useState(false);
  const listId = useId();
  const sorted = [...gaps].sort((a, b) =>
    (urgencyOrder[a.urgency.trim().toLowerCase()] ?? 4) -
    (urgencyOrder[b.urgency.trim().toLowerCase()] ?? 4),
  );
  const visible = expanded ? sorted : sorted.slice(0, GAP_PREVIEW_COUNT);
  return <section>
    <div className="sg-heading">
      <h3 style={{ fontSize: 17 }}>Your next skills to build</h3>
      <span className="pill">{gaps.length} {gaps.length === 1 ? "GAP" : "GAPS"}</span>
    </div>
    {gaps.length === 0 ? <p className="helper" style={{ marginTop: 14 }}>No specific skill gaps were identified for this role.</p> : <>
      <p className="sg-caption">Showing {visible.length} of {gaps.length} · Highest urgency first</p>
      <ul className="sg-list" id={listId}>
        {visible.map((gap, i) => {
          const priority = urgencyOrder[gap.urgency.trim().toLowerCase()];
          return <li key={`${gap.esco_id}-${i}`}>
            <Link className="sg-link" href={`/simulate?profile=${encodeURIComponent(profileId)}&skill_id=${encodeURIComponent(gap.esco_id)}`} aria-label={`Practise ${gap.skill}, ${gap.urgency} urgency`}>
              <span className="sg-skill"><span>{gap.skill}</span><small>{gap.type}</small></span>
              <span className="sg-urgency" data-priority={priority !== undefined && priority <= 1 ? "high" : "standard"} title={`${gap.urgency} urgency`}>{gap.urgency}</span>
              <Icon name="practice" size={14} />
            </Link>
          </li>;
        })}
      </ul>
      {gaps.length > GAP_PREVIEW_COUNT && <button type="button" className="sg-toggle" aria-expanded={expanded} aria-controls={listId} onClick={() => setExpanded((value) => !value)}>
        {expanded ? "Show fewer" : `Show all ${gaps.length} gaps`}
        <span className={expanded ? "sg-chevron-expanded" : "sg-chevron"}><Icon name="chevron" size={14} /></span>
      </button>}
    </>}
  </section>;
}

export default function MatchesPage() {
  const { id } = useParams<{ id: string }>();
  const { setActive } = useActiveProfile();
  const [scenario, setScenario] = useState<MatchScenario>("moderate");
  const [count, setCount] = useState(5);
  const resource = useResource(useCallback(() => getMatches(id, scenario, count), [id, scenario, count]));
  useEffect(() => { setActive(id); }, [id, setActive]);
  return <>
    <PageIntro eyebrow="02 / FIND YOUR DIRECTION" title="Possibilities, with perspective." description="Explore how your skills connect to roles—and how that fit changes as AI reshapes the workplace."><Link className="btn secondary" href={`/profile/${id}`}>Your profile<Icon name="profile" size={15} /></Link></PageIntro>
    <div className="controls"><div className="field"><label id="scenario-label">AI-disruption scenario</label><div className="tabs" role="group" aria-labelledby="scenario-label"><button className={scenario === "moderate" ? "selected" : ""} aria-pressed={scenario === "moderate"} onClick={() => setScenario("moderate")}>Moderate adoption</button><button className={scenario === "fast" ? "selected" : ""} aria-pressed={scenario === "fast"} onClick={() => setScenario("fast")}>Fast adoption</button></div></div><div className="field" style={{ flex: "0 0 auto" }}><label htmlFor="result-count">Roles to explore</label><select id="result-count" value={count} onChange={(e) => setCount(Number(e.target.value))}>{Array.from({ length: 20 }, (_, i) => <option value={i + 1} key={i}>{i + 1} {i === 0 ? "role" : "roles"}</option>)}</select></div></div>
    <p className="helper" style={{ margin: "-8px 0 24px" }}>{scenario === "moderate" ? "A measured pace of AI adoption, with more time for skills and roles to evolve." : "An accelerated shift, where AI adoption transforms workplace tasks more quickly."} These scenarios help you plan; they are not forecasts or guarantees.</p>
    {resource.loading ? <Loading label={`Exploring ${scenario} adoption signals…`} /> : resource.error ? <ErrorState message={resource.error} retry={resource.retry} /> : resource.data?.results.length === 0 ? <Empty title="The role map is still taking shape." description="Our role dataset is still being seeded, so there may be no matches to show yet. This is about the available data—not your potential. Your skills profile is ready when the roles arrive."><button className="btn" onClick={resource.retry}>Check for roles again<Icon size={15} /></button><Link className="btn secondary" href={`/simulate?profile=${encodeURIComponent(id)}`}>Practise in the meantime<Icon name="practice" size={15} /></Link></Empty> : <div className="stagger">{resource.data?.results.map((match, index) => <article className="panel match-card" key={`${match.esco_id}-${index}`}><div className="match-head"><div><div className="eyebrow" style={{ color: "var(--muted)" }}>DIRECTION {String(index + 1).padStart(2, "0")}</div><h2>{match.target_role}</h2></div><div style={{ textAlign: "right" }}><div className="score">{(match.match_score * 100).toFixed(1)}<small>%</small></div><span className="helper">match score</span></div></div>
      <div className="breakdown">{([{ label: "RRF score", value: match.score_breakdown.rrf_score }, { label: "Hard-skill coverage", value: match.score_breakdown.hard_skill_coverage }, { label: "Seniority match", value: match.score_breakdown.seniority_match }]).map((score) => <div key={score.label}><div className="meta-row"><span>{score.label}</span><b>{score.value.toFixed(3)}</b></div><Meter value={score.value} /></div>)}</div><p className="helper">Scores range from 0 to 1. RRF combines ranking signals; coverage reflects overlapping hard skills; seniority compares experience.</p>
      {(match.ctci_score !== null || match.compression_type) && <div className="pills" style={{ marginTop: 15 }}>{match.ctci_score !== null && <span className="pill">CTCI SCORE: {match.ctci_score.toFixed(3)}</span>}{match.compression_type && <span className="pill">{match.compression_type}</span>}</div>}
      <div className="divider" /><div className="two-col"><SkillsGapList gaps={match.skills_gap} profileId={id} /><section><h3 style={{ fontSize: 17 }}>The impact beyond the role</h3>{match.sdg_alignment.length === 0 ? <p className="helper" style={{ marginTop: 14 }}>SDG alignment has not been mapped for this role yet.</p> : match.sdg_alignment.map((sdg, i) => <div className="sdg-entry" key={i} style={{ borderColor: sdg.color_hex && /^#[\da-fA-F]{6}$/.test(sdg.color_hex) ? sdg.color_hex : undefined }}><h3>SDG {sdg.sdg_goal} · {sdg.sdg_name}</h3>{sdg.target && <span className="pill">Target {sdg.target}</span>}<p style={{ marginTop: 9 }}>{sdg.impact_reasoning}</p><small>Source: {sdg.source}</small></div>)}</section></div></article>)}</div>}
    <p className="notice">A match score is a starting point for exploration, not a judgement of your abilities. Use the skill gaps to choose a practical next step.</p>
  </>;
}
