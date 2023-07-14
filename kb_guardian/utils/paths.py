from pathlib import Path
from typing import Any, Dict, Tuple

import yaml


def get_project_root() -> Path:  # noqa: D103
    return Path(__file__).parent.parent.parent


def get_config(config_location: str) -> Dict[str, Any]:
    """
    Load the config file.

    Args:
        config_location (str): Location of the config file.

    Returns:
        Dict[str, Any]: The config file
    """  # noqa: E501
    with open(config_location, "r") as f:
        config = yaml.safe_load(f)
    return config


def get_default_config() -> Dict[str, Any]:
    """
    Load the default config file.

    The project root will be set to the directory where this repository is cloned.

    Returns:
        Dict[str, Any]: The default config file
    """
    project_root = get_project_root()

    with open(project_root / "default_config.yml", "r") as f:
        config = yaml.safe_load(f)

    config["project_root"] = project_root
    return config


def get_vectorstore_paths(config: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """
    Return the paths to the current and future indexfile and vectorstore.

    Args:
        config (Dict[str, Any]): configuration containing the location of the vector store files

    Returns:
        Tuple[str, str, str, str]: current location of index file and vector store file,
        future location of extended index file and extended vector store file
    """  # noqa: E501
    project_root = config["project_root"]

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
    project_root = config["project_root"]
    raw_dir = Path(project_root / config["raw_dir"])
    extension_dir = Path(project_root / config["extension_dir"])

    return raw_dir, extension_dir
