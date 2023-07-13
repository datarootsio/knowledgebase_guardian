import os
from pathlib import Path

from kb_guardian.utils.paths import (
    get_config,
    get_data_folders,
    get_project_root,
    get_vectorstore_paths,
)


def test_get_project_root() -> None:
    """Test whether project the project root is retrieved correctly."""
    project_root = get_project_root()

    dirs = [f.name for f in os.scandir(project_root)]

    folders = ["data", "images", "kb_guardian", "scripts", "tests"]

    for folder in folders:
        assert folder in dirs


def test_get_config() -> None:
    """Test whether the config file is loaded correctly."""
    config = get_config()

    assert len(config) == 13


def test_get_vectorstore_paths() -> None:
    """Test whether the vectorstore paths are loaded correctly."""
    config = {"vectorstore_dir": "data/vectorstore", "vectorstore_name": "belgium"}
    index_path, vectorstore_path, _, _ = get_vectorstore_paths(config)

    assert Path(index_path).exists()
    assert Path(vectorstore_path).exists()


def test_get_data_folders() -> None:
    """Test whether the data folder paths are loaded correctly."""
    config = {"raw_dir": "data/raw", "extension_dir": "data/extension"}
    raw_path, extended_path = get_data_folders(config)

    assert raw_path.exists()
    assert extended_path.exists()
