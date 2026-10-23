"use client";

import Link from "next/link";
import { ErrorState, PageIntro } from "@/components/ui";

export default function PageError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return <><PageIntro eyebrow="A MOMENT TO REGROUP" title="Your path is still here." description="We hit an unexpected interruption while opening this page. Try again, or return to the overview." /><ErrorState message={error.message || "We couldn’t open this page right now."} retry={reset} /><Link className="text-link" href="/">Return to the observatory</Link></>;
}
