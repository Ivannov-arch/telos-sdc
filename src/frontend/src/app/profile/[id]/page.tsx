"use client";

import Link from "next/link";
import { useCallback, useEffect } from "react";
import { useParams } from "next/navigation";
import { getProfile, type SkillEntry } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { useActiveProfile } from "@/components/shell";
import { ErrorState, Icon, Loading, Meter, PageIntro, profileName } from "@/components/ui";

function Skills({ title, skills }: { title: string; skills: SkillEntry[] }) {
  return <section className="panel"><div className="meta-row"><h2>{title}</h2><span className="pill">{skills.length} SKILLS</span></div>{skills.length === 0 ? <p className="helper">No {title.toLowerCase()} were identified in this profile.</p> : skills.map((skill, i) => <div key={i} className="skill-row"><div className="meta-row"><strong>{skill.label ?? skill.skill_name}</strong><span>{Math.round(skill.confidence_score * 100)}% confidence</span></div><small>{skill.esco_id ? `ESCO match · Entered as “${skill.skill_name}”` : "No ESCO match resolved yet"}</small><Meter value={skill.confidence_score} />{skill.esco_id && <details style={{ marginTop: 9 }}><summary className="helper" style={{ cursor: "pointer" }}>Taxonomy reference</summary><p className="helper" style={{ overflowWrap: "anywhere" }}>{skill.esco_id}</p></details>}</div>)}<p className="helper" style={{ marginTop: 18 }}>Confidence describes the taxonomy match—not how good you are at this skill.</p></section>;
}
export default function ProfileDetail() {
  const { id } = useParams<{ id: string }>();
  const { setActive } = useActiveProfile();
  const resource = useResource(useCallback(() => getProfile(id), [id]));
  useEffect(() => { if (resource.data) setActive(resource.data.id); }, [resource.data, setActive]);
  const profile = resource.data;
  return <><PageIntro eyebrow="01 / YOUR SKILLS, MAPPED" title={profile ? profileName(profile.id) : "Your skills profile"} description="A clearer picture of what you bring, and a starting point for where to go next."><Link href="/profiles" className="btn secondary">Switch profile<Icon name="chevron" size={15} /></Link></PageIntro>
    {resource.loading ? <Loading label="Connecting your skills…" /> : resource.error ? <ErrorState message={resource.error} retry={resource.retry} /> : profile && <div className="reveal">
      <div className="pills"><span className="pill accent">ACTIVE PROFILE</span><span className="pill">{profile.source_type === "pdf" ? "CV UPLOAD" : "SKILLS FORM"}</span><span className="pill">{profile.has_dense_vector ? "SEMANTIC VECTOR READY" : "SEMANTIC VECTOR NOT AVAILABLE"}</span></div>
      <div className="stat-list"><div><strong>{profile.hard_skills.length}</strong><small>Hard skills mapped</small></div><div><strong>{profile.soft_skills.length}</strong><small>Soft skills mapped</small></div><div><strong>{profile.experience_years}<span style={{ fontSize: 13 }}> years</span></strong><small>Professional experience</small></div></div>
      {profile.message && <p className="notice" style={{ margin: "0 0 24px" }}>{profile.message}</p>}
      <div className="two-col"><div className="stack"><Skills title="Hard skills" skills={profile.hard_skills} /><Skills title="Soft skills" skills={profile.soft_skills} /></div><aside className="stack"><section className="panel" style={{ background: "#e8efdc" }}><Icon name="target" size={26} /><h2 style={{ marginTop: 17 }}>Put your strengths in perspective.</h2><p style={{ fontSize: 12 }}>Explore roles that fit your skills. Compare scenarios and see the gaps you can work on.</p><div className="actions"><Link className="btn" href={`/match/${id}`}>Find my role matches<Icon size={15} /></Link></div></section><section className="panel"><Icon name="practice" size={24} /><h2 style={{ marginTop: 16 }}>Build confidence by doing.</h2><p style={{ fontSize: 12 }}>Short workplace tasks. Transparent rubrics. Feedback you can use.</p><div className="actions"><Link className="text-link" href={`/simulate?profile=${encodeURIComponent(id)}`}>Go to practice lab<Icon size={15} /></Link></div></section><p className="helper" style={{ overflowWrap: "anywhere" }}>Profile reference: {id}<br />{profile.has_dense_vector ? "A semantic embedding is available to support skill-based matching." : "No semantic embedding is stored for this profile. Matching availability depends on the backend."}</p></aside></div>
    </div>}
  </>;
}
