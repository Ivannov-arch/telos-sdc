import { useEffect, useRef, useState } from 'react';
import { ArrowRight, ArrowUpRight, Check, ChevronDown, FlaskConical, Globe2, Home, ScanFace, Sparkles, Target, X } from 'lucide-react';
import './CareerStudio.css';

type Panel = 'profile' | 'profiles' | 'matches' | 'practice' | null;

function StudioOrbit() {
  return <div className="cs-observatory" aria-label="Your unique skills connect to future-fit roles and meaningful impact">
    <svg className="cs-orbit" viewBox="0 0 500 370" fill="none" aria-hidden="true">
      <circle cx="253" cy="179" r="139" fill="#edb394" opacity=".5"/>
      <circle cx="253" cy="179" r="139" stroke="#a8756c" strokeWidth=".8"/>
      <circle cx="253" cy="179" r="99" stroke="#a8756c" strokeDasharray="2 7"/>
      <ellipse cx="253" cy="179" rx="171" ry="65" transform="rotate(-31 253 179)" stroke="#243dbb" strokeWidth="1.2"/>
      <ellipse cx="253" cy="179" rx="81" ry="146" transform="rotate(-33 253 179)" stroke="#a8756c" strokeWidth=".8"/>
      <path d="M132 84 253 179 392 151M253 179l-54 123" stroke="#243dbb" strokeDasharray="3 5"/>
      <circle cx="253" cy="179" r="48" fill="#243dbb"/>
      <path d="M253 145c1 22 12 33 34 34-22 1-33 12-34 34-1-22-12-33-34-34 22-1 33-12 34-34Z" fill="#f5e76a"/>
      <circle cx="132" cy="84" r="9" fill="#243dbb"/>
      <circle cx="132" cy="84" r="3" fill="#f5e76a"/>
      <rect x="385" y="144" width="14" height="14" transform="rotate(15 392 151)" fill="#f5e76a" stroke="#243dbb"/>
      <circle cx="199" cy="302" r="7" fill="#243dbb"/>
      <circle cx="333" cy="65" r="4" fill="#bb7d65"/>
      <path d="M111 231v12m-6-6h12M362 280v12m-6-6h12" stroke="#243dbb"/>
      <path d="m349 42 9 6-9 6" stroke="#a8756c"/>
    </svg>
    <div className="cs-orbit-label one"><ScanFace size={15}/>Your unique skills</div>
    <div className="cs-orbit-label two"><Target size={15}/>Future-fit roles</div>
    <div className="cs-orbit-label three"><Globe2 size={15}/>Meaningful impact</div>
    <div className="cs-caption cs-mono"><span>HUMAN POTENTIAL, CONNECTED.</span><span>01 / ∞</span></div>
  </div>;
}

export default function CareerStudio() {
  const [panel, setPanel] = useState<Panel>(null);
  const [name, setName] = useState('');
  const [skills, setSkills] = useState('');
  const [profile, setProfile] = useState<{name: string; skills: string} | null>(null);
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const closeRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (!panel) return;
    const previous = document.activeElement as HTMLElement | null;
    closeRef.current?.focus();
    const listener = (event: KeyboardEvent) => { if(event.key === 'Escape') setPanel(null); };
    window.addEventListener('keydown', listener);
    return () => { window.removeEventListener('keydown', listener); previous?.focus(); };
  }, [panel]);
  const open = (next: Panel) => { setPanel(next); setSubmitted(false); };
  const cards = [
    {icon: ScanFace, number: '01 / DISCOVER', title: 'Start with what you know.', description: 'Upload your CV or tell us your skills. We’ll map them to a shared language of work.', action: profile ? 'View your skills' : 'Build your profile', panel: 'profile' as Panel},
    {icon: Target, number: '02 / EXPLORE', title: 'See where you could go.', description: 'Explore role matches, understand AI’s impact, and see exactly which skills to build next.', action: 'Explore role matches', panel: 'matches' as Panel},
    {icon: FlaskConical, number: '03 / GROW', title: 'Make progress, in practice.', description: 'Try short workplace simulations. Get specific feedback. Build confidence with every attempt.', action: 'Enter the practice lab', panel: 'practice' as Panel},
  ];
  return <div className="career-studio">
    <aside className="cs-sidebar">
      <button className="cs-brand" onClick={() => setPanel(null)} aria-label="Aiversecity home"><span className="cs-brand-mark"><Sparkles size={21}/></span>Aiversecity</button>
      <div className="cs-brand-sub">A future that fits you</div>
      <div className="cs-nav-label cs-mono">YOUR WORKSPACE</div>
      <nav className="cs-nav" aria-label="Main navigation">
        <button className="cs-active" onClick={() => setPanel(null)} aria-current="page"><Home size={17}/>Overview<span className="cs-nav-dot"/></button>
        <button onClick={() => open('profiles')}><ScanFace size={17}/>My profiles</button>
        <button onClick={() => open('matches')}><Target size={17}/>Role matches</button>
        <button onClick={() => open('practice')}><FlaskConical size={17}/>Practice lab</button>
      </nav>
      <div className="cs-sidebar-bottom">
        <div className="cs-side-note"><Globe2 size={23}/><strong>Skills for a better future.</strong><p>Find your place in a changing world of work. Make your next move count.</p></div>
        <div className="cs-credit">Built for SDC XMUM Hackathon<br/><span className="cs-mono">XMUM · MALAYSIA</span></div>
      </div>
    </aside>
    <div className="cs-workspace">
      <header className="cs-topbar"><div className="cs-breadcrumb">Workspace<span>/</span><strong>Overview</strong></div><button className="cs-profile" onClick={() => open('profiles')}><span className="cs-avatar">{profile ? profile.name.slice(0,2).toUpperCase() : 'AV'}</span>{profile ? profile.name : 'Choose your profile'}<ChevronDown size={12}/></button></header>
      <main className="cs-main">
        <div className="cs-intro cs-enter"><div><div className="cs-mono">YOUR CAREER OBSERVATORY</div><h1>Your potential. A clearer direction.</h1><p>The world of work is changing. Let’s find where you fit next.</p></div><div className="cs-status cs-mono"><i/>BUILT FOR WHAT’S NEXT</div></div>
        <section className="cs-hero cs-enter">
          <div className="cs-hero-copy"><div className="cs-mono">HUMAN SKILLS. NEW POSSIBILITIES.</div><h2>The future of work<br/>has a place <em>for you.</em></h2><p>Turn what you know into what comes next. Discover your strengths, explore resilient roles, and build the skills to get there.</p><div className="cs-actions"><button className="cs-primary" onClick={() => open('profile')}>{profile ? 'Continue your journey' : 'Map my potential'}<ArrowUpRight size={16}/></button><button className="cs-text-button" onClick={() => open('profiles')}>{profile ? 'Switch profile' : 'I already have a profile'}<ArrowRight size={14}/></button></div></div>
          <StudioOrbit/>
        </section>
        <div className="cs-signals"><span><Check size={14}/>Grounded in the ESCO skills taxonomy</span><span><Globe2 size={14}/>Connected to the UN SDGs</span><span><ScanFace size={14}/>Your skills, not just your job title</span></div>
        <section>
          <div className="cs-section-heading"><div><div className="cs-mono">A LITTLE CLARITY GOES A LONG WAY</div><h2>Your next chapter, in three steps.</h2></div><span className="cs-pace cs-mono">AT YOUR OWN PACE</span></div>
          <div className="cs-cards">{cards.map(({icon: Icon, number, title, description, action, panel: destination}) => <button className="cs-card" key={number} onClick={() => open(destination)}><div className="cs-card-top"><span className="cs-card-icon"><Icon size={18}/></span><span className="cs-mono">{number}</span></div><h3>{title}</h3><p>{description}</p><span className="cs-card-link">{action}<ArrowRight size={14}/></span></button>)}</div>
        </section>
        <div className="cs-insights"><section className="cs-insight"><div className="cs-bars" aria-hidden="true"><i/><i/><i/></div><div><div className="cs-mono">MORE THAN A MATCH SCORE</div><h3>A career that moves the world forward.</h3><p>See how your potential roles contribute to the UN Sustainable Development Goals. Good work can do good, too.</p></div></section><section className="cs-insight"><Sparkles size={33} strokeWidth={1.3}/><div><h3>AI changes jobs. Not your worth.</h3><p>Compare moderate and fast AI-disruption scenarios. These are signals to help you plan—not predictions about your limits.</p></div></section></div>
        <footer className="cs-footer"><span>Aiversecity — human potential, mapped for what’s next.</span><span>ESCO-powered skills · UN SDG-aligned · No account needed</span></footer>
      </main>
    </div>
    {panel && <div className="cs-overlay" onClick={() => setPanel(null)}><section className="cs-dialog cs-enter" role="dialog" aria-modal="true" aria-labelledby="cs-dialog-title" onClick={event => event.stopPropagation()} onKeyDown={event => {
      if (event.key !== 'Tab') return;
      const elements = event.currentTarget.querySelectorAll<HTMLElement>('button, input, textarea');
      const first = elements[0]; const last = elements[elements.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    }}>
      <button ref={closeRef} className="cs-close" onClick={() => setPanel(null)} aria-label="Close dialog"><X size={16}/></button>
      <div className="cs-mono">{panel === 'practice' ? 'THE PRACTICE LAB' : panel === 'matches' ? 'POSSIBLE NEXT CHAPTERS' : 'YOUR STARTING POINT'}</div>
      <h2 id="cs-dialog-title">{panel === 'profile' ? 'Let’s start with you.' : panel === 'profiles' ? 'A space for your potential.' : panel === 'matches' ? 'Your skills can go places.' : 'Small practice. Real confidence.'}</h2>
      {panel === 'profile' && <form onSubmit={event => { event.preventDefault(); setProfile({name: name.trim(), skills: skills.trim()}); setPanel('profiles'); }}>
        <p>You’re more than a job title. Tell us what you bring to the table.</p>
        <label>Your name<input required value={name} onChange={event => setName(event.target.value)} placeholder="How should we call you?" autoComplete="name"/></label>
        <label>Your skills<textarea required value={skills} onChange={event => setSkills(event.target.value)} placeholder="For example: research, data analysis, helping people…"/></label>
        <button className="cs-primary" type="submit">{profile ? 'Save my profile' : 'Create my profile'}<ArrowRight size={16}/></button><p style={{fontSize:10, marginTop:14}}>Design preview · Your profile stays in this session.</p>
      </form>}
      {panel === 'profiles' && (profile ? <><p>Your next chapter starts with the strengths you already have.</p><div className="cs-saved"><ScanFace size={28}/><div><strong>{profile.name}</strong><small>{profile.skills}</small></div></div><div className="cs-actions"><button className="cs-primary" onClick={() => open('matches')}>Explore directions<ArrowRight size={16}/></button><button className="cs-text-button" onClick={() => {setName(profile.name);setSkills(profile.skills);open('profile');}}>Edit profile</button><button className="cs-text-button" onClick={() => {if(window.confirm('Delete this session’s profile?')){setProfile(null);setName('');setSkills('');}}}>Delete</button></div></> : <><p>No profiles yet. Add your strengths, experiences, and the things you enjoy. There’s no perfect starting point—just yours.</p><button className="cs-primary" onClick={() => open('profile')}>Build your first profile<ArrowRight size={16}/></button></>)}
      {panel === 'matches' && <><p>{profile ? `Curious where your strengths could take you, ${profile.name}?` : 'Build a profile to find directions grounded in your own skills.'} These sample directions show what you can explore.</p><div className="cs-role"><strong>Learning experience designer</strong><p>Connect research, communication, and creative problem-solving to make learning work for people.</p></div><div className="cs-role"><strong>Sustainability analyst</strong><p>Turn evidence into decisions. Combine data skills with a drive to make a meaningful difference.</p></div><p style={{fontSize:10, marginTop:16}}>Illustrative roles only. Live ESCO matching is not connected in this design preview.</p><button className="cs-primary" onClick={() => open('profile')}>{profile ? 'Refine my skills' : 'Map my skills first'}<ArrowRight size={16}/></button></>}
      {panel === 'practice' && <><p>A team is introducing an AI assistant to handle customer questions. Some colleagues worry their expertise will be overlooked.</p><div className="cs-role"><strong>Your challenge</strong><p>Write a short plan that puts human expertise at the center while exploring what AI could help with.</p></div>{submitted ? <div className="cs-saved"><Check size={25}/><div><strong>Reflection captured.</strong><small>Review your plan: Does it name a human responsibility, a small test, and a way to listen to the team? This is a self-reflection, not an AI assessment.</small></div></div> : <form onSubmit={event => {event.preventDefault();setSubmitted(true);}}><label>Your approach<textarea required value={answer} onChange={event => setAnswer(event.target.value)} placeholder="I’d start by talking to the team about…"/></label><button className="cs-primary" type="submit">Reflect on my approach<ArrowRight size={16}/></button></form>}{submitted && <button className="cs-text-button" style={{marginTop:18}} onClick={() => setSubmitted(false)}>Keep working on my response<ArrowRight size={14}/></button>}</>}
    </section></div>}
  </div>;
}
