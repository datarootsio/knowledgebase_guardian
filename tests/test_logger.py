from langchain.schema import Document
from pytest import LogCaptureFixture

from kb_guardian.logger import format_retrieved_documents, log_contradiction_result

source_doc1 = Document(
    page_content="Content of source doc 1.", metadata={"source": "Source 1"}
)
source_doc2 = Document(
    page_content="Content of source doc 2.", metadata={"source": "Source 2"}
)
chunk = Document(page_content="Content of a chunk.", metadata={"source": "Test source"})


def test_format_retrieved_documents() -> None:
    """Test whether source documents are formatted correctly for logging."""
    formatted_docs = format_retrieved_documents([source_doc1, source_doc2])

    assert (
        """
        1. Retrieved chunk from document Source 1 with the following content:
        Content of source doc 1.
    """
        in formatted_docs
    )

    assert (
        """
        2. Retrieved chunk from document Source 2 with the following content:
        Content of source doc 2.
    """
        in formatted_docs
    )


def test_log_contradiction_result_success(caplog: LogCaptureFixture) -> None:
    """
    Test whether a chunk that does not contain contradictions is logged correctly.

    Args:
        caplog (LogCaptureFixture): Pytest fixture to capture and validate logs.
    """
    llm_result = {
        "answer": "CONSISTENT: this chunk was consistent.",
        "source_documents": [source_doc1, source_doc2],
    }

    log_contradiction_result(chunk, llm_result, contradiction=False)

    assert (
        """
        No contradiction detected for document Test source.

        Conclusion from the LLM:
        CONSISTENT: this chunk was consistent.

        Content of new document:
        Content of a chunk.

        Retrieved documents:
    """
        in caplog.text
    )


def test_log_contradiction_result_failure(caplog: LogCaptureFixture) -> None:
    """
    Test whether a chunk that does not contain contradictions is logged correctly.

    Args:
        caplog (LogCaptureFixture): Pytest fixture to capture and validate logs.
    """
    llm_result = {
        "answer": """
        INCONSISTENT: the following contradictions were detected for this chunk:
        1. Contradiction1
        2. Contradiction2
        """,
        "source_documents": [source_doc1, source_doc2],
    }

    log_contradiction_result(chunk, llm_result, contradiction=True)

    # Assertions are split in three because otherwise the log formatting
    # conflicts with the pre-commit hooks regarding trailing whitespaces

    assert (
        """
        Contradiction detected for document Test source.

        Conclusion from the LLM:
    """
        in caplog.text
    )

    assert (
        """
\t\t        INCONSISTENT: the following contradictions were detected for this chunk:
\t\t        1. Contradiction1
\t\t        2. Contradiction2
\t\t"""
        in caplog.text
    )

    assert (
        """
        Content of new document:
        Content of a chunk.

        Retrieved documents:
    """
        in caplog.text
    )
