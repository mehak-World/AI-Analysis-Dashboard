import { Lightbulb, Briefcase } from "lucide-react";
import type { DatasetSummaryInfo } from "../types/dashboard.types";

const DatasetOverview = ({ summary }: { summary: DatasetSummaryInfo }) => {
  if (!summary) return null;

  return (
    <div className="rounded-xl bg-zinc-900/40 ring-1 ring-zinc-800 p-4 sm:p-6 space-y-4 sm:space-y-5">
      <h2 className="text-xs font-semibold text-zinc-400 uppercase tracking-widest">What this data is about</h2>

      {summary.overview && (
        <p className="text-sm text-zinc-200 leading-relaxed">{summary.overview}</p>
      )}

      {summary.businessSummary && (
        <div className="flex gap-3 rounded-lg bg-gradient-to-br from-teal-500/10 to-blue-500/10 ring-1 ring-teal-500/20 p-3 sm:p-4">
          <Briefcase size={16} className="text-teal-300 shrink-0 mt-0.5" />
          <p className="text-sm text-zinc-300 leading-relaxed">{summary.businessSummary}</p>
        </div>
      )}

      {summary.keyFindings?.length > 0 && (
        <div>
          <div className="flex items-center gap-1.5 text-[11px] font-semibold text-zinc-500 uppercase tracking-widest mb-3">
            <Lightbulb size={12} />
            Key findings
          </div>
          <ul className="space-y-2.5">
            {summary.keyFindings.map((finding, i) => (
              <li key={i} className="flex gap-3 text-sm text-zinc-300">
                <span className="shrink-0 w-5 h-5 mt-0.5 rounded-md bg-gradient-to-br from-teal-400/20 to-blue-500/20 ring-1 ring-teal-400/30 flex items-center justify-center text-[10px] font-bold text-teal-300">
                  {i + 1}
                </span>
                <span className="leading-relaxed min-w-0">{finding}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DatasetOverview;