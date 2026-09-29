from google import genai
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded

from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def ask_gemini(prompt: str) -> str:
    try:
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )

        if response and response.text:
            return response.text.strip()

        return "No response generated."

    except ResourceExhausted:
        return "Gemini quota exceeded. Please try again later."

    except DeadlineExceeded:
        return "Gemini request timed out."

    except Exception as e:
        print("Gemini Error:", e)
        return "Gemini service unavailable."