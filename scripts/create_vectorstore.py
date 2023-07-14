import argparse
from argparse import Namespace

from dotenv import load_dotenv

from kb_guardian.kb_management import create_vectorstore
from kb_guardian.utils.paths import get_config, get_default_config

DEFAULT_CONFIG = get_default_config()


def parse_arguments() -> Namespace:
    """
    Parse and return arguments for the vectorstore creation.

    Returns:
        Namespace: The arguments necessary for vectorstore creation
    """
    parser = argparse.ArgumentParser(description="Create vectorstore")

    parser.add_argument(
        "--config-file",
        dest="config_file",
        help="The location of the config file",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    if args.config_file:
        config = get_config(args.config_file)
    else:
        config = DEFAULT_CONFIG

    if config["azure_openai"]:
        load_dotenv(".env.cloud", override=True)
    else:
        load_dotenv(".env", override=True)

    create_vectorstore(config)
