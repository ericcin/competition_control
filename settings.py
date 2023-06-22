"""
Module Name: settings
Author: Equipe 3
Purpose: Funções de log e debug.
Created: 2023-06-13
"""

import logging
import datetime
from typing import Any, Dict
from decouple import config

# Set up the logger
def init_logger(fname: str = "common") -> logging.Logger:
   print(f"Creating logger for: {fname}")
   if (fname == ""):
       fname = "common"
   logger = logging.getLogger(fname)
   logger.setLevel(logging.DEBUG)
   log_file = f"logs/{fname}.log"
   file_handler = logging.FileHandler(log_file)
   file_handler.setLevel(logging.DEBUG)
   formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
   file_handler.setFormatter(formatter)
   logger.addHandler(file_handler)
   if (fname!="common"):
      logger.debug(f"Module {fname} is running.")
   else:
      logger.debug("Running.")
   return logger

# Log the module load message
common_logger = init_logger()
logger = init_logger(__name__)

def time_print(message) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: {message}")

def info_message(message: str) -> None:
    common_logger.info(message)
    time_print(message)

def warning_message(message: str) -> None:
    common_logger.warning(message)
    time_print(message)

def error_message(message: str) -> None:
    common_logger.error(message)
    time_print(message)

def critical_message(message: str) -> None:
    common_logger.critical(message)
    time_print(message)

def debug_message(message: str) -> None:
    common_logger.info(message)
    time_print(message)

def load_settings() -> Dict[str, str]:
    info_message("Buscando configurações...")
    settings = {
       'CONCURRENCY_TABLES_DIRECTORY': config('CONCURRENCY_TABLES_DIRECTORY')
    }
    debug_message(settings)
    return settings

def inspect_type(variable: Any) -> str:
    if isinstance(variable, dict):
        # Check the types of the dictionary's values
        value_types = [f"{value}({inspect_type(value)})" for value in variable.values()]
        result = f"dict[{', '.join(value_types)}]"
    elif isinstance(variable, list):
        value_types = [f"{value}({inspect_type(value)})" for value in variable]
        result = f"list{value_types}"
    else:
        result = f"{variable}({type(variable).__name__})"
    return result

def inspect_structure(variable: Any) -> str:
    if isinstance(variable, dict):
        # Check the types of the dictionary's values
        value_structures = [f"{inspect_structure(value)}" for value in variable.values()]
        result = f"dict[{', '.join(value_structures)}]"
    elif isinstance(variable, list):
        value_structures = [f"{inspect_structure(value)}" for value in variable]
        result = f"list{value_structures}"
    else:
        result = f"{variable}({type(variable).__name__})"
    return result

def check_type(variable: Any) -> str:
    result = inspect_type(variable)
    debug_message(result)
    return result

def check_structure(variable: Any) -> str:
    result = inspect_structure(variable)
    debug_message(result)
    return result