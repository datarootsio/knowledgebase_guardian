import os
from typing import Any, Dict

from kb_guardian.contradiction_detection import contradiction_detection
from kb_guardian.docs_chunks_conversion import create_document_chunks
from kb_guardian.logger import INFO_LOGGER
from kb_guardian.utils.paths import (
    get_data_folders,
    get_default_config,
    get_vectorstore_paths,
)
from kb_guardian.utils.vectorstore import (
    create_FAISS_vectorstore,
    load_FAISS_vectorstore,
    save_FAISS_vectorstore,
)

CONFIG = get_default_config()


def create_vectorstore(config: Dict[str, Any]) -> None:
    """
    Create a FAISS vectorstore based on an initial set of documents.

    Args:
        config (Dict[str, Any]): configuration specifying data locations and settings for the chunking and embedding.

    Returns:
        None
    """  # noqa: E501
    CONFIG.update(config)

    index_path, vectorstore_path, _, _ = get_vectorstore_paths(CONFIG)
    raw_data_folder, _ = get_data_folders(CONFIG)

    docs_chunks = create_document_chunks(
        data_path=raw_data_folder,
        extension=CONFIG["extension"],
        chunk_size=CONFIG["chunk_size"],
        chunk_overlap=CONFIG["chunk_overlap"],
    )

    vectorstore = create_FAISS_vectorstore(
        docs_chunks, CONFIG["azure_openai"], CONFIG["embedding_model"]
    )
    save_FAISS_vectorstore(vectorstore, index_path, vectorstore_path)


def extend_vectorstore(
    config: Dict[str, Any], detect_contradictions: bool = True
) -> None:
    """
    Extend a FAISS vectorstore with a set of documents and optionally apply contradiction detection to avoid adding conflicting documents.

    Args:
        config (Dict[str, Any]): configuration specifying data location and settings for the chunking and contradiction detection chain
        detect_contradictions (str, optional): Whether to look for contradictions between the new documents and the documents that are already in the vectorstore. Defaults to True.
    """  # noqa: E501
    config = CONFIG.update(config)

    (
        index_path,
        vectorstore_path,
        extended_index_path,
        extended_vectorstore_path,
    ) = get_vectorstore_paths(CONFIG)
    _, extension_data_folder = get_data_folders(CONFIG)

    if not (os.path.isfile(vectorstore_path)):
        INFO_LOGGER.error(
            f"Vectorstore {vectorstore_path} does not exist and can therefore not be extended."  # noqa: E501
        )
    else:
        vectorstore = load_FAISS_vectorstore(index_path, vectorstore_path)

        INFO_LOGGER.info("Splitting documents into chunks...")
        docs_chunks = create_document_chunks(
            data_path=extension_data_folder,
            extension=CONFIG["extension"],
            chunk_size=CONFIG["chunk_size"],
            chunk_overlap=CONFIG["chunk_overlap"],
        )

        if not detect_contradictions:
            INFO_LOGGER.info(
                "Extending the vectorstore by force. No contradiction detection will be performed."  # noqa: E501
            )
            vectorstore.add_documents(docs_chunks)
        else:
            vectorstore = contradiction_detection(vectorstore, docs_chunks, CONFIG)

        INFO_LOGGER.info("Saving the extended vectorstore...")
        save_FAISS_vectorstore(
            vectorstore, extended_index_path, extended_vectorstore_path
        )
