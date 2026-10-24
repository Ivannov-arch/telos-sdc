"use client";

import Link from "next/link";
import { MISSIONS } from "@/lib/missions";
import { Icon, PageIntro } from "@/components/ui";

function Observatory() {
  return <div className="observatory" aria-label="Your skills connect to future roles and meaningful impact">
    <svg className="orbit-svg" viewBox="0 0 450 350" fill="none" aria-hidden="true">
      <defs>
        <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="var(--orbit-grid)" opacity=".4" /></pattern>
        <radialGradient id="core"><stop stopColor="var(--lime)" stopOpacity=".19" /><stop offset="1" stopColor="var(--lime)" stopOpacity="0" /></radialGradient>
      </defs>
      <rect width="450" height="350" fill="url(#grid)" />
      <circle cx="225" cy="170" r="142" fill="url(#core)" />
      <circle cx="225" cy="170" r="130" stroke="var(--orbit-ring)" strokeOpacity=".45" />
      <circle cx="225" cy="170" r="98" stroke="var(--orbit-ring-dash)" strokeDasharray="3 7" strokeOpacity=".5" />
      <ellipse cx="225" cy="170" rx="162" ry="67" transform="rotate(-32 225 170)" stroke="var(--orbit-orbit)" strokeOpacity=".6" />
      <ellipse cx="225" cy="170" rx="93" ry="145" transform="rotate(-35 225 170)" stroke="var(--orbit-orbit)" strokeOpacity=".4" />
      <path d="m114 76 111 94 133-18M225 170l-55 112" stroke="var(--orbit-path)" strokeOpacity=".5" />
      <circle cx="225" cy="170" r="43" fill="var(--orbit-center-bg)" stroke="var(--orbit-center-border)" />
      <circle cx="225" cy="170" r="34" fill="var(--lime)" />
      <path d="m225 150 5.7 14.3L245 170l-14.3 5.7L225 190l-5.7-14.3L205 170l14.3-5.7z" fill="var(--petrol)" />
      <circle cx="114" cy="76" r="5" fill="var(--lime)" />
      <circle cx="358" cy="152" r="5" fill="var(--lime)" />
      <circle cx="170" cy="282" r="5" fill="var(--lime)" />
      <circle cx="300" cy="68" r="3" fill="var(--orbit-dot)" />
      <circle cx="110" cy="222" r="3" fill="var(--orbit-dot)" />
    </svg>
    <div className="orbit-tag one"><Icon name="profile" size={15} /> Your decisions</div><div className="orbit-tag two"><Icon name="target" size={15} /> Future-fit roles</div><div className="orbit-tag three"><Icon name="globe" size={15} /> Real-world impact</div><div className="orbit-caption"><span>HUMAN POTENTIAL, CONNECTED.</span><span>01 / ∞</span></div>
  </div>;
}
export default function Home() {
  return <>
    <PageIntro eyebrow="THE HUMAN–AI DECISION LAB" title="Play your career future." description="No CV needed. A live crisis, an AI advisor, and four decisions show where you truly belong."><div className="status"><span className="status-dot" /> ABOUT 3 MINUTES</div></PageIntro>
    <section className="hero reveal"><div className="hero-copy"><div className="eyebrow"><span className="status-dot" style={{ background: "var(--lime)" }} /> THE CRISIS SIMULATION</div><h2>Play the crisis.<br />Discover <em>your future.</em></h2><p>Step into a global crisis and decide alongside an AI advisor. How you decide reveals your strengths, the roles that fit, and the skills to build next.</p><div className="actions"><Link className="btn lime" href="/play">Start the simulation<Icon size={16} /></Link><Link href="#how" className="text-link">See how it works<Icon size={14} /></Link></div></div><Observatory /></section>
    <div className="signal-strip"><span><Icon name="check" size={14} /> No CV and no login</span><span><Icon name="globe" size={14} /> Linked to the UN SDGs</span><span><Icon name="profile" size={14} /> Roles mapped to the ESCO taxonomy</span></div>
    <section id="how"><div className="section-header"><div><div className="eyebrow" style={{ color: "var(--muted)" }}>FROM A GAME TO A CAREER MAP</div><h2>Four steps. Under five minutes.</h2></div><span className="pill">NO RIGHT ANSWERS</span></div>
      <div className="journey four stagger">
        <Link className="journey-card" href="/play"><div className="card-top"><span className="icon-box"><Icon name="profile" /></span><span className="step-num">01 / PROFILE</span></div><h3>Tell us your starting point.</h3><p>Your skills, interests and learning time. Two minutes, no CV.</p><span className="text-link">Begin<Icon size={14} /></span></Link>
        <Link className="journey-card featured" href="/play"><div className="card-top"><span className="icon-box"><Icon name="practice" /></span><span className="step-num">02 / PLAY</span></div><h3>Lead through a crisis.</h3><p>Four rounds with an AI advisor, and a twist you won’t see coming.</p><span className="text-link">Enter the control room<Icon size={14} /></span></Link>
        <Link className="journey-card" href="/results"><div className="card-top"><span className="icon-box"><Icon name="spark" /></span><span className="step-num">03 / REVEAL</span></div><h3>See what it showed.</h3><p>The simulation was a skill sensor. Review the evidence behind each signal.</p><span className="text-link">Your results<Icon size={14} /></span></Link>
        <Link className="journey-card" href="/results"><div className="card-top"><span className="icon-box"><Icon name="target" /></span><span className="step-num">04 / GROW</span></div><h3>Follow your roadmap.</h3><p>Three matching roles and a step-by-step reskilling path for each.</p><span className="text-link">Explore roles<Icon size={14} /></span></Link>
      </div>
    </section>
    <section><div className="section-header"><div><div className="eyebrow" style={{ color: "var(--muted)" }}>CHOOSE A CRISIS</div><h2>Three missions. Three global challenges.</h2></div></div>
      <div className="mission-grid stagger">{MISSIONS.map((m) => <Link key={m.id} href={`/play?mission=${m.id}`} className="mission-card"><div className="card-top"><span className="step-num">{m.code}</span><span className="pill accent">{m.sdg}</span></div><h3>{m.title}</h3><strong>{m.crisis}</strong><p>{m.pitch}</p><span className="mission-pick">Play this mission<Icon size={14} /></span></Link>)}</div>
    </section>
    <div className="insight-row stagger"><section className="insight"><div className="sdg-bars" aria-hidden="true"><i /><i /><i /></div><div><div className="eyebrow" style={{ fontSize: 8, marginBottom: 7 }}>MORE THAN A MATCH SCORE</div><h3>A career that moves the world forward.</h3><p>Every mission is tied to a UN Sustainable Development Goal, and so are the roles and learning steps you’re shown.</p></div></section><section className="insight"><Icon name="spark" size={32} /><div><h3>AI changes jobs. Not your worth.</h3><p>See your path under moderate and rapid AI adoption. These are signals to help you plan, not predictions about your limits.</p></div></section></div>
    <section><div className="section-header"><div><div className="eyebrow" style={{ color: "var(--muted)" }}>MORE TOOLS</div><h2>Prefer to start from your CV?</h2></div></div>
      <div className="insight-row stagger" style={{ marginTop: 0 }}><Link className="insight" href="/profiles"><Icon name="profile" size={28} /><div><h3>Skill profiles</h3><p>Upload a CV or enter skills and map them to ESCO, then match against roles.</p></div></Link><Link className="insight" href="/simulate"><Icon name="practice" size={28} /><div><h3>Practice lab</h3><p>Short workplace tasks with rubric-based feedback.</p></div></Link></div>
    </section>
  </>;
}
