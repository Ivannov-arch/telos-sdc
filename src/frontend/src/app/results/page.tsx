"use client";

import Link from "next/link";
import { missionById } from "@/lib/missions";
import { useSavedSessions } from "@/lib/sessions";
import { dateLabel, Empty, Icon, PageIntro } from "@/components/ui";

export default function ResultsPage() {
  const sessions = useSavedSessions();
  return <>
    <PageIntro eyebrow="YOUR RESULTS" title="Every run, in one place." description="Simulations you’ve played in this browser. Open one to continue or revisit what it showed."><Link className="btn" href="/play">New simulation<Icon name="plus" size={15} /></Link></PageIntro>
    {!sessions.length ? <Empty title="No simulations yet." description="Play a three-minute crisis mission and your results will appear here." icon="practice"><Link className="btn lime" href="/play">Start the simulation<Icon size={15} /></Link></Empty>
      : <div className="profile-grid stagger">{sessions.map((s) => { const m = missionById(s.mission); return <Link key={s.id} href={`/play/${encodeURIComponent(s.id)}`} className="panel profile-card"><div className="pills"><span className="pill accent">{m?.code ?? "MISSION"}</span>{m && <span className="pill">{m.sdg}</span>}</div><h2>{m?.title ?? "Crisis simulation"}</h2><div className="pills">{s.skills.slice(0, 5).map((k) => <span key={k} className="pill">{k}</span>)}</div><div className="meta-row"><span>{dateLabel(s.startedAt)}</span><span className="text-link">Open<Icon size={14} /></span></div></Link>; })}</div>}
  </>;
}
