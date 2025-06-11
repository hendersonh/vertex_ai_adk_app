import datetime
import vertexai
from zoneinfo import ZoneInfo
from vertexai.preview.generative_models import FunctionDeclaration # New import
from vertexai.preview.language_models import ReasoningEngine

# --- CONFIGURATION ---
# PLEASE EDIT THESE VALUES
PROJECT_ID = "chatbot-8ebb8"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://chatbot-8ebb8-adk-staging"
# -------------------

# PART 1: DEFINE YOUR AGENT'S TOOLS
# ==================================
class WeatherTimeTools:
    """A collection of tools for getting weather and time."""

    def get_weather(self, city: str) -> dict:
        """Retrieves the current weather report for a specified city.

        Args:
            city (str): The name of the city to get the weather for.

        Returns:
            dict: A dictionary containing the status ('success' or 'error'),
                  the weather report if successful, or an error message.
        """
        print(f"Tool called: get_weather(city='{city}')")
        if city.lower() == "new york":
            return {"status": "success", "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)."}
        else:
            return {"status": "error", "error_message": f"Weather information for '{city}' is not available."}

    def get_current_time(self, city: str) -> dict:
        """Returns the current time in a specified city.

        Args:
            city (str): The name of the city to get the current time for.

        Returns:
            dict: A dictionary containing the status ('success' or 'error'),
                  the current time report if successful, or an error message.
        """
        print(f"Tool called: get_current_time(city='{city}')")
        if city.lower() == "new york":
            tz_identifier = "America/New_York"
        else:
            # Allowing the agent to respond if it doesn't know the timezone,
            # rather than erroring out the tool call immediately.
            return {"status": "success", "report": f"Sorry, I don't have timezone information for {city}."}

        try:
            tz = ZoneInfo(tz_identifier)
            now = datetime.datetime.now(tz)
            report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
            return {"status": "success", "report": report}
        except Exception as e:
            # This will catch issues with ZoneInfo or datetime formatting
            return {"status": "error", "error_message": str(e)}

# PART 2: DEPLOY THE AGENT
# ========================
def deploy_agent():
    """Initializes, creates, and deploys the agent."""

    # Initialize Vertex AI SDK
    vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

    # Instantiate your tool class
    tool_definitions = WeatherTimeTools()

    # Create FunctionDeclarations from the methods
    get_weather_tool_declaration = FunctionDeclaration.from_func(
        tool_definitions.get_weather
    )
    get_current_time_tool_declaration = FunctionDeclaration.from_func(
        tool_definitions.get_current_time
    )

    # Create the Reasoning Engine
    reasoning_engine = ReasoningEngine.create(
        tools=[get_weather_tool_declaration, get_current_time_tool_declaration],
        model_name='gemini-1.5-flash-001', # Using a common and available model
        display_name="Weather and Time Agent (Simplified FD)", # Changed display name
    )

    print("Agent deployment complete!")
    print(f"Resource Name:\n{reasoning_engine.resource_name}")
    return reasoning_engine

if __name__ == "__main__":
    deploy_agent()
