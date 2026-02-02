"use client";

import { useState, useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import { motion } from "framer-motion";
import { MessageCircle, Sparkles } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  async function sendMessage(text: string) {
    if (!text.trim()) return;

    const userMsg: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      const botMsg: Message = {
        role: "assistant",
        content: data.answer || "No response received.",
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Sorry — could not connect to server. Please ensure the server is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 md:p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6 text-center"
      >
        <div className="flex items-center justify-center gap-3 mb-2">
          <div className="relative">
            <MessageCircle className="w-8 h-8 text-primary" />
            <Sparkles className="w-4 h-4 text-accent absolute -top-1 -right-1" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold gradient-text">
            Customer Support Assistant
          </h1>
        </div>
        <p className="text-sm text-muted-foreground">
          Powered by RAG • Instant answers from our knowledge base
        </p>
      </motion.div>

      {/* Chat Container with Glassmorphism */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className="flex-1 glass rounded-3xl shadow-2xl overflow-hidden flex flex-col"
      >
        <div
          ref={scrollRef}
          className="flex-1 space-y-4 overflow-y-auto p-6 scroll-smooth"
        >
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex flex-col items-center justify-center h-full text-center py-12"
            >
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center mb-4">
                <MessageCircle className="w-10 h-10 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Start a conversation</h3>
              <p className="text-muted-foreground max-w-md">
                Ask anything about our services, policies, courses, or products.
                I'm here to help! 🚀
              </p>
            </motion.div>
          )}

          {messages.map((msg, i) => (
            <ChatMessage key={i} {...msg} />
          ))}

          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-muted/50 rounded-2xl px-5 py-4 w-fit text-sm text-muted-foreground flex items-center gap-3"
            >
              <span className="font-medium">Thinking</span>
              <div className="flex gap-1">
                <motion.span
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 1.4, repeat: Infinity }}
                  className="w-2 h-2 rounded-full bg-primary"
                />
                <motion.span
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 1.4, repeat: Infinity, delay: 0.2 }}
                  className="w-2 h-2 rounded-full bg-primary"
                />
                <motion.span
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 1.4, repeat: Infinity, delay: 0.4 }}
                  className="w-2 h-2 rounded-full bg-primary"
                />
              </div>
            </motion.div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-border/50 bg-background/50 backdrop-blur-sm p-4">
          <ChatInput onSend={sendMessage} loading={loading} />
        </div>
      </motion.div>
    </div>
  );
}
