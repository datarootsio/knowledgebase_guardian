import logging
from typing import Any, Dict

from langchain.schema import Document


def setup_logger(logger_name: str, file_name: str):
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(file_name)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


INFO_LOGGER = setup_logger("execution_info", "execution.log")
CONTRADICTION_LOGGER = setup_logger("contradictions", "contradictions.log")


def log_contradiction(doc: Document, llm_result: Dict[str, Any]):
    """
    Log the document for which a contradiction was detected, together with the explanation of the LLM and the documents from the vectorstore with which the new document conflicts.

    Args:
        doc (Document): The new document (chunk) that conflicts with the documents in the existing vectorstore
        llm_result (Dict[str, Any]): The output of the LLM, describing the contradiction(s).
        logger (Logger): The logger object to use for logging the contradictions.
    """  # noqa: E501
    source_docs = [
        f'\t{source_doc.metadata["source"]}\n'
        for source_doc in llm_result["source_documents"]
    ]

    answer = llm_result["answer"].replace("\n", "\n\t")
    doc_content = doc.page_content.replace("\n", "\n\t")
    retrieved_docs = [
        source_doc.page_content.replace("\n", "\n\t")
        for source_doc in llm_result["source_documents"]
    ]
    retrieved_docs_string = "\n\n".join(retrieved_docs)

    CONTRADICTION_LOGGER.info(
        f"""
        Contradiction detected for document {doc.metadata["source"]},
        while comparing with the following documents:
        {source_docs}
        Conclusion from the LLM:
        {answer}

        Content of new document:
        {doc_content}

        Retrieved documents:
        {retrieved_docs_string}
    """
    )

    for source_doc in llm_result["source_documents"]:
        CONTRADICTION_LOGGER.info(source_doc.page_content)


def log_consistency(doc: Document, llm_result: Dict[str, Any]):
    """
    Log the document for which a contradiction was detected, together with the explanation of the LLM and the documents from the vectorstore with which the new document conflicts.

    Args:
        doc (Document): The new document (chunk) that conflicts with the documents in the existing vectorstore
        llm_result (Dict[str, Any]): The output of the LLM, describing the contradiction(s).
        logger (Logger): The logger object to use for logging the contradictions.
    """  # noqa: E501
    source_docs = [
        f'{source_doc.metadata["source"]}'
        for source_doc in llm_result["source_documents"]
    ]

    answer = llm_result["answer"].replace("\n", "\n\t")

    INFO_LOGGER.info(
        f"""
        No contradiction detected for document {doc.metadata["source"]},
        while comparing with the following documents:
        {source_docs}
        Conclusion from the LLM:
        {answer}
    """
    )
