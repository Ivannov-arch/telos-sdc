import type { Metadata } from "next";
import * as React from "react";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Telos / Aiversecity — Future-Ready Workforce Matching & SDG Engine",
  description:
    "AI-powered workforce transition platform integrating RRF hybrid search, ESCO skill gap analysis, micro-task simulations, and United Nations Sustainable Development Goals (SDG) alignment.",
  keywords: [
    "Workforce Transition",
    "ESCO Taxonomy",
    "UN SDG",
    "SDC XMUM",
    "Skill Gap Analysis",
    "BGE-M3",
    "pgvector",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-screen bg-slate-50/50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col font-sans antialiased selection:bg-indigo-500 selection:text-white`}
      >
        <Providers>
          <React.Suspense fallback={<div className="h-16 w-full border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-950/80" />}>
            <Navbar />
          </React.Suspense>
          <main className="flex-1">{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
