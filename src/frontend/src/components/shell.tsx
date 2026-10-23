"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { createContext, useContext, useSyncExternalStore, type ReactNode } from "react";
import { Icon, profileName } from "./ui";

const key = "aiversecity.active-profile";
const subscribers = new Set<() => void>();
function subscribe(callback: () => void) {
  subscribers.add(callback);
  window.addEventListener("storage", callback);
  return () => { subscribers.delete(callback); window.removeEventListener("storage", callback); };
}
function snapshot() { try { return localStorage.getItem(key); } catch { return null; } }
function chooseProfile(id: string) {
  try { localStorage.setItem(key, id); } catch { /* Memory fallback remains available for this visit. */ }
  memoryId = id;
  subscribers.forEach((callback) => callback());
}
let memoryId: string | null = null;
const ActiveContext = createContext<{ activeId: string | null; setActive: (id: string) => void; ready: boolean }>({ activeId: null, setActive: chooseProfile, ready: false });
export function useActiveProfile() { return useContext(ActiveContext); }
const serverSnapshot = () => null;
function getSnapshot() { return snapshot() ?? memoryId; }
const readySnapshot = () => true;
const notReadySnapshot = () => false;
export function Shell({ children }: { children: ReactNode }) {
  const activeId = useSyncExternalStore(subscribe, getSnapshot, serverSnapshot);
  const ready = useSyncExternalStore(subscribe, readySnapshot, notReadySnapshot);
  const pathname = usePathname();
  const nav = [
    { href: "/", label: "Overview", icon: "home", active: pathname === "/" },
    { href: "/profiles", label: "My profiles", icon: "profile", active: pathname.startsWith("/profile") },
    { href: activeId ? `/match/${activeId}` : "/profiles?next=matches", label: "Role matches", icon: "target", active: pathname.startsWith("/match") },
    { href: activeId ? `/simulate?profile=${encodeURIComponent(activeId)}` : "/simulate", label: "Practice lab", icon: "practice", active: pathname.startsWith("/simulate") },
  ];
  const current = nav.find((item) => item.active)?.label ?? "Your next chapter";
  return <ActiveContext.Provider value={{ activeId, setActive: chooseProfile, ready }}><div className="app">
    <aside className="sidebar"><Link href="/" className="brand" aria-label="Aiversecity home"><span className="brand-mark"><Icon name="spark" size={23} /></span>Aiversecity</Link><div className="brand-sub">A future that fits you</div>
      <div className="nav-label">YOUR WORKSPACE</div><nav aria-label="Main navigation">{nav.map((item) => <Link key={item.label} href={item.href} className={`nav-link ${item.active ? "active" : ""}`} aria-current={item.active ? "page" : undefined}><Icon name={item.icon} /><span>{item.label}</span>{item.active && <span className="nav-dot" />}</Link>)}</nav>
      <div className="sidebar-bottom"><div className="side-note"><Icon name="globe" size={20} /><div style={{ marginTop: 10 }}><strong>Skills for a better future.</strong><p>Find your place in a changing world of work. Make your next move count.</p></div></div><div className="project-credit">Built for SDC XMUM Hackathon<br /><span style={{ fontFamily: "var(--font-code)", fontSize: 9 }}>XMUM · MALAYSIA</span></div></div>
    </aside>
    <div className="workspace"><div className="topbar"><div className="breadcrumb">Workspace <span>/</span> <b>{current}</b></div><Link href="/profiles" className="profile-switch"><span className="avatar">{activeId ? activeId.slice(0, 2).toUpperCase() : "AV"}</span><span>{activeId ? profileName(activeId) : "Choose your profile"}</span><Icon name="chevron" size={13} /></Link></div>
      <main className="main">{children}<footer className="footer"><span>Aiversecity — human potential, mapped for what’s next.</span><span>ESCO-powered skills · UN SDG-aligned · No account needed</span></footer></main>
    </div>
  </div></ActiveContext.Provider>;
}
