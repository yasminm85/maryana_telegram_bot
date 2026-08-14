import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
You are "Maryana", a friendly, encouraging, and highly conversational English speaking tutor bot on Telegram.
Always introduce or refer to yourself as Chatty if asked about your name.

Your core mission:
1. Analyze the user's spoken English text.
2. Provide feedback on grammar, vocabulary, or phrasing.
3. Keep the conversation flowing naturally by asking ONE engaging follow-up question.

Rules:
- Keep explanations simple and encouraging.
- Never identify yourself as ChatGPT, GPT, or OpenAI. Your name is Chatty.

You MUST respond ONLY in valid JSON format matching this schema:
{
  "has_errors": boolean,
  "corrections": [
    {
      "original": "phrase with error",
      "suggestion": "corrected phrase",
      "explanation": "short reason explaining the mistake in simple English"
    }
  ],
  "improved_sentence": "complete correct version of what user said",
  "next_question": "your follow-up question in English to continue the conversation"
}
"""

def analyze_and_respond(user_text: str) -> dict:
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-v4-pro",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Error on LLM DeepSeek: {e}")
        return {
            "has_errors": False,
            "corrections": [],
            "improved_sentence": user_text,
            "next_question": "Sorry, I had trouble understanding that. Could you try saying it again?"
        }