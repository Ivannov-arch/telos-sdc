import { useState } from "react";
import "./dispatch-desk.css";

type Mission = {
  id: string;
  title: string;
  headline: string;
  sdg: string;
  place: string;
  summary: string;
  pressure: string;
  figure: string;
  roles: string[];
  skills: string[];
  tone: string;
};

const missions: Mission[] = [
  {
    id: "A",
    title: "Supply under pressure",
    headline: "Food routes are breaking across Southeast Asia.",
    sdg: "SDG 02 · ZERO HUNGER",
    place: "SOUTHEAST ASIA",
    summary: "A flood has cut the region’s main supply corridor. Four routes remain, but the relief budget only covers two.",
    pressure: "4 routes · 2 can be funded",
    figure: "2.4m",
    roles: ["Humanitarian logistics coordinator", "Food systems analyst", "Emergency programme officer"],
    skills: ["Resource allocation", "Systems thinking", "Decisive leadership"],
    tone: "mission-amber",
  },
  {
    id: "B",
    title: "The credit algorithm",
    headline: "A lending model is locking people out.",
    sdg: "SDG 10 · REDUCED INEQUALITIES",
    place: "REGIONAL REVIEW",
    summary: "A regulator has found a pattern of unfair loan denials. You have one day to decide what should happen to the model.",
    pressure: "18% disparity · review in 24h",
    figure: "18%",
    roles: ["Responsible AI policy specialist", "Algorithm auditor", "Digital inclusion lead"],
    skills: ["Ethical judgement", "Evidence review", "Stakeholder negotiation"],
    tone: "mission-rose",
  },
  {
    id: "C",
    title: "Grid failure",
    headline: "A clean-energy grid has gone dark.",
    sdg: "SDG 07 · CLEAN ENERGY",
    place: "COASTAL POWER GRID",
    summary: "Peak demand has overwhelmed a regional grid. Hospitals and homes need power while engineers locate the fault.",
    pressure: "2.3m homes · peak demand",
    figure: "2.3m",
    roles: ["Energy resilience planner", "Grid operations analyst", "Climate adaptation officer"],
    skills: ["Crisis coordination", "Risk analysis", "Adaptive planning"],
    tone: "mission-sage",
  },
];

function Mark({ children }: { children: React.ReactNode }) {
  return <span className="dd-mark" aria-hidden="true">{children}</span>;
}

function Arrow({ diagonal = false }: { diagonal?: boolean }) {
  return <svg aria-hidden="true" viewBox="0 0 20 20" fill="none" className={diagonal ? "dd-arrow diagonal" : "dd-arrow"}>
    {diagonal ? <path d="M5 15 15 5M6 5h9v9" /> : <path d="M3.5 10h12m-5-5 5 5-5 5" />}
  </svg>;
}

function WorldSignal({ mission }: { mission: Mission }) {
  return <div className={`dd-visual ${mission.tone}`}>
    <div className="dd-map-caption"><span>FIELD SIGNAL / 0{mission.id}</span><span>LIVE SCENARIO</span></div>
    <svg viewBox="0 0 520 300" className="dd-map" role="img" aria-label={`Illustrative impact map for ${mission.place.toLowerCase()}`}>
      <defs>
        <pattern id="dispatch-grid" width="24" height="24" patternUnits="userSpaceOnUse">
          <path d="M24 0H0V24" fill="none" stroke="currentColor" strokeWidth=".55" opacity=".28" />
        </pattern>
        <radialGradient id="dispatch-halo"><stop stopColor="currentColor" stopOpacity=".22" /><stop offset="1" stopColor="currentColor" stopOpacity="0" /></radialGradient>
      </defs>
      <rect width="520" height="300" fill="url(#dispatch-grid)" />
      <ellipse cx="280" cy="152" rx="205" ry="91" fill="url(#dispatch-halo)" />
      <path className="dd-contour" d="M38 182c46-41 93-44 137-25 38 17 66 5 101-17 45-28 76-16 115 8 28 18 52 17 92-9M62 225c39-34 78-36 112-20 40 18 71 14 109-8 44-26 73-15 105 5 37 23 62 17 101-11M100 115c38 14 71 4 104-17 33-22 76-28 110-6 24 16 49 18 79 4" />
      <path className="dd-route dd-route-a" d="M109 205C164 170 197 96 271 92s112 57 155 40" />
      <path className="dd-route dd-route-b" d="M109 205c66 10 105 31 166 15 64-17 92-66 151-88" />
      <path className="dd-route dd-route-c" d="M155 93c43 28 66 77 120 127 32 30 71 37 116 32" />
      <circle className="dd-hotspot halo" cx="272" cy="92" r="51" />
      <circle className="dd-hotspot" cx="272" cy="92" r="5" />
      <circle className="dd-node" cx="109" cy="205" r="5" />
      <circle className="dd-node" cx="155" cy="93" r="4" />
      <circle className="dd-node" cx="426" cy="132" r="4" />
      <circle className="dd-node" cx="426" cy="252" r="4" />
      <text x="283" y="78" className="dd-map-label">{mission.place}</text>
      <text x="70" y="236" className="dd-map-small">RESPONSE HUB</text>
      <text x="361" y="274" className="dd-map-small">IMPACT ZONE</text>
    </svg>
    <div className="dd-map-footer"><span><i /> RESPONSE HUB</span><span><i className="dash" /> POSSIBLE ROUTE</span><span>ILLUSTRATIVE MAP</span></div>
    <div className="dd-impact"><span>AT STAKE</span><strong>{mission.figure}</strong><small>people affected</small></div>
  </div>;
}

export default function DispatchDesk() {
  const [activeId, setActiveId] = useState("A");
  const [view, setView] = useState<"dispatch" | "pathways">("dispatch");
  const [briefingOpen, setBriefingOpen] = useState(false);
  const [sessionReady, setSessionReady] = useState(false);
  const mission = missions.find((item) => item.id === activeId) ?? missions[0];

  return <main className="dispatch-desk">
    <header className="dd-topbar">
      <a href="#desk" className="dd-brand" onClick={(event) => { event.preventDefault(); setView("dispatch"); }}>
        <span className="dd-brand-mark"><span /></span><span>Aiversecity<small>HUMAN FUTURES LAB</small></span>
      </a>
      <nav className="dd-nav" aria-label="Workspace">
        <button className={view === "dispatch" ? "active" : ""} onClick={() => setView("dispatch")}>Mission desk</button>
        <button className={view === "pathways" ? "active" : ""} onClick={() => setView("pathways")}>Career pathways</button>
      </nav>
      <div className="dd-user"><span className="dd-user-mark">AV</span><span>Guest explorer</span><span className="dd-online"><i /> OPEN ACCESS</span></div>
    </header>

    <section className="dd-heading" id="desk">
      <div className="dd-heading-label"><span className="dd-overline">A THREE-MINUTE DECISION LAB</span><span className="dd-heading-rule" /></div>
      <div className="dd-heading-row">
        <div>
          <h1>{view === "dispatch" ? <>Choose the pressure<br /><em>you want to meet.</em></> : <>Your choices point<br /><em>toward real work.</em></>}</h1>
          <p>{view === "dispatch" ? "Pick a live global challenge. Your decisions reveal strengths no CV can show." : "The simulation is a skills sensor. Explore the roles and capabilities your decisions can uncover."}</p>
        </div>
        <div className="dd-progress"><span>01</span><i /><span>02</span><i /><span>03</span><small>CHOOSE · DECIDE · DISCOVER</small></div>
      </div>
    </section>

    {view === "dispatch" ? <section className="dd-workspace">
      <aside className="dd-mission-list" aria-label="Choose a mission">
        <div className="dd-list-head"><span className="dd-overline">SELECT A SCENARIO</span><span>3 MISSIONS</span></div>
        {missions.map((item, index) => <button className={`dd-mission-option ${activeId === item.id ? "selected" : ""}`} key={item.id} onClick={() => { setActiveId(item.id); setSessionReady(false); }}>
          <span className="dd-option-index">0{index + 1}</span>
          <span className="dd-option-copy"><strong>{item.title}</strong><small>{item.sdg}</small></span>
          <span className="dd-option-arrow"><Arrow /></span>
        </button>)}
        <div className="dd-note"><Mark>↗</Mark><p><b>No right answer.</b><br />We’re interested in how you think, not whether you guess a key.</p></div>
        <div className="dd-framework"><span>BUILT ON</span><div><b>ESCO</b><i /> <b>UN SDGs</b><i /> <b>AI futures</b></div></div>
      </aside>

      <article className="dd-briefing">
        <div className="dd-briefing-top"><span className="dd-overline">{mission.sdg}</span><span className="dd-case-id">CASE 0{mission.id} / FIELD BRIEF</span></div>
        <div className="dd-briefing-grid">
          <div className="dd-story">
            <div className="dd-location"><span className="dd-location-dot" />{mission.place}</div>
            <h2>{mission.headline}</h2>
            <p>{mission.summary}</p>
            <div className="dd-pressure"><Mark>!</Mark><span><small>THE CONSTRAINT</small><b>{mission.pressure}</b></span></div>
            <button className="dd-launch" onClick={() => { setBriefingOpen(true); setSessionReady(false); }}>
              Enter this scenario <Arrow /><span>≈ 3 MIN</span>
            </button>
            <div className="dd-assurance"><span>01</span> Four decisions <i /> AI advisor <i /> A surprise twist</div>
          </div>
          <WorldSignal mission={mission} />
        </div>
        <div className="dd-evidence">
          <div className="dd-evidence-label"><span className="dd-overline">WHAT YOUR DECISIONS CAN REVEAL</span><small>Signals, not labels.</small></div>
          <div className="dd-signal"><span>01</span><b>How you use evidence</b><i>01</i></div>
          <div className="dd-signal"><span>02</span><b>When you trust AI</b><i>02</i></div>
          <div className="dd-signal"><span>03</span><b>How you adapt</b><i>03</i></div>
          <button className="dd-next" aria-label="Next mission" onClick={() => setActiveId(missions[(missions.findIndex((item) => item.id === activeId) + 1) % missions.length].id)}><Arrow /></button>
        </div>
      </article>
    </section> : <section className="dd-pathways">
      <div className="dd-path-intro"><span className="dd-overline">CAREER PATHWAYS / START WITH CURIOSITY</span><h2>Take your instincts<br /><em>somewhere useful.</em></h2><p>Every mission maps the way you reason to real skills, resilient roles, and learning steps. No profile required to look around.</p><button className="dd-launch" onClick={() => setView("dispatch")}>Choose a mission <Arrow /></button></div>
      <div className="dd-path-content">
        <div className="dd-path-selector"><span>EXPLORE BY MISSION</span>{missions.map((item) => <button key={item.id} className={activeId === item.id ? "active" : ""} onClick={() => setActiveId(item.id)}>{item.title}<Arrow /></button>)}</div>
        <div className="dd-role-panel"><div className="dd-role-head"><div><span className="dd-overline">POSSIBLE DIRECTIONS</span><h3>{mission.sdg}</h3></div><span className="dd-open-pill">OPEN TO EXPLORE</span></div>
          <div className="dd-role-list">{mission.roles.map((role, index) => <div className="dd-role" key={role}><span>0{index + 1}</span><strong>{role}</strong><Arrow diagonal /></div>)}</div>
          <div className="dd-skills"><span className="dd-overline">SKILLS YOU MAY PUT TO WORK</span><div>{mission.skills.map((skill) => <span key={skill}>{skill}</span>)}</div></div>
          <div className="dd-role-foot"><span>Mapped to the ESCO skills taxonomy</span><button onClick={() => setView("dispatch")}>See the decision lab <Arrow /></button></div>
        </div>
      </div>
    </section>}

    <footer className="dd-footer"><span>AI changes jobs. <b>Not your worth.</b></span><span>Signals to help you plan — never predictions about your limits.</span><span>XMUM · MALAYSIA <i /> AIVERSECITY</span></footer>

    {briefingOpen && <div className="dd-modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setBriefingOpen(false); }}>
      <section className="dd-modal" role="dialog" aria-modal="true" aria-labelledby="dd-modal-title">
        <button className="dd-modal-close" aria-label="Close briefing" onClick={() => setBriefingOpen(false)}>×</button>
        <span className="dd-overline">{sessionReady ? "YOUR FIELD SESSION" : `FIELD BRIEF / CASE 0${mission.id}`}</span>
        <h2 id="dd-modal-title">{sessionReady ? "Your first decision is waiting." : mission.title}</h2>
        <p>{sessionReady ? "This preview is ready. In the full experience, you’ll meet an AI advisor, weigh evidence, and see how your approach translates into skills." : `${mission.summary} You’ll make four decisions, get an AI advisor’s recommendation, then respond to an unexpected turn.`}</p>
        <div className="dd-modal-meta"><span>04 DECISIONS</span><i /><span>≈ 03 MINUTES</span><i /><span>NO CV NEEDED</span></div>
        {sessionReady ? <button className="dd-launch" onClick={() => setBriefingOpen(false)}>Return to mission desk <Arrow /></button> : <button className="dd-launch" onClick={() => setSessionReady(true)}>Prepare my session <Arrow /></button>}
      </section>
    </div>}
  </main>;
}
