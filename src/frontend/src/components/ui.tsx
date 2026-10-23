"use client";

import Link from "next/link";
import type { ReactNode } from "react";

export function Icon({ name = "arrow", size = 18 }: { name?: string; size?: number }) {
  const paths: Record<string, ReactNode> = {
    arrow: <><path d="M4 12h15M13 6l6 6-6 6" /></>,
    home: <><path d="m3 10 9-7 9 7v10H3z" /><path d="M9 20v-7h6v7" /></>,
    profile: <><circle cx="12" cy="8" r="4" /><path d="M4 21v-2a8 8 0 0 1 16 0v2" /></>,
    target: <><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1" /></>,
    practice: <><path d="m13 2-9 12h7l-1 8 10-13h-7z" /></>,
    plus: <path d="M12 5v14M5 12h14" />,
    check: <path d="m5 12 4 4L19 6" />,
    upload: <><path d="M12 16V3m-5 5 5-5 5 5M4 16v5h16v-5" /></>,
    globe: <><circle cx="12" cy="12" r="9" /><ellipse cx="12" cy="12" rx="4" ry="9" /><path d="M3 12h18" /></>,
    chevron: <path d="m8 10 4 4 4-4" />,
    back: <path d="M20 12H5m6-6-6 6 6 6" />,
    spark: <><path d="m12 3 2.6 6.4L21 12l-6.4 2.6L12 21l-2.6-6.4L3 12l6.4-2.6z" /></>,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 6v6l4 2" /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name] ?? paths.arrow}</svg>;
}
export function PageIntro({ eyebrow, title, description, children }: { eyebrow: string; title: string; description: string; children?: ReactNode }) {
  return <header className="page-intro reveal"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{description}</p></div>{children}</header>;
}
export function Loading({ label = "Reading the signals…" }: { label?: string }) {
  return <div role="status" aria-live="polite"><p className="eyebrow" style={{ marginBottom: 20 }}>{label}</p><div className="skeleton short" /><div className="skeleton" /><div className="skeleton" /></div>;
}
export function ErrorState({ message, retry }: { message: string; retry?: () => void }) {
  return <div className="error" role="alert"><strong>A small interruption. Not a dead end.</strong><p>{message}</p>{retry && <button type="button" className="btn secondary" onClick={retry}>Try again <Icon name="arrow" size={14} /></button>}</div>;
}
export function Empty({ title, description, icon = "target", children }: { title: string; description: string; icon?: string; children?: ReactNode }) {
  return <section className="empty reveal"><div className="empty-icon"><Icon name={icon} size={29} /></div><h2>{title}</h2><p>{description}</p>{children && <div className="actions">{children}</div>}</section>;
}
export function NeedProfile() {
  return <Empty title="Your next chapter starts with you." description="Choose a profile or add your skills first. We’ll keep it selected as you explore roles and practise." icon="profile"><Link className="btn" href="/profile/new">Create a profile <Icon name="plus" size={15} /></Link><Link className="btn secondary" href="/profiles">Choose existing profile</Link></Empty>;
}
export function Meter({ value }: { value: number }) {
  return <div className="meter" role="meter" aria-label="Score" aria-valuenow={Math.round(value * 100)} aria-valuemin={0} aria-valuemax={100}><span style={{ width: `${Math.max(0, Math.min(100, value * 100))}%` }} /></div>;
}
export function profileName(id: string) { return `Profile ${id.slice(0, 6).toUpperCase()}`; }
export function dateLabel(date: string) { return new Date(date).toLocaleDateString("en-MY", { day: "numeric", month: "short", year: "numeric" }); }
