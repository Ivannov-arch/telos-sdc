"use client";

import * as React from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
} from "recharts";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { SdgBadge } from "@/components/sdg-badge";
import { getMatchResults, MatchResponse, MatchResult } from "@/lib/api";
import {
  Sparkles,
  SlidersHorizontal,
  ArrowUpRight,
  ChevronUp,
  ChevronDown,
  Info,
  CheckCircle,
  AlertTriangle,
  Flame,
  Award,
  RefreshCw,
  Route,
  Zap,
  Target,
  BarChart3,
  Radar as RadarIcon,
} from "lucide-react";

function ResultsContent() {
  const searchParams = useSearchParams();
  const userId =
    searchParams.get("user_id") || "587479a6-04d5-4371-a57f-c3b39c9b7be2";

  // Scenario toggle: "moderate" vs "fast" (Career Stress-Test Engine — Substep 6.3)
  const [scenario, setScenario] = React.useState<"moderate" | "fast">("moderate");

  // Keep track of moderate scores for delta computation (↑ or ↓ under fast disruption)
  const [moderateBaseline, setModerateBaseline] = React.useState<Record<string, number>>({});

  // Query match results with React Query
  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ["match-results", userId, scenario],
    queryFn: () => getMatchResults(userId, scenario, 6),
  });

  // When moderate data arrives, cache baseline scores for delta indicators
  React.useEffect(() => {
    if (scenario === "moderate" && data?.results) {
      const mapping: Record<string, number> = {};
      data.results.forEach((r, idx) => {
        mapping[r.esco_id] = idx;
      });
      setModerateBaseline(mapping);
    }
  }, [data, scenario]);

  const results: MatchResult[] = data?.results || [];

  // Chart data for BarChart (Match score comparison)
  const chartData = results.map((r) => ({
    name: r.target_role.length > 18 ? r.target_role.slice(0, 16) + "…" : r.target_role,
    fullName: r.target_role,
    matchScore: Math.round(r.match_score * 100),
    rrf: Math.round(r.score_breakdown.rrf_score * 100),
    coverage: Math.round(r.score_breakdown.hard_skill_coverage * 100),
    seniority: Math.round(r.score_breakdown.seniority_match * 100),
  }));

  // Aggregated SDG list across all recommendations (Substep 5.4 bonus)
  const aggregatedSdgs = React.useMemo(() => {
    const map = new Map<number, any>();
    results.forEach((r) => {
      r.sdg_alignment?.forEach((sdg) => {
        if (!map.has(sdg.sdg_goal)) {
          map.set(sdg.sdg_goal, sdg);
        }
      });
    });
    return Array.from(map.values());
  }, [results]);

  // Skill gap breakdown stats for RadarChart
  const radarData = React.useMemo(() => {
    if (results.length === 0) return [];
    const topRole = results[0];
    return [
      { subject: "Dense Vector Affinity", user: Math.round(topRole.score_breakdown.rrf_score * 100), fullMark: 100 },
      { subject: "Hard Skill Coverage", user: Math.round(topRole.score_breakdown.hard_skill_coverage * 100), fullMark: 100 },
      { subject: "Seniority Match", user: Math.round(topRole.score_breakdown.seniority_match * 100), fullMark: 100 },
      { subject: "SDG Alignment", user: Math.min(100, (topRole.sdg_alignment?.length || 1) * 35), fullMark: 100 },
      { subject: "Overall Match", user: Math.round(topRole.match_score * 100), fullMark: 100 },
    ];
  }, [results]);

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10 md:py-16">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8 pb-6 border-b border-slate-200/80 dark:border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Badge variant="secondary" className="gap-1 font-semibold text-xs">
              <Sparkles className="h-3.5 w-3.5 text-indigo-500" />
              Feature 3 + Feature 5 Live Dashboard
            </Badge>
            <span className="text-xs text-slate-500 dark:text-slate-400">
              User ID: <code className="font-mono text-[11px] bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded">{userId.slice(0, 8)}…</code>
            </span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
            Ranked Role Recommendations
          </h1>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
            Rankings computed via <strong>Reciprocal Rank Fusion (RRF)</strong> over BGE-M3 embeddings and PostgreSQL set-difference skill gap analysis.
          </p>
        </div>

        {/* AI Shock Scenario Slider / Toggle (Feature 6 & Substep 6.3) */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-2.5 rounded-2xl shadow-xs">
          <div className="flex items-center gap-2 px-2 text-xs font-semibold text-slate-600 dark:text-slate-400">
            <SlidersHorizontal className="h-4 w-4 text-indigo-500" />
            <span>AI Shock Scenario:</span>
          </div>
          <div className="inline-flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1">
            <button
              type="button"
              onClick={() => setScenario("moderate")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all cursor-pointer ${
                scenario === "moderate"
                  ? "bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-xs"
                  : "text-slate-600 hover:text-slate-900 dark:text-slate-400"
              }`}
            >
              Baseline / Moderate
            </button>
            <button
              type="button"
              onClick={() => setScenario("fast")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all flex items-center gap-1 cursor-pointer ${
                scenario === "fast"
                  ? "bg-rose-500 text-white shadow-xs"
                  : "text-slate-600 hover:text-slate-900 dark:text-slate-400"
              }`}
            >
              <Flame className="h-3.5 w-3.5" />
              <span>Fast AI Disruption</span>
            </button>
          </div>

          <Button
            variant="outline"
            size="icon"
            onClick={() => refetch()}
            disabled={isFetching}
            className="rounded-xl h-9 w-9 shrink-0"
            title="Refresh API Data"
          >
            <RefreshCw className={`h-4 w-4 ${isFetching ? "animate-spin" : ""}`} />
          </Button>
        </div>
      </div>

      {/* Fast Disruption Banner Notice */}
      <AnimatePresence>
        {scenario === "fast" && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden mb-8"
          >
            <div className="flex items-start gap-3 rounded-2xl bg-amber-500/10 border border-amber-500/30 p-4 text-amber-900 dark:text-amber-200">
              <Zap className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" />
              <div className="text-sm">
                <strong className="font-semibold">Career Stress-Test Active (Fast AI Disruption):</strong> Roles with high routine cognitive ratios experience disruption penalties in our hybrid matrix. Conversely, roles requiring complex judgment, stakeholder negotiation, and deep systems engineering rise in priority.
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading state */}
      {isLoading && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Skeleton className="h-64 rounded-2xl" />
            <Skeleton className="h-64 rounded-2xl" />
          </div>
          <div className="space-y-4">
            <Skeleton className="h-32 rounded-2xl" />
            <Skeleton className="h-32 rounded-2xl" />
            <Skeleton className="h-32 rounded-2xl" />
          </div>
        </div>
      )}

      {/* Error state */}
      {isError && (
        <Card className="border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/20 text-center p-10">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-100 text-rose-600 mx-auto mb-4">
            <AlertTriangle className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">Unable to fetch match results</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 max-w-md mx-auto mt-2">
            The FastAPI backend may be initializing or the user profile ID is invalid. Verify the backend service is running on port 8000.
          </p>
          <div className="mt-6 flex justify-center gap-3">
            <Link href="/profile">
              <Button variant="outline" className="rounded-xl">Select Demo Profile</Button>
            </Link>
            <Button onClick={() => refetch()} className="rounded-xl">Retry Request</Button>
          </div>
        </Card>
      )}

      {/* Results content */}
      {!isLoading && !isError && results.length > 0 && (
        <div className="space-y-10">
          {/* Visual Charts Overview (Recharts Match Score + Radar) */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Bar Chart: Match Score Comparison */}
            <Card className="lg:col-span-2 border-slate-200 dark:border-slate-800">
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <BarChart3 className="h-4 w-4 text-indigo-500" />
                      Composite Match Score Comparison
                    </CardTitle>
                    <CardDescription>
                      Comparing RRF Dense Semantic Rank vs Hard Skill Set-Difference Coverage
                    </CardDescription>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    Recharts Live
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="pt-4">
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 25 }}>
                      <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                      <XAxis
                        dataKey="name"
                        tick={{ fontSize: 11 }}
                        interval={0}
                        angle={-15}
                        textAnchor="end"
                      />
                      <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} unit="%" />
                      <RechartsTooltip
                        contentStyle={{
                          backgroundColor: "#0f172a",
                          borderRadius: "12px",
                          border: "1px solid #1e293b",
                          color: "#fff",
                          fontSize: "12px",
                        }}
                        formatter={(val: any) => [`${val}%`]}
                      />
                      <Bar dataKey="matchScore" name="Composite Match" fill="#6366f1" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="coverage" name="Hard Skill Coverage" fill="#10b981" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Radar Chart: Top Role Multi-Factor Profile */}
            <Card className="border-slate-200 dark:border-slate-800">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center gap-2">
                  <RadarIcon className="h-4 w-4 text-purple-500" />
                  Top Match Multi-Axis
                </CardTitle>
                <CardDescription>
                  Radar breakdown for {results[0]?.target_role}
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-2">
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                      <PolarGrid strokeOpacity={0.2} />
                      <PolarAngleAxis dataKey="subject" tick={{ fontSize: 9 }} />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 9 }} />
                      <Radar name="Alignment" dataKey="user" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.4} />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Aggregated SDG Footprint Banner (Substep 5.4 / 5.5) */}
          <div className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/70 dark:bg-slate-900/60 p-6 backdrop-blur-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
              <div className="flex items-center gap-2.5">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-500 text-white font-bold text-xs shadow-xs">
                  SDG
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                    Aggregated United Nations SDG Footprint
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Sustainable impact targets represented across your top role matches:
                  </p>
                </div>
              </div>
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded-full">
                {aggregatedSdgs.length} Aligned Goals
              </span>
            </div>

            <div className="flex flex-wrap gap-2">
              {aggregatedSdgs.map((sdg) => (
                <SdgBadge key={sdg.sdg_goal} alignment={sdg} />
              ))}
            </div>
          </div>

          {/* Role Cards List (Framer Motion Staggered Entrance) */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <span>Detailed Role Cards & Skill Gap Breakdown</span>
                <span className="text-xs font-normal text-slate-500 dark:text-slate-400">
                  (Showing Top {results.length} Roles)
                </span>
              </h2>
            </div>

            <div className="space-y-4">
              <AnimatePresence>
                {results.map((role, index) => {
                  const scorePercent = Math.round(role.match_score * 100);
                  const baselineIndex = moderateBaseline[role.esco_id];
                  const rankDelta =
                    scenario === "fast" && baselineIndex !== undefined
                      ? baselineIndex - index // positive means rose in rank
                      : 0;

                  // CTCI Signal indicator (Substep 2.4 — Phase 3)
                  // Substitutive vs Complementary
                  const isComplementary = role.match_score >= 0.75;
                  const ctciSignal =
                    role.compression_type ||
                    (isComplementary ? "Complementary" : "Substitutive");

                  return (
                    <motion.div
                      key={role.esco_id}
                      layout
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      transition={{ duration: 0.25, delay: index * 0.05 }}
                    >
                      <Card className="hover:border-indigo-400/80 hover:shadow-md transition-all duration-200">
                        <CardHeader className="pb-3">
                          <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                            <div className="space-y-1">
                              <div className="flex flex-wrap items-center gap-2">
                                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-400 text-xs font-bold">
                                  #{index + 1}
                                </span>
                                <CardTitle className="text-xl font-bold">
                                  {role.target_role}
                                </CardTitle>

                                {/* Delta Indicator under Fast AI Disruption */}
                                {scenario === "fast" && rankDelta !== 0 && (
                                  <Badge
                                    variant={rankDelta > 0 ? "success" : "destructive"}
                                    className="gap-1 text-[11px]"
                                  >
                                    {rankDelta > 0 ? (
                                      <>
                                        <ChevronUp className="h-3 w-3" />
                                        <span>+{rankDelta} Positions</span>
                                      </>
                                    ) : (
                                      <>
                                        <ChevronDown className="h-3 w-3" />
                                        <span>{rankDelta} Positions</span>
                                      </>
                                    )}
                                  </Badge>
                                )}
                              </div>

                              <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                                <span>ESCO ID: <code className="font-mono">{role.esco_id.slice(0, 8)}…</code></span>
                                <span>•</span>
                                {/* CTCI Signal (Substep 2.4) */}
                                <span
                                  className={`inline-flex items-center gap-1 rounded-md px-2 py-0.5 font-medium ${
                                    ctciSignal === "Complementary"
                                      ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200/60 dark:border-emerald-800"
                                      : "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400 border border-amber-200/60 dark:border-amber-800"
                                  }`}
                                >
                                  <span>CTCI: {ctciSignal} Compression</span>
                                </span>
                              </div>
                            </div>

                            {/* Score Display */}
                            <div className="flex items-baseline sm:flex-col sm:items-end justify-between shrink-0">
                              <div className="text-2xl font-black text-indigo-600 dark:text-indigo-400">
                                {scorePercent}%
                              </div>
                              <span className="text-[11px] text-slate-400 font-medium">
                                Composite Match
                              </span>
                            </div>
                          </div>
                        </CardHeader>

                        <CardContent className="space-y-4 pt-0">
                          {/* Match Progress Bar */}
                          <div>
                            <Progress value={scorePercent} className="h-2.5" />
                          </div>

                          {/* Score Weights Breakdown Tooltip Row */}
                          <div className="flex flex-wrap items-center justify-between text-xs text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-900/60 p-2.5 rounded-xl border border-slate-100 dark:border-slate-800/60 gap-2">
                            <div className="flex items-center gap-1.5">
                              <Info className="h-3.5 w-3.5 text-indigo-500" />
                              <span>Score Breakdown:</span>
                            </div>
                            <div className="flex flex-wrap items-center gap-3">
                              <span>RRF Semantic: <strong>{Math.round(role.score_breakdown.rrf_score * 100)}%</strong> (0.5w)</span>
                              <span>•</span>
                              <span>Hard Skill Coverage: <strong>{Math.round(role.score_breakdown.hard_skill_coverage * 100)}%</strong> (0.3w)</span>
                              <span>•</span>
                              <span>Seniority: <strong>{Math.round(role.score_breakdown.seniority_match * 100)}%</strong> (0.2w)</span>
                            </div>
                          </div>

                          {/* Skill Gap Badges (Set Difference T \ U) */}
                          <div>
                            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2 flex items-center justify-between">
                              <span>Skill Gap (Must-Learn Skills):</span>
                              <span className="text-[11px] font-normal text-slate-400">
                                {role.skills_gap?.length || 0} missing skills
                              </span>
                            </div>
                            {role.skills_gap && role.skills_gap.length > 0 ? (
                              <div className="flex flex-wrap gap-1.5">
                                {role.skills_gap.map((gap, gIdx) => (
                                  <Badge
                                    key={gIdx}
                                    variant={gap.type === "core" ? "core" : "supporting"}
                                    className="text-xs"
                                  >
                                    <span className="h-1.5 w-1.5 rounded-full mr-1.5 bg-current opacity-70" />
                                    {gap.skill}
                                    <span className="ml-1 opacity-60 text-[10px]">
                                      ({gap.type})
                                    </span>
                                  </Badge>
                                ))}
                              </div>
                            ) : (
                              <div className="flex items-center gap-1.5 text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                                <CheckCircle className="h-3.5 w-3.5" />
                                <span>No skill gap detected! Your profile completely covers required skills.</span>
                              </div>
                            )}
                          </div>

                          {/* SDG Alignment Badges */}
                          {role.sdg_alignment && role.sdg_alignment.length > 0 && (
                            <div>
                              <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2">
                                UN SDG Alignment:
                              </div>
                              <div className="flex flex-wrap gap-2">
                                {role.sdg_alignment.map((sdg, sIdx) => (
                                  <SdgBadge key={sIdx} alignment={sdg} />
                                ))}
                              </div>
                            </div>
                          )}
                        </CardContent>

                        <CardFooter className="flex items-center justify-between pt-3 border-t border-slate-100 dark:border-slate-800">
                          <span className="text-xs text-slate-500 dark:text-slate-400">
                            Verified via static PostgreSQL JOIN (Zero LLM hallucination)
                          </span>
                          <Link href={`/pathway/${encodeURIComponent(role.esco_id)}?user_id=${userId}&role_name=${encodeURIComponent(role.target_role)}`}>
                            <Button size="sm" variant="outline" className="rounded-xl gap-1.5 hover:bg-indigo-50 dark:hover:bg-indigo-950">
                              <Route className="h-3.5 w-3.5 text-indigo-600 dark:text-indigo-400" />
                              <span>Practice Micro-Tasks</span>
                              <ArrowUpRight className="h-3.5 w-3.5" />
                            </Button>
                          </Link>
                        </CardFooter>
                      </Card>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ResultsPage() {
  return (
    <React.Suspense
      fallback={
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16 space-y-6">
          <Skeleton className="h-12 w-64 rounded-xl" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Skeleton className="h-64 rounded-2xl" />
            <Skeleton className="h-64 rounded-2xl" />
          </div>
        </div>
      }
    >
      <ResultsContent />
    </React.Suspense>
  );
}
