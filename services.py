from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from tools import add , multiply

client = genai.Client(api_key = "AGEMINI_API_KEY")

chat = client.chats.create(
    model = "gemini-3.6-flash",
    config = types.GenerateContentConfig(
         tools=[add, multiply],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False
        )
    )
)
def ask_gemini(prompt:str):
    response = chat.send_message(prompt)
    return response.text