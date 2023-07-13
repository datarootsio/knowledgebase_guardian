from dotenv import load_dotenv

from kb_guardian.docs_chunks_conversion import create_document_chunks
from kb_guardian.utils.paths import get_config, get_data_folders, get_vectorstore_paths
from kb_guardian.utils.vectorstore import (
    create_FAISS_vectorstore,
    save_FAISS_vectorstore,
)

CONFIG = get_config()

if CONFIG["azure_openai"]:
    load_dotenv(".env.cloud", override=True)
else:
    load_dotenv(".env", override=True)

INDEX_PATH, VECTORSTORE_PATH, _, _ = get_vectorstore_paths(CONFIG)
RAW_DATA_FOLDER, _ = get_data_folders(CONFIG)


if __name__ == "__main__":
    docs_chunks = create_document_chunks(
        data_path=RAW_DATA_FOLDER,
        extension=CONFIG["extension"],
        chunk_size=CONFIG["chunk_size"],
        chunk_overlap=CONFIG["chunk_overlap"],
    )

    vectorstore = create_FAISS_vectorstore(docs_chunks)
    save_FAISS_vectorstore(vectorstore, INDEX_PATH, VECTORSTORE_PATH)
