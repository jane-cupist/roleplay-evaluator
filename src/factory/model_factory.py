import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()


class ModelFactory:
    @staticmethod
    def create_model(model_type: str = "cl", **kwargs) -> BaseChatModel:
        if model_type == "gp":
            return ChatOpenAI(
                model="gpt-4o",
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                **kwargs,
            )
        elif model_type == "cl":
            return ChatAnthropic(
                model="claude-3-7-sonnet-20250219",
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                **kwargs,
            )
        elif model_type == "ge":
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-001",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                **kwargs,
            )
        elif model_type == "ll":
            return ChatOpenAI(
                openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                openai_api_base="https://openrouter.ai/api/v1",
                model="meta-llama/llama-3.1-70b-instruct",
                **kwargs,
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
