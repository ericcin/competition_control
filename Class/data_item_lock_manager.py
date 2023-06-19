class dataItemLockManager:

    def __init__(self, data_items_names_list):
        self.data_items = {chave: 0 for chave in data_items_names_list}
        self.count = 0
        self.lock_register = []
        self.array_position = None

    def create_transaction_name(self):
        self.count = self.count + 1
        return 'transacao' + str(self.count)

    # lock compartilhado
    def read_lock(self, data_item, transaction):
        if self.has_exclusive_lock(data_item) == True:
            #TODO essa parte talvez seja interessante eu mostrar quem está com bloqueio exclusivo no item
            print("Impossível realizar lock compartilhado em " + data_item + " pois ele possui bloqueio exclusivo!")
        else:
            if self.has_shared_lock(data_item) == False:
                self.create_lock_register(data_item, 'read_lock', 1, transaction)
                print('Lock compartilhado em ' + data_item + ' realizado! Total de itens compartilhando item de dado: 1')
            else:
                print(self.check_transaction_in_read_lock(data_item, transaction))

    #lock exclusivo
    def write_lock(self, data_item, transaction):
        if self.has_shared_lock(data_item) == True:
            #TODO essa parte talvez seja interessante eu mostrar quem está com bloqueio compartilhado no item
            print("Impossível realizar lock exclusivo em " +data_item+ " pois ele possui bloqueio compartilhado pelas "
                                                "transações: " + str(self.lock_register[self.array_position][3]))
        else:
            if self.has_exclusive_lock(data_item) == False:
                self.create_lock_register(data_item, 'write_lock', 1, transaction)
                print('Lock exclusivo em ' + data_item + ' realizado pela ' + transaction + '!')
            else:
                print(self.check_transaction_in_write_lock(data_item, transaction))

    #desbloqueio
    def unlock(self, data_item, transaction):
        if self.transaction_has_lock(transaction) == True:
            del self.lock_register[self.array_position]
            print('Dado ' +data_item + ' desbloqueado com sucesso pela ' + transaction + '!')
        else:
            print('A ' + transaction + ' não pode realizar desbloqueio no dado ' + data_item + ' pois ela não possui'
                                                                                            'bloqueio sobre o dado!' )

    def create_lock_register(self, data_item, lock, number_of_locks, transaction):
        self.lock_register.append([data_item, lock, number_of_locks, [transaction]])

    def alter_lock_register(self, transaction):
        self.lock_register[self.array_position][2] = self.lock_register[self.array_position][2] + 1
        self.lock_register[self.array_position][3].append(transaction)

    def transaction_has_lock(self, transaction):
        for pos, i in enumerate(self.lock_register):
            if transaction in i:
                self.array_position = pos
                return True
            else:
                return False

    def has_shared_lock(self, data_item):
        for pos, i in enumerate(self.lock_register):
            if data_item in i and 'read_lock' in i:
                self.array_position = pos
                return True
            else:
                return False

    def has_exclusive_lock(self, data_item):
        for pos, i in enumerate(self.lock_register):
            if data_item in i and 'write_lock' in i:
                self.array_position = pos
                return True
            else:
                return False

    def check_transaction_in_read_lock(self, data_item, transaction):
        if transaction not in self.lock_register[self.array_position][3]:
            self.alter_lock_register(transaction)
            return('Lock compartilhado em ' + data_item + ' realizado! Itens compartilhando item de dado: '
                  + str(self.lock_register[self.array_position][3]))
        else:
            return('Lock compartilhado em ' + data_item + ' já está sendo realizado pela ' + transaction)

    def check_transaction_in_write_lock(self, data_item, transaction):
        if transaction in self.lock_register[self.array_position][3]:
            return('Lock exclusivo em ' + data_item + ' já está sendo realizado pela ' + transaction)
        else:
            return ('Impossível realizar Lock exclusivo em ' + data_item + ' pois ele já possui lock exclusivo realizado'
                                                            ' pela ' + str(self.lock_register[self.array_position][3]))

    #executadas após a da main
    # def read_item(self, item, data_item_lock_manager_items):
    #
    #     self.data_items[item] = data_item_lock_manager_items[item]
    #     return self.data_items[item]

    def write_item(self, lock_register, transaction, item):
        pass