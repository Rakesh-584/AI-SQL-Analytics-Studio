"""
gemini_service.py

Handles communication with Google Gemini.
"""

from google import genai
from config import GEMINI_MODEL

_client = None


def configure_gemini(api_key: str):
    """
    Configure Gemini client.
    """
    global _client
    _client = genai.Client(api_key=api_key)


def generate_sql(prompt: str) -> str:
    """
    Generate PostgreSQL SQL using Gemini.
    """

    if _client is None:
        raise Exception("Gemini client is not configured.")

    try:

        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        sql = response.text.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

        return sql

    except Exception as e:
        raise Exception(f"Gemini Error: {e}")