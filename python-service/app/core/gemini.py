import asyncio
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded

from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

gemini = genai.GenerativeModel(settings.GEMINI_MODEL)

async def ask_gemini(prompt: str) -> str:
    try:
        response = await gemini.generate_content_async(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()

        return "No response generated."

    except ResourceExhausted:
        return "Gemini quota exceeded. Please try again later."

    except DeadlineExceeded:
        return "Gemini request timed out."

    except Exception as e:
        print("Gemini Error:", e)
        return "Gemini service unavailable."