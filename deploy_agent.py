import datetime
import vertexai
from zoneinfo import ZoneInfo
from vertexai.preview.reasoning_engines import Tool
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

    @Tool.from_function_schema(
        name="get_weather",
        description="Retrieves the current weather report for a specified city.",
        input_schema={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get the weather for."
                }
            },
            "required": ["city"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Either 'success' or 'error'"},
                "report": {"type": "string", "description": "The weather report if successful."},
                "error_message": {"type": "string", "description": "Details of the error if status is 'error'."}
            },
            "required": ["status"]
        }
    )
    def get_weather(self, city: str) -> dict:
        print(f"Tool called: get_weather(city='{city}')")
        if city.lower() == "new york":
            return {"status": "success", "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)."}
        else:
            return {"status": "error", "error_message": f"Weather information for '{city}' is not available."}

    @Tool.from_function_schema(
        name="get_current_time",
        description="Returns the current time in a specified city.",
        input_schema={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get the current time for."
                }
            },
            "required": ["city"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Either 'success' or 'error'"},
                "report": {"type": "string", "description": "The current time report if successful."},
                "error_message": {"type": "string", "description": "Details of the error if status is 'error'."}
            },
            "required": ["status"]
        }
    )
    def get_current_time(self, city: str) -> dict:
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
    tools = WeatherTimeTools()

    # Create the Reasoning Engine
    reasoning_engine = ReasoningEngine.create(
        tools=[tools.get_weather, tools.get_current_time],
        model_name='gemini-1.5-flash-001', # Using a common and available model
        display_name="Weather and Time Agent (Simplified)",
    )

    print("Agent deployment complete!")
    print(f"Resource Name:\n{reasoning_engine.resource_name}")
    return reasoning_engine

if __name__ == "__main__":
    deploy_agent()
