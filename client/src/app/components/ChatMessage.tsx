"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

type Props = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatMessage({ role, content }: Props) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "max-w-[80%] rounded-xl px-4 py-3 text-sm",
        isUser
          ? "ml-auto bg-primary text-primary-foreground"
          : "bg-muted text-foreground",
      )}
    >
      {content}
    </motion.div>
  );
}
