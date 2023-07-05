import argparse
import os
from typing import List

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import Document
from langchain.vectorstores import VectorStore
from langchain.vectorstores.base import VectorStoreRetriever

from docs_chunks_conversion import create_document_chunks
from logger import INFO_LOGGER, log_contradiction_result
from utils.deployment import get_deployment_llm
from utils.paths import get_config, get_data_folders, get_vectorstore_paths
from utils.vectorstore import load_FAISS_vectorstore, save_FAISS_vectorstore

CONFIG = get_config()

(
    INDEX_PATH,
    VECTORSTORE_PATH,
    EXTENDED_INDEX_PATH,
    EXTENDED_VECTORSTORE_PATH,
) = get_vectorstore_paths(CONFIG)
RAW_DATA_FOLDER, EXTENSION_DATA_FOLDER = get_data_folders(CONFIG)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Extend vectorstores")

    parser.add_argument(
        "--force-extend",
        dest="force_extend",
        default=False,
        help="Force the extension of an existing vectorstore",
    )
    args = parser.parse_args()
    return args


def get_detection_chain(retriever: VectorStoreRetriever) -> RetrievalQAWithSourcesChain:
    """
    Constructs and returns an LLM chain to detect contradictions at ingestion time.

    Args:
        retriever (VectorStoreRetriever): A retriever for the vector store to which you want to add new documents

    Returns:
        RetrievalQAWithSourcesChain: A retrieval chain that allows you to detect contradictions
    """  # noqa: E501
    llm = get_deployment_llm()

    messages = [
        SystemMessagePromptTemplate.from_template(CONFIG["system_message"]),
        HumanMessagePromptTemplate.from_template(CONFIG["user_message"]),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": prompt,
        },
    )

    chain.reduce_k_below_max_tokens = True
    chain.return_source_documents = True
    return chain


def contradiction_detection(
    vectorstore: VectorStore,
    chunks: List[Document],
) -> VectorStore:
    """
    This method uses an LLM to detect inconsistencies / contradictions between the documents in a vectorstore and the documents that should be added to that vectorstore.
    New documents that do not contradict the existing documents are added to the vectorstore.
    New documents that are contradicting the existing documents are not added. Instead, a log with information about the detected contradictions will be stored.

    Args:
        vectorstore (VectorStore): An existing vectorstore to which you want to add new information
        docs_chunks (List[Document]): Chunks of the new documents you want to add

    Returns:
        VectorStore: An updated version of the vectorstore, including the new documents that do not contradict the existing documents.
    """  # noqa: E501
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": CONFIG["nb_retrieval_docs"]}
    )
    chain = get_detection_chain(retriever)

    nb_valid, nb_contradiction = 0, 0
    for chunk in chunks:
        result = chain({"question": chunk.page_content})
        if result["answer"].startswith("CONSISTENT"):
            vectorstore.add_documents([chunk])
            log_contradiction_result(chunk, result, contradiction=False)
            nb_valid += 1
        else:
            log_contradiction_result(chunk, result, contradiction=True)
            nb_contradiction += 1

    INFO_LOGGER.info(
        f"""
        {nb_valid} new chunks have been added to the vectorstore.
        {nb_contradiction} chunks were found to contain contradictions and have been rejected."""  # noqa: E501
    )

    return vectorstore


if __name__ == "__main__":
    args = parse_arguments()

    if not (os.path.isfile(VECTORSTORE_PATH)):
        INFO_LOGGER.error(
            f"Vectorstore {VECTORSTORE_PATH} does not exist and can therefore not be extended."  # noqa: E501
        )

    else:
        vectorstore = load_FAISS_vectorstore(INDEX_PATH, VECTORSTORE_PATH)

        INFO_LOGGER.info("Splitting documents into chunks...")
        docs_chunks = create_document_chunks(
            data_path=EXTENSION_DATA_FOLDER,
            extension=CONFIG["extension"],
            chunk_size=CONFIG["chunk_size"],
            chunk_overlap=CONFIG["chunk_overlap"],
        )

        if args.force_extend:
            INFO_LOGGER.info(
                "Extending the vectorstore by force. No contradiction detection will be performed."  # noqa: E501
            )
            vectorstore.add_documents(docs_chunks)
        else:
            vectorstore = contradiction_detection(vectorstore, docs_chunks)

        INFO_LOGGER.info("Saving the extended vectorstore...")
        save_FAISS_vectorstore(
            vectorstore, EXTENDED_INDEX_PATH, EXTENDED_VECTORSTORE_PATH
        )
