# my_agent_package/agent.py

import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """
    Retrieves the current weather report for a specified city.
    Args:
        city (str): The name of the city to get the weather for.
    Returns:
        dict: A dictionary containing the status and report or an error message.
    """
    if city.lower() == "new york":
        return {"status": "success", "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)."}
    else:
        return {"status": "error", "error_message": f"Weather information for '{city}' is not available."}

def get_current_time(city: str) -> dict:
    """
    Returns the current time in a specified city.
    Args:
        city (str): The name of the city to get the current time for.
    Returns:
        dict: A dictionary containing the status and report or an error message.
    """
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have timezone information for {city}."}
    
    try:
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# Define your root agent, specifying a Gemini model available in Vertex AI
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash-001",  # Use a specific, supported Vertex AI model ID
    description="A helpful agent that can answer user questions about the time and weather in a city.",
    instruction="You must use your tools to answer questions about the weather or temperature or time. Do not make up information.",
    tools=[get_weather, get_current_time],
)
