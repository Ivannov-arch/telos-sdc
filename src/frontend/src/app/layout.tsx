import type { Metadata } from "next";
import { DM_Sans, Manrope, IBM_Plex_Mono } from "next/font/google";
import { Shell } from "@/components/shell";
import "./globals.css";

const body = DM_Sans({ variable: "--font-body", subsets: ["latin"] });
const display = Manrope({ variable: "--font-display", subsets: ["latin"] });
const code = IBM_Plex_Mono({ variable: "--font-code", subsets: ["latin"], weight: ["400", "500"] });
export const metadata: Metadata = {
  title: { default: "Telos — A future that fits you", template: "%s · Telos" },
  description: "Map your skills, explore roles under AI-disruption scenarios, and practise real workplace tasks. Humane, data-driven career guidance built for SDC XMUM in Malaysia.",
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en" className={`${body.variable} ${display.variable} ${code.variable}`}><body><Shell>{children}</Shell></body></html>;
}
