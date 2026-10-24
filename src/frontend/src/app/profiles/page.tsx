"use client";

import Link from "next/link";
import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { listProfiles } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { useActiveProfile } from "@/components/shell";
import { dateLabel, Empty, ErrorState, Icon, Loading, PageIntro, profileName } from "@/components/ui";

export default function ProfilesPage() {
  const resource = useResource(useCallback(() => listProfiles(), []));
  const { activeId, setActive } = useActiveProfile();
  const router = useRouter();
  const [search, setSearch] = useState("");
  const profiles = resource.data?.profiles.filter((profile) => `${profile.id} ${profile.hard_skills.map((s) => s.label ?? s.skill_name).join(" ")} ${profile.soft_skills.map((s) => s.label ?? s.skill_name).join(" ")}`.toLowerCase().includes(search.toLowerCase()));
  function choose(id: string) {
    setActive(id);
    const next = new URLSearchParams(window.location.search).get("next");
    router.push(next === "matches" ? `/match/${id}` : `/profile/${id}`);
  }
  return <>
    <PageIntro eyebrow="01 / YOUR STARTING POINT" title="Every path starts with a person." description="Choose a skills profile to continue, or create a new one. Your selection follows you across the workspace."><Link href="/profile/new" className="btn"><Icon name="plus" size={15} />New profile</Link></PageIntro>
    <div className="notice" style={{ margin: "0 0 25px" }}>This is a shared hackathon workspace, with no sign-in. Profiles are visible to other visitors. Please avoid sensitive personal information.</div>
    {resource.loading ? <Loading label="Finding your starting points…" /> : resource.error ? <ErrorState message={resource.error} retry={resource.retry} /> : resource.data?.profiles.length === 0 ? <Empty title="A blank page. Plenty of possibility." description="There aren’t any profiles here yet. Add your skills or upload a CV to begin mapping your next move." icon="profile"><Link href="/profile/new" className="btn">Create the first profile<Icon name="plus" size={15} /></Link></Empty> : <>
      <div className="field" style={{ marginBottom: 22, marginTop: 0 }}><label htmlFor="profile-search">Find a profile by skill or reference</label><input id="profile-search" type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Try “Python”, “communication”, or a profile reference" /></div>
      <div className="profile-grid stagger">{profiles?.map((profile) => <article className="panel profile-card" key={profile.id}><div className="meta-row"><span className="avatar"><Icon name="profile" size={16} /></span><span className={`pill ${activeId === profile.id ? "accent" : ""}`}>{activeId === profile.id ? "ACTIVE PROFILE" : profile.source_type === "pdf" ? "FROM CV" : "FROM SKILLS FORM"}</span></div><h2>{profileName(profile.id)}</h2><div className="meta-row"><span>{profile.experience_years} years of experience</span><span>{dateLabel(profile.created_at)}</span></div><div className="pills">{[...profile.hard_skills, ...profile.soft_skills].slice(0, 5).map((skill, i) => <span className="pill" key={i}>{skill.label ?? skill.skill_name}</span>)}{profile.hard_skills.length + profile.soft_skills.length > 5 && <span className="pill">+{profile.hard_skills.length + profile.soft_skills.length - 5} more</span>}</div><button onClick={() => choose(profile.id)} className="btn secondary" style={{ marginTop: "auto" }}>Continue with this profile<Icon size={15} /></button></article>)}</div>
      {profiles?.length === 0 && <Empty title="No profiles on this frequency." description="Try another skill or clear the search to see all available profiles." icon="profile"><button className="btn secondary" onClick={() => setSearch("")}>Clear search</button></Empty>}
    </>}
  </>;
}
