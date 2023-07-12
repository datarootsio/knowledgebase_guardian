import copy
import logging

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models.fake import FakeListChatModel
from langchain.llms.fake import FakeListLLM
from langchain.schema import Document
from pytest_mock import MockerFixture
from pytest_mock.logging import LogCaptureFixture

from kb_guardian.contradiction_detection import (
    contradiction_detection,
    get_detection_chain,
)
from kb_guardian.utils.paths import get_project_root
from kb_guardian.utils.vectorstore import load_FAISS_vectorstore

project_root = get_project_root()
vectorstore_path = str(project_root) + "/tests/files/leuven.pkl"
vectorstore_index = str(project_root) + "/tests/files/leuven.index"
vectorstore = load_FAISS_vectorstore(vectorstore_index, vectorstore_path)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


def test_get_detection_chain(mocker: MockerFixture) -> None:
    """
    Test whether the contradiction detection chain is correctly created.

    Args:
        mocker (MockerFixture): Pytest fixture used to mock an LLM.
    """
    llm = FakeListLLM(responses=["This is a fake LLM response."])

    mocker.patch(
        "kb_guardian.contradiction_detection.get_deployment_llm", return_value=llm
    )

    chain = get_detection_chain(retriever)

    assert isinstance(chain, RetrievalQAWithSourcesChain)
    assert chain.retriever == retriever
    assert chain.combine_documents_chain.llm_chain.llm == llm


def test_contradiction_detection(
    mocker: MockerFixture, caplog: LogCaptureFixture
) -> None:
    """
    Test whether the contradiction detection results are processed correctly.

    Args:
        mocker (MockerFixture): Pytest fixture used to mock an LLM.
        caplog (LogCaptureFixture): Pytest fixture used to capture and test logs.
    """
    caplog.set_level(logging.INFO)

    llm = FakeListChatModel(
        responses=[
            "CONSISTENT: this chunk was consistent.",
            """INCONSISTENT: the following contradictions were detected for this chunk:
        1. Contradiction1
        2. Contradiction2
        """,
        ]
    )

    chunks = [
        Document(
            page_content="Content of chunk 1", metadata={"source": "Fake source 1"}
        ),
        Document(
            page_content="Content of chunk 2", metadata={"source": "Fake source 2"}
        ),
    ]

    old_vectorstore = copy.deepcopy(vectorstore)

    mocker.patch(
        "kb_guardian.contradiction_detection.get_deployment_llm", return_value=llm
    )
    # This method is tested separately
    mocker.patch("kb_guardian.contradiction_detection.log_contradiction_result")

    new_vectorstore = contradiction_detection(vectorstore, chunks)

    assert "1 new chunks have been added to the vectorstore." in caplog.text
    assert (
        "1 chunks were found to contain contradictions and have been rejected."
        in caplog.text
    )
    assert len(new_vectorstore.docstore._dict) > len(old_vectorstore.docstore._dict)
