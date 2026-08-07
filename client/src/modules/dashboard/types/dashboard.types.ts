export type AllSessionsRes = {
  _id: string;
  originalName: string;
  currentStep: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  progress: number;
};

// ── Shared small pieces ─────────────────────────────────────────────

export type AxisMeta = {
  label: string;
  unit: string;
};

export type ChartConfig = {
  xKey?: string | null;
  yKey?: string | null;
  nameKey?: string;
  dataKey?: string;
  aggregation?: string;
  sort?: string;
  options?: Record<string, number | string>;
};

export type Chart = {
  id: string;
  name: string;
  type: "bar" | "histogram" | "scatter" | "pie" | "boxplot" | "heatmap" | string;
  reason?: string;
  config?: ChartConfig;
  data: Record<string, any>[];
  xAxis?: AxisMeta;
  yAxis?: AxisMeta;
  summary?: string;
  insight?: string;
  statistics?: Record<string, number | string | Record<string, any>>;
};

export type ColumnMetadata = {
  name: string;
  dtype: string;
  unit: string;
  description: string;
  category: string;
  exampleValues: string[];
};

export type DatasetProfile = {
  rowCount: number;
  columnCount: number;
  columns: string[];
  dtypes: Record<string, string>;
  nullPercents: Record<string, number>;
  duplicateRows: number;
  datasetSizeMB: number;
  numericColumns: number;
  categoricalColumns: number;
  datetimeColumns: number;
  booleanColumns: number;
  missingValues: number;
};

export type DatasetSummaryInfo = {
  overview: string;
  keyFindings: string[];
  businessSummary: string;
  recommendedQuestions: string[];
};

export type NumericColumnSummary = {
  count: number;
  mean: number;
  std: number;
  min: number;
  "25%": number;
  "50%": number;
  "75%": number;
  max: number;
};

export type Correlation = {
  columnA: string;
  columnB: string;
  value: number;
  explanation: string;
};

export type ConversationEntry = {
  role: string;
  content: string;
  createdAt?: string;
};

// ── Full session (get session by id) ────────────────────────────────

export type Session = {
  _id: string;
  originalName: string;
  s3Key: string;
  status: string;
  currentStep: string;
  progress: number;
  error: string;
  createdAt: string;
  updatedAt: string;

  datasetProfile: DatasetProfile;
  datasetSummary: DatasetSummaryInfo;
  recommendations: string[];

  sampleRows: Record<string, any>[];
  columnMetadata: ColumnMetadata[];
  nullCounts: Record<string, number>;
  statisticsExplanation: Record<string, string>;
  numericSummary: Record<string, NumericColumnSummary>;

  summaryCharts: Chart[];
  correlations: Correlation[];
  conversations: ConversationEntry[];
};