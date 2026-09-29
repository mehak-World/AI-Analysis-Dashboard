import { AlertCircle, Loader2, Sparkles } from "lucide-react";
import type { ChatMessage } from "../types/chat";

const ChatMessageBubble = ({ message }: { message: ChatMessage }) => {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-xl rounded-tr-sm bg-gradient-to-br from-teal-400 to-blue-500 px-3.5 py-2.5 text-sm text-zinc-950 font-medium">
          {message.text}
        </div>
      </div>
    );
  }

  if (message.status === "pending") {
    return (
      <div className="flex justify-start">
        <div className="flex items-center gap-2 rounded-xl rounded-tl-sm bg-zinc-900/60 ring-1 ring-zinc-800 px-3.5 py-2.5 text-sm text-zinc-400">
          <Loader2 size={13} className="animate-spin text-teal-300" />
          Thinking...
        </div>
      </div>
    );
  }

  if (message.status === "error") {
    return (
      <div className="flex justify-start">
        <div className="flex items-center gap-2 max-w-[85%] rounded-xl rounded-tl-sm bg-red-950/30 ring-1 ring-red-900/50 px-3.5 py-2.5 text-sm text-red-400">
          <AlertCircle size={14} className="shrink-0" />
          {message.error}
        </div>
      </div>
    );
  }

  const { result } = message;
  const chart = result.charts?.[0];

  return (
    <div className="flex justify-start">
      <div className="max-w-[90%] space-y-3 rounded-xl rounded-tl-sm bg-zinc-900/60 ring-1 ring-zinc-800 px-3.5 py-3">
        <p className="text-sm text-zinc-200 leading-relaxed">{result.explanation}</p>

        {chart && (
          <div className="rounded-lg bg-zinc-950/60 ring-1 ring-zinc-800/80 px-3 py-2.5">
            <div className="flex items-center gap-1.5 text-[11px] font-medium text-teal-300 uppercase tracking-wide">
              <Sparkles size={11} />
              {chart.name}
            </div>
            {/* Chart rendering intentionally deferred here — see note below */}
            <p className="mt-1 text-[11px] text-zinc-500">
              {chart.type} chart · {chart.data?.length ?? 0} data points
            </p>
          </div>
        )}

        {result.recommendations?.length > 0 && (
          <div className="space-y-1 pt-1 border-t border-zinc-800/80">
            <p className="text-[10px] font-medium text-zinc-500 uppercase tracking-wide">Recommendations</p>
            <ul className="space-y-1">
              {result.recommendations.map((rec, i) => (
                <li key={i} className="text-[11px] text-zinc-400 leading-relaxed flex gap-1.5">
                  <span className="text-teal-400 shrink-0">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessageBubble;