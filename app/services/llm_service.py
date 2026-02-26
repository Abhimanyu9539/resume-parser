import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Configuration from environment variables
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


def get_llm(
    model_name: str = OPENAI_CHAT_MODEL, temperature: float = 0.0
) -> ChatOpenAI:
    """Returns an instance of the configured ChatOpenAI model."""
    return ChatOpenAI(model=model_name, temperature=temperature)


def get_embeddings(model_name: str = OPENAI_EMBED_MODEL) -> OpenAIEmbeddings:
    """Returns an instance of the configured OpenAI embeddings model."""
    return OpenAIEmbeddings(model=model_name)
