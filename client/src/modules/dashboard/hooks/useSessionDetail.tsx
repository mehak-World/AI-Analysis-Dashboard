import { useEffect, useRef, useState } from "react";
import { getSessionById } from "../api/api.dashboard";
import type { Session } from "../types/dashboard.types";

const POLL_INTERVAL = 3000;

const useSessionDetail = (sessionId: string | null, onReady?: () => void) => {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchSession = async (id: string) => {
    try {
      const res = await getSessionById(id);
      const data = res?.data?.data;
      setSession(data);
      setError("");
      return data as Session;
    } catch (err: any) {
      setError(err?.message || "Failed to load session");
      return null;
    }
  };

  useEffect(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }

    if (!sessionId) {
      setSession(null);
      return;
    }

    let cancelled = false;
    setLoading(true);

    const startPolling = () => {
      pollRef.current = setInterval(async () => {
        const data = await fetchSession(sessionId);
        if (data && data.status !== "processing") {
          if (pollRef.current) clearInterval(pollRef.current);
          pollRef.current = null;
          if (data.status === "ready") onReady?.();
        }
      }, POLL_INTERVAL);
    };

    fetchSession(sessionId).then((data) => {
      if (cancelled) return;
      setLoading(false);
      if (data?.status === "processing") startPolling();
    });

    return () => {
      cancelled = true;
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [sessionId]);

  return { session, loading, error };
};

export default useSessionDetail;