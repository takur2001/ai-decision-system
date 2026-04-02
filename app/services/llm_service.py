import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


class LLMService:
    @staticmethod
    def analyze(text: str):
        if not api_key:
            return {
                "status": "unavailable",
                "analysis": None,
                "error": "OPENAI_API_KEY not found"
            }

        try:
            client = OpenAI(api_key=api_key)

            prompt = f"""
            Analyze the following case and provide:
            1. Risk analysis
            2. Recommended action
            3. Confidence level

            Case:
            {text}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a financial risk analyst AI."},
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "status": "available",
                "analysis": response.choices[0].message.content,
                "error": None
            }

        except Exception:
            return {
                "status": "unavailable",
                "analysis": None,
                "error": "LLM service unavailable"
            }