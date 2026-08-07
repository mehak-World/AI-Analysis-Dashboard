import { useState } from "react";
import { correlationStrength } from "../utils/dashboard";
import type { Correlation } from "../types/dashboard.types";

const CorrelationSection = ({ correlations }: { correlations: Correlation[] }) => {
  const [tooltip, setTooltip] = useState<{ x: number; y: number; a: string; b: string; v: number } | null>(null);

  if (!correlations?.length) return null;

  const cols = [...new Set(correlations.flatMap((c) => [c.columnA, c.columnB]))];
  const getValue = (a: string, b: string) => {
    if (a === b) return 1;
    return correlations.find((c) => (c.columnA === a && c.columnB === b) || (c.columnA === b && c.columnB === a))?.value ?? 0;
  };
  const getColor = (v: number) => {
    const abs = Math.abs(v);
    if (v > 0) return `rgba(45, 212, 191, ${0.15 + abs * 0.7})`; // teal
    return `rgba(96, 165, 250, ${0.15 + abs * 0.7})`; // blue
  };
  const cellSize = Math.max(24, Math.min(40, Math.floor(400 / cols.length)));
  const labelW = 90;
  const size = labelW + cols.length * cellSize + 10;

  return (
    <div className="rounded-xl bg-zinc-900/40 ring-1 ring-zinc-800 p-6">
      <h2 className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-1">How columns relate</h2>
      <p className="text-xs text-zinc-500 mb-5">Teal = moves together · Blue = moves oppositely · darker = stronger</p>

      <div className="overflow-auto mb-6">
        <svg width={size} height={size} style={{ fontFamily: "inherit" }}>
          {cols.map((col, ci) => (
            <text
              key={col}
              x={labelW + ci * cellSize + cellSize / 2}
              y={labelW - 6}
              textAnchor="end"
              fontSize={9}
              fill="#a1a1aa"
              transform={`rotate(-40, ${labelW + ci * cellSize + cellSize / 2}, ${labelW - 6})`}
            >
              {col}
            </text>
          ))}
          {cols.map((row, ri) => (
            <text key={row} x={labelW - 8} y={labelW + ri * cellSize + cellSize / 2 + 3} textAnchor="end" fontSize={9} fill="#a1a1aa">
              {row}
            </text>
          ))}
          {cols.map((row, ri) =>
            cols.map((col, ci) => {
              const v = getValue(col, row);
              return (
                <rect
                  key={`${col}-${row}`}
                  x={labelW + ci * cellSize}
                  y={labelW + ri * cellSize}
                  width={cellSize - 2}
                  height={cellSize - 2}
                  rx={4}
                  fill={getColor(v)}
                  style={{ cursor: "pointer" }}
                  onMouseEnter={(e) => setTooltip({ x: e.clientX, y: e.clientY, a: col, b: row, v })}
                  onMouseLeave={() => setTooltip(null)}
                />
              );
            })
          )}
        </svg>
        {tooltip && (
          <div
            className="fixed z-50 bg-zinc-900 ring-1 ring-zinc-700 rounded-lg px-3 py-2 text-xs pointer-events-none"
            style={{ left: tooltip.x + 12, top: tooltip.y + 12 }}
          >
            <span className="text-white">{tooltip.a}</span> <span className="text-zinc-500">×</span>{" "}
            <span className="text-white">{tooltip.b}</span>
            <br />
            <span className="font-bold text-teal-300">{tooltip.v.toFixed(2)}</span>
          </div>
        )}
      </div>

      <div className="space-y-3">
        {correlations.map((c) => {
          const strength = correlationStrength(c.value);
          return (
            <div key={`${c.columnA}-${c.columnB}`} className="flex gap-3 items-start">
              <span className={`shrink-0 mt-0.5 px-2 py-0.5 rounded-full text-[10px] font-semibold ring-1 ${strength.className}`}>
                {strength.label}
              </span>
              <p className="text-xs text-zinc-400 leading-relaxed">{c.explanation}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CorrelationSection;