from os import getenv
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

ollama_llm = ChatOllama(
    model="qwen3-vl:4b",
    temperature=0,
)

gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=getenv("GOOGLE_API_KEY")
)
