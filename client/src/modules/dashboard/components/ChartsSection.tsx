import { Sparkles, TrendingUp } from "lucide-react";
import { renderChart } from "./ChartRenderer";
import type { Chart } from "../types/dashboard.types";

const ChartsSection = ({ charts }: { charts: Chart[] }) => {
  const visible = charts?.filter((c) => c.type !== "heatmap" && c.data?.length > 0) ?? [];

  if (visible.length === 0) return null;

  return (
    <div>
      <h2 className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-3">Charts</h2>
      <div
        className="grid gap-4 sm:gap-5"
        style={{ gridTemplateColumns: "repeat(auto-fill, minmax(min(100%, 340px), 1fr))" }}
      >
        {visible.map((chart, i) => (
          <div key={chart.id} className="min-w-0 rounded-xl bg-zinc-900/40 ring-1 ring-zinc-800 overflow-hidden">
            <div className="px-4 sm:px-5 pt-4 sm:pt-5 pb-2">
              <div className="text-sm font-semibold text-white capitalize">
                {chart.name?.replace(/_/g, " ")}
              </div>
              {chart.reason && (
                <p className="text-xs text-zinc-500 mt-1 leading-relaxed">{chart.reason}</p>
              )}
            </div>

            <div className="px-2 sm:px-3">{renderChart(chart, i)}</div>

            {chart.summary && (
              <div className="px-4 sm:px-5 pt-3 flex gap-2">
                <Sparkles size={13} className="text-cyan-400 shrink-0 mt-0.5" />
                <p className="text-xs text-zinc-400 leading-relaxed">{chart.summary}</p>
              </div>
            )}

            {chart.insight && (
              <div className="mx-3 sm:mx-4 mt-3 mb-4 rounded-lg bg-gradient-to-br from-teal-500/10 to-blue-500/10 ring-1 ring-teal-500/20 px-3 sm:px-4 py-3 flex gap-2.5">
                <TrendingUp size={14} className="text-teal-300 shrink-0 mt-0.5" />
                <p className="text-xs text-zinc-300 leading-relaxed">{chart.insight}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChartsSection;