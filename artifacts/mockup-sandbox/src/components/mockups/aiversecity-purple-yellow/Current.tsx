import type { ReactNode } from "react";
import "./_group.css";

function Icon({ name = "arrow", size = 18 }: { name?: string; size?: number }) {
  const paths: Record<string, ReactNode> = {
    arrow: <path d="M4 12h15M13 6l6 6-6 6" />,
    home: <><path d="m3 10 9-7 9 7v10H3z" /><path d="M9 20v-7h6v7" /></>,
    profile: <><circle cx="12" cy="8" r="4" /><path d="M4 21v-2a8 8 0 0 1 16 0v2" /></>,
    target: <><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1" /></>,
    practice: <path d="m13 2-9 12h7l-1 8 10-13h-7z" />,
    check: <path d="m5 12 4 4L19 6" />,
    globe: <><circle cx="12" cy="12" r="9" /><ellipse cx="12" cy="12" rx="4" ry="9" /><path d="M3 12h18" /></>,
    chevron: <path d="m8 10 4 4 4-4" />,
    spark: <path d="m12 3 2.6 6.4L21 12l-6.4 2.6L12 21l-2.6-6.4L3 12l6.4-2.6z" />,
  };

  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name] ?? paths.arrow}</svg>;
}

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
    <div className="orbit-tag one"><Icon name="profile" size={15} />Your unique skills</div>
    <div className="orbit-tag two"><Icon name="target" size={15} />Future-fit roles</div>
    <div className="orbit-tag three"><Icon name="globe" size={15} />Meaningful impact</div>
    <div className="orbit-caption"><span>HUMAN POTENTIAL, CONNECTED.</span><span>01 / ∞</span></div>
  </div>;
}

export default function Current({ className = "" }: { className?: string }) {
  return <div className={`app ${className}`}>
    <aside className="sidebar">
      <a href="#overview" className="brand" aria-label="Aiversecity home"><span className="brand-mark"><Icon name="spark" size={23} /></span>Aiversecity</a>
      <div className="brand-sub">A future that fits you</div>
      <div className="nav-label">YOUR WORKSPACE</div>
      <nav aria-label="Main navigation">
        <a href="#overview" className="nav-link active" aria-current="page"><Icon name="home" /><span>Overview</span><span className="nav-dot" /></a>
        <a href="#profiles" className="nav-link"><Icon name="profile" /><span>My profiles</span></a>
        <a href="#matches" className="nav-link"><Icon name="target" /><span>Role matches</span></a>
        <a href="#practice" className="nav-link"><Icon name="practice" /><span>Practice lab</span></a>
      </nav>
      <div className="sidebar-bottom">
        <div className="side-note"><Icon name="globe" size={20} /><div style={{ marginTop: 10 }}><strong>Skills for a better future.</strong><p>Find your place in a changing world of work. Make your next move count.</p></div></div>
        <div className="project-credit">Built for SDC XMUM Hackathon<br /><span style={{ fontFamily: "var(--font-code)", fontSize: 9 }}>XMUM · MALAYSIA</span></div>
      </div>
    </aside>
    <div className="workspace">
      <div className="topbar">
        <div className="breadcrumb">Workspace <span>/</span> <b>Overview</b></div>
        <a href="#profiles" className="profile-switch"><span className="avatar">AV</span><span>Choose your profile</span><Icon name="chevron" size={13} /></a>
      </div>
      <main className="main">
        <header className="page-intro">
          <div><div className="eyebrow">YOUR CAREER OBSERVATORY</div><h1>Your potential. A clearer direction.</h1><p>The world of work is changing. Let’s find where you fit next.</p></div>
          <div className="status"><span className="status-dot" /> BUILT FOR WHAT’S NEXT</div>
        </header>
        <section className="hero">
          <div className="hero-copy">
            <div className="eyebrow"><span className="status-dot" style={{ background: "var(--lime)" }} /> HUMAN SKILLS. NEW POSSIBILITIES.</div>
            <h2>The future of work<br />has a place <em>for you.</em></h2>
            <p>Turn what you know into what comes next. Discover your strengths, explore resilient roles, and build the skills to get there.</p>
            <div className="actions"><a className="btn lime" href="#profile">Map my potential<Icon size={16} /></a><a href="#profiles" className="text-link">I already have a profile<Icon size={14} /></a></div>
          </div>
          <Observatory />
        </section>
        <div className="signal-strip">
          <span><Icon name="check" size={14} />Grounded in the ESCO skills taxonomy</span>
          <span><Icon name="globe" size={14} />Connected to the UN SDGs</span>
          <span><Icon name="profile" size={14} />Your skills, not just your job title</span>
        </div>
        <section>
          <div className="section-header"><div><div className="eyebrow" style={{ color: "var(--muted)" }}>A LITTLE CLARITY GOES A LONG WAY</div><h2>Your next chapter, in three steps.</h2></div><span className="pill">AT YOUR OWN PACE</span></div>
          <div className="journey">
            <a className="journey-card featured" href="#profile"><div className="card-top"><span className="icon-box"><Icon name="profile" /></span><span className="step-num">01 / DISCOVER</span></div><h3>Start with what you know.</h3><p>Upload your CV or tell us your skills. We’ll map them to a shared language of work.</p><span className="text-link">Build your profile<Icon size={14} /></span></a>
            <a className="journey-card" href="#matches"><div className="card-top"><span className="icon-box"><Icon name="target" /></span><span className="step-num">02 / EXPLORE</span></div><h3>See where you could go.</h3><p>Explore role matches, understand AI’s impact, and see exactly which skills to build next.</p><span className="text-link">Explore role matches<Icon size={14} /></span></a>
            <a className="journey-card" href="#practice"><div className="card-top"><span className="icon-box"><Icon name="practice" /></span><span className="step-num">03 / GROW</span></div><h3>Make progress, in practice.</h3><p>Try short workplace simulations. Get specific feedback. Build confidence with every attempt.</p><span className="text-link">Enter the practice lab<Icon size={14} /></span></a>
          </div>
        </section>
        <div className="insight-row">
          <section className="insight"><div className="sdg-bars" aria-hidden="true"><i /><i /><i /></div><div><div className="eyebrow" style={{ fontSize: 8, marginBottom: 7 }}>MORE THAN A MATCH SCORE</div><h3>A career that moves the world forward.</h3><p>See how your potential roles contribute to the UN Sustainable Development Goals. Good work can do good, too.</p></div></section>
          <section className="insight"><Icon name="spark" size={32} /><div><h3>AI changes jobs. Not your worth.</h3><p>Compare moderate and fast AI-disruption scenarios. These are signals to help you plan—not predictions about your limits.</p></div></section>
        </div>
        <footer className="footer"><span>Aiversecity — human potential, mapped for what’s next.</span><span>ESCO-powered skills · UN SDG-aligned · No account needed</span></footer>
      </main>
    </div>
  </div>;
}
