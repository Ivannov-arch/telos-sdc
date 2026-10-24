---
name: Next 16 / Turbopack dev quirks in this project
description: Non-obvious behaviors of the Next.js 16 + Tailwind v4 frontend dev setup that cost several attempts to diagnose.
---

- The page never hydrates (stuck on loading skeletons, no errors) when the HMR websocket is blocked. Turbopack's dev runtime waits for the HMR connection before hydrating. Any origin used to test (including 127.0.0.1 for headless checks) must be in `allowedDevOrigins`.
  **Why:** two rounds of screenshots showed skeletons while the user's preview worked fine.
- CSS Modules silently become plain CSS (classes export as undefined) because the Tailwind v4 Turbopack rule matches `*.css` including `*.module.css`. Use global classes in globals.css.
- Turbopack's persistent cache in `src/frontend/.next` can keep serving stale globals.css across restarts; `rm -rf src/frontend/.next` then restart.
- Headless verification that works here: `chromium --headless=new --remote-debugging-port` driven over CDP with a small Node script (see /tmp pattern: Page.navigate, wait, Runtime.evaluate innerText). `--dump-dom` alone captures pre-hydration HTML.
