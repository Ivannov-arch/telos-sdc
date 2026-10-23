import { forwardRef, type HTMLAttributes } from "react";

export type PanelTone = "default" | "soft" | "raised";

export interface PanelProps extends HTMLAttributes<HTMLElement> {
  tone?: PanelTone;
  as?: "section" | "article" | "div";
}

export const Panel = forwardRef<HTMLElement, PanelProps>(
  function Panel({ tone = "default", as: Element = "section", className = "", ...props }, ref) {
    const classes = ["telos-panel", tone === "default" ? "" : `telos-panel--${tone}`, className]
      .filter(Boolean)
      .join(" ");
    return <Element ref={ref as never} className={classes} {...props} />;
  },
);

Panel.displayName = "Panel";
