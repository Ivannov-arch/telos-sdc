import { forwardRef, type HTMLAttributes } from "react";

export type BadgeTone = "neutral" | "brand" | "accent" | "soft";

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: BadgeTone;
}

export const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  function Badge({ tone = "neutral", className = "", ...props }, ref) {
    const classes = ["telos-badge", tone !== "neutral" ? `telos-badge--${tone}` : "", className]
      .filter(Boolean)
      .join(" ");
    return <span ref={ref} className={classes} {...props} />;
  },
);

Badge.displayName = "Badge";
