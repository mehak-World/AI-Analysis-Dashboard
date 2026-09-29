import { useEffect, useRef, useState } from "react";
import { MessageCircle, X, Send } from "lucide-react";
import useChat from "../hooks/useChat"
import ChatMessageBubble from "./ChatMessageBubble";

const ChatWidget = ({ sessionId }: { sessionId: string }) => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const { messages, sendMessage, sending } = useChat(sessionId);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <>
      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-[380px] max-w-[calc(100vw-2rem)] h-[560px] max-h-[calc(100vh-8rem)] flex flex-col rounded-2xl bg-zinc-950 ring-1 ring-zinc-800 shadow-2xl shadow-black/50 overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800/80 shrink-0">
            <div>
              <h3 className="text-sm font-semibold text-white">Ask about this dataset</h3>
              <p className="text-[11px] text-zinc-500">Powered by your data, not guesses</p>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="text-zinc-500 hover:text-zinc-300 transition-colors"
              aria-label="Close chat"
            >
              <X size={18} />
            </button>
          </div>

          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
            {messages.length === 0 && (
              <div className="h-full flex items-center justify-center text-center px-6">
                <p className="text-xs text-zinc-500 leading-relaxed">
                  Ask a question about your data — relationships, trends, rankings,
                  distributions, or a general overview.
                </p>
              </div>
            )}
            {messages.map((m) => (
              <ChatMessageBubble key={m.id} message={m} />
            ))}
          </div>

          <div className="flex items-center gap-2 px-3 py-3 border-t border-zinc-800/80 shrink-0">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
              placeholder="Ask a question..."
              disabled={sending}
              className="flex-1 bg-zinc-900 ring-1 ring-zinc-800 rounded-lg px-3 py-2 text-sm text-white placeholder:text-zinc-600 outline-none focus:ring-teal-500/50 disabled:opacity-50"
            />
            <button
              onClick={handleSend}
              disabled={sending || !input.trim()}
              className="shrink-0 w-9 h-9 rounded-lg bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center disabled:opacity-40 transition-opacity"
              aria-label="Send"
            >
              <Send size={15} className="text-zinc-950" />
            </button>
          </div>
        </div>
      )}

      <button
        onClick={() => setOpen((o) => !o)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 shadow-lg shadow-teal-500/20 flex items-center justify-center hover:scale-105 transition-transform"
        aria-label={open ? "Close chat" : "Open chat"}
      >
        {open ? <X size={20} className="text-zinc-950" /> : <MessageCircle size={20} className="text-zinc-950" />}
      </button>
    </>
  );
};

export default ChatWidget;