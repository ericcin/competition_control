class dataItemLockManager:

    def __init__(self, data_items_names_list):
        self.data_items = {chave: 0 for chave in data_items_names_list}
        self.count = 0
        self.lock_register = []

    # lock compartilhado
    def read_lock(self, data_item, transaction):
        # if data_item not in self.data_items:
        #     raise ValueError("Invalid data item")
        #
        # if data_item in self.exclusive_locks:
        #     return("Wait")
        # else:
        #     self.shared_locks.add((data_item, transaction))
        #     return("Ok")
        has_shared_lock_answer = self.has_shared_lock(data_item)
        has_exclusive_lock_answer = self.has_exclusive_lock(data_item)

        if has_exclusive_lock_answer != False:
            #essa parte talvez seja interessante eu mostrar quem está com bloqueio exclusivo no item
            print("Impossível realizar lock compartilhado em " +data_item+ " pois ele possui bloqueio exclusivo!")
        else:
            if has_shared_lock_answer == False:
                self.lock_register.append([data_item, 'read_lock', 1, [transaction]])
                print('Lock compartilhado em ' + data_item + ' realizado! Total de itens compartilhando item de dado: 1')
            else:
                if transaction not in self.lock_register[has_shared_lock_answer][3]:
                    self.lock_register[has_shared_lock_answer][2] = self.lock_register[has_shared_lock_answer][2] + 1
                    self.lock_register[has_shared_lock_answer][3].append(transaction)
                    print('Lock compartilhado em ' + data_item + ' realizado! Total de itens compartilhando item de dado: '
                          + str(self.lock_register[has_shared_lock_answer][2]))
                else:
                    print('Lock compartilhado em ' +data_item + ' já está sendo realizado pela ' +transaction)

    #lock exclusivo
    def write_lock(self, data_item, transaction):
        has_shared_lock_answer = self.has_shared_lock(data_item)
        has_exclusive_lock_answer = self.has_exclusive_lock(data_item)

        if has_shared_lock_answer != False:
            #essa parte talvez seja interessante eu mostrar quem está com bloqueio compartilhado no item
            print("Impossível realizar lock exclusivo em " +data_item+ " pois ele possui bloqueio compartilhado pelas "
                                                "transações: " + str(self.lock_register[has_shared_lock_answer][3]))
        else:
            if has_exclusive_lock_answer == False:
                #aqui eu tenho que ver como funcionaria se já tivesse um item desses na lista, mas com 0 ali no numero de
                #transações por ex
                self.lock_register.append([data_item, 'write_lock', 1, [transaction]])
                print('Lock exclusivo em ' + data_item + ' realizado pela transacao ' + transaction +'!')
            else:
                print('Lock exclusivo em ' + data_item + ' já está sendo realizado pela ' + transaction)

        # if data_item not in self.data_items:
        #     print("Invalid data item")
        #
        # if data_item in self.registro_lock:
        #     return("Wait")
        # else:
        #     self.exclusive_locks[data_item] = transaction
        #     return("Ok")

    #desbloqueio
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

    def create_lock_register(self):
        pass

    def has_shared_lock(self, data_item):
        pass

    def has_exclusive_lock(self, data_item):
        return data_item in self.exclusive_locks


    # def has_shared_lock(self, data_item):
    #     return any(item == data_item for item, _ in self.shared_locks)

    # def list_locks(self, data_item):
    #     locks = []
    #     if data_item in self.exclusive_locks:
    #         locks.append(('Exclusive', self.exclusive_locks[data_item]))
    #     for item, transaction in self.shared_locks:
    #         if item == data_item:
    #             locks.append(('Shared', transaction))
    #     return locks

    # def get_lock_status(self, data_item, transaction):
    #     if data_item not in self.data_items:
    #         raise ValueError("Invalid data item")
    #
    #     if data_item in self.exclusive_locks:
    #         if self.exclusive_locks[data_item] == transaction:
    #             return "E"
    #         else:
    #             return " "
    #     elif any(item == data_item for item, _ in self.shared_locks):
    #         return "S"
    #     else:
    #         return " "

    def read_item(self, item):
        pass

    def write_item(self, item):
        pass