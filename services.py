from dataclasses import dataclass

from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from tools import add , multiply ,get_weather

client = genai.Client(api_key = "GEMINI_API_KEY")


from tools import add, multiply, get_weather


# -----------------------------
# Gemini Client
# -----------------------------

client = genai.Client(api_key=GEMINI_API_KEY)


# -----------------------------
# Chat Session + Tools
# -----------------------------

def extract_city(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"""
Extract the city name from this request.

Return ONLY the city name.
If no city is mentioned, return NONE.

User request:
{prompt}
"""
    )

    city = response.text.strip()

    if city.upper() == "NONE":
        return None

    return city

def extract_task(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"""
Identify what the user wants to do.

Return ONLY one of these:
weather
calculation
weather_and_calculation
unknown

User request:
{prompt}
"""
    )

    return response.text.strip().lower()

def extract_calculation(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"""
Extract the calculation from the user's request.

Return ONLY in this exact format:

operation|a|b

Allowed operations:
add
multiply

Example:
Calculate 15 multiplied by 7
multiply|15|7

Calculate 20 plus 10
add|20|10

If there is no calculation, return:
NONE

User request:
{prompt}
"""
    )

    result = response.text.strip()

    if result.upper() == "NONE":
        return None

    operation, a, b = result.split("|")

    return {
        "operation": operation,
        "a": int(a),
        "b": int(b)
    }


# -----------------------------
# Agent State
# -----------------------------

@dataclass
class AgentState:
    city: str | None = None
    temperature: float | None = None
    calculation: int | None = None
    final_result: int | None = None


agent_state = AgentState()


# -----------------------------
# Update State
# -----------------------------

def update_state(
    city=None,
    temperature=None,
    calculation=None,
    final_result=None
):
    if city is not None:
        agent_state.city = city

    if temperature is not None:
        agent_state.temperature = temperature

    if calculation is not None:
        agent_state.calculation = calculation

    if final_result is not None:
        agent_state.final_result = final_result

    return agent_state

def process_weather(city: str):
    weather = get_weather(city)

    # Agar API error message return kare
    if isinstance(weather, str):
        return weather

    update_state(
        city=weather["city"],
        temperature=weather["temperature"]
    )

    return weather

def process_calculation(a, b, operation):
    if operation == "multiply":
        result = multiply(a, b)

    elif operation == "add":
        result = add(a, b)

    else:
        return "Unsupported operation"

    update_state(
        calculation=result
    )

    return result
def run_agent_workflow(city: str, calculation=None):
    reset_state()
    weather = process_weather(city)

    if isinstance(weather, str):
        return weather

# TEMPORARY TEST ONLY
    agent_state.temperature = 32

    if calculation is None:
    
        return agent_state

    # Weather condition
    if agent_state.temperature > 30:

        result = process_calculation(
            calculation["a"],
            calculation["b"],
            calculation["operation"]
        )

        if isinstance(result, str):
            return result

        result = add(result, 10)

        update_state(
            final_result=result
        )

    return agent_state


# -----------------------------
# Reset State
# -----------------------------

def reset_state():
    agent_state.city = None
    agent_state.temperature = None
    agent_state.calculation = None
    agent_state.final_result = None

    return agent_state


# -----------------------------
# Gemini Function
# -----------------------------
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

weather = process_weather("Mumbai")

result = process_calculation(20, 5, "multiply")
result = add(result, 10)

update_state(
    final_result=result
)

def execute_task(city=None, task=None, calculation=None):

    if task == "weather":
        return process_weather(city)

    elif task == "calculation":
        if calculation is None:
            return "Please provide a valid calculation."

        return process_calculation(
            calculation["a"],
            calculation["b"],
            calculation["operation"]
        )

    elif task == "weather_and_calculation":
        return run_agent_workflow(
            city,
            calculation
        )

    else:
        return "I don't understand the requested task."

def ask_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[multiply, add],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False
            )
        )
    )

    print("TOOL HISTORY:", response.automatic_function_calling_history)








