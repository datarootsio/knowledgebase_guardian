import argparse
from argparse import Namespace

from dotenv import load_dotenv

from kb_guardian.kb_management import extend_vectorstore
from kb_guardian.utils.paths import get_config, get_default_config

DEFAULT_CONFIG = get_default_config()


def parse_arguments() -> Namespace:
    """
    Parse and return arguments for the contradiction detection mechanism.

    Returns:
        Namespace: The arguments necessary for contradiction detection
    """
    parser = argparse.ArgumentParser(description="Extend vectorstores")

    parser.add_argument(
        "--config-file",
        dest="config_file",
        help="The location of the config file",
    )

    parser.add_argument(
        "--disable-contradiction-detection",
        dest="detect_contradictions",
        action="store_false",
        help="Disable contradiction detection and extend the vectorstore by force",  # noqa: E501
    )
    parser.set_defaults(detect_contradictions=True)
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

    extend_vectorstore(config, args.detect_contradictions)
