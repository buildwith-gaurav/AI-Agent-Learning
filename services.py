from database import init_database
from dataclasses import dataclass
from database import get_connection

from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from tools import add, multiply, get_weather


client = genai.Client(api_key = GEMINI_API_KEY)


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
        model="gemini-3.6-flash",
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
        model="gemini-3.6-flash",
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
        model="gemini-3.6-flash",
        contents=f"""
Extract the calculation from the user's request.

Return ONLY in this exact format:

operation|a|b

Allowed operations:
add
multiply

Examples:

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

    try:
        operation, a, b = result.split("|")

        if operation not in ["add", "multiply"]:
            return None

        return {
            "operation": operation,
            "a": int(a),
            "b": int(b)
        }

    except (ValueError, TypeError):
        return None


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


def should_calculate(calculation=None):
    if agent_state.temperature is None:
        return False

    if agent_state.temperature <= 30:
        return False

    if calculation is None:
        return False

    return True

def run_agent_workflow(city: str, calculation=None):

    reset_state()

    weather = process_weather(city)

    if isinstance(weather, str):
        return weather

    state_check = validate_state()

    if state_check != "State is valid.":
        return state_check

    if should_calculate(calculation):

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

    return state_to_dict()


# -----------------------------
# Reset State
# -----------------------------

def reset_state():
    agent_state.city = None
    agent_state.temperature = None
    agent_state.calculation = None
    agent_state.final_result = None

    return agent_state

def validate_state():
    if agent_state.city is None:
        return "City is missing."

    if agent_state.temperature is None:
        return "Temperature is missing."

    return "State is valid."


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
            tools=[multiply, add , get_weather],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False
            )
        )
    )

    print("TOOL HISTORY:", response.automatic_function_calling_history)

    return response.text

def extract_task(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
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
        model="gemini-3.6-flash",
        contents=f"""

{prompt}
"""
    )

    result = response.text.strip()

    if result.upper() == "NONE":
        return None

    try:
        operation, a, b = result.split("|")

        if operation not in ["add", "multiply"]:
            return None

        return {
            "operation": operation,
            "a": int(a),
            "b": int(b)
        }

    except (ValueError, TypeError):
        return None

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

conversation_memory = []
def save_memory(user_prompt, result):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories (user_prompt, result)
        VALUES (?, ?)
        """,
        (user_prompt, str(result))
    )

    connection.commit()
    connection.close()
def get_memory():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT user_prompt, result FROM memories ORDER BY id DESC LIMIT 5"
    )

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "user": row[0],
            "result": row[1]
        }
        for row in rows
    ]

def get_last_memory():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_prompt, result
        FROM memories
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return {
        "user": row[0],
        "result": row[1]
    }

def search_memory(keyword):
    results = []

    keyword = keyword.lower().strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_prompt, result
        FROM memories
        ORDER BY id DESC
        LIMIT 5
        """
    )

    rows = cursor.fetchall()
    connection.close()

    memories = [
        {
            "user": row[0],
            "result": row[1]
        }
        for row in rows
    ]

    for memory in memories:
        user_text = memory["user"].lower()

        if keyword in user_text:
            results.append(memory)

    if results:
        return results

    stop_words = {
        "tell", "me", "more", "about",
        "what", "is", "the", "a", "an",
        "in", "on", "for", "to", "of"
    }

    keywords = [
        word for word in keyword.split()
        if word not in stop_words
    ]

    for memory in memories:
        user_text = memory["user"].lower()

        if any(word in user_text for word in keywords):
            results.append(memory)

    return results

def extract_memory_keyword(prompt):
    words = prompt.lower().split()

    stop_words = {
        "tell", "me", "more", "about",
        "what", "is", "the", "a", "an",
        "in", "on", "for", "to", "of"
    }

    meaningful_words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(meaningful_words)

def get_agent_context(memory_keyword=None):
    context = {
        "current_state": state_to_dict(),
        "recent_memory": get_memory()
    }

    if memory_keyword:
        context["memory_search_results"] = search_memory(memory_keyword)

    return context
def get_relevant_context(keyword):
    return {
        "current_state": state_to_dict(),
        "relevant_memories": search_memory(keyword)
    }

def build_memory_context(prompt):
    keyword = extract_memory_keyword(prompt)
    memories = search_memory(keyword)

    if not memories:
        return "No relevant previous conversation found."

    context = "Relevant previous conversations:\n"

    for memory in memories:
        context += (
            f"User: {memory['user']}\n"
            f"Result: {memory['result']}\n"
        )

    return context

    if not memories:
        return "No relevant previous conversation found."

    context = "Relevant previous conversations:\n"

    for memory in memories:
        context += (
            f"User: {memory['user']}\n"
            f"Result: {memory['result']}\n"
        )

    return context

def build_prompt_with_memory(prompt):
    memory_context = build_memory_context(prompt)

    return f"""
Current user request:
{prompt}

Previous conversation context:
{memory_context}
"""

    return conversation_memory[-1]
def clear_memory():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM memories")

    connection.commit()
    connection.close()


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

def finalize_calculation(result):
    if isinstance(result, str):
        return result

    final_result = add(result, 10)

    update_state(
        final_result=final_result
    )

    return final_result

def run_agent_workflow(city: str, calculation=None):

    reset_state()

    weather = process_weather(city)

    if isinstance(weather, str):
        return weather

    state_check = validate_state()

    if state_check != "State is valid.":
        return state_check

    if should_calculate(calculation):

        result = process_calculation(
            calculation["a"],
            calculation["b"],
            calculation["operation"]
        )

        if isinstance(result, str):
            return result

        result = finalize_calculation(result)

        if isinstance(result, str):
            return result

    return state_to_dict()
def state_to_dict():
    return {
        "city": agent_state.city,
        "temperature": agent_state.temperature,
        "calculation": agent_state.calculation,
        "final_result": agent_state.final_result
    }


# -----------------------------
# Reset State
# -----------------------------

def reset_state():
    agent_state.city = None
    agent_state.temperature = None
    agent_state.calculation = None
    agent_state.final_result = None

    return agent_state




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
def run_prompt(prompt: str):

    city = extract_city(prompt)
    task = extract_task(prompt)

    calculation = None

    if task in ["calculation", "weather_and_calculation"]:
        calculation = extract_calculation(prompt)

    result = execute_task(
        city=city,
        task=task,
        calculation=calculation
    )

    memory_context = build_memory_context(prompt)

    save_memory(prompt, result)

    return {
        "response": result,
        "memory_context": memory_context
    }

def run_task_with_memory(prompt, city=None, task=None, calculation=None):

    result = execute_task(
        city=city,
        task=task,
        calculation=calculation
    )

    save_memory(prompt, result)

    return result
