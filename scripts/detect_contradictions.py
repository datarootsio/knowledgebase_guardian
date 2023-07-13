import argparse
import os
from argparse import Namespace

from dotenv import load_dotenv

from kb_guardian.contradiction_detection import contradiction_detection
from kb_guardian.docs_chunks_conversion import create_document_chunks
from kb_guardian.logger import INFO_LOGGER
from kb_guardian.utils.paths import get_config, get_data_folders, get_vectorstore_paths
from kb_guardian.utils.vectorstore import load_FAISS_vectorstore, save_FAISS_vectorstore

CONFIG = get_config()

if CONFIG["azure_openai"]:
    load_dotenv(".env.cloud", override=True)
else:
    load_dotenv(".env", override=True)

(
    INDEX_PATH,
    VECTORSTORE_PATH,
    EXTENDED_INDEX_PATH,
    EXTENDED_VECTORSTORE_PATH,
) = get_vectorstore_paths(CONFIG)
RAW_DATA_FOLDER, EXTENSION_DATA_FOLDER = get_data_folders(CONFIG)


def parse_arguments() -> Namespace:
    """
    Parse and return arguments for the contradiction detection mechanism.

    Returns:
        Namespace: The arguments necessary for contradiction detection
    """
    parser = argparse.ArgumentParser(description="Extend vectorstores")

    parser.add_argument(
        "--force-extend",
        dest="force_extend",
        default=False,
        help="Force the extension of an existing vectorstore",
    )
    args = parser.parse_args()
    return args


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
