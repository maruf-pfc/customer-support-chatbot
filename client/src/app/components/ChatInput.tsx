"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";
import { useState } from "react";

type Props = {
  onSend: (message: string) => void;
  loading: boolean;
};

export default function ChatInput({ onSend, loading }: Props) {
  const [input, setInput] = useState("");

  function handleSend() {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  }

  return (
    <div className="flex gap-2">
      <Input
        placeholder="Ask something..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        disabled={loading}
      />
      <Button onClick={handleSend} disabled={loading}>
        <Send size={16} />
      </Button>
    </div>
  );
}
