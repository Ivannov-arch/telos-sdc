"use client";

import * as React from "react";
import { SDG_METADATA } from "@/lib/sdg-data";
import { SdgAlignment } from "@/lib/api";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { ExternalLink, Award, Sparkles, CheckCircle2 } from "lucide-react";

interface SdgBadgeProps {
  alignment?: SdgAlignment;
  goalNumber?: number;
  variant?: "badge" | "pill" | "detailed";
  className?: string;
}

export function SdgBadge({
  alignment,
  goalNumber,
  variant = "badge",
  className = "",
}: SdgBadgeProps) {
  const goal = alignment?.sdg_goal ?? goalNumber ?? 8;
  const meta = SDG_METADATA[goal] || {
    goal,
    name: alignment?.sdg_name || `SDG ${goal}`,
    color: alignment?.color_hex || "#A21942",
    shortDesc: "UN Sustainable Development Goal",
    icon: "Target",
  };

  const color = alignment?.color_hex || meta.color;
  const target = alignment?.target || `Target ${goal}.1`;
  const reasoning =
    alignment?.impact_reasoning ||
    "Contributes directly to inclusive economic productivity and ethical technological upskilling.";
  const source = alignment?.source || "UNSD SDG API";

  return (
    <Dialog>
      <DialogTrigger asChild>
        <button
          type="button"
          aria-label={`View SDG ${goal}: ${meta.name}`}
          className={`group relative inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold text-white shadow-xs transition-all duration-200 hover:scale-105 hover:shadow-md cursor-pointer ${className}`}
          style={{ backgroundColor: color }}
        >
          <span className="flex h-4 w-4 items-center justify-center rounded-full bg-white/25 text-[10px] font-bold">
            {goal}
          </span>
          <span className="truncate max-w-[130px] font-medium tracking-tight">
            {meta.name}
          </span>
          <span className="opacity-70 group-hover:opacity-100 transition-opacity">
            ⓘ
          </span>
        </button>
      </DialogTrigger>

      <DialogContent className="sm:max-w-md border-0 p-0 overflow-hidden rounded-2xl shadow-2xl">
        <div
          className="p-6 text-white"
          style={{
            background: `linear-gradient(135deg, ${color} 0%, ${color}dd 100%)`,
          }}
        >
          <div className="flex items-center justify-between">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/20 px-3 py-1 text-xs font-medium backdrop-blur-xs">
              <Award className="h-3.5 w-3.5" />
              <span>United Nations Sustainable Development Goal</span>
            </div>
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-base font-extrabold shadow-sm" style={{ color }}>
              {goal}
            </div>
          </div>
          <DialogTitle className="mt-4 text-2xl font-bold text-white tracking-tight">
            SDG {goal}: {meta.name}
          </DialogTitle>
          <p className="mt-1 text-sm text-white/90 font-normal leading-relaxed">
            {meta.shortDesc}
          </p>
        </div>

        <div className="p-6 space-y-4 bg-white dark:bg-slate-900">
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
              Aligned Target
            </div>
            <div className="flex items-center gap-2">
              <span
                className="inline-flex items-center gap-1 rounded-md px-2.5 py-0.5 text-xs font-bold text-white"
                style={{ backgroundColor: color }}
              >
                Target {target}
              </span>
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Audited Workforce Contribution
              </span>
            </div>
          </div>

          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1 flex items-center gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-indigo-500" />
              Impact Rationale
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-slate-800/60 p-3.5 rounded-xl border border-slate-100 dark:border-slate-800">
              {reasoning}
            </p>
          </div>

          <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
              <span>
                Audited & Curated Source: <strong className="text-slate-700 dark:text-slate-200">{source}</strong>
              </span>
            </div>
            <a
              href={`https://sdgs.un.org/goals/goal${goal}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 font-medium hover:underline"
            >
              <span>UNSD Portal</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
