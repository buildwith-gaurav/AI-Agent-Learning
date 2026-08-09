from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key="gemini_api_key")



chat = client.chats.create(
    model = "gemini-3.6-flash"
)

def ask_gemini(prompt: str):
    response = chat.send_message(prompt)    
   

    return response.text