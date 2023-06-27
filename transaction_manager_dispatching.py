"""
Module Name: transaction_manager_dispatching
Author: Equipe 3
Purpose: Recebe mensagens em JSON e despacham para o método adequado do TransactionManager.
Created: 2023-06-19
"""
from typing import Any, Dict, List

import json

from transaction_manager import TransactionManager
from lock_manager_dispatching import get_lock_manager
from settings import debug_message, info_message, init_logger, inspect_type

logger = init_logger(__name__)

transaction_manager = TransactionManager(get_lock_manager())


def get_transaction_manager():
    return transaction_manager


def reset(message: Dict[str, Any]) -> Dict[str, Any]:
    global transaction_manager
    # debug_message(
    #     f"""transaction_manager_dispatching: __init__:
    #             inspect_type(message) = {inspect_type(message)},
    #             message = {message}"""
    # )
    try:
        transactions = message["transactions"]
        # debug_message(f"transactions: {transactions}")
        transaction_manager = TransactionManager(transactions, get_lock_manager)
        result = transaction_manager.list_transactions()
    except Exception as e:
        result = {"error": f"reset: {str(e)}"}
        # debug_message(result)
    # debug_message(f"reset: result: {result}")
    return result


def init_transaction_manager(message: List[str]) -> Dict[str, Any]:
    reset({"transactions": message})
    return transaction_manager


def list_transactions(message: Dict[str, Any]) -> Dict[str, Any]:
    # debug_message(f"list_transactions: message: {message}")
    try:
        result = transaction_manager.list_transactions()
    except Exception as e:
        result = {"error": f"list_transactions: {str(e)}"}
    # debug_message(f"list_transactions: result: {result}")
    return result

def add_transaction(message: Dict[str, Any]) -> Dict[str, Any]:
    # debug_message(f"add_transaction: message: {message}")
    try:
        transaction_string = message["transaction_string"]
        # debug_message(f"transaction_string: {transaction_string}")
        result = transaction_manager.add_transaction(transaction_string)
    except Exception as e:
        result = {"error": f"{str(e)}"}
    # debug_message(f"add_transaction: result: {result}")
    return result

def list_locks(message: Dict[str, Any]) -> Dict[str, Any]:
    # debug_message(f"transaction_manager_dispatcher: list_locks: message: {message}")
    try:
        result = transaction_manager.list_locks()
    except Exception as e:
        result = {"error": f"transaction_manager_dispatcher: list_locks: {str(e)}"}
    # debug_message(f"transaction_manager_dispatcher: list_locks: result: {result}")
    return result

def step_into(message: Dict[str, Any]) -> Dict[str, Any]:
    debug_message(f"transaction_manager_dispatcher: step_into: message: {message}")
    try:
        result = transaction_manager.step_into()
    except Exception as e:
        result = {"error": f"step_into: {str(e)}"}
    debug_message(f"transaction_manager_dispatcher: step_into: result: {result}")
    return result

def transaction_manager_dispatcher(method, message):
    info_message(f"transaction_manager_dispatcher: method = {method}")
    switch = {
        "reset": reset,
        "list_transactions": list_transactions,
        "list_locks": list_locks,
        "step_into": step_into,
        "add_transaction": add_transaction,
    }
    if method in switch:
        debug_message(f"transaction_manager_dispatcher: message: {message}")
        result = switch[method](message)
    else:
        result = {"status": "error", "message": "Invalid method"}
    debug_message(f"transaction_manager_dispatcher: result: {result}")
    return json.dumps(result)
    # return result
