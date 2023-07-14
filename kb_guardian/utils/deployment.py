import os

from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.embeddings import OpenAIEmbeddings


def get_deployment_embedding(
    azure_openai: bool = False, embedding_model: str = "text-embedding-ada-002"
) -> OpenAIEmbeddings:
    """
    Return an embedding deployed on Azure or an embedding from OpenAI.

    When using AzureOpenAI, the DEPLOYMENT_EMBEDDING environment variable should be set.

    Args:
        azure_openai (bool): True if using an embedding deployed on Azure OpenAI, else False. Defaults to False.
        embedding_model (str): OpenAI embedding model to use. This argument is not relevant when using Azure OpenAI. Defaults to text-embedding-ada-002.

    Returns:
        OpenAIEmbeddings: An embedding provided by OpenAI or deployed on AzureOpenAI.
    """  # noqa: E501
    if azure_openai:
        deployment_embedding = os.getenv("DEPLOYMENT_EMBEDDING")
        return OpenAIEmbeddings(
            deployment=deployment_embedding,
            chunk_size=1,
        )
    else:
        return OpenAIEmbeddings(model=embedding_model)


def get_deployment_llm(
    azure_openai: bool = False, llm: str = "gpt-3.5-turbo"
) -> BaseChatModel:
    """
    Return an LLM deployed on Azure or an LLM from OpenAI.

    When using AzureOpenAI, the DEPLOYMENT_LLM environment variable should be set.

    Args:
        azure_openai (bool): True if using an LLM deployed on Azure OpenAI, else False. Defaults to False.
        llm (str): OpenAI LLM to use. This argument is not relevant when using Azure OpenAI. Defaults to gpt-3.5-turbo.
    Returns:
        BaseChatModel: An LLM provided by OpenAI
    """  # noqa: E501
    if azure_openai:
        deployment_llm = os.getenv("DEPLOYMENT_LLM")
        return AzureChatOpenAI(
            deployment_name=deployment_llm, streaming=True, temperature=0
        )
    else:
        return ChatOpenAI(model_name=llm, streaming=True, temperature=0)
