
import type { Feature } from './types';
import { BotMessageSquare, BrainCircuit, Landmark, BarChart4, Handshake, FileText } from 'lucide-react';

export const NAV_LINKS = [
  { name: 'Home', path: '/' },
  { name: 'Features', path: '/#features' },
  { name: 'About', path: '/about' },
  { name: 'Contact', path: '/contact' },
];

export const FEATURES: Feature[] = [
  {
    slug: 'ai-powered-idea-validation',
    title: 'AI Powered Business Idea Validation',
    description: 'Get real-time insights into your business performance with predictive analysis and actionable recommendations.',
    icon: BrainCircuit,
  },
  {
    slug: 'smart-finance-tax',
    title: 'Smart Finance & Tax',
    description: 'Automate bookkeeping, expense tracking and tax calculations with compliance for your region.',
    icon: Landmark,
  },
  {
    slug: 'idea-validation',
    title: 'Idea Validation',
    description: 'Test business concepts before investing with market analysis, competitor research, and feasibility scoring.',
    icon: FileText,
  },
  {
    slug: 'investor-matching',
    title: 'Investor Matching',
    description: 'Connect with the perfect investors and mentors based on your business profile, stage, and industry.',
    icon: Handshake,
  },
  {
    slug: 'bizbot-assistant',
    title: 'BizBot Assistant',
    description: 'Your Business Advisor available 24/7 to answer questions and provide strategic guidance.',
    icon: BotMessageSquare,
  },
  {
    slug: 'advanced-analytics',
    title: 'Advanced Analytics',
    description: 'Deep dive into your business data with customizable reports, charts, and performance metrics.',
    icon: BarChart4,
  },
];
