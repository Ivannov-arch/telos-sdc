"use client";

import { Suspense, useState, type FormEvent } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { startGame, type MissionId } from "@/lib/api";
import { MISSIONS } from "@/lib/missions";
import { saveSession } from "@/lib/sessions";
import { ErrorState, Icon, Loading, PageIntro } from "@/components/ui";

const parse = (text: string) => [...new Set(text.split(/[,;\n]/).map((s) => s.trim()).filter(Boolean))];

function SetupForm() {
  const router = useRouter();
  const params = useSearchParams();
  const initial = params.get("mission");
  const [mission, setMission] = useState<MissionId | null>(initial === "A" || initial === "B" || initial === "C" ? initial : null);
  const [skills, setSkills] = useState("");
  const [interests, setInterests] = useState("");
  const [hours, setHours] = useState("5");
  const [error, setError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    const skillList = parse(skills);
    const time = Number(hours);
    if (!mission) { setError("Choose a mission to play."); return; }
    if (!skillList.length) { setError("Add at least one skill so we can compare what you say with what you do."); return; }
    if (!Number.isInteger(time) || time < 1 || time > 40) { setError("Learning time must be a whole number of hours between 1 and 40."); return; }
    setStarting(true);
    try {
      const res = await startGame({ skills: skillList, interests: parse(interests), learning_time: time }, mission);
      saveSession({ id: res.session_id, mission, startedAt: new Date().toISOString(), skills: skillList });
      router.push(`/play/${encodeURIComponent(res.session_id)}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "We couldn’t start the simulation. Please try again.");
      setStarting(false);
    }
  }

  return <form onSubmit={submit} className="reveal"><fieldset disabled={starting} style={{ border: 0, padding: 0, margin: 0, minWidth: 0 }}>
    <div className="eyebrow" style={{ color: "var(--muted)", marginBottom: 14 }}>STEP 1 OF 2 · CHOOSE YOUR CRISIS</div>
    <div className="mission-grid stagger" role="radiogroup" aria-label="Mission">
      {MISSIONS.map((m) => <button key={m.id} type="button" role="radio" aria-checked={mission === m.id} className={`mission-card ${mission === m.id ? "selected" : ""}`} onClick={() => setMission(m.id)}>
        <div className="card-top"><span className="step-num">{m.code}</span><span className="pill accent">{m.sdg}</span></div>
        <h3>{m.title}</h3><strong>{m.crisis}</strong><p>{m.pitch}</p>
        <span className="mission-pick">{mission === m.id ? <><Icon name="check" size={14} /> Selected</> : "Select this mission"}</span>
      </button>)}
    </div>
    <div className="two-col" style={{ marginTop: 34 }}>
      <section className="panel">
        <div className="eyebrow" style={{ color: "var(--muted)", marginBottom: 12 }}>STEP 2 OF 2 · QUICK SKILL PROFILE</div>
        <h2>Tell us what you think you’re good at.</h2>
        <p className="helper">Under two minutes. No CV and no login. We’ll compare this with how you actually decide.</p>
        <div className="field"><label htmlFor="skills">Your skills</label><textarea id="skills" value={skills} onChange={(e) => setSkills(e.target.value)} placeholder="Python, data analysis, communication, project management" style={{ minHeight: 96 }} /><small>Separate skills with commas or put each on a new line.</small></div>
        <div className="field"><label htmlFor="interests">Career interests <span style={{ fontWeight: 400, color: "var(--muted)" }}>(optional)</span></label><input id="interests" value={interests} onChange={(e) => setInterests(e.target.value)} placeholder="Logistics, climate, finance" /></div>
        <div className="field"><label htmlFor="hours">Hours per week you could spend learning</label><input id="hours" type="number" inputMode="numeric" min={1} max={40} step={1} value={hours} onChange={(e) => setHours(e.target.value)} style={{ maxWidth: 140 }} /></div>
        {error && <ErrorState message={error} />}
        <div className="actions"><button type="submit" className="btn lime">{starting ? "Opening the control room…" : "Enter the control room"}{!starting && <Icon size={16} />}</button></div>
      </section>
      <aside className="stack"><section className="panel" style={{ background: "var(--featured-bg)" }}>
        <div className="eyebrow" style={{ marginBottom: 15 }}>WHAT TO EXPECT</div><h2>Four rounds. About three minutes.</h2>
        <ol className="number-list"><li>Set your own strategy. The AI advisor is offline.</li><li>The advisor comes online and makes a recommendation.</li><li>Conditions change without warning.</li><li>Commit to a final decision.</li></ol>
      </section><section className="panel"><Icon name="spark" size={22} /><h3 style={{ marginTop: 13, fontSize: 16 }}>There are no wrong answers.</h3><p style={{ fontSize: 12, marginTop: 10 }}>Answer the way you really would. The more naturally you play, the more useful your results will be.</p></section></aside>
    </div>
  </fieldset></form>;
}

export default function PlayPage() {
  return <>
    <PageIntro eyebrow="THE CRISIS SIMULATION" title="Play your career future." description="Step into a live global crisis. How you decide alongside AI shows what no CV can." />
    <Suspense fallback={<Loading label="Preparing the missions…" />}><SetupForm /></Suspense>
  </>;
}
