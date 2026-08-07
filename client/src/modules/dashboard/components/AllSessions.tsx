import { formatDistanceToNow } from "date-fns";
import {
  FileText,
  CheckCircle2,
  Loader2,
  AlertCircle,
  Clock,
  Sparkles,
  Plus,
} from "lucide-react";
import { useEffect, useRef } from "react";
import type { AllSessionsRes } from "../types/dashboard.types";

interface AllSessionsProps {
  sessions: AllSessionsRes[];
  loading: boolean;
  pagination: { page: number; limit: number; total: number };
  setPagination: (updater: (prev: any) => any) => void;
  selectedSessionId: string | null;
  onSelectSession: (id: string) => void;
  onNewSession: () => void;
}

const AllSessions = ({
  sessions,
  loading,
  pagination,
  setPagination,
  selectedSessionId,
  onSelectSession,
  onNewSession,
}: AllSessionsProps) => {
  const loaderRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !loading && sessions.length < pagination.total) {
          setPagination((prev) => ({ ...prev, page: prev.page + 1 }));
        }
      },
      { threshold: 0.5 }
    );
    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => observer.disconnect();
  }, [loading, sessions.length, pagination.total, setPagination]);

  const getStatus = (status: string) => {
    switch (status) {
      case "ready":
        return { icon: <CheckCircle2 size={12} />, text: "Ready", className: "text-emerald-400" };
      case "processing":
        return { icon: <Loader2 size={12} className="animate-spin" />, text: "Processing", className: "text-cyan-300" };
      case "failed":
        return { icon: <AlertCircle size={12} />, text: "Failed", className: "text-red-400" };
      default:
        return { icon: <Clock size={12} />, text: "Queued", className: "text-amber-400" };
    }
  };

  return (
    <aside className="w-72 h-screen bg-zinc-950 border-r border-zinc-800/80 flex flex-col shrink-0">
      {/* Header */}
      <div className="px-4 py-4 border-b border-zinc-800/80">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center shrink-0">
            <Sparkles size={13} className="text-zinc-950" />
          </div>
          <span className="text-sm font-semibold text-white tracking-tight">DataLens</span>
        </div>

        <button
          onClick={onNewSession}
          className="w-full py-2 rounded-lg text-sm font-medium text-zinc-950 bg-gradient-to-r from-teal-400 to-blue-500 hover:opacity-90 transition-opacity flex items-center justify-center gap-1.5"
        >
          <Plus size={15} />
          New Analysis
        </button>
      </div>

      {/* Compact session list */}
      <div className="flex-1 overflow-y-auto py-1">
        {sessions.length === 0 && !loading && (
          <div className="px-4 py-6 text-xs text-zinc-600 text-center">No analyses yet</div>
        )}

        {sessions.map((session) => {
          const badge = getStatus(session.status);
          const active = selectedSessionId === session._id;

          return (
            <button
              key={session._id}
              onClick={() => onSelectSession(session._id)}
              className={`w-full text-left px-4 py-2.5 flex items-center gap-2.5 border-l-2 transition-colors ${
                active
                  ? "bg-zinc-900 border-l-teal-400"
                  : "border-l-transparent hover:bg-zinc-900/60"
              }`}
            >
              <FileText size={14} className="text-cyan-300 shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-white truncate">{session.originalName}</p>
                <div className={`flex items-center gap-1 text-[10px] mt-0.5 ${badge.className}`}>
                  {badge.icon}
                  <span>{badge.text}</span>
                  <span className="text-zinc-600">·</span>
                  <span className="text-zinc-600">
                    {formatDistanceToNow(new Date(session.updatedAt), { addSuffix: true })}
                  </span>
                </div>
              </div>
            </button>
          );
        })}

        <div ref={loaderRef} className="py-4 flex justify-center">
          {loading && <Loader2 className="animate-spin text-cyan-400" size={16} />}
        </div>
      </div>
    </aside>
  );
};

export default AllSessions;