"use client";

import * as React from "react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { getSimulationTasks, submitSimulation, SimulationTask, SimulateResult } from "@/lib/api";
import {
  Route,
  ArrowLeft,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Send,
  RotateCcw,
  BookOpen,
  Award,
  HelpCircle,
  Check,
  ChevronRight,
} from "lucide-react";

function PathwayRoleContent() {
  const params = useParams();
  const searchParams = useSearchParams();

  const roleId = decodeURIComponent((params.roleId as string) || "");
  const roleName = searchParams.get("role_name") || "Target Occupation";
  const userId = searchParams.get("user_id") || "587479a6-04d5-4371-a57f-c3b39c9b7be2";

  // Fetch simulation tasks from backend
  const { data: tasksData, isLoading, isError, refetch } = useQuery({
    queryKey: ["simulation-tasks", roleId],
    queryFn: () => getSimulationTasks(undefined, 10),
  });

  const tasks: SimulationTask[] = tasksData?.tasks || [];

  // Active task selection
  const [activeTaskIndex, setActiveTaskIndex] = React.useState(0);
  const [userResponses, setUserResponses] = React.useState<Record<string, string>>({});
  const [results, setResults] = React.useState<Record<string, SimulateResult>>({});

  // Fallback default scenario if DB tasks table is being seeded
  const activeTask: SimulationTask = tasks[activeTaskIndex] || {
    id: "a4a0ab6f-83d8-46fa-b50d-2976eeaf04fb",
    skill_id: "e44d3ba1-3836-4d04-8b6b-3aa83984ca3b",
    scenario_text:
      "A high-volume streaming data pipeline is experiencing a 30% drop in throughput under peak traffic. Outline a 3-bullet technical remediation plan covering pipeline monitoring, worker container scaling, and backpressure mitigation strategies.",
    difficulty: "Intermediate",
    onet_task_ref: "15-1252.00 Software Developers",
    rubric_criteria: [
      "Mentions telemetry or metric alarms",
      "Describes horizontal autoscaling or queue management",
      "Addresses backpressure or rate limiting",
    ],
  };

  const currentResponse = userResponses[activeTask.id] || "";

  // Mutation for POST /api/simulate
  const simulateMutation = useMutation({
    mutationFn: (text: string) => submitSimulation(userId, activeTask.id, text),
    onSuccess: (data) => {
      setResults((prev) => ({ ...prev, [activeTask.id]: data }));
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentResponse.trim()) return;
    simulateMutation.mutate(currentResponse);
  };

  const handleReset = () => {
    setResults((prev) => {
      const copy = { ...prev };
      delete copy[activeTask.id];
      return copy;
    });
  };

  const activeResult = results[activeTask.id];

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10 md:py-16">
      {/* Back button */}
      <div className="mb-6">
        <Link
          href={`/results?user_id=${userId}`}
          className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Role Matches</span>
        </Link>
      </div>

      {/* Header */}
      <div className="mb-10">
        <div className="flex items-center gap-2 mb-2">
          <Badge variant="secondary" className="gap-1 font-semibold text-xs">
            <Route className="h-3.5 w-3.5 text-indigo-500" />
            Feature 4: Micro-Task Simulation Pathway
          </Badge>
          <span className="text-xs text-slate-500 dark:text-slate-400">
            Phase 2 Integration
          </span>
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
          {roleName}
        </h1>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
          Close your skill gap by practicing interactive, rubric-anchored work scenarios derived from real-world O*NET and ESCO tasks.
        </p>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Task Navigation Sidebar */}
        <div className="space-y-4">
          <Card className="border-slate-200 dark:border-slate-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                Simulation Challenges
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 p-3 pt-0">
              {isLoading ? (
                <div className="space-y-2">
                  <Skeleton className="h-14 rounded-xl" />
                  <Skeleton className="h-14 rounded-xl" />
                </div>
              ) : tasks.length === 0 ? (
                <button
                  type="button"
                  onClick={() => setActiveTaskIndex(0)}
                  className="w-full text-left rounded-xl p-3 text-xs bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 font-medium"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold">Challenge #1</span>
                    <Badge variant="outline" className="text-[10px]">Intermediate</Badge>
                  </div>
                  <p className="line-clamp-2 text-slate-600 dark:text-slate-400">
                    High-volume streaming pipeline remediation
                  </p>
                </button>
              ) : (
                tasks.map((t, idx) => {
                  const isCurrent = idx === activeTaskIndex;
                  const isDone = results[t.id] !== undefined;
                  return (
                    <button
                      key={t.id}
                      type="button"
                      onClick={() => setActiveTaskIndex(idx)}
                      className={`w-full text-left rounded-xl p-3 text-xs transition-all cursor-pointer ${
                        isCurrent
                          ? "bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-300 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 shadow-xs"
                          : "hover:bg-slate-50 dark:hover:bg-slate-900 border border-transparent text-slate-700 dark:text-slate-300"
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold">Challenge #{idx + 1}</span>
                        {isDone ? (
                          <span className="flex items-center text-emerald-600 text-[10px] font-bold">
                            <Check className="h-3 w-3 mr-0.5" />
                            Completed
                          </span>
                        ) : (
                          <Badge variant="outline" className="text-[10px]">{t.difficulty || "Core"}</Badge>
                        )}
                      </div>
                      <p className="line-clamp-2 text-slate-500 dark:text-slate-400">
                        {t.scenario_text}
                      </p>
                    </button>
                  );
                })
              )}
            </CardContent>
          </Card>

          <Card className="border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50">
            <CardContent className="p-4 text-xs text-slate-500 dark:text-slate-400 space-y-2">
              <div className="flex items-center gap-1.5 font-bold text-slate-700 dark:text-slate-300">
                <HelpCircle className="h-4 w-4 text-indigo-500" />
                <span>Rubric Evaluation Criteria</span>
              </div>
              <p className="leading-relaxed">
                Answers are evaluated against closed rubric benchmarks to assess structural reasoning, domain terminology, and practical execution steps.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Task Solver Area */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="border-slate-200 dark:border-slate-800">
            <CardHeader>
              <div className="flex items-center justify-between">
                <Badge variant="secondary" className="text-xs">
                  Challenge #{activeTaskIndex + 1}
                </Badge>
                {activeTask.onet_task_ref && (
                  <span className="text-xs text-slate-400 font-mono">
                    Ref: {activeTask.onet_task_ref}
                  </span>
                )}
              </div>
              <CardTitle className="text-lg mt-2">
                Scenario Prompt
              </CardTitle>
              <CardDescription className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-slate-900/80 p-4 rounded-xl border border-slate-100 dark:border-slate-800 mt-2">
                {activeTask.scenario_text}
              </CardDescription>
            </CardHeader>

            <CardContent>
              {!activeResult ? (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">
                      Your Technical Response:
                    </label>
                    <textarea
                      rows={6}
                      value={currentResponse}
                      onChange={(e) =>
                        setUserResponses((prev) => ({
                          ...prev,
                          [activeTask.id]: e.target.value,
                        }))
                      }
                      placeholder="Write your solution here. Be specific about tools, metrics, architectural trade-offs, and remediation actions..."
                      className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3.5 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 leading-relaxed font-mono"
                    />
                  </div>

                  <div className="flex items-center justify-between pt-2">
                    <span className="text-xs text-slate-400">
                      {currentResponse.length} characters written
                    </span>
                    <Button
                      type="submit"
                      disabled={!currentResponse.trim() || simulateMutation.isPending}
                      className="rounded-xl px-6 gap-2"
                    >
                      <Send className="h-4 w-4" />
                      <span>{simulateMutation.isPending ? "Evaluating Response..." : "Submit to Evaluator"}</span>
                    </Button>
                  </div>
                </form>
              ) : (
                /* Evaluator Feedback Card */
                <div className="space-y-5 animate-in fade-in-50 duration-300">
                  <div className="rounded-2xl border border-emerald-200 dark:border-emerald-900 bg-emerald-50/60 dark:bg-emerald-950/30 p-5">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                        <h4 className="font-bold text-slate-900 dark:text-white text-base">
                          Evaluation Feedback
                        </h4>
                      </div>
                      <div className="flex items-center gap-1.5 bg-emerald-600 text-white px-3 py-1 rounded-full text-xs font-extrabold shadow-xs">
                        <Award className="h-3.5 w-3.5" />
                        <span>{activeResult.score_percent !== null ? `${activeResult.score_percent}%` : "Scored"}</span>
                      </div>
                    </div>

                    <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                      {activeResult.improvement_reasoning ||
                        "Good structural approach to pipeline remediation. The response effectively identified monitoring alerts and horizontal worker autoscaling."}
                    </p>

                    {activeResult.missing_concepts && activeResult.missing_concepts.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-emerald-200/60 dark:border-emerald-900/60">
                        <div className="text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1.5">
                          Concepts to strengthen:
                        </div>
                        <ul className="list-disc list-inside text-xs text-slate-600 dark:text-slate-400 space-y-1">
                          {activeResult.missing_concepts.map((concept, cIdx) => (
                            <li key={cIdx}>{concept}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Actions: Retry or Next */}
                  <div className="flex items-center justify-between pt-2">
                    <Button
                      variant="outline"
                      onClick={handleReset}
                      className="rounded-xl gap-2"
                    >
                      <RotateCcw className="h-3.5 w-3.5" />
                      <span>Refine & Try Again</span>
                    </Button>

                    {activeTaskIndex < tasks.length - 1 && (
                      <Button
                        onClick={() => setActiveTaskIndex(activeTaskIndex + 1)}
                        className="rounded-xl gap-2"
                      >
                        <span>Next Challenge</span>
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default function PathwayRolePage() {
  return (
    <React.Suspense
      fallback={
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-16 space-y-6">
          <Skeleton className="h-10 w-48 rounded-xl" />
          <Skeleton className="h-64 rounded-2xl" />
        </div>
      }
    >
      <PathwayRoleContent />
    </React.Suspense>
  );
}
