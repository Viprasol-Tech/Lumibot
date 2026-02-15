import { useState, useEffect, useCallback } from "react";

export default function useFetch(fetcher, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(() => {
    setLoading(true);
    fetcher()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, deps);

  useEffect(load, [load]);

  return { data, loading, error, reload: load };
}
