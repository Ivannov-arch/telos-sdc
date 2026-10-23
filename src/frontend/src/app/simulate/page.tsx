"use client";

import Link from "next/link";
import { Suspense, useCallback, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { getSimulationHistory, listSimulationTasks } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { useActiveProfile } from "@/components/shell";
import { dateLabel, Empty, ErrorState, Icon, Loading, NeedProfile, PageIntro } from "@/components/ui";

function PracticeContent() {
  const params = useSearchParams();
  const { activeId, setActive, ready } = useActiveProfile();
  const queryProfile = params.get("profile");
  const profileId = queryProfile || activeId;
  const skillId = params.get("skill_id") || undefined;
  useEffect(() => { if (queryProfile) setActive(queryProfile); }, [queryProfile, setActive]);
  const tasks = useResource(useCallback(() => listSimulationTasks(skillId), [skillId]));
  const history = useResource(useCallback(() => profileId ? getSimulationHistory(profileId) : Promise.resolve({ history: [], total_attempts: 0 }), [profileId]));
  if (!ready && !queryProfile) return <Loading />;
  if (!profileId) return <NeedProfile />;
  return <>
    {skillId && <div className="panel" style={{ marginBottom: 22, padding: 18 }}><div className="meta-row"><span className="pills"><span className="pill accent">FOCUSED PRACTICE</span><span className="helper">Showing tasks for your selected skill gap.</span></span><Link className="text-link" href={`/simulate?profile=${encodeURIComponent(profileId)}`}>Show all tasks<Icon size={14} /></Link></div></div>}
    <div className="two-col"><section><div className="section-header" style={{ marginTop: 0 }}><div><h2>Small tasks. Real progress.</h2><p>Read the scenario, use the rubric, and give it your best thinking.</p></div>{tasks.data && <span className="pill">{tasks.data.count} AVAILABLE</span>}</div>
      {tasks.loading ? <Loading label="Preparing your practice space…" /> : tasks.error ? <ErrorState message={tasks.error} retry={tasks.retry} /> : tasks.data?.tasks.length === 0 ? <Empty title={skillId ? "This skill’s practice is on its way." : "The lab is getting ready."} description={skillId ? "There aren’t any simulations for this skill yet. Explore the other available tasks while we expand the library." : "No simulation tasks have been added yet. Your profile is ready; check back as the task library grows."} icon="practice">{skillId ? <Link className="btn" href={`/simulate?profile=${encodeURIComponent(profileId)}`}>Explore all tasks<Icon size={15} /></Link> : <button className="btn secondary" onClick={tasks.retry}>Check again</button>}</Empty> : <div className="stack stagger">{tasks.data?.tasks.map((task) => <article className="panel task-card" key={task.id}><div className="meta-row"><span className="icon-box"><Icon name="practice" /></span><span className="pill">{task.difficulty}</span></div><h2>{task.skill_name}</h2><p style={{ whiteSpace: "pre-wrap" }}>{task.scenario_text}</p><details style={{ marginTop: 17 }}><summary className="helper" style={{ cursor: "pointer" }}>What you’ll be assessed on · {task.rubric_criteria.length} criteria</summary><ul className="rubric">{task.rubric_criteria.map((criterion, i) => <li key={i}>{criterion}</li>)}</ul></details><div className="actions"><Link className="btn" href={`/simulate/${encodeURIComponent(task.id)}?profile=${encodeURIComponent(profileId)}${skillId ? `&skill_id=${encodeURIComponent(skillId)}` : ""}`}>Try this simulation<Icon size={15} /></Link></div></article>)}</div>}
    </section><aside><section className="panel"><div className="meta-row"><h2>Your practice journal</h2><Icon name="clock" size={19} /></div><p className="helper">Progress is a collection of attempts, not a single score.</p>{history.loading ? <div style={{ marginTop: 20 }}><Loading label="Opening your journal…" /></div> : history.error ? <ErrorState message={history.error} retry={history.retry} /> : !history.data?.history.length ? <div style={{ padding: "30px 0 12px", textAlign: "center" }}><Icon name="practice" size={28} /><h3 style={{ fontSize: 17, margin: "15px 0 9px" }}>Your first attempt is a beginning.</h3><p style={{ fontSize: 12 }}>Complete a simulation and your feedback will appear here. No perfect answers required.</p></div> : <><div className="pills" style={{ margin: "17px 0" }}><span className="pill accent">{history.data.total_attempts} ATTEMPTS</span></div>{history.data.history.map((attempt) => <article className="history-item" key={attempt.id}><div className="meta-row"><span>{dateLabel(attempt.created_at)}</span><b style={{ color: "var(--petrol)", fontSize: 21 }}>{attempt.score_percent.toFixed(0)}<small style={{ fontSize: 11 }}>%</small></b></div><p>{attempt.improvement_reasoning}</p>{attempt.missing_concepts.length > 0 && <div className="pills">{attempt.missing_concepts.map((concept, i) => <span className="pill" key={i}>{concept}</span>)}</div>}<details><summary>Review your response</summary>{attempt.simulation_tasks && <p>{attempt.simulation_tasks.scenario_text}</p>}<p style={{ whiteSpace: "pre-wrap" }}>{attempt.user_response}</p></details><Link className="text-link" style={{ marginTop: 13 }} href={`/simulate/${encodeURIComponent(attempt.task_id)}?profile=${encodeURIComponent(profileId)}`}>Practise again<Icon size={13} /></Link></article>)}</>}</section><p className="notice">Feedback is a learning aid, not a professional certification. Take what’s useful, reflect, and try again.</p></aside></div>
  </>;
}
export default function PracticePage() {
  return <><PageIntro eyebrow="03 / LEARN BY DOING" title="A little practice. A stronger next step." description="Work through real-world scenarios and get constructive, rubric-based feedback. This is a space to grow." /><Suspense fallback={<Loading />}><PracticeContent /></Suspense></>;
}
