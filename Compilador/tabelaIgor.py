class TabelaSimbolos:

    def __init__(self):
        self.tabela = {}
        self.arqv = None

    def existeIdent(self, nome):
        if nome in self.tabela:
            return True
        else:
            return False

    def declaraIdent(self, nome, valor):
        if not self.existeIdent(nome):
            self.tabela[nome] = valor
            return True
        else:
            return False