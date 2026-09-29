import { useCallback, useEffect, useRef, useState } from "react";
import type { ChatMessage, ChatResult } from "../types/chat"
import { sendMsg } from "../api/api.chat";

let idCounter = 0;
const nextId = () => `msg_${Date.now()}_${idCounter++}`;

export default function useChat(sessionId: string | null) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sending, setSending] = useState(false);
  const sessionRef = useRef(sessionId);

  // Chat is scoped per-session — switching sessions starts fresh.
  useEffect(() => {
    if (sessionRef.current !== sessionId) {
      sessionRef.current = sessionId;
      setMessages([]);
    }
  }, [sessionId]);

  const sendMessage = useCallback(
    async (question: string) => {
      if (!sessionId || !question.trim() || sending) return;

      const userMsg: ChatMessage = { id: nextId(), role: "user", text: question };
      const pendingId = nextId();
      const pendingMsg: ChatMessage = { id: pendingId, role: "assistant", status: "pending" };

      setMessages((prev) => [...prev, userMsg, pendingMsg]);
      setSending(true);

      try {
        const response = await sendMsg(sessionId, question)
        const result: ChatResult = response.data.data;

        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingId ? { id: pendingId, role: "assistant", status: "done", result } : m
          )
        );
      } catch (err: any) {
        const errorText =
          err?.response?.data?.message || "Something went wrong answering that. Try rephrasing?";

        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingId ? { id: pendingId, role: "assistant", status: "error", error: errorText } : m
          )
        );
      } finally {
        setSending(false);
      }
    },
    [sessionId, sending]
  );

  return { messages, sendMessage, sending };
}