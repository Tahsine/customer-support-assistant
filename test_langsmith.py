from os import getenv
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=getenv("GOOGLE_API_KEY")
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

agent.invoke(
    {"messages": [{
        "role": "user",
        "content": "What is the weather in San Francisco?"
    }]}
)