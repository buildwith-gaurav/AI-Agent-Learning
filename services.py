from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from tools import add , multiply ,get_weather

client = genai.Client(api_key = "REMOVED_SECRET")

chat = client.chats.create(
    model = "gemini-3.6-flash",
    config = types.GenerateContentConfig(
         tools=[add, multiply,get_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False
        )
    )
)
def ask_gemini(prompt:str):
    response = chat.send_message(prompt)
    return response.text