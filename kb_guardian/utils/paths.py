from pathlib import Path
from typing import Any, Dict, Tuple

import yaml


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_config() -> Dict[str, Any]:
    project_root = get_project_root()

    with open(project_root / "config.yml", "r") as f:
        config = yaml.safe_load(f)

    return config


def get_vectorstore_paths(config: Dict[str, Any]) -> Tuple[str, str, str, str]:
    project_root = get_project_root()

    prefix = project_root / config["vectorstore_dir"] / config["vectorstore_name"]

    index_path = f"{prefix}.index"
    vectorstore_path = f"{prefix}.pkl"
    extended_index_path = f"{prefix}_extended.index"
    extended_vectorstore_path = f"{prefix}_extended.pkl"

    return index_path, vectorstore_path, extended_index_path, extended_vectorstore_path


def get_data_folders(config: Dict[str, Any]) -> Tuple[Path, Path]:
    project_root = get_project_root()

    raw_dir = Path(project_root / config["raw_dir"])
    extension_dir = Path(project_root / config["extension_dir"])

    return raw_dir, extension_dir
