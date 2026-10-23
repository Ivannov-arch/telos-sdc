"use client";

import Link from "next/link";
import { Suspense, useCallback, useEffect, useState, type FormEvent } from "react";
import { useParams, useSearchParams } from "next/navigation";
import { listSimulationTasks, submitSimulation, type SimulateResult } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { useActiveProfile } from "@/components/shell";
import { Empty, ErrorState, Icon, Loading, NeedProfile, PageIntro } from "@/components/ui";

function AttemptContent() {
  const { taskId } = useParams<{ taskId: string }>();
  const params = useSearchParams();
  const { activeId, setActive, ready } = useActiveProfile();
  const queryProfile = params.get("profile");
  const profileId = queryProfile || activeId;
  const skillId = params.get("skill_id") || undefined;
  const tasks = useResource(useCallback(() => listSimulationTasks(skillId, 100), [skillId]));
  const [response, setResponse] = useState("");
  const [result, setResult] = useState<SimulateResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  useEffect(() => { if (queryProfile) setActive(queryProfile); }, [queryProfile, setActive]);
  const back = `/simulate${profileId ? `?profile=${encodeURIComponent(profileId)}${skillId ? `&skill_id=${encodeURIComponent(skillId)}` : ""}` : ""}`;
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!profileId || !response.trim() || submitting) return;
    setSubmitting(true); setError(null);
    try { setResult(await submitSimulation(profileId, taskId, response.trim())); }
    catch (err) { setError(err instanceof Error ? err.message : "Your response couldn’t be evaluated. Please try again."); }
    finally { setSubmitting(false); }
  }
  if (!ready && !queryProfile) return <Loading />;
  if (!profileId) return <NeedProfile />;
  if (tasks.loading) return <Loading label="Setting the scene…" />;
  if (tasks.error) return <ErrorState message={tasks.error} retry={tasks.retry} />;
  const task = tasks.data?.tasks.find((item) => item.id === taskId);
  if (!task) return <Empty title="This task isn’t on the board." description="It may have moved or is not available in the current task library. Head back to find another skill to practise." icon="practice"><Link className="btn" href={back}>Back to practice<Icon name="back" size={15} /></Link></Empty>;
  return <><Link className="text-link" href={back} style={{ marginBottom: 24 }}><Icon name="back" size={15} />Back to practice lab</Link><div className="two-col reveal"><div className="stack"><section className="panel"><div className="pills"><span className="pill accent">WORKPLACE SIMULATION</span><span className="pill">{task.difficulty}</span></div><h2 style={{ fontSize: 29, marginTop: 20 }}>{task.skill_name}</h2><div className="eyebrow" style={{ marginTop: 25, marginBottom: 13, color: "var(--muted)" }}>YOUR SCENARIO</div><p style={{ whiteSpace: "pre-wrap", fontSize: 14 }}>{task.scenario_text}</p>{task.onet_task_ref && <p className="helper" style={{ marginTop: 18 }}>O*NET task reference: {task.onet_task_ref}</p>}</section>
    {result ? <section className="panel result" aria-live="polite"><div className="eyebrow" style={{ textAlign: "center" }}>{result.evaluated ? "YOUR FEEDBACK" : "RESPONSE RECORDED"}</div><div className="score-ring"><span>{result.score_percent.toFixed(0)}<span style={{ fontSize: 17 }}>%</span></span><small>rubric score</small></div><h2>{result.evaluated ? "A next step, not a final verdict." : "Your response is in."}</h2>{!result.evaluated && <p className="notice" style={{ margin: "0 0 17px" }}>This response has not been fully evaluated. Treat the displayed score as provisional.</p>}<p style={{ whiteSpace: "pre-wrap", fontSize: 13 }}>{result.improvement_reasoning}</p><div className="divider" /><h3 style={{ fontSize: 16 }}>Ideas to bring into your next attempt</h3>{result.missing_concepts.length ? <ul className="rubric">{result.missing_concepts.map((concept, i) => <li key={i}>{concept}</li>)}</ul> : <p style={{ fontSize: 12, marginTop: 12 }}>No missing concepts were flagged. Keep refining your reasoning and clarity.</p>}<details style={{ marginTop: 22 }}><summary className="helper" style={{ cursor: "pointer" }}>Review your submitted response</summary><p style={{ whiteSpace: "pre-wrap", fontSize: 12, marginTop: 12 }}>{response}</p></details><div className="actions"><button className="btn" onClick={() => { setResult(null); setError(null); }}>Improve & try again<Icon name="practice" size={15} /></button><Link className="btn secondary" href={back}>Back to practice</Link></div></section> : <section className="panel"><form onSubmit={submit}><div className="field" style={{ marginTop: 0 }}><label htmlFor="answer" style={{ fontSize: 18, fontFamily: "var(--font-display)" }}>How would you approach this?</label><p className="helper">Walk us through your reasoning. Use specific examples where they help.</p><textarea id="answer" value={response} onChange={(e) => setResponse(e.target.value)} disabled={submitting} required minLength={1} placeholder="Here’s how I would approach the situation…" style={{ minHeight: 245 }} /><div className="meta-row"><small>No timer. Take the time you need.</small><small>{response.length.toLocaleString()} characters</small></div></div>{error && <ErrorState message={error} />}<div className="actions"><button className="btn" type="submit" disabled={submitting || !response.trim()}>{submitting ? "Reflecting on your response…" : "Submit for feedback"}{!submitting && <Icon size={15} />}</button></div>{submitting && <div role="status" style={{ marginTop: 20 }}><div className="skeleton short" style={{ height: 9 }} /><p className="helper">Checking your response against the rubric. Your work is safe on this page.</p></div>}</form></section>}</div>
    <aside className="stack"><section className="panel" style={{ background: "var(--featured-bg)" }}><Icon name="target" size={25} /><h2 style={{ marginTop: 15 }}>No hidden goalposts.</h2><p style={{ fontSize: 12 }}>Your response will be assessed against these criteria:</p>{task.rubric_criteria.length ? <ol className="number-list">{task.rubric_criteria.map((criterion, i) => <li key={i}>{criterion}</li>)}</ol> : <p className="notice">No rubric criteria have been published for this task.</p>}</section><section className="panel"><h3 style={{ fontSize: 16 }}>Make your thinking visible.</h3><p style={{ fontSize: 12, marginTop: 10 }}>Explain what you’d do, why you’d do it, and what you’d watch out for. A thoughtful approach matters more than a polished answer.</p></section></aside></div></>;
}
export default function AttemptPage() {
  return <><PageIntro eyebrow="03 / THE PRACTICE LAB" title="Try it here. Take it further." description="A low-stakes space to work through a real situation and learn from the feedback." /><Suspense fallback={<Loading />}><AttemptContent /></Suspense></>;
}
