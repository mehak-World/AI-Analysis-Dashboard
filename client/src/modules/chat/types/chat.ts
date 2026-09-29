export interface ChatChart {
  id: string;
  name: string;
  type: string;
  reason: string;
  config: Record<string, unknown>;
  data: Record<string, unknown>[];
  xAxis: { label: string; unit: string };
  yAxis: { label: string; unit: string };
  statistics: Record<string, unknown>;
  summary: string;
  insight: string;
}

export interface ChatResult {
  plan: {
    intent: string;
    user_question: string;
    analysis_goal: string;
    requested_chart: boolean;
    confidence: number;
  };
  charts: (ChatChart | null)[];
  statistics: Record<string, unknown>;
  evidence: Record<string, unknown>;
  explanation: string;
  recommendations: string[];
  prediction: unknown;
}

export type ChatMessage =
  | { id: string; role: "user"; text: string }
  | { id: string; role: "assistant"; status: "pending" }
  | { id: string; role: "assistant"; status: "error"; error: string }
  | { id: string; role: "assistant"; status: "done"; result: ChatResult };