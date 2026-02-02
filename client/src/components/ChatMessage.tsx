"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

type Props = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatMessage({ role, content }: Props) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 16, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4, ease: [0.4, 0, 0.2, 1] }}
      className={cn(
        "flex gap-3 items-start",
        isUser && "flex-row-reverse"
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          "w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md",
          isUser
            ? "bg-gradient-to-br from-primary to-primary/80 text-primary-foreground"
            : "bg-gradient-to-br from-muted to-muted/60 text-foreground"
        )}
      >
        {isUser ? <User size={18} /> : <Bot size={18} />}
      </div>

      {/* Message Bubble */}
      <motion.div
        whileHover={{ scale: 1.01 }}
        transition={{ duration: 0.2 }}
        className={cn(
          "max-w-[75%] rounded-2xl px-5 py-3.5 text-[15px] leading-relaxed shadow-lg transition-smooth",
          isUser
            ? "bg-gradient-to-br from-primary to-primary/90 text-primary-foreground shadow-primary/20"
            : "bg-card text-card-foreground border border-border/50 shadow-sm"
        )}
      >
        <div className="whitespace-pre-wrap break-words">{content}</div>
      </motion.div>
    </motion.div>
  );
}
