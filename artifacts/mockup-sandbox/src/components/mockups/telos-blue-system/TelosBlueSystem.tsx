import { useState } from "react";
import { ArrowRight, ArrowUpRight, Check, Copy, Sparkles } from "lucide-react";
import "./TelosBlueSystem.css";

const colorTokens = [
  { name: "Background", role: "Canvas", value: "#f0f2f6", kind: "pale" },
  { name: "Foreground", role: "Primary text", value: "#16233c", kind: "dark" },
  { name: "Surface", role: "Cards & controls", value: "#f7f9fc", kind: "pale" },
  { name: "Muted", role: "Supporting text", value: "#6b717d", kind: "mid" },
  { name: "Line", role: "Borders & dividers", value: "#d8dce4", kind: "pale" },
  { name: "Petrol", role: "Primary action", value: "#16284c", kind: "dark" },
  { name: "Lime", role: "Accent emphasis", value: "#84a8ef", kind: "mid" },
  { name: "Mint", role: "Soft surface", value: "#e1e5ec", kind: "pale" },
  { name: "Coral", role: "Secondary accent", value: "#3d67bc", kind: "dark" },
];

const spacingTokens = [
  { name: "space-1", value: "4px", width: 8 },
  { name: "space-2", value: "8px", width: 16 },
  { name: "space-3", value: "12px", width: 24 },
  { name: "space-4", value: "16px", width: 32 },
  { name: "space-6", value: "24px", width: 48 },
  { name: "space-8", value: "32px", width: 64 },
  { name: "space-12", value: "48px", width: 96 },
];

const semanticColors = [
  { name: "SDG 1", value: "#a23f5f" },
  { name: "SDG 2", value: "#c58b34" },
  { name: "SDG 3", value: "#4d7859" },
];

export default function TelosBlueSystem() {
  const [notice, setNotice] = useState("A small, useful system for the next step.");
  const [primaryUsed, setPrimaryUsed] = useState(false);

  async function copyColor(name: string, value: string) {
    try {
      await navigator.clipboard.writeText(value);
      setNotice(`${name} copied · ${value}`);
    } catch {
      setNotice(`${name} token · ${value} · clipboard unavailable in this preview`);
    }
  }

  return (
    <div className="telos-showcase">
      <aside className="ts-sidebar">
        <a className="ts-brand" href="#overview" aria-label="Telos Blue design system overview">
          <span className="ts-brand-mark"><Sparkles size={18} strokeWidth={1.8} /></span>
          <span>Aiversecity<small>TELOS / BLUE</small></span>
        </a>

        <div className="ts-nav-label">THE SYSTEM</div>
        <nav className="ts-nav" aria-label="Design system sections">
          <a className="is-active" href="#overview"><span className="ts-nav-dot" />Overview</a>
          <a href="#color"><span className="ts-nav-dot" />Color</a>
          <a href="#type"><span className="ts-nav-dot" />Typography</a>
          <a href="#space"><span className="ts-nav-dot" />Spatial tokens</a>
          <a href="#components"><span className="ts-nav-dot" />Components</a>
        </nav>

        <div className="ts-sidebar-note">
          <span className="ts-mono">DESIGN INTENT</span>
          <p>Make complex career choices feel a little clearer, and always leave room for the person behind the data.</p>
        </div>
        <div className="ts-sidebar-foot ts-mono">SDC XMUM · MALAYSIA<br />SYSTEM 01 / 2026</div>
      </aside>

      <div className="ts-workspace">
        <header className="ts-topbar">
          <div className="ts-crumb">Design library <span>/</span> <strong>Telos Blue</strong></div>
          <div className="ts-version"><i /> FOUNDATION KIT <b>01.0</b></div>
        </header>

        <main className="ts-main">
          <section className="ts-intro" id="overview">
            <div>
              <div className="ts-eyebrow ts-mono">AIVERSECITY · VISUAL LANGUAGE</div>
              <h1>Clear signals.<br /><em>Room to choose.</em></h1>
              <p className="ts-intro-copy">A calm, evidence-led foundation for mapping skills, exploring future roles, and practising what comes next.</p>
            </div>
            <div className="ts-intro-aside">
              <span className="ts-orbit-mark" aria-hidden="true">
                <i className="ts-orbit-ring ring-one" />
                <i className="ts-orbit-ring ring-two" />
                <i className="ts-orbit-center"><Sparkles size={21} /></i>
                <i className="ts-orbit-node node-one" />
                <i className="ts-orbit-node node-two" />
                <i className="ts-orbit-node node-three" />
              </span>
              <span className="ts-mono ts-orbit-caption">SKILL → POSSIBILITY → IMPACT</span>
            </div>
          </section>

          <div className="ts-principles">
            <div><span className="ts-principle-index ts-mono">01</span><b>Human first</b><span>Encourage without overpromising.</span></div>
            <div><span className="ts-principle-index ts-mono">02</span><b>Evidence in view</b><span>Keep signals legible and grounded.</span></div>
            <div><span className="ts-principle-index ts-mono">03</span><b>Room to act</b><span>Make each next step feel possible.</span></div>
          </div>

          <section className="ts-section" id="color">
            <div className="ts-section-head">
              <div><div className="ts-eyebrow ts-mono">FOUNDATION / 01</div><h2>Color has a job.</h2></div>
              <p>Brand hues shift to blue; source saturation and value stay constant. Evidence colors stay independent.</p>
            </div>
            <div className="ts-palette">
              {colorTokens.map((token) => (
                <button
                  className={`ts-swatch ts-swatch-${token.kind}`}
                  key={token.name}
                  onClick={() => copyColor(token.name, token.value)}
                  aria-label={`Copy ${token.name} color ${token.value}`}
                  type="button"
                >
                  <span className="ts-swatch-color" style={{ backgroundColor: token.value }}>
                    <span className="ts-copy-icon"><Copy size={13} /></span>
                  </span>
                  <span className="ts-swatch-meta">
                    <strong>{token.name}</strong>
                    <span>{token.role}</span>
                    <code>{token.value}</code>
                  </span>
                </button>
              ))}
            </div>
            <div className="ts-color-note">
              <span className="ts-note-mark">H</span>
              <p><strong>Hue-only shift · 220°</strong><br />The original color relationships stay intact; only their direction on the spectrum changes.</p>
              <span className="ts-chart-label ts-mono">SDG DATA COLORS</span>
              <div className="ts-data-colors">{semanticColors.map((color) => <span key={color.name} title={`${color.name} ${color.value}`} style={{ background: color.value }} />)}</div>
            </div>
          </section>

          <section className="ts-section" id="type">
            <div className="ts-section-head">
              <div><div className="ts-eyebrow ts-mono">FOUNDATION / 02</div><h2>Three voices, one system.</h2></div>
              <p>Display carries direction. Body copy carries detail. Monospace keeps the data quiet and precise.</p>
            </div>
            <div className="ts-type-layout">
              <article className="ts-type-hero">
                <span className="ts-mono">MANROPE · DISPLAY</span>
                <h3>Your next move<br />can start here.</h3>
                <div className="ts-type-hero-foot"><span>Confident, never commanding.</span><ArrowUpRight size={16} /></div>
              </article>
              <div className="ts-type-list">
                <div className="ts-type-row">
                  <span className="ts-type-role ts-mono">DM SANS<br />BODY</span>
                  <div><strong>Skills travel further than titles.</strong><p>Use clear, practical language. Keep the person—not the prediction—at the center.</p></div>
                </div>
                <div className="ts-type-row">
                  <span className="ts-type-role ts-mono">IBM PLEX<br />MONO</span>
                  <div className="ts-mono ts-mono-sample">ESCO · SDG · 01 / 03<br /><small>Labels, metadata, precise signals.</small></div>
                </div>
                <div className="ts-type-scale">
                  <span className="ts-mono">TYPE SCALE</span>
                  <div><b className="scale-xxs">11</b><b className="scale-sm">12</b><b className="scale-base">14</b><b className="scale-lg">16</b><b className="scale-xl">21</b><b className="scale-2xl">29</b></div>
                  <small>px · measured hierarchy, not noise</small>
                </div>
              </div>
            </div>
          </section>

          <section className="ts-section" id="space">
            <div className="ts-section-head">
              <div><div className="ts-eyebrow ts-mono">FOUNDATION / 03</div><h2>Space for a better read.</h2></div>
              <p>Compact where information matters; generous where a decision needs breathing room.</p>
            </div>
            <div className="ts-spatial-grid">
              <article className="ts-token-panel">
                <div className="ts-panel-head"><h3>Spacing scale</h3><span className="ts-mono">4PX BASE</span></div>
                <div className="ts-space-list">
                  {spacingTokens.map((token) => (
                    <div className="ts-space-row" key={token.name}>
                      <code>{token.name}</code><span className="ts-space-track"><i style={{ width: `${token.width}px` }} /></span><span>{token.value}</span>
                    </div>
                  ))}
                </div>
              </article>
              <article className="ts-token-panel">
                <div className="ts-panel-head"><h3>Shape & depth</h3><span className="ts-mono">SOFT EDGES</span></div>
                <div className="ts-shapes">
                  <span className="shape-sm">7</span><span className="shape-md">10</span><span className="shape-lg">12</span><span className="shape-xl">14</span><span className="shape-pill">999</span>
                </div>
                <div className="ts-elevation-row"><span className="elevation-one">ELEVATION 01</span><span className="elevation-two">ELEVATION 02</span></div>
                <p className="ts-panel-caption">A fine border first. A tinted shadow only when the layer needs to lift.</p>
              </article>
            </div>
          </section>

          <section className="ts-section" id="components">
            <div className="ts-section-head">
              <div><div className="ts-eyebrow ts-mono">FOUNDATION / 04</div><h2>Small pieces. Clear intent.</h2></div>
              <p>Native, accessible controls with distinct emphasis levels and visible focus.</p>
            </div>
            <div className="ts-component-grid">
              <article className="ts-component-card ts-button-card">
                <div className="ts-card-title"><h3>Actions</h3><span className="ts-mono">BUTTON / 4 VARIANTS</span></div>
                <div className="ts-button-row">
                  <button type="button" className="ts-button primary" onClick={() => { setPrimaryUsed(!primaryUsed); setNotice(primaryUsed ? "Primary action ready for preview." : "Primary action state previewed."); }}>
                    {primaryUsed ? "Step saved" : "Explore roles"} {primaryUsed ? <Check size={14} /> : <ArrowRight size={14} />}
                  </button>
                  <button type="button" className="ts-button accent" onClick={() => setNotice("Accent action previewed.")}>Map my skills</button>
                  <button type="button" className="ts-button secondary" onClick={() => setNotice("Secondary action previewed.")}>Learn more</button>
                  <button type="button" className="ts-button quiet" onClick={() => setNotice("Quiet action previewed.")}>View notes</button>
                </div>
                <div className="ts-interaction-status" aria-live="polite"><span className={primaryUsed ? "status-active" : ""} />{notice}</div>
              </article>
              <article className="ts-component-card">
                <div className="ts-card-title"><h3>Labels</h3><span className="ts-mono">BADGE / TONE</span></div>
                <div className="ts-badge-row"><span className="ts-badge">Transferable skill</span><span className="ts-badge brand">Role match</span><span className="ts-badge accent">Evidence-led</span><span className="ts-badge soft">In progress</span></div>
                <p className="ts-helper-copy">Use a label to clarify context, not to carry status by color alone.</p>
              </article>
              <article className="ts-component-card">
                <div className="ts-card-title"><h3>Fields</h3><span className="ts-mono">DEFAULT / FOCUS</span></div>
                <label className="ts-field"><span>Role to explore</span><input type="text" defaultValue="Learning support teacher" /><small>Start with a role, skill, or interest.</small></label>
                <label className="ts-field"><span>Work context</span><select defaultValue="team"><option value="team">Team project</option><option value="independent">Independent work</option></select></label>
              </article>
              <article className="ts-component-card">
                <div className="ts-card-title"><h3>States</h3><span className="ts-mono">ERROR / DISABLED</span></div>
                <label className="ts-field"><span>Email address</span><input className="is-error" type="text" defaultValue="not-an-email" aria-invalid="true" /><small className="ts-field-error">Enter the email address in the expected format.</small></label>
                <label className="ts-field"><span>Saved preference</span><input type="text" defaultValue="Career transition" disabled /></label>
              </article>
            </div>
          </section>

          <footer className="ts-footer">
            <div><span className="ts-brand-mark small-mark"><Sparkles size={15} /></span><span>Telos Blue · Aiversecity</span></div>
            <span className="ts-mono">HUMAN POTENTIAL, MAPPED FOR WHAT’S NEXT.</span>
          </footer>
        </main>
      </div>
    </div>
  );
}
