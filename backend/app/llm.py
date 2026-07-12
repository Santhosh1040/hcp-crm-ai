import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=ENV_PATH)


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            f"GROQ_API_KEY is not configured. "
            f"Expected .env at: {ENV_PATH}"
        )

    return ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0,
    )