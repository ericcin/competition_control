"""
Module Name: LockManager
Author: Equipe 3
Purpose: Gerenciador de bloqueios em itens de dados.
Created: 2023-06-13
"""

from settings import debug_message, init_logger, inspect_type

logger = init_logger(__name__)


class LockManager:
    def __init__(self, data_items = ["Users", "Products", "Orders"]):
        debug_message(
            f"""LockManager: __init__:
                inspect_type(data_items) = {inspect_type(data_items)},
                data_items = {data_items}"""
        )
        self.data_items = data_items
        self.exclusive_locks = {}
        self.shared_locks = {}

    def acquire_exclusive_lock(self, data_item, transaction):
        if data_item not in self.data_items:
            raise ValueError("Invalid data item")

        if data_item in self.exclusive_locks or data_item in self.shared_locks:
            return "Wait"
        else:
            self.exclusive_locks[data_item] = transaction
            return "Ok"

    def acquire_shared_lock(self, data_item, transaction):
        if data_item not in self.data_items:
            raise ValueError("Invalid data item")

        if data_item in self.exclusive_locks:
            return "Wait"
        else:
            self.shared_locks.add((data_item, transaction))
            return "Ok"

    def release_lock(self, data_item, transaction):
        if data_item not in self.data_items:
            raise ValueError("Invalid data item")

        if data_item in self.exclusive_locks:
            if self.exclusive_locks[data_item] == transaction:
                del self.exclusive_locks[data_item]
            else:
                raise ValueError(
                    "Transaction does not hold an exclusive lock on the data item"
                )
        elif (data_item, transaction) in self.shared_locks:
            self.shared_locks.remove((data_item, transaction))
        else:
            raise ValueError("Transaction does not hold a lock on the data item")

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
        if data_item not in self.data_items:
            raise ValueError("Invalid data item")

        if data_item in self.exclusive_locks:
            if self.exclusive_locks[data_item] == transaction:
                return "E"
            else:
                return " "
        elif any(item == data_item for item, _ in self.shared_locks):
            return "S"
        else:
            return " "

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
