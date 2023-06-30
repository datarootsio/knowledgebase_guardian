import os

from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings


def get_deployment_embedding() -> OpenAIEmbeddings:
    """
    Returns a deployed embedding based on the DEPLOYMENT_EMBEDDING environment variable.

    Returns:
        OpenAIEmbeddings: A deployed embedding
    """
    deployment_embedding = os.getenv("DEPLOYMENT_EMBEDDING")
    embeddings = OpenAIEmbeddings(
        deployment=deployment_embedding,
        chunk_size=1,
    )

    return embeddings


def get_deployment_llm() -> AzureChatOpenAI:
    """
    Returns a deployed LLM based on the DEPLOYMENT_LLM environment variable.

    Returns:
        AzureChatOpenAI: A deployed LLM
    """
    deployment_llm = os.getenv("DEPLOYMENT_LLM")
    llm = AzureChatOpenAI(deployment_name=deployment_llm, streaming=True, temperature=0)

    return llm
