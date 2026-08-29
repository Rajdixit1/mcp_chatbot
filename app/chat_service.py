import os

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-20b"


async def generate_response(messages: list[dict]) -> str:

    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_completion_tokens=1000,
    )

    return response.choices[0].message.content