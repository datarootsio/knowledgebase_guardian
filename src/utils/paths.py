from pathlib import Path
from typing import Any, Dict, List


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_vectorstore_paths(config: Dict[str, Any]) -> List[Path]:
    project_root = get_project_root()

    prefix = f"{project_root}/{config['vectorstore_dir']}/{config['vectorstore_name']}"

    index_path = f"{prefix}.index"
    vectorstore_path = f"{prefix}.pkl"
    extended_index_path = f"{prefix}_extended.index"
    extended_vectorstore_path = f"{prefix}_extended.pkl"

    return index_path, vectorstore_path, extended_index_path, extended_vectorstore_path


def get_data_folders(config: Dict[str, Any]) -> List[Path]:
    project_root = get_project_root()

    raw_dir = f"{project_root}/{config['raw_dir']}"
    extension_dir = f"{project_root}/{config['extension_dir']}"

    return raw_dir, extension_dir
