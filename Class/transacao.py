class transacao:

    def __init__(self, data_items_names_list):
        self.data_items = {chave: 0 for chave in data_items_names_list}
        self.transactions = []
    def read_item(self, lock_register, transaction, item, data_item_lock_manager_items):

        self.data_items[item] = data_item_lock_manager_items[item]
        return self.data_items[item]

    def write_item(self, lock_register, transaction, item):
        pass



    #a logica principal que usarei nessa classe: os valores do data_items pra essa transacao é atualizada
    # logo depois é passado para o data_items do data_item_lock_manager, assim, caso em algum momento, alguma outra
    # transacao, vá utilizar um valor que havia sido lido antes de uma outra transação mudar, o programa poderá
    # comparar o valor do dado nessa classe transacao com o valor do dado na classa data_item_lock_manager..
    # caso os valores sejam diferentes, será enviada uma mensagem pro usuario explicando que o valor de x dado
    # precisa ser lido novamente pois foi atualizado por outra transação