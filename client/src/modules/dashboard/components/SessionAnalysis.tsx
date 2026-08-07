import { Loader2, AlertCircle, CheckCircle2 } from "lucide-react";
import useSessionDetail from "../hooks/useSessionDetail";
import { PROCESSING_STEPS } from "../utils/dashboard";
import StatCards from "./StatCards";
import DatasetOverview from "./DatasetOverview";
import ChartsSection from "./ChartsSection";
import NumericSummarySection from "./NumericSummarySection";
import CorrelationSection from "./CorrelationSection";

interface SessionAnalysisProps {
  sessionId: string;
  onSessionReady: () => void;
}

const SessionAnalysis = ({ sessionId, onSessionReady }: SessionAnalysisProps) => {
  const { session, loading, error } = useSessionDetail(sessionId, onSessionReady);

  if (loading && !session) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <Loader2 className="animate-spin text-cyan-400" size={24} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex items-center gap-2 text-red-400 text-sm">
          <AlertCircle size={16} />
          {error}
        </div>
      </div>
    );
  }

  if (!session) return null;

  if (session.status === "processing") {
    const activeIndex = PROCESSING_STEPS.findIndex((s) => s.id === session.currentStep);

    return (
      <div className="flex-1 flex items-center justify-center p-10">
        <div className="w-full max-w-md">
          <div className="mb-7">
            <h2 className="text-xl font-bold text-white mb-1">Analyzing Dataset</h2>
            <p className="text-sm text-zinc-400">{session.originalName}</p>
          </div>

          <div className="rounded-xl bg-zinc-900/40 ring-1 ring-zinc-800 p-5">
            {PROCESSING_STEPS.map((step, i) => {
              const done = i < activeIndex;
              const active = i === activeIndex;
              return (
                <div
                  key={step.id}
                  className={`flex items-center gap-3 py-2 transition-opacity ${
                    done || active ? "opacity-100" : "opacity-35"
                  }`}
                >
                  <div
                    className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                      done
                        ? "bg-gradient-to-br from-teal-400 to-blue-500"
                        : active
                        ? "bg-teal-400/15 ring-1 ring-teal-400"
                        : "bg-zinc-800"
                    }`}
                  >
                    {done && <CheckCircle2 size={14} className="text-zinc-950" />}
                    {active && <Loader2 size={13} className="animate-spin text-teal-300" />}
                  </div>
                  <span
                    className={`text-sm ${
                      done ? "text-white font-medium" : active ? "text-teal-300 font-medium" : "text-zinc-500"
                    }`}
                  >
                    {step.label}
                  </span>
                </div>
              );
            })}
          </div>

          <div className="mt-4 h-1.5 rounded-full bg-zinc-800 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-teal-400 to-blue-500 transition-all duration-500"
              style={{ width: `${session.progress ?? 0}%` }}
            />
          </div>
        </div>
      </div>
    );
  }

  if (session.status === "failed") {
    return (
      <div className="flex-1 flex items-center justify-center p-10">
        <div className="flex items-center gap-2 text-red-400 text-sm">
          <AlertCircle size={16} />
          {session.error || "Analysis failed"}
        </div>
      </div>
    );
  }

  // status === "ready"
  return (
    <div className="flex flex-col min-h-full">
      <div className="px-8 py-5 border-b border-zinc-800/80 flex items-start justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight">{session.originalName}</h1>
          <p className="text-xs text-zinc-500 mt-1">
            Analyzed {new Date(session.updatedAt).toLocaleString("en-IN")}
          </p>
        </div>
        <div className="flex gap-2 flex-wrap">
          <span className="px-2.5 py-1 rounded-md text-xs font-medium bg-zinc-900 ring-1 ring-zinc-800 text-zinc-300">
            {session.datasetProfile?.rowCount?.toLocaleString()} rows
          </span>
          <span className="px-2.5 py-1 rounded-md text-xs font-medium bg-zinc-900 ring-1 ring-zinc-800 text-zinc-300">
            {session.datasetProfile?.columnCount} cols
          </span>
        </div>
      </div>

      <div className="p-8 space-y-6">
        <StatCards profile={session.datasetProfile} />
        <DatasetOverview summary={session.datasetSummary} />
        <ChartsSection charts={session.summaryCharts} />
        <NumericSummarySection
            numericSummary={session.numericSummary}
            statisticsExplanation={session.statisticsExplanation}
        />
        <CorrelationSection correlations={session.correlations} />
        </div>
    </div>
  );
};

export default SessionAnalysis;