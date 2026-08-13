from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from tools import multiply,add


client = genai.Client(api_key="GEMINI_API_KEY")


def ask_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[multiply,add],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False
            )
        )
    )

    print("TOOL HISTORY:", response.automatic_function_calling_history)

    return response.text