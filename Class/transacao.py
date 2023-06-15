class Transacao:

    def __init__(self, data_items_names_list):
        self.data_items = {chave: None for chave in data_items_names_list}
