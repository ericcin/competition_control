class dataItemLockManager:

    def __init__(self, data_items_names_list):
        self.data_items = {chave: None for chave in data_items_names_list}
        self.contador = 0
        self.registro_lock = []

    def write_lock(self, data_item, transaction):
        if data_item not in self.data_items:
            print("Invalid data item")

        if data_item in self.exclusive_locks or data_item in self.shared_locks:
            return("Wait)
        else:
            self.exclusive_locks[data_item] = transaction
            return("Ok")

    def read_lock(self, data_item, transaction):
        if data_item not in self.data_items:
            raise ValueError("Invalid data item")

        if data_item in self.exclusive_locks:
            return("Wait)
        else:
            self.shared_locks.add((data_item, transaction))
            return("Ok")

    def unlock(self, data_item, transaction):
        if data_item not in self.data_items:
            raise ValueError("Invalid data item")

        if data_item in self.exclusive_locks:
            if self.exclusive_locks[data_item] == transaction:
                del self.exclusive_locks[data_item]
            else:
                raise ValueError("Transaction does not hold an exclusive lock on the data item")
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
            locks.append(('Exclusive', self.exclusive_locks[data_item]))
        for item, transaction in self.shared_locks:
            if item == data_item:
                locks.append(('Shared', transaction))
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

    def read_item(self, item):
        pass

    def write_item(self, item):
        pass