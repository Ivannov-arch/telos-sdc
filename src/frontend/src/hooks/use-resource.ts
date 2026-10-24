"use client";

import { useCallback, useEffect, useState } from "react";

export function useResource<T>(load: () => Promise<T>) {
  const [state, setState] = useState<{ data: T | null; error: string | null; loading: boolean }>({ data: null, error: null, loading: true });
  const [version, setVersion] = useState(0);
  const retry = useCallback(() => setVersion((v) => v + 1), []);
  useEffect(() => {
    let live = true;
    Promise.resolve().then(() => {
      if (live) setState({ data: null, error: null, loading: true });
      return load();
    }).then((data) => { if (live) setState({ data, error: null, loading: false }); })
      .catch((error: unknown) => { if (live) setState({ data: null, error: error instanceof Error ? error.message : "We couldn’t load this information. Please try again.", loading: false }); });
    return () => { live = false; };
  }, [load, version]);
  return { ...state, retry };
}
