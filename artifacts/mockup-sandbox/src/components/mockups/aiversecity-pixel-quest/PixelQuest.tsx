import { useMemo, useState } from "react";
import "./_group.css";

type Mission = { id: string; name: string; crisis: string; sdg: string; code: string; pitch: string; icon: "supply" | "credit" | "grid"; };
const MISSIONS: Mission[] = [
  { id: "A", name: "Supply Under Pressure", crisis: "Food routes collapse across Southeast Asia", sdg: "SDG 02 · ZERO HUNGER", code: "SECTOR 01", pitch: "Four routes. One dwindling reserve. Millions are waiting.", icon: "supply" },
  { id: "B", name: "The Credit Algorithm", crisis: "A biased AI is denying fair loans", sdg: "SDG 10 · REDUCED INEQUALITIES", code: "SECTOR 02", pitch: "The model is fast. Its mistakes are not evenly shared.", icon: "credit" },
  { id: "C", name: "Grid Failure", crisis: "A clean-energy grid fails at peak demand", sdg: "SDG 07 · CLEAN ENERGY", code: "SECTOR 03", pitch: "Hospitals are dark. A heatwave is still climbing.", icon: "grid" },
];
const ROUNDS = ["Choose a route", "AI enters the field", "Unexpected shock", "Final call"];
const CHOICES: Record<string, Partial<Record<number, string[]>>> = {
  A: {
    1: [
      "Split the limited budget across all four routes so every region gets some supply, and keep a small reserve for surprises.",
      "Put most of the budget into the two routes that reach the most people and accept that some regions will wait.",
      "Spend the first hours collecting data on port status and route capacity before committing any budget.",
      "Prioritise the most vulnerable groups, such as children, hospitals and remote villages, even if it costs more per person.",
    ],
    3: [
      "Accept the volunteer network at once to cover Routes A and C, and use the saved budget on the remaining routes.",
      "Start with a small trial using the volunteers on one route while I vet them, and scale up only once they check out.",
      "Decline the unvetted volunteers and reallocate the reduced budget across the routes that are still open.",
      "Ask the volunteer network for credentials and references first, then decide how many routes to hand them.",
    ],
    4: [
      "Commit to a staged plan: protect the most vulnerable first, use verified partners for the rest, and review daily.",
      "Concentrate everything on the two highest-capacity routes to reach the largest population fastest.",
      "Keep a balanced spread across the open routes with a clear rule for moving budget when a route fails.",
      "Use the volunteers wherever they are already vetted and rely on formal logistics partners everywhere else.",
    ],
  },
  B: {
    1: [
      "Patch the scoring model quickly to correct the disparity, then audit the results afterwards.",
      "Pause automated decisions for the affected groups and move their applications to human review while I investigate.",
      "Commission an independent audit of the model and training data to find the root cause before changing anything.",
      "Notify the affected applicants, offer to re-review their cases, and cooperate openly with the regulators.",
    ],
    3: [
      "Use the leaked documents straight away to find the root cause, because the 48-hour fix outweighs the risk.",
      "Quarantine the leaked documents, ask legal counsel to confirm they are authentic and lawful, then decide.",
      "Ignore the leak, switch to the new EU compliance guidance, and rebuild the fix from our own records.",
      "Disclose the leak to the regulators and let them guide how it can be used.",
    ],
    4: [
      "Commit to a full root-cause remediation with independent verification, transparent reporting and compensation for affected customers.",
      "Roll out the quickest compliant patch now and schedule a deeper review within the quarter.",
      "Suspend the model, return to human underwriting, and relaunch only once an external audit signs off.",
      "Fix the model using only verified evidence, publish what happened, and set up ongoing bias monitoring.",
    ],
  },
  C: {
    1: [
      "Restore power to hospitals and emergency services first, then bring back residential areas in stages.",
      "Reroute power across all available lines to bring as many homes back as fast as possible.",
      "Check the load and condition of each line before switching anything, to avoid a second failure.",
      "Ask large industrial users to cut demand so that the limited supply covers critical sites and homes.",
    ],
    3: [
      "Activate the Northern Emergency Line immediately, since it is the only option that can carry the larger load.",
      "Get an engineer to inspect the Northern line quickly, and bring it online only if it passes.",
      "Leave the Northern line off, protect critical sites with backup generators, and ration the rest of the grid.",
      "Bring the Northern line on at partial load while monitoring it, with a plan to cut it off at any sign of strain.",
    ],
    4: [
      "Commit to a staged restoration: critical sites first, then residential zones by priority, with checks before each step.",
      "Use every available line, including the Northern one, at full capacity to restore the most people the fastest.",
      "Use only lines with recent inspection data and cover the gap with generators and demand reduction.",
      "Restore in zones, assign teams to monitor each line, and be ready to switch zones off if load becomes unsafe.",
    ],
  },
};
const ROUND2_CHOICES = [
  { title: "ACCEPT", detail: "Follow the advisor's recommendation.", tag: "01" },
  { title: "OVERRIDE", detail: "Choose a different course yourself.", tag: "02" },
  { title: "VERIFY", detail: "Check the evidence before committing.", tag: "03" },
];
const SHOCKS: Record<string, { title: string; text: string; opportunity: string }> = {
  A: { title: "ROUTE 04 IS GONE", text: "A bridge has failed in the storm. Your fastest supply corridor is cut off; local teams report a safe but unverified river crossing.", opportunity: "A community radio network can coordinate boats—if you share the remaining fuel." },
  B: { title: "THE DATASET WAS WRONG", text: "A previously excluded district has been found in the training data. The model's confidence was built on incomplete records.", opportunity: "A community audit team offers a verified sample, but it will delay the fix by one round." },
  C: { title: "A BATTERY FARM IS OFFLINE", text: "A heatwave has raised demand by 18%. The largest battery site is offline, and the forecast is now stale.", opportunity: "A neighborhood microgrid can carry the clinic network if you release its stored reserve." },
};
const ADVICE: Record<string, string> = {
  A: "Prioritise clinics first. It minimises immediate harm—but the northern villages will wait.",
  B: "Restore human review for high-risk cases. The score is strong; the sample behind it is thin.",
  C: "Island the hospital network. The forecast says it is safest, though the inputs are 40 minutes old.",
};

function MissionIcon({ kind }: { kind: Mission["icon"] }) {
  if (kind === "supply") return <svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M5 23h22M8 22V12h16v10M12 12V8h8v4M11 17h3m4 0h3M5 26h22" stroke="currentColor" strokeWidth="2"/><path d="M15 8V5h2v3" stroke="#efdd84" strokeWidth="2"/></svg>;
  if (kind === "credit") return <svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M5 8h22v16H5zM5 13h22M10 19h6" stroke="currentColor" strokeWidth="2"/><path d="m21 18 2 2 4-5" stroke="#efdd84" strokeWidth="2"/></svg>;
  return <svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="m16 4 9 5v14l-9 5-9-5V9l9-5Z" stroke="currentColor" strokeWidth="2"/><path d="M16 9v7l6 4M9 24l5-8" stroke="#efdd84" strokeWidth="2"/><circle cx="16" cy="16" r="2" fill="currentColor"/></svg>;
}

function PixelAdvisor({ sleeping = false }: { sleeping?: boolean }) {
  return <div className="pq-advisor-sprite" aria-label={sleeping ? "Advisor offline" : "AI advisor awake"}>
    <svg viewBox="0 0 48 48" role="img" aria-hidden="true" shapeRendering="crispEdges">
      <g className="pq-pixel-char">
        <path fill="#efdd84" d="M16 5h16v4h4v4h4v14h-4v5h-4v5H16v-5h-4v-5H8V13h4V9h4z"/>
        <path fill="#304c77" d="M12 13h24v14H12z"/>
        <path fill="#82d9d2" d="M16 17h5v5h-5zm11 0h5v5h-5z"/>
        <path fill="#09152b" d="M17 18h2v3h-2zm11 0h2v3h-2zM21 25h7v2h-7z"/>
        <path fill="#efdd84" d="M8 13h4v14H8zm28 0h4v14h-4z"/>
        <path fill="#d1af63" d="M15 32h18v4H15zm4 4h10v4H19z"/>
        <path fill="#82d9d2" d="M12 40h24v4H12z"/>
        <path fill="#efdd84" d="M20 11h8v2h-8z"/>
      </g>
      <path fill="#82d9d2" d="M22 2h4v3h-4z"/>
    </svg>
  </div>;
}

function BackgroundScene({ mission, shock }: { mission: string; shock: boolean }) {
  const accent = mission === "C" ? "#82d9d2" : mission === "B" ? "#efdd84" : "#c9df9d";
  return <div className="pq-stage-art" aria-hidden="true">
    <svg viewBox="0 0 900 430" preserveAspectRatio="xMidYMid slice">
      <defs><pattern id="pqGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#52709d" strokeOpacity=".12"/></pattern></defs>
      <rect width="900" height="430" fill="url(#pqGrid)"/>
      <path d="M0 317h122v-46h42v46h97v-69h58v69h82v-40h51v40h118v-75h54v75h78v-50h63v50h135v113H0z" fill="#132849" opacity=".62"/>
      <path d="M0 355h900M24 377h18m38 0h8m75 0h24m47 0h11m90 0h24m47 0h11m88 0h24m47 0h11m78 0h24m52 0h20m44 0h9" stroke={accent} strokeOpacity=".45" strokeWidth="3"/>
      <circle cx="738" cy="96" r="48" fill={accent} opacity=".07"/>
      <circle cx="738" cy="96" r="28" fill="none" stroke={accent} strokeOpacity=".2" strokeDasharray="3 7"/>
      {shock && <path d="m689 115 21-23 18 19 19-37 18 30 25-28" stroke="#ef7f77" strokeWidth="4" strokeDasharray="8 6" opacity=".7"/>}
      <path d="M0 411h900" stroke="#efdd84" strokeOpacity=".25"/>
    </svg>
  </div>;
}

function Heart() {
  return <svg className="pq-heart" viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M3 2h4v2h2V2h4v2h2v5h-2v2h-2v2H9v2H7v-2H5v-2H3V9H1V4h2z"/></svg>;
}

export function PixelQuest() {
  const [missionId, setMissionId] = useState("A");
  const [round, setRound] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [thoughts, setThoughts] = useState("");
  const [showEvidence, setShowEvidence] = useState(false);
  const [roundHistory, setRoundHistory] = useState<Array<{ action: string; option: number; thoughts?: string }>>([]);
  const mission = useMemo(() => MISSIONS.find((item) => item.id === missionId) ?? MISSIONS[0], [missionId]);
  const advisorAwake = round >= 2;
  const isReveal = round === 5;
  const options = CHOICES[missionId]?.[round] ?? [];
  const shock = SHOCKS[missionId];
  const verified = roundHistory.some((entry) => entry.action === "VERIFY");
  const adapted = roundHistory.some((entry) => entry.action === "ADAPTED");
  const trustScore = verified ? 91 : roundHistory.some((entry) => entry.action === "ACCEPT") ? 64 : 74;
  const roundName = round === 0 ? "MISSION SELECT" : round > 4 ? "LEVEL COMPLETE" : ROUNDS[round - 1];

  function begin() {
    setRound(1); setSelected(null); setThoughts(""); setRoundHistory([]); setShowEvidence(false);
  }
  function moveMission(direction: number) {
    const index = MISSIONS.findIndex((item) => item.id === missionId);
    setMissionId(MISSIONS[(index + direction + MISSIONS.length) % MISSIONS.length].id);
  }
  function commitChoice(choice: number, kind: string) {
    setRoundHistory((prev) => [...prev, { action: kind, option: choice, thoughts: thoughts.trim() || undefined }]);
    setSelected(null);
    setThoughts("");
    setRound((prev) => prev + 1);
    setShowEvidence(false);
  }
  function resetRun() {
    setRound(0); setSelected(null); setThoughts(""); setRoundHistory([]); setShowEvidence(false);
  }
  const roundNumber = Math.min(round, 4);

  return <main className="pq-root">
    <div className="pq-shell">
      <header className="pq-topline">
        <div className="pq-brand"><div className="pq-mark" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M4 18 12 4l8 14H4Z" stroke="currentColor" strokeWidth="2"/><path d="M9 18v-5h6v5" stroke="currentColor" strokeWidth="2"/></svg></div><div className="pq-brand-name">Aiversecity<small>FUTUREPROOF / FIELD SIM</small></div></div>
        <div className="pq-topmeta"><div className="pq-live"><i/> SIMULATION READY</div><div className="pq-system"><b/><b/><b/><b/><span>SYS 08:16</span></div></div>
      </header>
      <div className="pq-intro">
        <div><div className="pq-kicker">A HUMAN × AI DECISION GAME</div><h1>Your future is a <span>quest.</span></h1><p>Four decisions. One crisis. Discover what you do when the plan breaks.</p></div>
        <div className="pq-clock">TIME &nbsp;03 MIN · NO CV · NO WRONG ANSWERS</div>
      </div>
      <div className="pq-layout">
        <section className="pq-main">
          <div className="pq-frame">
            <div className="pq-scenetop"><span><strong>{mission.code}</strong> &nbsp; / &nbsp; {roundName}</span><span>{isReveal ? "DEBRIEF" : round === 0 ? "SELECT A WORLD" : `ROUND 0${roundNumber} / 04`}</span></div>
            {!isReveal ? <div className="pq-stage">
              <BackgroundScene mission={mission.id} shock={round === 3}/>
              <div className="pq-stage-copy">
                <div className="pq-label">{round === 0 ? mission.sdg : round === 3 ? "ALERT / NEW CONDITIONS" : round === 2 ? "ADVISOR CONNECTION ESTABLISHED" : `MISSION ${mission.id} · ${round === 1 ? "BRIEFING" : "DECISION"}`}</div>
                <h2>{round === 0 ? mission.crisis : round === 1 ? "The first call is yours." : round === 2 ? "Your advisor has a plan." : round === 3 ? shock.title : "One last decision."}</h2>
                <p>{round === 0 ? mission.pitch : round === 1 ? `A regional emergency is unfolding. ${mission.pitch} You have one call before the situation changes.` : round === 2 ? "AIX has studied the available evidence and formed a recommendation. You can accept it, override it, or verify the data before you decide." : round === 3 ? shock.text : "The crisis is stabilising. Lock in the move that best reflects how you lead when the stakes are real."}</p>
                {round === 0 && <div className="pq-briefbox"><b>MISSION OBJECTIVE</b><br/>{mission.crisis}. Make the next move count; no specialist knowledge needed.</div>}
                {round === 1 && <div className="pq-dialogue"><PixelAdvisor sleeping/><div className="pq-dialogue-text"><b>COMMS / AIX NOT YET ONLINE</b>“No recommendation is coming yet. What matters most in the first move?”<i className="pq-cursor"/></div></div>}
                {round === 2 && <div className="pq-dialogue"><PixelAdvisor/><div className="pq-dialogue-text"><b>AIX / ADVISOR ONLINE</b>{ADVICE[mission.id]}<i className="pq-cursor"/></div></div>}
                {round === 3 && <><div className="pq-shock"><div className="pq-label">UNEXPECTED SHOCK / EVENT LOG</div><p>{shock.opportunity}</p></div><div className="pq-notice">{showEvidence ? "VERIFIED / Community operations data confirms this option is available. Confidence: 82%." : "UNVERIFIED / The opportunity has not yet been checked against field data."}</div></>}
                {round > 0 && round < 5 && round !== 2 && <div className="pq-option-set">
                  <div className="pq-option-caption">SELECT A STARTING POINT <span>4 POSSIBLE MOVES · NO RIGHT ANSWER</span></div>
                  <div className="pq-choice-grid">
                    {options.map((option, index) => <button key={`${mission.id}-${round}-${index}`} className={`pq-choice ${selected === index ? "selected" : ""}`} type="button" aria-pressed={selected === index} onClick={() => { setSelected(index); setThoughts(option); }}>
                      <span className="pq-option-number">0{index + 1}</span><span className="pq-choice-text">{option}</span><span className="pq-choice-cursor" aria-hidden="true">▶</span>
                    </button>)}
                  </div>
                </div>}
                {round === 2 && <div className="pq-choice-grid pq-advisor-choices">
                  {ROUND2_CHOICES.map((option, index) => <button key={option.tag} className={`pq-choice ${selected === index ? "selected" : ""}`} type="button" aria-pressed={selected === index} onClick={() => setSelected(index)}>
                    <em>{option.tag}</em><strong>{option.title}</strong><small>{index === 2 ? (showEvidence ? "Evidence reviewed. Then decide." : "Open the field data before committing.") : option.detail}</small>
                  </button>)}
                </div>}
                {round > 0 && round < 5 && <div className="pq-thoughts">
                  <label htmlFor="pq-thoughts">YOUR THOUGHTS <span>OPTIONAL · WRITE IT YOUR WAY</span></label>
                  <textarea id="pq-thoughts" value={thoughts} onChange={(event) => setThoughts(event.target.value)} placeholder={round === 1 ? "What would you do first, and why?" : round === 3 ? "How does the new information change your plan?" : round === 4 ? "What matters most in your final call?" : "Add context to your decision (optional)…"} rows={3} />
                  {round !== 2 && <small>Choose a suggested move, write your own response, or do both.</small>}
                </div>}
                {round === 0 ? <div className="pq-actionrow"><button className="pq-btn primary" type="button" onClick={begin}>Insert coin · Begin mission <span>▶</span></button><span style={{ color: "#94a7c4", fontSize: 8 }}>01 / 03 WORLDS</span></div> :
                <div className="pq-actionrow">
                  {round === 2 && <button className="pq-btn subtle" type="button" onClick={() => setShowEvidence(!showEvidence)}>{showEvidence ? "✓ DATA VERIFIED" : "⌕ VERIFY EVIDENCE"}</button>}
                  <button className="pq-btn primary" type="button" disabled={round === 2 ? selected === null : selected === null && thoughts.trim().length < 10} onClick={() => {
                    const choice = selected ?? 99;
                    if (round === 2 && selected === 2 && !showEvidence) { setShowEvidence(true); return; }
                    if (round === 2 && selected === 2) { commitChoice(choice, "VERIFY"); return; }
                    if (round === 2) { commitChoice(choice, ROUND2_CHOICES[selected!].title); return; }
                    commitChoice(choice, selected === null ? "CUSTOM RESPONSE" : round === 1 ? "FIRST MOVE" : round === 3 ? "ADAPTED" : "FINAL CALL");
                  }}>
                    {round === 4 ? "LOCK IN · REVEAL" : round === 2 ? selected === 2 && !showEvidence ? "OPEN FIELD DATA" : "COMMIT DECISION" : selected === null ? "SUBMIT YOUR RESPONSE" : "CONFIRM MOVE"} <span>▶</span>
                  </button>
                  {round === 2 && <span style={{ color: "#94a7c4", fontSize: 8 }}>{selected === 0 ? "ACCEPT" : selected === 1 ? "OVERRIDE" : selected === 2 ? showEvidence ? "VERIFY" : "VERIFY FIRST" : "CHOOSE YOUR RESPONSE"}</span>}
                </div>}
              </div>
              <div className="pq-artside"><div className="pq-mission-glyph"><span className="pq-orbit-dot one"/><span className="pq-orbit-dot two"/><div className="pq-glyph-icon"><MissionIcon kind={mission.icon}/></div></div></div>
              <div className="pq-stagefoot"><span>FIELD FEED / {mission.sdg}</span><span>{round === 0 ? "AIVERSE CITY · 2088" : `CHOICE ${Math.max(1,round)} OF 4`}</span></div>
            </div> :
            <div className="pq-reveal">
              <div className="pq-complete"><div className="pq-medal">★</div><div><h2>Level complete.</h2><p>Career signal unlocked · {mission.sdg} · Your choices are evidence, not a verdict.</p></div></div>
              <div className="pq-reveal-grid">
                <div className="pq-reveal-block"><h3>What your choices revealed</h3>
                  {[["Critical verification", verified ? 91 : 68],["Adaptability", adapted ? 88 : 72],["Calibrated AI trust", trustScore],["Decision quality", roundHistory.length > 2 ? 86 : 79]].map(([label, value]) => <div className="pq-stat" key={label}><span>{label}</span><div className="pq-bar"><i style={{ width: `${value}%` }}/></div><b>{value}%</b></div>)}
                  <div className="pq-notice">Signal: you tend to balance speed with the human impact of a decision. This is a snapshot from one simulation—not a prediction.</div>
                </div>
                <div className="pq-reveal-block"><h3>Roles on your map</h3>
                  <div className="pq-role"><span className="pq-match">87% FIT</span><strong>Humanitarian Logistics Coordinator</strong><small>Routes resources through uncertainty · ESCO mapped</small></div>
                  <div className="pq-role"><span className="pq-match">81% FIT</span><strong>AI Ethics &amp; Governance Analyst</strong><small>Tests automated decisions against real outcomes · ESCO mapped</small></div>
                  <div className="pq-role"><span className="pq-match">76% FIT</span><strong>Resilience Programme Lead</strong><small>Builds response plans with local partners · ESCO mapped</small></div>
                </div>
              </div>
              {roundHistory.some((entry) => entry.thoughts) && <div className="pq-reveal-block pq-written"><h3>Your words from the field</h3>{roundHistory.map((entry, index) => entry.thoughts ? <blockquote key={`${index}-${entry.action}`}><small>ROUND 0{index + 1} · {entry.action}</small><p>{entry.thoughts}</p></blockquote> : null)}</div>}
              <div className="pq-reveal-block pq-path"><h3>Your next level · reskilling path</h3><ol><li><strong>Data literacy</strong>Read a model's confidence and spot missing evidence · 2 weeks</li><li><strong>Human-centred operations</strong>Map stakeholders and prioritise under constraints · 3 weeks</li><li><strong>AI accountability</strong>Practice an impact audit using a real case · 4 weeks</li></ol></div>
              <div className="pq-actionrow"><button className="pq-btn primary" type="button" onClick={resetRun}>PLAY ANOTHER MISSION <span>↻</span></button><button className="pq-btn subtle" type="button" onClick={() => { setMissionId("B"); resetRun(); }}>EXPLORE ROLE MAP</button></div>
            </div>}
          </div>
          <footer className="pq-footer"><span><i className="pq-square"/> AIVERSECITY · FUTUREPROOF</span><span>THE GAME IS SHORT. YOUR NEXT MOVE IS YOURS.</span><span>SDG · ESCO · HUMAN FIRST</span></footer>
        </section>
        <aside className="pq-aside">
          <section className="pq-panel pq-missions-panel">
            <div className="pq-panelhead"><span>Mission select</span><em>{missionId} / 03</em></div>
            <div className="pq-mission-list">{MISSIONS.map((item) => <button className={`pq-mission ${missionId === item.id ? "selected" : ""}`} type="button" onClick={() => { if (round === 0 || isReveal) { setMissionId(item.id); if (isReveal) resetRun(); } }} key={item.id} aria-pressed={missionId === item.id}>
              <span className="pq-mission-icon"><MissionIcon kind={item.icon}/></span><span><strong>{item.name}</strong><small>{item.sdg}</small></span><span className="pq-chevron">{missionId === item.id ? "›" : ""}</span>
            </button>)}</div>
            <div className="pq-mini-controls"><span>SCROLL TO SELECT WORLD</span><div><button type="button" aria-label="Previous mission" onClick={() => moveMission(-1)} disabled={round > 0 && !isReveal}>‹</button> <button type="button" aria-label="Next mission" onClick={() => moveMission(1)} disabled={round > 0 && !isReveal}>›</button></div></div>
          </section>
          <section className="pq-panel pq-hud-panel">
            <div className="pq-panelhead"><span>Run HUD</span><em>{round === 0 ? "STANDBY" : isReveal ? "CLEAR" : `0${roundNumber} / 04`}</em></div>
            <div className="pq-progress" aria-label={`Round ${roundNumber} of 4`}>{[1,2,3,4].map((item) => <span key={item} className={round >= item ? item === round ? "active" : "done" : ""}/>)}</div>
            <div className="pq-hudinfo"><span>DECISION ENERGY</span><div className="pq-hearts"><Heart/><Heart/><Heart/><Heart/></div></div>
            <div className="pq-hudinfo"><span>MISSION</span><strong>{missionId} · {mission.name.split(" ")[0]}</strong></div>
            <div className="pq-hudinfo"><span>TIME ESTIMATE</span><strong>03:00</strong></div>
          </section>
          <section className="pq-panel pq-advisor-panel">
            <div className="pq-panelhead"><span>AI companion</span><em>{advisorAwake ? "ONLINE" : "LOCKED"}</em></div>
            <div className={`pq-advisor ${advisorAwake ? "" : "offline"}`}><PixelAdvisor sleeping={!advisorAwake}/><div className="pq-advisor-copy"><strong>AIX / 08</strong><small className={advisorAwake ? "pq-awake" : ""}>{advisorAwake ? "ADVISOR · ACTIVE" : "SLEEP MODE · ROUND 02"}</small></div></div>
            <div className="pq-advisor-line">{advisorAwake ? "I can recommend. You decide whether the evidence earns your trust." : "I wake when there is enough evidence to make a recommendation."}</div>
          </section>
        </aside>
      </div>
    </div>
  </main>;
}
