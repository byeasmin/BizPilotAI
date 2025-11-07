import { GoogleGenAI, Chat } from "@google/genai";

// Ensure the API key is available in the environment variables
if (!process.env.API_KEY) {
  // In a real app, you'd handle this more gracefully.
  // For this context, we'll log an error.
  console.error("API_KEY environment variable not set.");
}

const systemInstruction = "You are BizPilot, an expert business advisor specializing in the startup ecosystem, tax laws, and registration processes in Bangladesh. Your goal is to provide a clear, actionable, step-by-step roadmap for entrepreneurs. Use markdown for clear formatting, including headings, lists, and bold text. Make your advice practical and specific to Bangladesh.";

let chat: Chat;

function getChatSession(): Chat {
    if (!chat) {
        const ai = new GoogleGenAI({ apiKey: process.env.API_KEY! });
        chat = ai.chats.create({
            model: "gemini-2.5-pro",
            config: {
                systemInstruction: systemInstruction,
                temperature: 0.7,
                topP: 0.95,
            },
        });
    }
    return chat;
}

export async function generateRoadmapStream(
  prompt: string,
  onStream: (chunk: string) => void,
  onComplete?: () => void,
  onError?: (error: Error) => void
): Promise<void> {
  const chatSession = getChatSession();

  try {
    const responseStream = await chatSession.sendMessageStream({ message: prompt });
    for await (const chunk of responseStream) {
      onStream(chunk.text);
    }
  } catch (error) {
    console.error("Error calling Gemini API:", error);
    const errorMessage = "I'm sorry, but I encountered an issue while generating the roadmap. Please check your connection or API key and try again.";
    onStream(errorMessage);
    if (onError) {
        onError(error instanceof Error ? error : new Error(String(error)));
    }
  } finally {
    if (onComplete) {
      onComplete();
    }
  }
}
