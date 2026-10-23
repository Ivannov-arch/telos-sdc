# Telos Blue design-system guidance

This package is a reusable visual foundation extracted from Aiversecity's Telos frontend. It is not an application, route, or screen. Keep future work within the design-system boundary unless a screen application is separately approved.

## Setup and import order

1. Link the local package from the consuming project. From `src/frontend`, run
   `npm install ../../artifacts/telos-blue`; from the mockup sandbox, use
   `npm install ../telos-blue`. Keep the local path dependency so this private
   package remains inside the repository.
2. Import `@aiversecity/telos-blue/styles.css` once at the application entry point, after any CSS reset and before local component overrides.
3. Import the primitives from `@aiversecity/telos-blue` or their documented component subpath.
4. Keep existing font loading in the host project. This system specifies DM Sans for body copy, Manrope for display/headings, and IBM Plex Mono for utility/code text; its CSS includes robust fallback stacks and does not fetch fonts itself.

For the Next.js frontend, add `"@aiversecity/telos-blue"` to
`transpilePackages` in `next.config.ts` because this package exports TypeScript
source. Do this only when applying the system to the app.

```tsx
import "@aiversecity/telos-blue/styles.css";
import { Badge, Button, Input, Panel } from "@aiversecity/telos-blue";
```

## Token mapping and hue method

The source palette came from `src/frontend/src/app/globals.css`. Brand colors were transformed in HSV by changing hue only to 220° and preserving each source token's saturation and value exactly. The exact resulting hex values are:

| Source role | Original | Telos Blue |
| --- | --- | --- |
| background | `#f3f6f0` | `#f0f2f6` |
| foreground | `#163c38` | `#16233c` |
| surface | `#fafcf7` | `#f7f9fc` |
| muted | `#6b7d74` | `#6b717d` |
| line | `#dce4d8` | `#d8dce4` |
| petrol / primary | `#164c43` | `#16284c` |
| lime / accent | `#d6ef84` | `#84a8ef` |
| mint / soft | `#e4ece1` | `#e1e5ec` |
| coral / secondary | `#bc583d` | `#3d67bc` |

Use `--petrol` for primary actions, `--lime` for selected emphasis, `--mint` for gentle surfaces, and `--coral` for secondary emphasis and focus indication. `--background`, `--surface`, `--foreground`, `--muted`, and `--line` are semantic foundation roles. Do not reassign those roles to unrelated meanings.

Visualization values are purposefully separate from brand hues: `--viz-sdg-1`, `--viz-sdg-2`, and `--viz-sdg-3` retain the source chart colors. Add additional visualization tokens as data semantics, not as new brand aliases.

## Typography, spacing, and shape

- Body: DM Sans; display and headings: Manrope; utility/code labels: IBM Plex Mono.
- Type scale uses `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--text-xl`, `--text-2xl`, and responsive `--text-display`.
- Spacing tokens follow the source interface's compact, deliberate rhythm: `--space-1` through `--space-12`.
- Use the small, medium, large, and pill radii (`--radius-sm` through `--radius-pill`) in proportion to component purpose.
- Borders should use `--line`; elevations are intentionally soft and tinted (`--elevation-1`, `--elevation-2`). Prefer border and surface contrast over heavy shadows.

## Components and conventions

- `Button` is a native button with typed `primary`, `accent`, `secondary`, and `quiet` variants and `small`, `medium`, and `large` sizes. Use `type="submit"` only for form submission; its default is `button`.
- `Panel` is a semantic section by default. Choose `article` or `div` through `as` where that better describes the content, and `default`, `soft`, or `raised` tone according to hierarchy.
- `Badge` is a non-interactive inline label. It is not a button or a status workflow.
- `Input`, `Textarea`, and `Select` are native controls. They accept native attributes and optional `label`, `hint`, and `error` props, associate labels and descriptions, and render error text as an alert.
- Components forward refs and accept `className` for restrained local composition. Keep behavior and domain-specific workflows in the consuming application.
- Preserve useful native semantics; do not style non-interactive elements to imply actions.

## Accessibility

- Keep all controls keyboard-operable and retain `:focus-visible` indicators. Do not remove outlines without a clearly visible equivalent.
- Give icon-only controls an accessible name in the consuming application. Use visible labels whenever practical.
- Associate help and error text with its field; use concise, actionable errors.
- Maintain adequate text/background contrast and never communicate status by color alone.
- Honor reduced-motion preferences. Component transitions are brief and limited to subtle feedback.
- Preserve native disabled behavior and do not use disabled styling as a substitute for explaining unavailable actions.

## Scope rule

This package contains tokens, reusable primitives, documentation, and a component/token preview only. Do not move, edit, re-home, or apply it to an existing screen or mockup. Any application of this system to a screen must be separately approved.
