__version__ = "0.1.3"

import importlib
import logging
import sys
from typing import TYPE_CHECKING, Optional

from .types import *  # noqa # isort: skip
from .parsers.parser import Parser
from .parsers.think_parser import ThinkParser
from .parsers.xml_parser import XMLParser
from .rubrics.judge_rubric import JudgeRubric
from .rubrics.rubric import Rubric
from .rubrics.rubric_group import RubricGroup
from .utils.data_utils import (
    extract_boxed_answer,
    extract_hash_answer,
    load_example_dataset,
)

# Setup default logging configuration
def setup_logging(
    level: str = "INFO",
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
) -> None:
    """
    Setup basic logging configuration for the verifiers package.

    Args:
        level: The logging level to use. Defaults to "INFO".
        log_format: Custom log format string. If None, uses default format.
        date_format: Custom date format string. If None, uses default format.
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"

    # Create a StreamHandler that writes to stderr
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))

    # Get the root logger for the verifiers package
    logger = logging.getLogger("verifiers")
    logger.setLevel(level.upper())
    logger.addHandler(handler)

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False


setup_logging()

__all__ = [
    "Parser",
    "ThinkParser",
    "XMLParser",
    "Rubric",
    "JudgeRubric",
    "RubricGroup",
    "extract_boxed_answer",
    "extract_hash_answer",
    "load_example_dataset",
    "setup_logging",
]

_LAZY_IMPORTS = {
    "get_model": "verifiers.utils.model_utils:get_model",
    "get_model_and_tokenizer": "verifiers.utils.model_utils:get_model_and_tokenizer",
    "get_tokenizer": "verifiers.utils.model_utils:get_tokenizer",
    "GRPOConfig": "verifiers.trainers:GRPOConfig",
    "GRPOTrainer": "verifiers.trainers:GRPOTrainer",
    "grpo_defaults": "verifiers.trainers:grpo_defaults",
    "lora_defaults": "verifiers.trainers:lora_defaults",
}


def __getattr__(name: str):
    try:
        module, attr = _LAZY_IMPORTS[name].split(":")
        return getattr(importlib.import_module(module), attr)
    except KeyError:
        raise AttributeError(f"module 'verifiers' has no attribute '{name}'")
    except ModuleNotFoundError as e:
        # warn that accessed var needs [all] to be installed
        raise AttributeError(
            f"To use verifiers.{name}, install as `verifiers[all]`. "
        ) from e
