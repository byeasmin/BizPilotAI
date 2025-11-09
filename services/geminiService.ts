interface RoadmapResponse {
  roadmap: string;
  feasibility_score: number;
}

export async function generateRoadmapStream(
  prompt: string,
  onStream: (chunk: string) => void,
  onComplete?: () => void,
  onError?: (error: Error) => void
): Promise<void> {
  try {
    // Extract idea details from prompt (simple parsing)
    const ideaMatch = prompt.match(/Idea: ([^\n]+)/);
    const categoryMatch = prompt.match(/Category: ([^\n]+)/);
    const audienceMatch = prompt.match(/Target Audience: ([^\n]+)/);

    const idea = ideaMatch ? ideaMatch[1].trim() : '';
    const category = categoryMatch ? categoryMatch[1].trim() : '';
    const targetAudience = audienceMatch ? audienceMatch[1].trim() : '';

    const response = await fetch('http://localhost:8000/generate-roadmap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        idea,
        category,
        target_audience: targetAudience,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: RoadmapResponse = await response.json();

    // Simulate streaming by splitting the response into chunks
    const roadmapText = data.roadmap;
    const chunks = roadmapText.split(' ');

    for (const chunk of chunks) {
      onStream(chunk + ' ');
      await new Promise(resolve => setTimeout(resolve, 50)); // Simulate delay
    }

    if (onComplete) {
      onComplete();
    }
  } catch (error) {
    console.error('Error generating roadmap:', error);
    const errorMessage = "I'm sorry, but I encountered an issue while generating the roadmap. Please ensure the backend is running.";
    onStream(errorMessage);
    if (onError) {
      onError(error instanceof Error ? error : new Error(String(error)));
    }
    if (onComplete) {
      onComplete();
    }
  }
}
