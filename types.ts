
import type React from 'react';

export interface Feature {
  slug: string;
  title: string;
  description: string;
  icon: React.ElementType;
}

export interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
}
