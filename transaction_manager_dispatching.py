"""
Module Name: transaction_manager_dispatching
Author: Equipe 3
Purpose: Recebe mensagens em JSON e despacham para o método adequado do TransactionManager.
Created: 2023-06-19
"""
from typing import Any, Dict, List

from transaction_manager import TransactionManager
from lock_manager_dispatching import get_lock_manager
from settings import debug_message, info_message, init_logger, inspect_type

logger = init_logger(__name__)

transaction_manager = TransactionManager(get_lock_manager())


def get_transaction_manager():
    return transaction_manager


def reset(message: Dict[str, Any]) -> Dict[str, Any]:
    global transaction_manager
    debug_message(
        f"""transaction_manager_dispatching: __init__:
                inspect_type(message) = {inspect_type(message)},
                message = {message}"""
    )
    try:
        transactions = message["transactions"]
        debug_message(f"transactions: {transactions}")
        transaction_manager = TransactionManager(transactions, get_lock_manager)
        result = transaction_manager.list_transactions()
    except Exception as e:
        result = {"error": f"reset: {str(e)}"}
        debug_message(result)
    debug_message(f"reset: result: {result}")
    return result


def init_transaction_manager(message: List[str]) -> Dict[str, Any]:
    reset({"transactions": message})
    return transaction_manager


def list_transactions(message: Dict[str, Any]) -> Dict[str, Any]:
    debug_message(f"list_transactions: message: {message}")
    try:
        result = transaction_manager.list_transactions()
    except Exception as e:
        result = {"error": f"list_transactions: {str(e)}"}
    debug_message(f"list_transactions: result: {result}")
    return result


def transaction_manager_dispatcher(method, message):
    info_message(f"transaction_manager_dispatcher: method = {method}")
    switch = {
        "reset": reset,
        "list_transactions": list_transactions,
    }
    if method in switch:
        debug_message(f"transaction_manager_dispatcher: message: {message}")
        result = switch[method](message)
    else:
        result = {"status": "error", "message": "Invalid method"}
    debug_message(f"transaction_manager_dispatcher: {result}")
    return result
