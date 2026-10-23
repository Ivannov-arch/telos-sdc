"use client";

import * as React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { getSimulationTasks, SimulationTask } from "@/lib/api";
import { Route, Sparkles, ArrowRight, BookOpen, Layers } from "lucide-react";

export default function PathwayIndexPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["all-simulation-tasks"],
    queryFn: () => getSimulationTasks(undefined, 20),
  });

  const tasks = data?.tasks || [];

  const sampleRoles = [
    { id: "e44d3ba1-3836-4d04-8b6b-3aa83984ca3b", title: "AI / Machine Learning Engineer", tasksCount: 3, level: "Advanced" },
    { id: "2d1f0412-3fba-4a62-87c2-8fe2679958ee", title: "Data Platform Architect", tasksCount: 4, level: "Intermediate" },
    { id: "f1a141b2-c0e4-4d89-bf83-05b1f8eb6c30", title: "Cloud Systems & DevOps Engineer", tasksCount: 2, level: "Intermediate" },
  ];

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10 md:py-16">
      <div className="text-center max-w-2xl mx-auto mb-12">
        <Badge variant="secondary" className="mb-3">
          Feature 4: Reskilling Pathways
        </Badge>
        <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
          Micro-Task Reskilling Pathways
        </h1>
        <p className="mt-3 text-slate-600 dark:text-slate-400">
          Bridging the gap between static career recommendations and verified practical execution. Choose a role or tackle standalone scenario simulations below.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {sampleRoles.map((role) => (
          <Card key={role.id} className="hover:border-indigo-400/60 hover:shadow-md transition-all flex flex-col justify-between">
            <CardHeader>
              <div className="flex items-center justify-between mb-1">
                <Badge variant="outline" className="text-[10px]">{role.level}</Badge>
                <span className="text-xs text-slate-400 font-mono">{role.tasksCount} Tasks</span>
              </div>
              <CardTitle className="text-lg">{role.title}</CardTitle>
              <CardDescription>
                Targeted problem scenarios covering core skill gaps.
              </CardDescription>
            </CardHeader>
            <CardFooter>
              <Link href={`/pathway/${encodeURIComponent(role.id)}?role_name=${encodeURIComponent(role.title)}`} className="w-full">
                <Button variant="default" className="w-full rounded-xl gap-2">
                  <span>Enter Pathway</span>
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </CardFooter>
          </Card>
        ))}
      </div>

      {/* Available Scenarios Pool */}
      <div className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/40 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Layers className="h-4 w-4 text-indigo-500" />
            <span>Available Simulation Scenarios Pool</span>
          </h2>
          <span className="text-xs text-slate-400">Seeded from O*NET Statements</span>
        </div>

        {isLoading ? (
          <div className="space-y-3">
            <Skeleton className="h-16 rounded-xl" />
            <Skeleton className="h-16 rounded-xl" />
          </div>
        ) : tasks.length === 0 ? (
          <p className="text-sm text-slate-500 py-4">
            No custom tasks loaded in DB yet. You can still test the primary pathway with our pre-configured scenario.
          </p>
        ) : (
          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/60"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-[10px]">{task.difficulty || "Standard"}</Badge>
                    {task.onet_task_ref && (
                      <span className="text-[10px] font-mono text-slate-400">{task.onet_task_ref}</span>
                    )}
                  </div>
                  <p className="text-xs text-slate-700 dark:text-slate-300 line-clamp-2">
                    {task.scenario_text}
                  </p>
                </div>
                <Link href={`/pathway/${encodeURIComponent(task.skill_id)}?role_name=Simulation+Challenge`}>
                  <Button size="sm" variant="outline" className="rounded-xl shrink-0">
                    Solve Task
                  </Button>
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
