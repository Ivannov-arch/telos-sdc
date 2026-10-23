import { forwardRef, useId, type InputHTMLAttributes, type SelectHTMLAttributes, type TextareaHTMLAttributes, type ReactNode } from "react";

interface SharedFieldProps {
  label?: ReactNode;
  hint?: ReactNode;
  error?: ReactNode;
  className?: string;
  id?: string;
}

export interface InputProps extends SharedFieldProps, Omit<InputHTMLAttributes<HTMLInputElement>, "id"> {}
export interface TextareaProps extends SharedFieldProps, Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "id"> {}
export interface SelectProps extends SharedFieldProps, Omit<SelectHTMLAttributes<HTMLSelectElement>, "id"> {}

function fieldClasses(className?: string) {
  return ["telos-field", className].filter(Boolean).join(" ");
}

function describedBy(id: string, hint?: ReactNode, error?: ReactNode, additional?: string) {
  return [hint ? `${id}-hint` : "", error ? `${id}-error` : "", additional ?? ""].filter(Boolean).join(" ") || undefined;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, hint, error, className, id, ...props }, ref) {
    const generatedId = useId();
    const controlId = id ?? generatedId;
    return (
      <div className={fieldClasses(className)}>
        {label != null && <label className="telos-field__label" htmlFor={controlId}>{label}</label>}
        <input
          ref={ref}
          id={controlId}
          className="telos-field__control"
          {...props}
          aria-invalid={error ? true : props["aria-invalid"]}
          aria-describedby={describedBy(controlId, hint, error, props["aria-describedby"])}
        />
        {hint != null && <span className="telos-field__hint" id={`${controlId}-hint`}>{hint}</span>}
        {error != null && <span className="telos-field__error" id={`${controlId}-error`} role="alert">{error}</span>}
      </div>
    );
  },
);
Input.displayName = "Input";

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  function Textarea({ label, hint, error, className, id, ...props }, ref) {
    const generatedId = useId();
    const controlId = id ?? generatedId;
    return (
      <div className={fieldClasses(className)}>
        {label != null && <label className="telos-field__label" htmlFor={controlId}>{label}</label>}
        <textarea
          ref={ref}
          id={controlId}
          className="telos-field__control telos-field__control--textarea"
          {...props}
          aria-invalid={error ? true : props["aria-invalid"]}
          aria-describedby={describedBy(controlId, hint, error, props["aria-describedby"])}
        />
        {hint != null && <span className="telos-field__hint" id={`${controlId}-hint`}>{hint}</span>}
        {error != null && <span className="telos-field__error" id={`${controlId}-error`} role="alert">{error}</span>}
      </div>
    );
  },
);
Textarea.displayName = "Textarea";

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  function Select({ label, hint, error, className, id, children, ...props }, ref) {
    const generatedId = useId();
    const controlId = id ?? generatedId;
    return (
      <div className={fieldClasses(className)}>
        {label != null && <label className="telos-field__label" htmlFor={controlId}>{label}</label>}
        <select
          ref={ref}
          id={controlId}
          className="telos-field__control telos-field__control--select"
          {...props}
          aria-invalid={error ? true : props["aria-invalid"]}
          aria-describedby={describedBy(controlId, hint, error, props["aria-describedby"])}
        >
          {children}
        </select>
        {hint != null && <span className="telos-field__hint" id={`${controlId}-hint`}>{hint}</span>}
        {error != null && <span className="telos-field__error" id={`${controlId}-error`} role="alert">{error}</span>}
      </div>
    );
  },
);
Select.displayName = "Select";
