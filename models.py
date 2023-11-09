
class Produto:
    nome = ""
    ingredientes = ""
    preco = 0.0
    vegetariano = False

    def __init__(self, nome, ingredientes, preco, vegetariano):
        self.nome = nome
        self.ingredientes = ingredientes
        self.preco = preco
        self.vegetariano = vegetariano

    def get_dictionary(self):
        return {
            "nome": self.nome,
            "ingredientes": self.ingredientes,
            "preco": self.preco,
            "vegetariano": self.vegetariano
        }
