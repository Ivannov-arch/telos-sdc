"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { createProfileFromForm, createProfileFromPdf } from "@/lib/api";
import { useActiveProfile } from "@/components/shell";
import { ErrorState, Icon, PageIntro } from "@/components/ui";

export default function NewProfilePage() {
  const [mode, setMode] = useState<"form" | "pdf">("form");
  const [hard, setHard] = useState("");
  const [soft, setSoft] = useState("");
  const [years, setYears] = useState("0");
  const [summary, setSummary] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const { setActive } = useActiveProfile();
  const router = useRouter();
  const parse = (text: string) => [...new Set(text.split(/[,;\n]/).map((s) => s.trim()).filter(Boolean))];
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    if (mode === "pdf" && (!file || !file.name.toLowerCase().endsWith(".pdf") || file.size > 5 * 1024 * 1024 || file.size === 0)) { setError("Choose a non-empty PDF file, no larger than 5 MB."); return; }
    if (mode === "form" && parse(hard).length + parse(soft).length === 0) { setError("Tell us at least one skill so we have a place to start."); return; }
    if (mode === "form" && (!Number.isFinite(Number(years)) || Number(years) < 0)) { setError("Experience must be a valid number of years, starting at zero."); return; }
    setSaving(true);
    try {
      const profile = mode === "pdf" ? await createProfileFromPdf(file!) : await createProfileFromForm({ hard_skills: parse(hard), soft_skills: parse(soft), experience_years: Number(years), raw_text: summary.trim() || null });
      setActive(profile.id);
      router.push(`/profile/${encodeURIComponent(profile.id)}`);
    } catch (err) { setError(err instanceof Error ? err.message : "Your profile couldn’t be created. Please try again."); setSaving(false); }
  }
  return <>
    <PageIntro eyebrow="01 / MAP YOUR POTENTIAL" title="You bring more than a job title." description="Tell us what you can do. We’ll connect your skills to the ESCO taxonomy, a shared language for careers." />
    <div className="two-col reveal"><section className="panel">
      <div className="tabs" role="tablist" aria-label="Profile creation method"><button type="button" role="tab" aria-selected={mode === "form"} className={mode === "form" ? "selected" : ""} onClick={() => { setMode("form"); setError(null); }} disabled={saving}>Enter my skills</button><button type="button" role="tab" aria-selected={mode === "pdf"} className={mode === "pdf" ? "selected" : ""} onClick={() => { setMode("pdf"); setError(null); }} disabled={saving}>Upload a CV</button></div>
      <form onSubmit={submit}><fieldset disabled={saving} style={{ border: 0, padding: 0, margin: 0 }}>
        {mode === "form" ? <><h2>A picture of your strengths.</h2><p className="helper">Technical abilities, people skills, and everything you’ve learned along the way.</p><div className="field"><label htmlFor="hard">Hard skills</label><textarea id="hard" value={hard} onChange={(e) => setHard(e.target.value)} placeholder="Python, data analysis, project management" /><small>Separate skills with commas or put each on a new line.</small></div><div className="field"><label htmlFor="soft">Soft skills</label><textarea id="soft" value={soft} onChange={(e) => setSoft(e.target.value)} placeholder="Critical thinking, teamwork, communication" /></div><div className="field"><label htmlFor="years">Years of experience</label><input id="years" type="number" min="0" step="0.5" required value={years} onChange={(e) => setYears(e.target.value)} /><small>Just starting out? Zero is a perfectly good starting point.</small></div><div className="field"><label htmlFor="summary">A little context <span style={{ fontWeight: 400, color: "var(--muted)" }}>(optional)</span></label><textarea id="summary" value={summary} onChange={(e) => setSummary(e.target.value)} placeholder="Tell us about your projects, experience, or what you enjoy working on." /></div></> : <><h2>Let your experience do the talking.</h2><p className="helper" style={{ marginBottom: 23 }}>We’ll extract your skills and experience from your CV.</p><div className="upload-zone"><Icon name="upload" size={30} /><h3>Your next chapter starts here.</h3><p className="helper">PDF format · Maximum 5 MB</p><input aria-label="Choose CV PDF" type="file" accept=".pdf,application/pdf" onChange={(e) => { setFile(e.target.files?.[0] ?? null); setError(null); }} />{file && <p className="helper" style={{ marginTop: 13 }}>{file.name} · {(file.size / 1024 / 1024).toFixed(2)} MB</p>}</div></>}
        {error && <ErrorState message={error} />}<div className="actions"><button type="submit" className="btn">{saving ? "Resolving your skills…" : "Create my skills profile"}{!saving && <Icon size={16} />}</button></div>
        {saving && <div role="status" style={{ marginTop: 20 }}><div className="skeleton short" style={{ height: 8, marginBottom: 10 }} /><p className="helper">Matching your skills to ESCO. This can take a little while.</p></div>}
      </fieldset></form>
    </section><aside className="stack"><section className="panel" style={{ background: "var(--featured-bg)" }}><div className="eyebrow" style={{ marginBottom: 15 }}>FROM EXPERIENCE TO POSSIBILITY</div><h2>Here’s what happens next.</h2><ol className="number-list"><li>Your skills are resolved against ESCO, with a confidence score for each match.</li><li>Your profile is compared with roles under different AI-disruption scenarios.</li><li>You get a clearer view of your skills gaps and a place to practise.</li></ol></section><section className="panel"><Icon name="profile" size={22} /><h3 style={{ marginTop: 13, fontSize: 16 }}>No account. A little care.</h3><p style={{ fontSize: 12, marginTop: 10 }}>This shared demo has no private accounts. Don’t upload sensitive personal information. You can enter only your skills instead.</p></section></aside></div>
  </>;
}
