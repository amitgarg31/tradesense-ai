import os

import google.generativeai as genai
from openai import OpenAI


class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.api_key = os.getenv("LLM_API_KEY")

        if not self.api_key:
            print("⚠️  Warning: LLM_API_KEY not found. LLM features will fail.")

        if self.provider == "openai":
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4o-mini"
            self.embedding_model = "text-embedding-3-small"
        else:
            # Default to Gemini
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            self.embedding_model = "models/text-embedding-004"

    def generate_summary(self, text: str) -> str:
        prompt = f"Summarize the following trading data and provide insights:\n\n{text}"

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a financial analyst AI.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                )
                return response.choices[0].message.content
            else:
                response = self.model.generate_content(prompt)
                return response.text
        except Exception as e:
            print(f"❌ LLM Generation Error: {e}")
            return "Error generating summary."

    def generate_embedding(self, text: str) -> list[float]:
        try:
            if self.provider == "openai":
                response = self.client.embeddings.create(
                    input=text, model=self.embedding_model
                )
                return response.data[0].embedding
            else:
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document",
                )
                return result["embedding"]
        except Exception as e:
            print(f"❌ LLM Embedding Error: {e}")
            return []
