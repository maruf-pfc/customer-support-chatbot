"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";

type Props = {
  onSend: (message: string) => void;
  loading: boolean;
};

export default function ChatInput({ onSend, loading }: Props) {
  const [input, setInput] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!loading && inputRef.current) {
      inputRef.current.focus();
    }
  }, [loading]);

  function handleSend() {
    if (!input.trim() || loading) return;
    onSend(input.trim());
    setInput("");
  }

  return (
    <div className="flex gap-3">
      <Input
        ref={inputRef}
        placeholder="Ask anything..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
        disabled={loading}
        className="flex-1 h-12 px-5 rounded-xl border-2 border-border/50 focus:border-primary/50 transition-all duration-300 bg-background/80 backdrop-blur-sm"
      />
      <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
        <Button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          size="icon"
          className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 shadow-lg shadow-primary/25 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send size={20} />
        </Button>
      </motion.div>
    </div>
  );
}
