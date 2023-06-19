"""
Module Name: concurrency_dispatching
Author: Equipe 3
Purpose: Recebe mensagens em JSON e despacham para o método adequado do LockManager.
Created: 2023-06-14
"""
import json
from typing import Any, Dict, List

from lock_manager import LockManager
from settings import debug_message, info_message, init_logger, inspect_type

logger = init_logger(__name__)

lock_manager = LockManager()


def get_lock_manager():
    return lock_manager


def reset(message: Dict[str, Any]) -> Dict[str, Any]:
    global lock_manager
    debug_message(
        f"""lock_manager_dispatching: __init__:
                inspect_type(message) = {inspect_type(message)},
                message = {message}"""
    )
    try:
        data_items = message["data_items"]
        debug_message(f"data_items: {data_items}")
        lock_manager = LockManager(data_items)
        result = lock_manager.list_data_items()
    except Exception as e:
        result = {"error": f"reset: {str(e)}"}
        debug_message(result)
    debug_message(f"reset: result: {result}")
    return result


def init_lock_manager(message: List[str]) -> Dict[str, Any]:
    reset({"data_items": message})
    return lock_manager


def list_data_items(message: Dict[str, Any]) -> Dict[str, Any]:
    debug_message(f"list_data_items: message: {message}")
    try:
        result = lock_manager.list_data_items()
    except Exception as e:
        result = {"error": f"list_data_items: {str(e)}"}
    debug_message(f"list_data_items: result: {result}")
    return result


def formatted_list_data_items(message: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = lock_manager.formatted_list_data_items()
    except Exception as e:
        result = {"error": f"formatted_list_data_items: {str(e)}"}
    debug_message(f"result: {result}")
    return result


def get_lock_status(message):
    # Implementation for 'get_lock_status' method

    # Process the message
    # ...
    return message


def list_locks(message):
    # Implementation for 'list_locks' method

    # Process the message
    # ...
    return message


def has_shared_lock(message):
    # Implementation for 'has_shared_lock' method

    # Process the message
    # ...
    return message


def has_exclusive_lock(message):
    # Implementation for 'has_exclusive_lock' method

    # Process the message
    # ...
    return message


def release_lock(message):
    # Implementation for 'release_lock' method

    # Process the message
    # ...
    return message


def acquire_shared_lock(message):
    # Implementation for 'acquire_shared_lock' method

    # Process the message
    # ...
    return message


def acquire_exclusive_lock(message):
    # Implementation for 'acquire_exclusive_lock' method

    # Process the message
    # ...
    return message


def lock_manager_dispatcher(method, message):
    info_message(f"lock_manager_dispatcher: method = {method}")
    switch = {
        "reset": reset,
        "get_lock_status": get_lock_status,
        "list_locks": list_locks,
        "has_shared_lock": has_shared_lock,
        "has_exclusive_lock": has_exclusive_lock,
        "release_lock": release_lock,
        "acquire_shared_lock": acquire_shared_lock,
        "acquire_exclusive_lock": acquire_exclusive_lock,
        "list_data_items": list_data_items,
        "formatted_list_data_items": formatted_list_data_items,
    }
    if method in switch:
        debug_message(f"lock_manager_dispatcher: message: {message}")
        result = switch[method](message)
    else:
        result = {"status": "error", "message": "Invalid method"}
    debug_message(f"lock_manager_dispatcher: {result}")
    return result
