import { forwardRef, type ButtonHTMLAttributes } from "react";

export type ButtonVariant = "primary" | "accent" | "secondary" | "quiet";
export type ButtonSize = "small" | "medium" | "large";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  function Button({ variant = "primary", size = "medium", className = "", type = "button", ...props }, ref) {
    const classes = ["telos-button", `telos-button--${variant}`, size !== "medium" ? `telos-button--${size}` : "", className]
      .filter(Boolean)
      .join(" ");

    return <button ref={ref} type={type} className={classes} {...props} />;
  },
);

Button.displayName = "Button";
