from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key="GEMINI_API_KEY")



chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "system_instruction": """
        You are a helpful AI tutor.
        Explain technical concepts in simple language.
        Give examples whenever useful.
        """
    }
)

def ask_gemini(prompt: str):
    response = chat.send_message(prompt)    
   

    return response.text