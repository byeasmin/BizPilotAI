import React, { useState, useRef, useEffect } from 'react';
import type { ChatMessage } from '../types';
import { generateRoadmapStream } from '../services/geminiService';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { Send, Mic, Square, Loader2 } from 'lucide-react';
import ChatMessageBubble from '../components/ChatMessageBubble';

const AIPoweredIdeaValidationPage: React.FC = () => {
  const [initialIdea, setInitialIdea] = useState('');
  const [category, setCategory] = useState('');
  const [targetAudience, setTargetAudience] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  
  const { transcript, isListening, startListening, stopListening } = useSpeechRecognition();
  const chatEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setCurrentMessage(transcript);
  }, [transcript]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      const scrollHeight = textarea.scrollHeight;
      textarea.style.height = `${scrollHeight}px`;
    }
  }, [currentMessage]);

  const handleInitialSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!initialIdea.trim()) return;
    setIsLoading(true);
    setIsStarted(true);

    const userMessageText = `My business idea is: "${initialIdea}". The category is "${category}" and the target audience is "${targetAudience}". Please provide a business roadmap.`;
    const firstUserMessage: ChatMessage = {
      sender: 'user',
      text: userMessageText,
    };
    
    setChatHistory([firstUserMessage, { sender: 'ai', text: '' }]);

    const prompt = `I want to start a business in Bangladesh with the following details:
- Idea: ${initialIdea}
- Category: ${category || 'Not specified'}
- Target Audience: ${targetAudience || 'Not specified'}

Please provide a detailed step-by-step business roadmap covering these key areas:
1.  **Business Registration:** Explain the necessary steps and entities (e.g., RJSC).
2.  **Tax & Compliance:** Outline the basic tax filing requirements and necessary licenses.
3.  **Market Segmentation:** Suggest specific market segments to target within Bangladesh.
4.  **Investor Landscape:** Mention types of potential investors or funding sources available in the local ecosystem.`;
    
    await generateRoadmapStream(
        prompt,
        (chunk) => {
            setChatHistory(prev => {
                const newHistory = [...prev];
                newHistory[newHistory.length - 1].text += chunk;
                return newHistory;
            });
        },
        () => setIsLoading(false)
    );
  };
  
  const handleSendMessage = async () => {
    if (!currentMessage.trim() || isLoading) return;

    const newUserMessage: ChatMessage = { sender: 'user', text: currentMessage };
    const messageToSend = currentMessage;
    setCurrentMessage('');

    setChatHistory(prev => [...prev, newUserMessage, { sender: 'ai', text: '' }]);
    setIsLoading(true);
    
     await generateRoadmapStream(
        messageToSend,
        (chunk) => {
            setChatHistory(prev => {
                const newHistory = [...prev];
                newHistory[newHistory.length - 1].text += chunk;
                return newHistory;
            });
        },
        () => setIsLoading(false)
    );
  };

  if (!isStarted) {
    return (
      <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg">
        <h1 className="text-2xl md:text-3xl font-bold text-center text-secondary mb-2">AI Business Idea Validation</h1>
        <p className="text-center text-gray-600 mb-6">Let's craft a roadmap for your next big venture. Fine-tuned for the Bangladeshi market.</p>
        <form onSubmit={handleInitialSubmit} className="space-y-4">
          <div>
            <label htmlFor="idea" className="block text-sm font-medium text-gray-700">Your Business Idea</label>
            <textarea
              id="idea"
              value={initialIdea}
              onChange={(e) => setInitialIdea(e.target.value)}
              placeholder="e.g., An online shop for handmade clothing"
              rows={3}
              className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              required
            />
          </div>
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700">Business Category</label>
            <input
              type="text"
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="e.g., E-commerce, Fashion"
              className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            />
          </div>
          <div>
            <label htmlFor="audience" className="block text-sm font-medium text-gray-700">Target Audience</label>
            <input
              type="text"
              id="audience"
              value={targetAudience}
              onChange={(e) => setTargetAudience(e.target.value)}
              placeholder="e.g., Young adults in urban areas"
              className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            />
          </div>
          <button type="submit" disabled={isLoading} className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-br from-primary to-primary-700 hover:from-primary-600 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:from-teal-300 disabled:to-teal-400 disabled:cursor-not-allowed transition-all duration-300">
            {isLoading ? <Loader2 className="animate-spin" /> : 'Generate Roadmap'}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] max-w-4xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="flex-grow p-6 overflow-y-auto">
        <div className="space-y-6">
          {chatHistory.map((msg, index) => (
            <ChatMessageBubble key={index} message={msg} />
          ))}
          {isLoading && chatHistory[chatHistory.length - 1]?.text === '' && (
             <ChatMessageBubble message={{sender: 'ai', text: '...'}} />
          )}
          <div ref={chatEndRef} />
        </div>
      </div>
      <div className="border-t p-4 bg-white">
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSendMessage(); } }}
            placeholder="Ask a follow-up question..."
            rows={1}
            className="w-full pr-28 py-2 pl-4 border border-gray-300 rounded-full focus:ring-primary focus:border-primary resize-none overflow-y-hidden"
            style={{maxHeight: '150px'}}
          />
          <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center space-x-1">
            <button onClick={isListening ? stopListening : startListening} className={`p-2 rounded-full ${isListening ? 'bg-red-500 text-white animate-pulse' : 'hover:bg-gray-100 text-gray-600'}`}>
              {isListening ? <Square size={20} /> : <Mic size={20} />}
            </button>
            <button onClick={handleSendMessage} disabled={isLoading || !currentMessage.trim()} className="bg-gradient-to-br from-primary to-primary-700 text-white p-2 rounded-full hover:from-primary-600 hover:to-primary-800 disabled:from-teal-300 disabled:to-teal-400 disabled:cursor-not-allowed transition-all duration-300">
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIPoweredIdeaValidationPage;