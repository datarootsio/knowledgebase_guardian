from pathlib import Path
from typing import Any, Dict, Tuple

import yaml


def get_project_root() -> Path:  # noqa: D103
    return Path(__file__).parent.parent.parent


def get_config() -> Dict[str, Any]:  # noqa: D103
    project_root = get_project_root()

    with open(project_root / "config.yml", "r") as f:
        config = yaml.safe_load(f)

    return config


def get_vectorstore_paths(config: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """
    Return the paths to the current and future indexfile and vectorstore.

    Args:
        config (Dict[str, Any]): configuration containing the location of the vector store folder

    Returns:
        Tuple[str, str, str, str]: current location of index file and vector store file,
        future location of extended index file and extended vector store file
    """  # noqa: E501
    project_root = get_project_root()

    prefix = project_root / config["vectorstore_dir"] / config["vectorstore_name"]

    index_path = f"{prefix}.index"
    vectorstore_path = f"{prefix}.pkl"
    extended_index_path = f"{prefix}_extended.index"
    extended_vectorstore_path = f"{prefix}_extended.pkl"

    return index_path, vectorstore_path, extended_index_path, extended_vectorstore_path


def get_data_folders(config: Dict[str, Any]) -> Tuple[Path, Path]:
    """
    Return the paths to the raw and extension data folders.

    Args:
        config (Dict[str, Any]): configuration describing the location of the data folders

    Returns:
        Tuple[Path, Path]: location of raw and extension data folders
    """  # noqa: E501
    project_root = get_project_root()

    raw_dir = Path(project_root / config["raw_dir"])
    extension_dir = Path(project_root / config["extension_dir"])

    return raw_dir, extension_dir
