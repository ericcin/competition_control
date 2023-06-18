"""
Module Name: concurrency_dispatching
Author: Equipe 3
Purpose: Recebe mensagens em JSON e despacham para o método adequado do LockManager.
Created: 2023-06-14
"""
from typing import Any, Dict

from lock_manager import LockManager
from settings import debug_message, info_message, init_logger

logger = init_logger(__name__)

def init(message: Dict[str, Any]) -> Dict[str, Any]:
    try:
        data_items = message["data_items"]
        global lock_manager
        lock_manager = LockManager(data_items)
        result = lock_manager.list_data_items()
    except Exception as e:
        result = {"error": f"init: {str(e)}"}
        debug_message(result)
    debug_message(f"init: result: {result}")
    return result

def list_data_items(message: Dict[str, Any]) -> Dict[str, Any]:
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

def dispatcher(method, message):
    info_message(f"lock_manager_dispatcher: method = {method}")
    switch = {
        "init": init,
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