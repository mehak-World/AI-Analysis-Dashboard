import { useState } from "react";
import { ChevronDown } from "lucide-react";
import type { NumericColumnSummary } from "../types/dashboard.types";

interface NumericSummarySectionProps {
  numericSummary: Record<string, NumericColumnSummary>;
  statisticsExplanation: Record<string, string>;
}

const NumericSummarySection = ({ numericSummary, statisticsExplanation }: NumericSummarySectionProps) => {
  const [expanded, setExpanded] = useState(false);
  const columns = Object.keys(numericSummary || {});
  if (columns.length === 0) return null;

  return (
    <div className="rounded-xl bg-zinc-900/40 ring-1 ring-zinc-800 p-4 sm:p-6">
      <h2 className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-4">
        Numeric columns, explained
      </h2>

      <div className="space-y-5">
        {columns.map((col) => (
          <div key={col} className="border-b border-zinc-800/60 last:border-0 pb-5 last:pb-0">
            <div className="text-sm font-semibold text-white capitalize mb-2 break-words">
              {col.replace(/_/g, " ")}
            </div>
            <div className="grid sm:grid-cols-2 gap-x-6 gap-y-1.5">
              {["mean", "std", "min", "max"].map((stat) => {
                const text = statisticsExplanation?.[`${col}_${stat}`];
                if (!text) return null;
                return (
                  <p key={stat} className="text-xs text-zinc-400 leading-relaxed">
                    {text}
                  </p>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={() => setExpanded((v) => !v)}
        className="mt-5 flex items-center gap-1.5 text-xs font-medium text-cyan-300 hover:text-cyan-200 transition-colors"
      >
        <ChevronDown size={14} className={`transition-transform ${expanded ? "rotate-180" : ""}`} />
        {expanded ? "Hide" : "Show"} raw statistics table
      </button>

      {expanded && (
        <div className="overflow-x-auto mt-4 -mx-1 sm:mx-0">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b border-zinc-800">
                <th className="sticky left-0 bg-zinc-950 px-3 py-2 text-left text-[10px] font-semibold text-zinc-500 uppercase tracking-widest">
                  Stat
                </th>
                {columns.map((c) => (
                  <th key={c} className="px-3 py-2 text-right text-[11px] font-medium text-zinc-300 whitespace-nowrap">
                    {c}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {["count", "mean", "std", "min", "25%", "50%", "75%", "max"].map((stat, si) => (
                <tr key={stat} className={si % 2 === 0 ? "" : "bg-white/[0.02]"}>
                  <td className="sticky left-0 bg-zinc-950 px-3 py-1.5 text-xs text-zinc-500 font-mono">{stat}</td>
                  {columns.map((col) => {
                    const val = numericSummary[col]?.[stat as keyof NumericColumnSummary];
                    return (
                      <td key={col} className="px-3 py-1.5 text-right text-xs text-zinc-200 font-mono whitespace-nowrap">
                        {typeof val === "number" ? (val > 1000 ? val.toLocaleString() : val.toFixed(2)) : "—"}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default NumericSummarySection;