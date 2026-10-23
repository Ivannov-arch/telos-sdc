import { useEffect, useState } from 'react';
import { ArrowRight, ArrowUpRight, Check, ChevronDown, Compass, Globe2, House, MoveUpRight, Orbit, Sparkles, Target, UsersRound, X, FlaskConical } from 'lucide-react';
import './career-atelier.css';

type Panel = 'profile' | 'profiles' | 'matches' | 'practice' | null;

function CareerConstellation() {
  return <div className="ca-art" aria-label="A printed constellation connecting your skills, future roles, and meaningful impact">
    <svg viewBox="0 0 470 365" fill="none" aria-hidden="true">
      <defs><pattern id="atelier-hatch" width="5" height="5" patternTransform="rotate(35)" patternUnits="userSpaceOnUse"><path d="M0 0V5" stroke="#e4af7d" strokeWidth=".6" opacity=".35"/></pattern></defs>
      <circle cx="240" cy="177" r="143" fill="url(#atelier-hatch)" />
      <circle cx="240" cy="177" r="143" stroke="#edbf8d" strokeOpacity=".5"/>
      <circle cx="240" cy="177" r="132" stroke="#e1a777" strokeOpacity=".5" strokeDasharray="1 5"/>
      <circle cx="240" cy="177" r="106" stroke="#f0c9a1" strokeOpacity=".55"/>
      <ellipse cx="240" cy="177" rx="165" ry="63" transform="rotate(-31 240 177)" stroke="#f0c9a1" strokeOpacity=".6"/>
      <ellipse cx="240" cy="177" rx="76" ry="148" transform="rotate(-31 240 177)" stroke="#f0c9a1" strokeOpacity=".5"/>
      <path d="M240 28V326M90 177H390M135 72L345 282M136 281L344 73" stroke="#eeb484" strokeOpacity=".35"/>
      {Array.from({length:24},(_,i)=>{const a=i*Math.PI/12;return <path key={i} d={`M${240+Math.cos(a)*138} ${177+Math.sin(a)*138} L${240+Math.cos(a)*143} ${177+Math.sin(a)*143}`} stroke="#ecc091" strokeOpacity=".75"/>;})}
      <path d="M137 80L240 177L375 155M240 177L179 285" stroke="#f1c89a" strokeDasharray="4 4"/>
      <circle cx="240" cy="177" r="44" fill="#a44732" stroke="#edbc83"/>
      <circle cx="240" cy="177" r="34" fill="#edc588"/>
      <path d="M240 151L246 170L266 177L246 184L240 203L233 184L214 177L233 170Z" fill="#9b4633"/>
      <circle cx="137" cy="80" r="6" fill="#f2d7ac"/><circle cx="375" cy="155" r="5" fill="#f2d7ac"/><circle cx="179" cy="285" r="5" fill="#f2d7ac"/>
      <path d="M327 57V69M321 63H333M115 231V241M110 236H120" stroke="#edc39a"/>
      <text x="236" y="18" fontFamily="serif" fontSize="9" fill="#edc39a">N</text>
      <text x="403" y="181" fontFamily="serif" fontSize="9" fill="#edc39a">E</text>
      <text x="236" y="346" fontFamily="serif" fontSize="9" fill="#edc39a">S</text>
      <text x="65" y="181" fontFamily="serif" fontSize="9" fill="#edc39a">W</text>
    </svg>
    <div className="ca-tag one"><UsersRound size={14}/>Your unique skills</div>
    <div className="ca-tag two"><Target size={14}/>Future-fit roles</div>
    <div className="ca-tag three"><Globe2 size={14}/>Meaningful impact</div>
    <div className="ca-artcaption ca-mono"><span>Human potential, connected.</span><span>Fig. 01 / ∞</span></div>
  </div>;
}

export default function CareerAtelier() {
  const [panel,setPanel] = useState<Panel>(null);
  const [name,setName] = useState('');
  const [profile,setProfile] = useState('');
  const [saved,setSaved] = useState(false);
  const [started,setStarted] = useState(false);
  useEffect(()=>{ if(!panel)return; const close=(e:KeyboardEvent)=>{if(e.key==='Escape')setPanel(null);}; window.addEventListener('keydown',close); return()=>window.removeEventListener('keydown',close); },[panel]);
  const steps = [
    {icon:UsersRound,step:'01 / Discover',title:'Start with what you know.',text:'Upload your CV or tell us your skills. We’ll map them to a shared language of work.',link:'Build your profile',panel:'profile' as Panel},
    {icon:Target,step:'02 / Explore',title:'See where you could go.',text:'Explore role matches, understand AI’s impact, and see exactly which skills to build next.',link:'Explore role matches',panel:'matches' as Panel},
    {icon:FlaskConical,step:'03 / Grow',title:'Make progress, in practice.',text:'Try short workplace simulations. Get specific feedback. Build confidence with every attempt.',link:'Enter the practice lab',panel:'practice' as Panel},
  ];
  return <div className="career-atelier">
    <aside className="ca-sidebar">
      <button className="ca-brand" onClick={()=>setPanel(null)} aria-label="Aiversecity home"><span className="ca-brandmark"><Sparkles size={30} strokeWidth={1.3}/></span>Aiversecity<span style={{color:'#a44732',fontSize:16,marginLeft:-6}}>.</span></button>
      <div className="ca-sub">A future that fits you</div>
      <div className="ca-navlabel ca-mono">Your workspace</div>
      <nav className="ca-nav" aria-label="Main navigation">
        <button className={!panel?'active':''} onClick={()=>setPanel(null)}><House size={17} strokeWidth={1.5}/>Overview<span className="ca-dot"/></button>
        <button className={panel==='profiles'||panel==='profile'?'active':''} onClick={()=>setPanel('profiles')}><UsersRound size={17} strokeWidth={1.5}/>My profiles</button>
        <button className={panel==='matches'?'active':''} onClick={()=>setPanel('matches')}><Target size={17} strokeWidth={1.5}/>Role matches</button>
        <button className={panel==='practice'?'active':''} onClick={()=>setPanel('practice')}><FlaskConical size={17} strokeWidth={1.5}/>Practice lab</button>
      </nav>
      <div className="ca-sidebottom"><div className="ca-sidenote"><Globe2 size={24} strokeWidth={1.2}/><div><strong>Skills for a<br/>better future.</strong><p>Find your place in a changing world of work. Make your next move count.</p></div></div><div className="ca-credit">Built for SDC XMUM Hackathon<br/><span className="ca-mono" style={{fontSize:8}}>XMUM · Malaysia</span></div></div>
    </aside>
    <div className="ca-workspace">
      <header className="ca-topbar"><div className="ca-crumb">Workspace<span>/</span><strong>Overview</strong></div><button className="ca-profile" onClick={()=>setPanel('profiles')}><span className="ca-avatar">{profile?profile.slice(0,2).toUpperCase():'av'}</span>{profile||'Choose your profile'}<ChevronDown size={12}/></button></header>
      <main className="ca-main">
        <section className="ca-intro"><div><div className="ca-mono">Your career observatory</div><h1 className="ca-serif">Your potential. A clearer direction.</h1><p>The world of work is changing. Let’s find where you fit next.</p></div><div className="ca-status ca-mono"><span className="ca-dot"/>Built for what’s next</div></section>
        <section className="ca-hero"><div className="ca-herocopy"><div className="ca-mono"><span className="ca-dot"/>Human skills. New possibilities.</div><h2 className="ca-serif">The future of work<br/>has a place <em>for you.</em></h2><p>Turn what you know into what comes next. Discover your strengths, explore resilient roles, and build the skills to get there.</p><div className="ca-actions"><button className="ca-primary" onClick={()=>setPanel('profile')}>{profile?'Continue your journey':'Map my potential'}<ArrowRight size={15}/></button><button className="ca-textbtn" onClick={()=>setPanel('profiles')}>I already have a profile<ArrowUpRight size={13}/></button></div></div><CareerConstellation/></section>
        <div className="ca-signals"><span><Check size={14}/>Grounded in the ESCO skills taxonomy</span><span><Globe2 size={14}/>Connected to the UN SDGs</span><span><UsersRound size={14}/>Your skills, not just your job title</span></div>
        <section><div className="ca-sectionhead"><div><div className="ca-mono">A little clarity goes a long way</div><h2 className="ca-serif">Your next chapter, in three steps.</h2></div><span className="ca-pill ca-mono">At your own pace</span></div>
          <div className="ca-journey">{steps.map(({icon:Icon,step,title,text,link,panel:destination})=><button className="ca-card" key={step} onClick={()=>setPanel(destination)}><div className="ca-cardtop"><Icon className="ca-icon" size={27} strokeWidth={1.25}/><span className="ca-step ca-mono">{step}</span></div><h3>{title}</h3><p>{text}</p><span className="ca-cardlink">{link}<ArrowRight size={13}/></span></button>)}</div>
        </section>
        <div className="ca-insights"><section className="ca-insight"><div className="ca-bars" aria-hidden="true"><i/><i/><i/></div><div><div className="ca-mono">More than a match score</div><h3>A career that moves the world forward.</h3><p>See how your potential roles contribute to the UN Sustainable Development Goals. Good work can do good, too.</p></div></section><section className="ca-insight"><Orbit size={39} strokeWidth={1} style={{color:'#aa7153',flexShrink:0}}/><div><h3>AI changes jobs. Not your worth.</h3><p>Compare moderate and fast AI-disruption scenarios. These are signals to help you plan—not predictions about your limits.</p></div></section></div>
        <footer className="ca-footer"><span>Aiversecity — human potential, mapped for what’s next.</span><span>ESCO-powered skills · UN SDG-aligned · No account needed</span></footer>
      </main>
    </div>
    {panel&&<div className="ca-overlay" onClick={()=>setPanel(null)}><section className={`ca-dialog${panel==='practice'?' ca-dialog-sky':''}`} role="dialog" aria-modal="true" aria-label={panel==='practice'?'Practice lab':'Your career journey'} onClick={e=>e.stopPropagation()}><button className="ca-close" onClick={()=>setPanel(null)} aria-label="Close dialog"><X size={19}/></button>
      <div className="ca-mono" style={{color:panel==='practice'?'#376782':'#a44732'}}>Your next chapter</div>
      {panel==='profile'&&<><h2 className="ca-serif">{saved?'A good place to begin.':'Start with your story.'}</h2>{saved?<><p>Your profile for {profile} is ready for this preview. Your next step is to add skills and explore the directions they could take you.</p><div className="ca-actions"><button className="ca-primary" onClick={()=>setPanel('matches')}>Explore directions<ArrowRight size={15}/></button></div></>:<form onSubmit={e=>{e.preventDefault();setProfile(name.trim());setSaved(true);}}><p>Every career starts with a person, not a job title. What should we call you?</p><label htmlFor="atelier-name">Your name</label><input id="atelier-name" autoFocus required value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Amira Tan"/><button className="ca-primary" type="submit">Create preview profile<ArrowRight size={15}/></button><p style={{fontSize:10,marginTop:15}}>A local design preview. No account or personal data is sent.</p></form>}</>}
      {panel==='profiles'&&<><h2 className="ca-serif">Your journey, your pace.</h2>{profile?<><div className="ca-modalrow"><UsersRound size={20}/>{profile}<span>Active profile</span></div><div className="ca-actions"><button className="ca-primary" onClick={()=>setPanel('matches')}>Continue exploring<ArrowRight size={15}/></button></div></>:<><p>You haven’t created a profile in this preview yet. Start with your name, then find the possibilities in what you already know.</p><div className="ca-actions"><button className="ca-primary" onClick={()=>setPanel('profile')}>Build your profile<ArrowRight size={15}/></button></div></>}</>}
      {panel==='matches'&&<><Compass size={35} strokeWidth={1.2} style={{color:'#a44732',marginTop:24}}/><h2 className="ca-serif">Possibility starts with you.</h2><p>Real role matches need your skills profile. In the full experience, we connect your strengths to roles using the ESCO taxonomy, with AI-impact signals and practical next steps.</p><div className="ca-actions"><button className="ca-primary" onClick={()=>{setSaved(false);setPanel('profile');}}>Start with your profile<MoveUpRight size={15}/></button></div><p style={{fontSize:10,marginTop:16}}>Role matching is not connected in this design preview.</p></>}
      {panel==='practice'&&<><h2 className="ca-serif">{started?'Make your thinking visible.':'A little practice. Real confidence.'}</h2><p>{started?'A team is choosing between two projects: one with quick revenue, the other with longer-term social impact. What three questions would you ask before making a recommendation?':'Try a short workplace scenario. There’s no perfect starting point—just an opportunity to notice how you think.'}</p>{started?<><label htmlFor="atelier-reflection">Your first thoughts</label><input id="atelier-reflection" placeholder="I would start by asking…" /><p style={{fontSize:10}}>Reflection only. AI assessment is unavailable in this preview.</p></>:<div className="ca-actions"><button className="ca-primary" onClick={()=>setStarted(true)}>Try a scenario<ArrowRight size={15}/></button></div>}</>}
    </section></div>}
  </div>;
}
