import Link from "next/link";
import { Sparkles, Globe, Shield, Database } from "lucide-react";

export function Footer() {
  return (
    <footer className="w-full border-t border-slate-200/80 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-950/50 py-10 mt-auto transition-colors">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3 md:col-span-2">
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-indigo-600 text-white shadow-xs">
                <Sparkles className="h-4 w-4" />
              </div>
              <span className="font-bold text-slate-900 dark:text-white text-base">
                Telos / Aiversecity
              </span>
              <span className="rounded-md bg-indigo-100 dark:bg-indigo-950 px-2 py-0.5 text-[11px] font-semibold text-indigo-700 dark:text-indigo-400">
                SDC XMUM Hackathon
              </span>
            </div>
            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-md leading-relaxed">
              Future-ready workforce intelligence: Reciprocal Rank Fusion (RRF) hybrid role matching, automated ESCO taxonomy gap analysis, CTCI task compression metrics, and auditable UN SDG alignment.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-900 dark:text-slate-100 mb-3">
              Core Pipeline
            </h4>
            <ul className="space-y-2 text-sm text-slate-500 dark:text-slate-400">
              <li>
                <Link href="/profile" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Skills Intake (F1)
                </Link>
              </li>
              <li>
                <Link href="/results" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Role Matching & Gap (F3)
                </Link>
              </li>
              <li>
                <Link href="/pathway" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Micro-Task Simulation (F4)
                </Link>
              </li>
              <li>
                <Link href="/results" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  UN SDG Auditing (F5)
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-900 dark:text-slate-100 mb-3">
              Taxonomy & Standards
            </h4>
            <ul className="space-y-2 text-sm text-slate-500 dark:text-slate-400">
              <li className="flex items-center gap-1.5">
                <Database className="h-3.5 w-3.5 text-indigo-500" />
                <span>ESCO v1.2 / MASCO 2020</span>
              </li>
              <li className="flex items-center gap-1.5">
                <Globe className="h-3.5 w-3.5 text-emerald-500" />
                <span>UNSD SDG API Targets</span>
              </li>
              <li className="flex items-center gap-1.5">
                <Shield className="h-3.5 w-3.5 text-purple-500" />
                <span>BGE-M3 + pgvector RRF</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-slate-200/60 dark:border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 dark:text-slate-400 gap-4">
          <p>© 2026 Team Bluffing — SDC XMUM Domain 1 Submission. Public, synthetic and auditable datasets only.</p>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
              FastAPI + Next.js App Router
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
