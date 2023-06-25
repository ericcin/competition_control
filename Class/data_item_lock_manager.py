from datetime import datetime

class dataItemLockManager:

    def __init__(self, data_items_names_list):
        self.data_items = {chave: 0 for chave in data_items_names_list}
        self.count = 0
        self.lock_register = []
        self.complete_lock_register = []
        self.array_position = None
        self.errors = []

    def create_transaction_name(self):
        self.count = self.count + 1
        return 't' + str(self.count)

    # lock compartilhado
    def read_lock(self, data_item, transaction):
        if self.has_exclusive_lock(data_item) == True:
            self.get_error(data_item, transaction, 'read_lock', 'write_lock', self.lock_register[self.array_position][3])
            return ("Impossível realizar lock compartilhado em " + data_item + " pois ele possui bloqueio exclusivo:" +
                    str(self.lock_register[self.array_position]))
        else:
            if self.has_shared_lock(data_item) == False:
                self.create_lock_register(data_item, 'read_lock', 1, transaction)
                return 'Lock compartilhado em ' + data_item + ' realizado! Total de itens compartilhando item de dado: 1'
            else:
                return self.check_transaction_in_read_lock(data_item, transaction)

    # lock exclusivo
    def write_lock(self, data_item, transaction):
        if self.has_shared_lock(data_item) == True:
            return ("Impossível realizar lock exclusivo em " + data_item +
                    " pois ele possui bloqueio compartilhado pelas transações: "
                    + str(self.lock_register[self.array_position][3]))
        else:
            if self.has_exclusive_lock(data_item) == False:
                self.create_lock_register(data_item, 'write_lock', 1, transaction)
                return 'Lock exclusivo em ' + data_item + ' realizado pela ' + transaction + '!'
            else:
                return self.check_transaction_in_write_lock(data_item, transaction)

    # desbloqueio
    def unlock(self, data_item, transaction):
        if self.transaction_has_lock_in_specific_item(transaction, data_item) == True:
            if len(self.lock_register[self.array_position][3]) == 1:
                del self.lock_register[self.array_position]
                self.insert_unlock_in_complete_lock_register(data_item, transaction)
                return 'Dado ' + data_item + ' desbloqueado com sucesso pela ' + transaction + '!'
            if len(self.lock_register[self.array_position][3]) > 1:
                self.lock_register[self.array_position][3].remove(transaction)
                self.insert_unlock_in_complete_lock_register(data_item, transaction)
                return 'Dado ' + data_item + ' desbloqueado com sucesso pela ' + transaction + '!'
        else:
            return ('A ' + transaction + ' não pode realizar desbloqueio no dado '
                    + data_item + ' pois ela não possui bloqueio sobre o dado!')

    def increment_lock(self):
        pass

    def decrement_lock(self):
        pass

    def create_lock_register(self, data_item, lock, number_of_locks, transaction):
        self.lock_register.append([data_item, lock, number_of_locks, [transaction]])
        self.insert_in_complete_lock_register(data_item, lock, number_of_locks, transaction)

    def insert_in_complete_lock_register(self, data_item, lock, number_of_locks, transaction):
        self.complete_lock_register.append([data_item, lock, number_of_locks, [transaction], self.get_now_date_time()])

    def insert_unlock_in_complete_lock_register(self, data_item, transaction):
        self.complete_lock_register.append([data_item, 'unlock', transaction, self.get_now_date_time()])

    def alter_lock_register(self, transaction):
        self.lock_register[self.array_position][2] = self.lock_register[self.array_position][2] + 1
        self.lock_register[self.array_position][3].append(transaction)
        self.complete_lock_register[self.array_position][2] = self.complete_lock_register[self.array_position][2] + 1
        self.complete_lock_register[self.array_position][3].append(transaction)
        self.complete_lock_register[self.array_position][4] = self.get_now_date_time()

    def transaction_has_lock_in_specific_item(self, transaction, item):
        if self.lock_register != []:
            for pos, i in enumerate(self.lock_register):
                print(i)
                if transaction in i[3] and item in i:
                    self.array_position = pos
                    return True
                else:
                    return False
        return False

    def transaction_has_write_lock_in_specific_item(self, transaction, item):
        if self.lock_register != []:
            for pos, i in enumerate(self.lock_register):
                if transaction in i[3] and item in i and 'write_lock' in i:
                    self.array_position = pos
                    return True
                else:
                    return False
        else:
            return False

    def has_shared_lock(self, data_item):
        if self.lock_register != []:
            for pos, i in enumerate(self.lock_register):
                if data_item in i and 'read_lock' in i:
                    self.array_position = pos
                    return True
                else:
                    return False
        else:
            return False

    def has_exclusive_lock(self, data_item):
        if self.lock_register != []:
            for pos, i in enumerate(self.lock_register):
                if data_item in i and 'write_lock' in i:
                    self.array_position = pos
                    return True
                else:
                    return False
        else:
            return False

    def check_transaction_in_read_lock(self, data_item, transaction):
        if transaction not in self.lock_register[self.array_position][3]:
            self.alter_lock_register(transaction)
            return ('Lock compartilhado em ' + data_item + ' realizado! Itens compartilhando item de dado: '
                    + str(self.lock_register[self.array_position][3]))
        else:
            return 'Lock compartilhado em ' + data_item + ' já está sendo realizado pela ' + transaction

    def check_transaction_in_write_lock(self, data_item, transaction):
        if transaction in self.lock_register[self.array_position][3]:
            return 'Lock exclusivo em ' + data_item + ' já está sendo realizado pela ' + transaction
        else:
            return ('Impossível realizar Lock exclusivo em ' + data_item
                    + ' pois ele já possui lock exclusivo realizado pela '
                    + str(self.lock_register[self.array_position][3]))

    def can_read_item(self, transaction, item):
        if self.transaction_has_lock_in_specific_item(transaction, item):
            return True
            # return 'Leitura de item realizada no item ' + item + ' para a ' + transaction + '!'
        else:
            return False
            # return ('Leitura de item não realizada, pois a ' + transaction + ' não possui bloqueio sobre o item ' +
            #         item + '!')

    def write_item(self, transaction, item, value):
        if self.transaction_has_write_lock_in_specific_item(transaction, item):
            self.data_items[item] = value
            return True
            # return 'Escrita de item feita no item ' + item + 'para a ' + transaction + '!'
        else:
            return False
            # return ('Escrita de item não realizada, pois a ' + transaction + ' não possui bloqueio exclusivo sobre o '
            #                                                                  'item ' + item + '!')

    def get_now_date_time(self):
        now = datetime.now()
        date_time = now.strftime('%d/%m/%Y %H:%M')
        return date_time

    # acima, ja ta tudo funcionando
    def get_error(self, data_item, transaction, attempted_action, cause, transaction_in_cause):
        self.errors.append([data_item, transaction, attempted_action, cause, transaction_in_cause])

    def solve_error(self):
        for i in self.errors:



