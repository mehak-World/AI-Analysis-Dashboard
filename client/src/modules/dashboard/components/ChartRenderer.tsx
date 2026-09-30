import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ScatterChart,
  Scatter,
  PieChart,
  Pie,
} from "recharts";
import { CHART_COLORS } from "../utils/dashboard";
import type { Chart } from "../types/dashboard.types";

const TOOLTIP_STYLE = {
  contentStyle: {
    background: "#18181b",
    border: "1px solid #3f3f46",
    borderRadius: 8,
    fontSize: 12,
    color: "#fafafa",
  },
  labelStyle: { color: "#a1a1aa" },
  itemStyle: { color: "#fafafa" },
};

const AXIS_TICK = {
  fontSize: 10,
  fill: "#a1a1aa",
};

const BarChartRenderer = ({
  chart,
  index,
}: {
  chart: Chart;
  index: number;
}) => {
  const xKey = chart.config?.xKey || "label";
  const yKey = chart.config?.yKey || "value";
  const isHistogram = chart.type === "histogram";
  const xDataKey = isHistogram ? "binStart" : xKey;

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart
        data={chart.data}
        margin={{
          top: 4,
          right: 8,
          left: -16,
          bottom: isHistogram ? 40 : 8,
        }}
      >
        <XAxis
          dataKey={xDataKey}
          tick={AXIS_TICK}
          angle={isHistogram ? -35 : 0}
          textAnchor={isHistogram ? "end" : "middle"}
          interval={0}
        />

        <YAxis tick={AXIS_TICK} width={40} />

        <Tooltip {...TOOLTIP_STYLE} />

        <Bar
          dataKey={isHistogram ? "count" : yKey}
          radius={[3, 3, 0, 0]}
        >
          {chart.data.map((_, i) => (
            <Cell
              key={i}
              fill={CHART_COLORS[index % CHART_COLORS.length]}
              fillOpacity={0.85}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

const ScatterChartRenderer = ({
  chart,
  index,
}: {
  chart: Chart;
  index: number;
}) => {
  const xKey = chart.config?.xKey || "x";
  const yKey = chart.config?.yKey || "y";

  return (
    <ResponsiveContainer width="100%" height={220}>
      <ScatterChart
        margin={{
          top: 4,
          right: 8,
          left: 8,
          bottom: 8,
        }}
      >
        <XAxis
          dataKey={xKey}
          name={xKey}
          tick={AXIS_TICK}
        />

        <YAxis
          dataKey={yKey}
          name={yKey}
          tick={AXIS_TICK}
          width={44}
        />

        <Tooltip
          {...TOOLTIP_STYLE}
          cursor={{
            strokeDasharray: "3 3",
            stroke: "#52525b",
          }}
        />

        <Scatter
          data={chart.data}
          fill={CHART_COLORS[index % CHART_COLORS.length]}
          fillOpacity={0.7}
        />
      </ScatterChart>
    </ResponsiveContainer>
  );
};

const PieChartRenderer = ({ chart }: { chart: Chart }) => {
  const nameKey =
    chart.config?.nameKey ||
    chart.config?.xKey ||
    "name";

  const dataKey =
    chart.config?.dataKey ||
    "count";

  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie
          data={chart.data}
          dataKey={dataKey}
          nameKey={nameKey}
          cx="50%"
          cy="50%"
          outerRadius={75}
          label={({ name, percent }) =>
            `${name ?? ""} (${((percent ?? 0) * 100).toFixed(0)}%)`
          }
          labelLine={{
            stroke: "#71717a",
            strokeWidth: 1,
          }}
        >
          {chart.data.map((_: any, i: any) => (
            <Cell
              key={i}
              fill={CHART_COLORS[i % CHART_COLORS.length]}
            />
          ))}
        </Pie>

        <Tooltip {...TOOLTIP_STYLE} />
      </PieChart>
    </ResponsiveContainer>
  );
};

// ─── Boxplot ────────────────────────────────────────────────────────
// Recharts has no built-in boxplot, so this is drawn as raw SVG from
// { min, q1, median, q3, max } — the shape your backend sends for chart.data[0].
const BoxplotRenderer = ({
  chart,
  index,
}: {
  chart: Chart;
  index: number;
}) => {
  const d = chart.data?.[0] as
    | {
        min: number;
        q1: number;
        median: number;
        q3: number;
        max: number;
      }
    | undefined;

  if (!d) {
    return (
      <div className="text-xs text-zinc-500 py-6 text-center">
        No data available
      </div>
    );
  }

  const {
    min,
    q1,
    median,
    q3,
    max,
  } = d;

  const color =
    CHART_COLORS[index % CHART_COLORS.length];

  const W = 320;
  const H = 150;
  const PAD = 44;
  const midY = H / 2;

  const range = max - min || 1;

  const scale = (v: number) =>
    PAD +
    ((v - min) / range) *
      (W - PAD * 2);

  const fmt = (v: number) =>
    v >= 1000
      ? `${(v / 1000).toFixed(1)}k`
      : Number.isInteger(v)
        ? v
        : v.toFixed(2);

  const points = [
    { v: min, label: "Min" },
    { v: q1, label: "Q1" },
    { v: median, label: "Median" },
    { v: q3, label: "Q3" },
    { v: max, label: "Max" },
  ];

  return (
    <div className="flex justify-center py-4">
      <svg
        width={W}
        height={H}
        style={{ overflow: "visible" }}
      >
        {/* Whisker line */}
        <line
          x1={scale(min)}
          y1={midY}
          x2={scale(max)}
          y2={midY}
          stroke="#52525b"
          strokeWidth={2}
        />

        {/* Min/max caps */}
        {[min, max].map((v, i) => (
          <line
            key={i}
            x1={scale(v)}
            y1={midY - 12}
            x2={scale(v)}
            y2={midY + 12}
            stroke="#71717a"
            strokeWidth={2}
          />
        ))}

        {/* IQR box */}
        <rect
          x={scale(q1)}
          y={midY - 20}
          width={scale(q3) - scale(q1)}
          height={40}
          fill={color}
          fillOpacity={0.2}
          stroke={color}
          strokeWidth={2}
          rx={4}
        />

        {/* Median line */}
        <line
          x1={scale(median)}
          y1={midY - 20}
          x2={scale(median)}
          y2={midY + 20}
          stroke={color}
          strokeWidth={3}
        />

        {/* Labels */}
        {points.map(({ v, label }) => (
          <g key={label}>
            <text
              x={scale(v)}
              y={midY + 38}
              textAnchor="middle"
              fontSize={9}
              fill="#a1a1aa"
            >
              {label}
            </text>

            <text
              x={scale(v)}
              y={midY - 28}
              textAnchor="middle"
              fontSize={9}
              fill="#fafafa"
              fontWeight={600}
            >
              {fmt(v)}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
};

export const renderChart = (
  chart: Chart,
  index: number
) => {
  if (!chart.data?.length) {
    return (
      <div className="text-xs text-zinc-500 py-6 text-center">
        No data available
      </div>
    );
  }

  switch (chart.type) {
    case "histogram":
    case "bar":
      return (
        <BarChartRenderer
          chart={chart}
          index={index}
        />
      );

    case "scatter":
      return (
        <ScatterChartRenderer
          chart={chart}
          index={index}
        />
      );

    case "pie":
      return (
        <PieChartRenderer
          chart={chart}
        />
      );

    case "boxplot":
      return (
        <BoxplotRenderer
          chart={chart}
          index={index}
        />
      );

    default:
      return (
        <div className="text-xs text-zinc-500 py-6 text-center">
          Chart type "{chart.type}" not supported yet
        </div>
      );
  }
};