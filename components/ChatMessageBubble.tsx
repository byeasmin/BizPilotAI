import React, { useState } from 'react';
import { Bot, User, Copy, Check } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import type { ChatMessage } from '../types';

interface ChatMessageBubbleProps {
  message: ChatMessage;
}

const ChatMessageBubble: React.FC<ChatMessageBubbleProps> = ({ message }) => {
  const [hasCopied, setHasCopied] = useState(false);

  const handleCopy = () => {
    if (message.text) {
      navigator.clipboard.writeText(message.text);
      setHasCopied(true);
      setTimeout(() => setHasCopied(false), 2000);
    }
  };

  const isAIMessage = message.sender === 'ai';
  const bubbleContent =
    message.text === '...'
      ? <div className="animate-pulse text-gray-500">...</div>
      : <ReactMarkdown>{message.text}</ReactMarkdown>;

  if (!isAIMessage) {
    // 🧍‍♂️ User message bubble (right side)
    return (
      <div className="flex items-start gap-3 justify-end">
        <div className="p-4 rounded-2xl max-w-lg bg-gradient-to-br from-teal-400 to-cyan-500 text-white shadow-md rounded-br-none">
          <div className="prose prose-sm max-w-none prose-p:text-white prose-strong:text-white prose-headings:text-white prose-ul:text-white prose-ol:text-white">
            <ReactMarkdown>{message.text}</ReactMarkdown>
          </div>
        </div>
        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-teal-100 flex items-center justify-center shadow-sm">
          <User className="w-6 h-6 text-teal-600" />
        </div>
      </div>
    );
  }

  // 🤖 AI message bubble (left side)
  return (
    <div className="flex items-start gap-3">
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-white border border-teal-200 flex items-center justify-center shadow-sm">
        <Bot className="w-6 h-6 text-teal-600" />
      </div>

      <div className="group relative p-4 rounded-2xl max-w-lg bg-gradient-to-br from-teal-50 to-white text-gray-800 border border-teal-100 shadow-sm rounded-bl-none w-full">
        <div className="prose prose-sm max-w-none text-gray-800">
          {bubbleContent}
        </div>

        {message.text && message.text !== '...' && (
          <button
            onClick={handleCopy}
            className="absolute top-2 right-2 p-1.5 rounded-md bg-white/70 text-gray-500 hover:bg-white shadow-sm opacity-0 group-hover:opacity-100 transition-opacity"
            aria-label="Copy message"
          >
            {hasCopied ? (
              <Check size={16} className="text-teal-600" />
            ) : (
              <Copy size={16} />
            )}
          </button>
        )}
      </div>
    </div>
  );
};

export default ChatMessageBubble;
