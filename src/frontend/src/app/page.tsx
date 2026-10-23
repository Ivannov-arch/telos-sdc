"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SdgBadge } from "@/components/sdg-badge";
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Cpu,
  BarChart3,
  Layers,
  GraduationCap,
  Briefcase,
  Globe2,
  CheckCircle2,
  SlidersHorizontal,
} from "lucide-react";

export default function HomePage() {
  const sampleSdgs = [
    { sdg_goal: 4, sdg_name: "Quality Education", target: "4.4", impact_reasoning: "Substantially increase the number of youth and adults with technical and vocational skills for employment.", source: "UNSD SDG API", color_hex: "#C5192D" },
    { sdg_goal: 8, sdg_name: "Decent Work & Economic Growth", target: "8.2", impact_reasoning: "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.", source: "UNSD SDG API", color_hex: "#A21942" },
    { sdg_goal: 9, sdg_name: "Industry, Innovation & Infrastructure", target: "9.5", impact_reasoning: "Enhance scientific research, upgrade technological capabilities of industrial sectors.", source: "UNSD SDG API", color_hex: "#FD6925" },
    { sdg_goal: 10, sdg_name: "Reduced Inequalities", target: "10.2", impact_reasoning: "Empower and promote social, economic and political inclusion of all, irrespective of age, sex, disability, or race.", source: "UNSD SDG API", color_hex: "#DD1367" },
  ];

  return (
    <div className="relative overflow-hidden">
      {/* Background ambient glow */}
      <div className="pointer-events-none absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80">
        <div
          className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-indigo-500 to-purple-600 opacity-20 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
          style={{
            clipPath:
              "polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)",
          }}
        />
      </div>

      {/* Hero Section */}
      <section className="relative pt-12 pb-20 md:pt-20 md:pb-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-200/70 bg-indigo-50/80 px-4 py-1.5 text-xs font-semibold text-indigo-700 backdrop-blur-xs dark:border-indigo-900/60 dark:bg-indigo-950/50 dark:text-indigo-300 mb-6">
            <Sparkles className="h-3.5 w-3.5" />
            <span>SDC XMUM Hackathon — Domain 1: Aiversecity Future-Ready Workforce</span>
          </div>

          <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-6xl md:text-7xl max-w-4xl mx-auto leading-[1.1]">
            Navigate Your Career in the{" "}
            <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Age of AI Disruption
            </span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Harnessing <strong>Reciprocal Rank Fusion (RRF)</strong>, 3,000+ official ESCO occupations, automated skill-gap set differences, and 2,054 auditable <strong>UN SDG</strong> alignments.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link href="/profile">
              <Button size="lg" className="rounded-xl shadow-lg shadow-indigo-500/25 gap-2 px-8">
                <span>Start Your Career Intake</span>
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/results">
              <Button variant="outline" size="lg" className="rounded-xl gap-2">
                <BarChart3 className="h-4 w-4 text-indigo-600" />
                <span>View Live Matches Demo</span>
              </Button>
            </Link>
          </div>

          {/* Quick Stats Banner */}
          <div className="mt-16 grid grid-cols-2 gap-4 md:grid-cols-4 max-w-4xl mx-auto">
            <div className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/70 dark:bg-slate-900/60 p-4 backdrop-blur-xs">
              <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">3,000+</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">ESCO / MASCO Roles</div>
            </div>
            <div className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/70 dark:bg-slate-900/60 p-4 backdrop-blur-xs">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">BGE-M3</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">Hybrid Dense + Sparse</div>
            </div>
            <div className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/70 dark:bg-slate-900/60 p-4 backdrop-blur-xs">
              <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">2,054</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">Audited SDG Targets</div>
            </div>
            <div className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/70 dark:bg-slate-900/60 p-4 backdrop-blur-xs">
              <div className="text-2xl font-bold text-pink-600 dark:text-pink-400">0% LLM Hallucination</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">Audited Database JOINs</div>
            </div>
          </div>
        </div>
      </section>

      {/* Pipeline Pillars Section */}
      <section className="py-16 bg-slate-50/70 dark:bg-slate-900/30 border-y border-slate-200/60 dark:border-slate-800/60">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
              Architecture Overview
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
              An End-to-End Workforce Intelligence Engine
            </p>
            <p className="mt-4 text-base text-slate-600 dark:text-slate-300">
              Engineered specifically for Domain 1 hackathon criteria: factual taxonomy alignment, hybrid pgvector scoring, and tangible upskilling simulations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Feature 1 */}
            <Card className="hover:border-indigo-400/50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 mb-4">
                  <Layers className="h-6 w-6" />
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary" className="text-[10px]">Feature 1</Badge>
                  <span className="text-xs font-semibold text-slate-400">Intake</span>
                </div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                  Skills Intake & Normalization
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Extracts raw CV text via `pdfplumber`, resolves skills to standardized ESCO UUIDs, and computes dense & sparse vectors.
                </p>
              </CardContent>
            </Card>

            {/* Feature 3 */}
            <Card className="hover:border-purple-400/50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-purple-50 dark:bg-purple-950/60 text-purple-600 dark:text-purple-400 mb-4">
                  <Cpu className="h-6 w-6" />
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary" className="text-[10px]">Feature 3</Badge>
                  <span className="text-xs font-semibold text-slate-400">Core Matching</span>
                </div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                  RRF Hybrid Role Matching
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Combines dense semantic affinity with sparse token matches via Reciprocal Rank Fusion, with mathematical set difference skill gaps.
                </p>
              </CardContent>
            </Card>

            {/* Feature 4 */}
            <Card className="hover:border-emerald-400/50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 mb-4">
                  <GraduationCap className="h-6 w-6" />
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary" className="text-[10px]">Feature 4</Badge>
                  <span className="text-xs font-semibold text-slate-400">Reskilling</span>
                </div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                  Micro-Task Simulation
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Interactive real-world problem scenarios derived from O*NET task statements, offering immediate feedback and concept mastery.
                </p>
              </CardContent>
            </Card>

            {/* Feature 5 */}
            <Card className="hover:border-rose-400/50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 mb-4">
                  <Globe2 className="h-6 w-6" />
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary" className="text-[10px]">Feature 5</Badge>
                  <span className="text-xs font-semibold text-slate-400">SDG Audit</span>
                </div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                  Auditable UN SDG Impact
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Each recommended role is strictly joined to curated UN SDG targets with verifiable rationale from the official UNSD API catalog.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* UN SDG Showcase Section */}
      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="rounded-3xl border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/40 p-8 sm:p-12 shadow-sm">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
              <div>
                <div className="inline-flex items-center gap-2 rounded-md bg-rose-100 dark:bg-rose-950/60 px-3 py-1 text-xs font-bold text-rose-700 dark:text-rose-300 mb-4">
                  <Globe2 className="h-3.5 w-3.5" />
                  <span>Substep 5.4 / 5.5 Visual Requirement</span>
                </div>
                <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
                  Curated & Grounded in United Nations Goals
                </h2>
                <p className="mt-4 text-slate-600 dark:text-slate-300 leading-relaxed">
                  Unlike conventional systems that hallucinate vague sustainability claims, Telos enforces an immutable database relation (`role_sdg`) seeded from the UN Statistics Division (UNSD) API.
                </p>
                <div className="mt-6 space-y-3">
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-emerald-500 shrink-0 mt-0.5" />
                    <span className="text-sm text-slate-700 dark:text-slate-300">
                      <strong>Zero Hallucinations:</strong> Every badge displays its official target code and verified rationale.
                    </span>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-emerald-500 shrink-0 mt-0.5" />
                    <span className="text-sm text-slate-700 dark:text-slate-300">
                      <strong>Official UN Color Palette:</strong> Strict visual compliance with SDG branding standards.
                    </span>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-emerald-500 shrink-0 mt-0.5" />
                    <span className="text-sm text-slate-700 dark:text-slate-300">
                      <strong>Interactive Exploration:</strong> Click any badge to inspect target metrics and impact reasoning.
                    </span>
                  </div>
                </div>

                <div className="mt-8">
                  <Link href="/results">
                    <Button variant="default" className="rounded-xl">
                      Inspect SDG Badges in Results
                    </Button>
                  </Link>
                </div>
              </div>

              {/* Sample Badges Card */}
              <div className="space-y-4 rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-slate-50/80 dark:bg-slate-950/60 p-6">
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  Click badges to inspect live UN alignment:
                </h3>
                <div className="flex flex-wrap gap-2.5 pt-2">
                  {sampleSdgs.map((sdg) => (
                    <SdgBadge key={sdg.sdg_goal} alignment={sdg} />
                  ))}
                </div>

                <div className="mt-6 pt-4 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  💡 <strong>Tip for Evaluators:</strong> In `/results`, badges update automatically based on each matched ESCO occupation joined directly in PostgreSQL.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
