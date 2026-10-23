import Link from "next/link";
import { Icon } from "@/components/ui";

export default function NotFound() {
  return <section className="empty" style={{ marginTop: 45, paddingTop: 70, paddingBottom: 70 }}><div className="eyebrow" style={{ marginBottom: 25 }}>404 / OFF THE MAP</div><div className="empty-icon"><Icon name="target" size={32} /></div><h2>A detour, not a dead end.</h2><p>This page isn’t on our map. Your next step is still out there—let’s get you back to familiar ground.</p><div className="actions"><Link href="/" className="btn">Back to the observatory<Icon size={16} /></Link><Link href="/profiles" className="btn secondary">Find your profile</Link></div></section>;
}
