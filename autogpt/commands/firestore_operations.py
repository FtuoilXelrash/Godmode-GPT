"""File operations for AutoGPT"""
from __future__ import annotations

import hashlib
import os
import os.path
from typing import Dict, Generator, Literal, Tuple

import charset_normalizer
import requests
from colorama import Back, Fore
from requests.adapters import HTTPAdapter, Retry
from autogpt.api_utils import get_file, list_files, write_file

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.logs import logger
from autogpt.spinner import Spinner
from autogpt.utils import readable_file_size

global_config = Config()

Operation = Literal["write", "append", "delete"]


@command("read_file", "Read file", '"filename": "<filename>"')
def f_read_file(filename: str, cfg, **kwargs) -> str:
    """Read a file and return the contents

    Args:
        filename (str): The name of the file to read

    Returns:
        str: The contents of the file
    """
    try:
        return get_file(filename, cfg.agent_id)
    except Exception as err:
        return f"Error: File doesn't exist"


@command("write_to_file", "Write to file", '"filename": "<filename>", "text": "<text>"')
def write_to_file(filename: str, text: str, cfg, **kwargs):
    """Write text to a file

    Args:
        filename (str): The name of the file to write to
        text (str): The text to write to the file

    Returns:
        str: A message indicating success or failure
    """
    write_file(text, filename, cfg.agent_id)


@command(
    "append_to_file", "Append to file", '"filename": "<filename>", "text": "<text>"'
)
def append_to_file(filename: str, append_text: str, should_log: bool = True, cfg = None, **kwargs) -> str:
    """Append text to a file

    Args:
        filename (str): The name of the file to append to
        text (str): The text to append to the file
        should_log (bool): Should log output

    Returns:
        str: A message indicating success or failure
    """
    try:
        text = get_file(filename, cfg.agent_id)
    except Exception as err:
        text = ""

    text +=  "\n" + append_text
    write_file(text, filename, cfg.agent_id)


@command("list_files", "List Files in Directory", '"directory": "<directory>"')
def f_list_files(cfg, **kwargs) -> list[str]:
    """lists files in a directory recursively

    Args:
        directory (str): The directory to search in

    Returns:
        list[str]: A list of files found in the directory
    """
    return list_files(
        cfg.agent_id
    )
