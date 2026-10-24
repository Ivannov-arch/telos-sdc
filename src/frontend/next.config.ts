import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Replit serves the dev server through a proxied iframe on a different host.
  // 127.0.0.1 is included so local smoke tests and screenshots hydrate (HMR must connect first).
  allowedDevOrigins: ["127.0.0.1", "*.replit.dev", "**.replit.dev", "*.replit.app", "**.replit.app", "*.repl.co", "**.repl.co"],
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
