"""
Module Name: lock_manager
Author: Equipe 3
Purpose: Gerenciador de bloqueios em itens de dados.
Created: 2023-06-13
"""

from settings import debug_message, init_logger, inspect_type

from typing import List, Dict, Tuple

logger = init_logger(__name__)


class LockManager:
    def __init__(self, data_items: List[str] = None) -> str:
        if data_items is None:
            data_items = ["Users", "Products", "Orders"]
        debug_message(
            f"""LockManager: __init__:
                inspect_type(data_items) = {inspect_type(data_items)},
                data_items = {data_items}"""
        )
        self.data_items: List[str] = data_items
        self.exclusive_locks: Dict[str, str] = {}
        self.shared_locks: List[Tuple[str, str]] = []

    def acquire_exclusive_lock(self, data_item: str, transaction: str) -> Dict[str, str]:
        debug_message(
            f"""LockManager: acquire_exclusive_lock:
            inspect_type(data_item) = {inspect_type(data_item)},
            inspect_type(transaction) = {inspect_type(transaction)},
            (data_item in self.exclusive_locks.keys()) = {(data_item in self.exclusive_locks.keys())},
            (data_item in [shared_lock[0] for shared_lock in self.shared_locks]) = {(data_item in [shared_lock[0] for shared_lock in self.shared_locks])},
            """
        )
        result = {"result": "NOT VALID", "data_string": f"('E', {data_item})"}
        if data_item not in self.data_items:
            result = {"result": "FAIL", "data_string": f"NO_ITEM_FOUND({data_item}"}

        if (data_item in self.exclusive_locks.keys()) or (data_item in [shared_lock[0] for shared_lock in self.shared_locks]):
            result = {"result": "WAIT", "data_string": f"('E', {data_item})"}
        else:
            self.exclusive_locks[data_item] = transaction
            result = {"result": "SUCCESS", "data_string": f"('E', {data_item})"}
        debug_message(
            f"""LockManager: acquire_exclusive_lock (exit):
            result: {result}
            self.list_locks(data_item): {self.list_locks(data_item)}
            """
        )
        return result

    def acquire_shared_lock(self, data_item: str, transaction: str) -> Dict[str, str]:
        debug_message(
            f"""LockManager: acquire_shared_lock:
            inspect_type(data_item) = {inspect_type(data_item)},
            inspect_type(transaction) = {inspect_type(transaction)},
            self.exclusive_locks.keys = {self.exclusive_locks.keys()},
            """
        )
        result = {"result": "NOT VALID", "data_string": f"('S', {data_item})"}
        if data_item not in self.data_items:
            result =  {"result": "FAIL", "data_string": f"NO_ITEM_FOUND({data_item}"}

        if (data_item in self.exclusive_locks.keys()):
            result =  {"result": "WAIT", "data_string": f"('S', {data_item})"}
        else:
            lock = (data_item, transaction)
            self.shared_locks.append(lock)
            result =  {"result": "SUCCESS", "data_string": f"('S', {data_item})"}
        debug_message(
            f"""LockManager: acquire_shared_lock (exit):
            data_item: {data_item}
            self.list_locks(data_item): {self.list_locks(data_item)}
            """
        )
        return result

    def release_lock(self, data_item: str, transaction: str) -> str:
        if data_item not in self.data_items:
            return f"ITEM_NOT_FOUND({data_item})"

        lock_released = "RELEASED({data_item}, {transaction})"
        if data_item in self.exclusive_locks:
            if self.exclusive_locks[data_item] == transaction:
                del self.exclusive_locks[data_item]
        elif (data_item, transaction) in self.shared_locks:
            self.shared_locks.remove((data_item, transaction))
        else:
            lock_released = f"NO_LOCK_FOUND({data_item}, {transaction})"

        return lock_released

    def has_exclusive_lock(self, data_item):
        return data_item in self.exclusive_locks

    def has_shared_lock(self, data_item):
        return any(item == data_item for item, _ in self.shared_locks)

    def list_locks(self, data_item):
        locks = []
        if data_item in self.exclusive_locks:
            locks.append(("Exclusive", self.exclusive_locks[data_item]))
        for item, transaction in self.shared_locks:
            if item == data_item:
                locks.append(("Shared", transaction))
        return locks

    def get_lock_status(self, data_item, transaction):
        debug_message(
            f"""LockManager: get_lock_status:
            inspect_type(data_item) = {inspect_type(data_item)},
            inspect_type(transaction) = {inspect_type(transaction)},
            inspect_type(self.exclusive_locks) = {inspect_type(self.exclusive_locks)},
            inspect_type(self.shared_locks) = {inspect_type(self.shared_locks)},
            """
        )
        if data_item not in self.data_items:
            return f"LockManager: get_lock_status: Invalid data item: {data_item}."

        lock_string = " "
        if data_item in self.exclusive_locks.keys():
            if self.exclusive_locks[data_item] == transaction:
                lock_string = "E"
        elif data_item in [lock[0] for lock in self.shared_locks]:
            transactions = [lock[1] for lock in self.shared_locks if lock[0] == data_item]
            if any(lock_transaction == transaction for lock_transaction in transactions):
                lock_string = "S"
        debug_message(
            f"""LockManager: get_lock_status (exit):
            inspect_type(data_item) = {inspect_type(data_item)},
            inspect_type(transaction) = {inspect_type(transaction)},
            inspect_type(self.exclusive_locks) = {inspect_type(self.exclusive_locks)},
            inspect_type(self.shared_locks) = {inspect_type(self.shared_locks)},
            inspect_type(lock_string) = {inspect_type(lock_string)},
            """
        )
        return lock_string

    def list_data_items(self):
        return self.data_items
    
    def count_data_items(self):
        return len(self.data_items)

    def formatted_list_data_items(self):
        data_items_list = self.list_data_items()
        json_data = {
            f"Data Item {i}": data_items_list[i] for i in range(len(data_items_list))
        }
        return json_data
