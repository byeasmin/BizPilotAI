from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

class IdeaValidator:
    def __init__(self):
        # Load pre-trained text generation model
        self.generator = pipeline('text-generation', model='gpt2', max_length=500, temperature=0.7)

        # Simple ML model for feasibility scoring (placeholder - in real scenario, train on dataset)
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = LogisticRegression()

        # Load or train model (for demo, we'll use a simple rule-based scoring)
        self._load_or_train_model()

    def _load_or_train_model(self):
        model_path = 'feasibility_model.pkl'
        if os.path.exists(model_path):
            self.classifier = joblib.load(model_path)
        else:
            # Placeholder training data
            sample_ideas = [
                "Online clothing store for handmade items",
                "AI-powered tutoring platform",
                "Mobile app for local food delivery",
                "Cryptocurrency trading bot",
                "Sustainable energy consulting"
            ]
            labels = [1, 1, 1, 0, 1]  # 1: feasible, 0: not feasible

            X = self.vectorizer.fit_transform(sample_ideas)
            self.classifier.fit(X, labels)
            joblib.dump(self.classifier, model_path)

    def score_feasibility(self, idea: str, category: str, target_audience: str) -> float:
        """
        Score the feasibility of a business idea using ML.
        Returns a score between 0 and 1.
        """
        combined_text = f"{idea} {category} {target_audience}"
        X = self.vectorizer.transform([combined_text])
        probability = self.classifier.predict_proba(X)[0][1]
        return probability

    def generate_roadmap(self, idea: str, category: str, target_audience: str) -> str:
        """
        Generate a business roadmap using AI text generation.
        """
        prompt = f"""Generate a detailed business roadmap for Bangladesh market:

Business Idea: {idea}
Category: {category}
Target Audience: {target_audience}

Please provide a step-by-step roadmap covering:
1. Business Registration (RJSC, etc.)
2. Tax & Compliance
3. Market Segmentation
4. Investor Landscape
5. Implementation Timeline

Roadmap:"""

        generated = self.generator(prompt, max_length=800, num_return_sequences=1)
        roadmap = generated[0]['generated_text'].replace(prompt, '').strip()

        # Add feasibility score
        score = self.score_feasibility(idea, category, target_audience)
        feasibility_note = f"\n\nFeasibility Score: {score:.2f} (based on AI analysis)"

        return roadmap + feasibility_note
