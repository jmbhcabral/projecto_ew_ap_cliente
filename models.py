
class Produto:
    nome = ""
    descricao_curta = ""
    preco_1 = 0.0
    vegetariano = False

    def __init__(self, nome, descricao_curta, preco_1, vegetariano):
        self.nome = nome
        self.descricao_curta = descricao_curta
        self.preco_1 = preco_1
        self.vegetariano = vegetariano

    def get_dictionary(self):
        return {
            "nome": self.nome,
            "descricao_curta": self.descricao_curta,
            "preco_1": self.preco_1,
            "vegetariano": self.vegetariano
        }
