import type { DatasetProfile } from "../types/dashboard.types";

const StatCards = ({ profile }: { profile: DatasetProfile }) => {
  const cards = [
    { label: "Rows", value: profile.rowCount?.toLocaleString(), gradient: "from-teal-400 to-blue-500" },
    { label: "Columns", value: profile.columnCount, gradient: "from-blue-400 to-indigo-500" },
    {
      label: "Missing values",
      value: profile.missingValues?.toLocaleString() ?? 0,
      gradient: profile.missingValues > 0 ? "from-amber-400 to-orange-500" : "from-emerald-400 to-teal-500",
    },
    {
      label: "Duplicate rows",
      value: profile.duplicateRows ?? 0,
      gradient: profile.duplicateRows > 0 ? "from-amber-400 to-orange-500" : "from-emerald-400 to-teal-500",
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
      {cards.map((c) => (
        <div key={c.label} className="relative rounded-xl bg-zinc-900/40 ring-1 ring-zinc-800 px-4 sm:px-5 py-3 sm:py-4 overflow-hidden">
          <div className={`absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r ${c.gradient}`} />
          <div className="text-[10px] font-medium text-zinc-500 uppercase tracking-widest">{c.label}</div>
          <div className="text-xl sm:text-2xl font-bold text-white mt-1 truncate">{c.value ?? "—"}</div>
        </div>
      ))}
    </div>
  );
};

export default StatCards;