import { useState } from "react";
import { ArrowRight, ArrowUpRight, Bookmark, Check, ChevronDown, Compass, FlaskConical, Info, Layers, MoveUpRight, Plus, Sparkles, X } from "lucide-react";
import "./CareerFieldnotes.css";

const roles = [
  { name: "Learning experience designer", group: "Education & human development", score: 86, skills: ["Communication", "Research", "Problem solving"], gap: "Instructional design", impact: "04 · Quality education", resilience: "Human-led", description: "Turn complex ideas into learning that sticks. Design experiences that help people build skills and confidence.", prompt: "A team is introducing a new digital tool. Some colleagues are confident; others are overwhelmed. Outline a 20-minute learning experience that helps both groups get started." },
  { name: "Community programme coordinator", group: "Social impact & public services", score: 79, skills: ["Communication", "Planning", "Collaboration"], gap: "Impact measurement", impact: "11 · Sustainable cities", resilience: "Relationship-led", description: "Bring people, resources, and local ideas together. Build programmes that respond to what a community actually needs.", prompt: "A local library wants to run a digital-skills workshop for older residents. Outline how you would understand their needs, invite participants, and measure whether it helped." },
  { name: "User research specialist", group: "Technology & human insight", score: 74, skills: ["Research", "Communication", "Critical thinking"], gap: "Interview methods", impact: "09 · Industry & innovation", resilience: "Judgment-led", description: "Make people’s needs visible. Turn conversations and observations into evidence that helps teams build better things.", prompt: "People keep abandoning an online course after the first lesson. Write three interview questions that could uncover why, without leading participants toward a particular answer." },
];

export function CareerFieldnotes() {
  const [step, setStep] = useState(1);
  const [selected, setSelected] = useState(0);
  const [intent, setIntent] = useState("Build on my strengths");
  const [fast, setFast] = useState(false);
  const [saved, setSaved] = useState<number[]>([]);
  const [savedView, setSavedView] = useState(false);
  const [modal, setModal] = useState<"profile" | "practice" | null>(null);
  const [skills, setSkills] = useState("Communication, Research, Problem solving, Planning");
  const [draftSkills, setDraftSkills] = useState(skills);
  const [answer, setAnswer] = useState("");
  const [reviewed, setReviewed] = useState(false);
  const [profileName, setProfileName] = useState("Alex Morgan");
  const [draftName, setDraftName] = useState(profileName);
  const role = roles[selected];
  const editProfile = () => { setDraftSkills(skills); setDraftName(profileName); setModal("profile"); };
  const startPractice = () => { setAnswer(""); setReviewed(false); setModal("practice"); };
  const toggleSaved = () => setSaved((old) => old.includes(selected) ? old.filter((v) => v !== selected) : [...old, selected]);
  const visibleRoles = roles.map((item, index) => ({ ...item, index })).filter((item) => !savedView || saved.includes(item.index));
  const initials = profileName.split(" ").map((s) => s[0]).join("").slice(0, 2);
  return <div className="fieldnotes">
    <header className="fn-header">
      <div className="fn-brand"><span className="fn-mark"><Sparkles size={19} strokeWidth={1.4} /></span>Aiversecity<span className="fn-mono" style={{ marginLeft: 17, color: "#9b8b80", borderLeft: "1px solid #d6cbbf", paddingLeft: 20, fontSize: 9 }}>FIELDNOTES</span></div>
      <nav className="fn-nav" aria-label="Workspace"><button className={!savedView ? "active" : ""} onClick={() => { setSavedView(false); setStep(1); }}>My next move</button><button className={savedView ? "active" : ""} onClick={() => { setSavedView(true); setStep(1); }}>Saved directions <span style={{ color: "#9c8479", marginLeft: 5 }}>{saved.length.toString().padStart(2, "0")}</span></button><button onClick={() => { setStep(2); setSavedView(false); }}>Practice lab <ArrowUpRight size={12} style={{ display: "inline", marginLeft: 4 }} /></button></nav>
      <button className="fn-profile" onClick={editProfile}><span className="fn-mono" style={{ fontSize: 9 }}>EXAMPLE PROFILE</span><span className="fn-avatar">{initials}</span><ChevronDown size={13} /></button>
    </header>
    <section className="fn-intro">
      <div><div className="fn-mono" style={{ color: "#967b70" }}>A WORKING PLAN FOR A CHANGING WORLD</div><h1>A next move.<br /><em>Not a leap of faith.</em></h1></div>
      <div className="fn-intro-note"><b>You don’t need your whole future figured out.</b><br />Start with what you know. Find a direction worth exploring. Try it on.</div>
    </section>
    <div className="fn-progress" aria-label="Career journey">
      {["Your starting point", "Possible directions", "A small experiment"].map((label, i) => <button key={label} className={step === i ? "active" : ""} onClick={() => { setStep(i); setSavedView(false); }}><span className="fn-step-number">{i === 0 && step > 0 ? <Check size={13} /> : `0${i + 1}`}</span><span className="fn-step-text">{label}<small>{["Skills, not just job titles", "Find the overlap", "Learn by doing"][i]}</small></span>{step === i && <MoveUpRight size={16} style={{ marginLeft: "auto" }} />}</button>)}
    </div>
    {step === 1 && <div className="fn-workspace">
      <section className="fn-shortlist">
        <div className="fn-section-heading"><h2>{savedView ? "Directions you’re keeping." : "Where could you go?"}</h2><span className="fn-mono" style={{ fontSize: 9, color: "#9b877a" }}>{visibleRoles.length} DIRECTIONS</span></div>
        {!savedView && <div className="fn-filter" aria-label="Career intention">{["Build on my strengths", "A change of direction"].map((value) => <button key={value} className={intent === value ? "active" : ""} onClick={() => { setIntent(value); setSelected(value === "A change of direction" ? 1 : 0); }}>{intent === value && <Check size={10} style={{ display: "inline", marginRight: 5 }} />}{value}</button>)}</div>}
        {visibleRoles.length ? visibleRoles.map((item) => <button className={`fn-role ${selected === item.index ? "selected" : ""}`} key={item.name} onClick={() => setSelected(item.index)} aria-pressed={selected === item.index}>
          <span className="fn-role-index">0{item.index + 1}</span><div><div className="fn-role-title">{item.name}</div><div className="fn-role-subtitle">{item.group}</div></div><div className="fn-fit"><strong>{item.score - (fast ? 3 : 0)}<span style={{ fontSize: 16 }}>%</span></strong><small>skills overlap</small></div><ArrowUpRight size={17} style={{ marginLeft: 5, color: selected === item.index ? "#743d48" : "#b9aaa0" }} />
        </button>) : <div className="fn-empty"><Bookmark size={25} style={{ margin: "auto" }} /><h2>Keep a possibility.</h2><p>Save a direction to come back to it.</p><button className="fn-primary" onClick={() => setSavedView(false)}>Explore directions <ArrowRight size={15} /></button></div>}
        <div className="fn-list-note"><Info size={13} style={{ flexShrink: 0, marginTop: 2 }} /><span>Possibilities, not prescriptions. Illustrative matches based on your example profile and the ESCO skills framework.</span></div>
      </section>
      <section className="fn-dossier" aria-label="Selected career direction">
        <div className="fn-dossier-top"><span className="fn-mono" style={{ color: "#96746b", fontSize: 9 }}>DIRECTION 0{selected + 1} / A CLOSER LOOK</span><button className="fn-bookmark" aria-label={saved.includes(selected) ? "Remove saved direction" : "Save direction"} onClick={toggleSaved}><Bookmark size={15} fill={saved.includes(selected) ? "#743d48" : "none"} /></button></div>
        <h2>{role.name}</h2><p className="fn-dossier-description">{role.description}</p>
        <div className="fn-dossier-grid"><div><div className="fn-mono" style={{ fontSize: 8, color: "#937a70" }}>IN AN AI-SHAPED WORLD</div><p style={{ display: "flex", alignItems: "center", gap: 6 }}><span style={{ width: 6, height: 6, borderRadius: "50%", background: "#80917a" }} />{fast ? "More adaptation needed" : role.resilience}</p></div><div><div className="fn-mono" style={{ fontSize: 8, color: "#937a70" }}>WORK THAT CONTRIBUTES</div><p>{role.impact} <ArrowUpRight size={11} style={{ display: "inline" }} /></p></div></div>
        <div className="fn-mono" style={{ fontSize: 8, color: "#937a70" }}>YOU ALREADY BRING</div><div>{role.skills.map((skill) => <span key={skill} className="fn-tag"><Check size={10} style={{ display: "inline", marginRight: 5 }} />{skill}</span>)}</div>
        <div className="fn-next"><div><div className="fn-mono" style={{ fontSize: 8, color: "#937a70" }}>YOUR NEXT SKILL</div><p style={{ fontSize: 12, marginTop: 6 }}>{role.gap}</p></div><button className="fn-primary" onClick={startPractice}>Try this direction <ArrowRight size={15} /></button></div>
      </section>
    </div>}
    {step === 0 && <div className="fn-practice"><section className="fn-practice-copy"><div className="fn-mono">01 / THE EXPERIENCE YOU CARRY</div><h2>You’re not starting<br />from nothing.</h2><p>A job title is only part of the story. Your skills travel with you—even when your direction changes.</p><div style={{ marginBottom: 24 }}>{skills.split(",").filter(Boolean).map((skill) => <span key={skill} className="fn-tag">{skill.trim()}</span>)}</div><button className="fn-primary" onClick={editProfile}>Edit my starting point <Plus size={15} /></button><button className="fn-text-button" style={{ marginLeft: 20 }} onClick={() => setStep(1)}>Find my directions <ArrowRight size={12} style={{ display: "inline" }} /></button></section><div className="fn-practice-art"><div className="fn-art-circle"><div className="fn-art-card"><Compass size={30} strokeWidth={1} /><div className="fn-mono" style={{ marginTop: 25 }}>YOUR SKILLS<br />GO WITH YOU.</div><span /><span /><span /></div></div></div></div>}
    {step === 2 && <div className="fn-practice"><section className="fn-practice-copy"><div className="fn-mono">03 / SMALL STEPS, REAL INSIGHT</div><h2>Try the work.<br /><em>Before the big move.</em></h2><p>Step into the shoes of a {role.name.toLowerCase()}. No perfect answers. Just a short workplace scenario to help you discover what feels right.</p><div className="fn-mono" style={{ marginBottom: 25, color: "#8c796e" }}>~ 8 MINUTES · {role.gap.toUpperCase()}</div><button className="fn-primary" onClick={startPractice}>Start the experiment <ArrowRight size={15} /></button></section><div className="fn-practice-art"><div className="fn-art-circle"><div className="fn-art-card"><FlaskConical size={30} strokeWidth={1} /><div className="fn-mono" style={{ marginTop: 25 }}>LESS GUESSING.<br />MORE DOING.</div><span /><span /><span /></div></div></div></div>}
    <div className="fn-context">
      <section className="fn-passport"><div className="fn-stamp"><Compass size={27} strokeWidth={1} /></div><div><div className="fn-mono" style={{ fontSize: 9 }}>YOUR STARTING POINT</div><p>{skills.split(",").slice(0, 3).join(" · ")}<br /><span style={{ fontSize: 10 }}>Based on {profileName.split(" ")[0]}’s example skills profile</span></p></div><button className="fn-text-button" onClick={editProfile}>Edit skills <ArrowUpRight size={11} style={{ display: "inline" }} /></button></section>
      <section className="fn-scenario"><div className="fn-switch"><span className="fn-mono" style={{ fontSize: 9 }}>WHAT IF AI MOVES {fast ? "FASTER" : "FASTER"}?</span><button role="switch" aria-checked={fast} aria-label="Fast AI adoption scenario" onClick={() => setFast(!fast)}><span style={{ transform: fast ? "translateX(15px)" : "translateX(0)" }} /></button></div><p>{fast ? "Fast adoption: a little more change, a little more learning. Compare how the signals shift." : "Explore a faster-adoption scenario. Your possibilities aren’t a fixed prediction."}</p></section>
    </div>
    <footer className="fn-footer"><span>AIVERSECITY / HUMAN POTENTIAL, IN PROGRESS.</span><span style={{ display: "flex", alignItems: "center", gap: 7 }}><Layers size={12} /> ESCO SKILLS · UN SUSTAINABLE DEVELOPMENT GOALS</span><span>ONE DIRECTION AT A TIME. ↗</span></footer>
    {modal && <div className="fn-overlay" onClick={() => setModal(null)}><section className="fn-dialog" role="dialog" aria-modal="true" aria-label={modal === "profile" ? "Edit your starting point" : "Career practice experiment"} onClick={(event) => event.stopPropagation()}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}><span className="fn-mono">{modal === "profile" ? "YOUR SKILLS PASSPORT" : "THE PRACTICE LAB"}</span><button className="fn-close" onClick={() => setModal(null)} aria-label="Close dialog"><X size={19} /></button></div>
      {modal === "profile" ? <form onSubmit={(event) => { event.preventDefault(); setSkills(draftSkills); setProfileName(draftName); setModal(null); }}><h2>A starting point. Not a box.</h2><p>Try this workspace with your own skills. This is an interactive preview; nothing is uploaded or sent to a server.</p><label>Your name<input autoFocus required value={draftName} onChange={(event) => setDraftName(event.target.value)} /></label><label>Skills you bring, separated by commas<textarea required value={draftSkills} onChange={(event) => setDraftSkills(event.target.value)} /></label><button className="fn-primary" type="submit">Keep these skills <Check size={15} /></button></form> : <><h2>Think like a {role.name.toLowerCase()}.</h2><p>{role.prompt}</p><label htmlFor="fn-response">Your first approach</label><textarea id="fn-response" autoFocus value={answer} onChange={(event) => { setAnswer(event.target.value); setReviewed(false); }} placeholder="Start with the people. What would you do first?" />{reviewed && <div className="fn-feedback"><strong>Your reflection checkpoint</strong><br />You’ve taken the first step. Re-read your approach: did you identify who needs help, choose one practical action, and explain how you’d know it worked?<br /><small>This is a self-guided reflection, not an AI assessment.</small></div>}<button className="fn-primary" disabled={answer.trim().length < 20} style={{ opacity: answer.trim().length < 20 ? .5 : 1 }} onClick={() => setReviewed(true)}>{reviewed ? "Review my reflection" : "Reflect on my approach"} <ArrowRight size={15} /></button><p style={{ marginTop: 12, fontSize: 10 }}>Write at least 20 characters. There’s no single right answer.</p></>}
    </section></div>}
  </div>;
}
