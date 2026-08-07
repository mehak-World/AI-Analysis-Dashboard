export const PROCESSING_STEPS = [
  { id: "eda", label: "Exploratory analysis" },
  { id: "charts", label: "Generating charts" },
  { id: "ai", label: "AI insights" },
  { id: "completed", label: "Finalizing" },
];

export const CHART_COLORS = ["#2dd4bf", "#3b82f6", "#a78bfa", "#f472b6", "#fbbf24", "#34d399"];

export const correlationStrength = (value: number) => {
  const abs = Math.abs(value);
  if (abs >= 0.7) return { label: "Strong", className: "text-teal-400 bg-teal-500/10 ring-teal-500/20" };
  if (abs >= 0.4) return { label: "Moderate", className: "text-amber-400 bg-amber-500/10 ring-amber-500/20" };
  return { label: "Weak", className: "text-zinc-400 bg-zinc-500/10 ring-zinc-500/20" };
};