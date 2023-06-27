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
        # debug_message(
        #     f"""LockManager: __init__:
        #         inspect_type(data_items) = {inspect_type(data_items)},
        #         data_items = {data_items}"""
        # )
        self.data_items: List[str] = data_items
        self.exclusive_locks: Dict[str, int] = {}
        self.shared_locks: List[Tuple[str, int]] = []

    def list_transaction_exclusive_locks(self, transaction):
        return [f"('E', {key})" for key, value in self.exclusive_locks.items() if value == transaction]

    def list_transaction_shared_locks(self, transaction):
        return [f"('S', {lock[0]})" for lock in self.shared_locks if lock[1] == transaction]

    def list_transaction_locks(self, transaction):
        return self.list_transaction_exclusive_locks(transaction) + self.list_transaction_shared_locks(transaction)

    def remove_transaction_exclusive_locks(self, transaction: int) -> None:
        keys_to_remove = [key for key, value in self.exclusive_locks.items() if value == transaction]
        for key in keys_to_remove:
            del self.exclusive_locks[key]

    def remove_transaction_shared_locks(self, transaction: int) -> None:
        self.shared_locks = [lock for lock in self.shared_locks if lock[1] != transaction]

    def remove_transaction_locks(self, transaction: int) -> None:
        self.remove_transaction_shared_locks(transaction)
        self.remove_transaction_exclusive_locks(transaction)

    def transaction_has_lock(self, data_item: str, transaction_id: int) -> str:
        lock_type = "N"
        if data_item in self.exclusive_locks:
            if self.exclusive_locks[data_item] == transaction_id:
                lock_type =  "E"
        for item, item_transaction_id in self.shared_locks:
            if item == data_item and item_transaction_id == transaction_id:
                lock_type =  "S"
        return lock_type

    def acquire_exclusive_lock(self, data_item: str, transaction: int) -> Dict[str, str]:
        # debug_message(
        #     f"""LockManager: acquire_exclusive_lock:
        #     inspect_type(data_item) = {inspect_type(data_item)},
        #     inspect_type(transaction) = {inspect_type(transaction)},
        #     (data_item in self.exclusive_locks.keys()) = {(data_item in self.exclusive_locks.keys())},
        #     (data_item in [shared_lock[0] for shared_lock in self.shared_locks]) = {(data_item in [shared_lock[0] for shared_lock in self.shared_locks])},
        #     """
        # )
        result = {"result": "NOT VALID", "data_string": f"('E', {data_item})"}
        if data_item not in self.data_items:
            result = {"result": "FAIL", "data_string": f"NO_ITEM_FOUND({data_item}"}

        # Is there an exclusive lock?
        if (data_item in self.exclusive_locks.keys()):
            # Is it ours?
            if (self.exclusive_locks[data_item] == data_item):
                result = {"result": "SUCCESS", "data_string": f"('E', {data_item})"}
            else:
                result = {"result": "WAIT", "data_string": f"('E', {data_item})"}
        # No exclusive locks, check for shared locks.
        else:
            shared_locks_on_data_item = [shared_lock for shared_lock in self.shared_locks if shared_lock[0]==data_item]
            # If we have shared locks on the item
            if (len(shared_locks_on_data_item)>0):
                # Assume failure and fix later
                result = {"result": "WAIT", "data_string": f"('E', {data_item})"}
                # If there is only one lock on the item
                if (len(shared_locks_on_data_item)==1):
                    # If the transaction is the lock owner, upgrade the lock
                    if shared_locks_on_data_item[0][1] == transaction:
                        self.exclusive_locks[data_item] = transaction
                        self.shared_locks = [lock for lock in self.shared_locks if lock[1] != transaction]
                        result = {"result": "SUCCESS", "data_string": f"('E', {data_item})"}
            # No exclusive locks, no shared locks
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

    def acquire_shared_lock(self, data_item: str, transaction: int) -> Dict[str, str]:
        # debug_message(
        #     f"""LockManager: acquire_shared_lock:
        #     inspect_type(data_item) = {inspect_type(data_item)},
        #     inspect_type(transaction) = {inspect_type(transaction)},
        #     self.exclusive_locks.keys = {self.exclusive_locks.keys()},
        #     """
        # )
        result = {"result": "NOT VALID", "data_string": f"('S', {data_item})"}
        if data_item not in self.data_items:
            result =  {"result": "FAIL", "data_string": f"NO_ITEM_FOUND({data_item}"}

        # Exists exclusive lock
        if (data_item in self.exclusive_locks.keys()):
            result =  {"result": "WAIT", "data_string": f"('S', {data_item})"}
        # No exclusive lock
        else:
            # Suceeded already
            result =  {"result": "SUCCESS", "data_string": f"('S', {data_item})"}
            # If there isn't a shared lock for the transaction, create it.
            if (transaction not in [shared_lock[1] for shared_lock in self.shared_locks if shared_lock[0] == data_item]):
                lock = (data_item, transaction)
                self.shared_locks.append(lock)
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
        # debug_message(
        #     f"""LockManager: get_lock_status:
        #     inspect_type(data_item) = {inspect_type(data_item)},
        #     inspect_type(transaction) = {inspect_type(transaction)},
        #     inspect_type(self.exclusive_locks) = {inspect_type(self.exclusive_locks)},
        #     inspect_type(self.shared_locks) = {inspect_type(self.shared_locks)},
        #     """
        # )
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
        # debug_message(
        #     f"""LockManager: get_lock_status (exit):
        #     inspect_type(data_item) = {inspect_type(data_item)},
        #     inspect_type(transaction) = {inspect_type(transaction)},
        #     inspect_type(self.exclusive_locks) = {inspect_type(self.exclusive_locks)},
        #     inspect_type(self.shared_locks) = {inspect_type(self.shared_locks)},
        #     inspect_type(lock_string) = {inspect_type(lock_string)},
        #     """
        # )
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
