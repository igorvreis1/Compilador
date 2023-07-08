"""
MiniPascal:

P= {
PROG    → programa id pvirg DECLS C-COMP
DECLS   → _ | variaveis LIST-DECLS
LIST-DECLS → DECL-TIPO D
D       → _ | LIST-DECLS
DECL-TIPO → LIST-ID dpontos TIPO pvirg
LIST-ID     → id E
E   → _ | virg LIST-ID
TIPO → inteiro | real | logico | caracter
C-COMP → abrech LISTA-COMANDOS fechach
LISTA-COMANDOS → COMANDOS G
G → _ | LISTA-COMANDOS
COMANDOS → SE | ENQUANTO | LEIA | ESCREVA | ATRIB
SE → se abrepar EXPR fechapar C-COMP H
H → _ | senao C-COMP
ENQUANTO → enquanto abrepar EXPR fechapar C-COMP
LEIA → leia abrepar LIST-ID fechapar pvirg
ATRIB → id atrib EXPR pvirg
ESCREVA → escreva abrepar LIST-W fechapar pvirg
LIST-W → ELEM-W L
L → _ | virg LIST-W
ELEM-W → EXPR | cadeia
EXPR → SIMPLES P
P → _ | oprel SIMPLES
SIMPLES → TERMO R
R → _ | opad SIMPLES
TERMO → FAT S
S → _ | opmul TERMO
FAT → id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT}

    Tokens::

    IDENT ATRIB READ PTOVIRG PRINT ADD MULT OPENPAR CLOSEPAR NUM ERROR FIMARQ

    Comentarios::

    iniciam com # ate o fim da linha

"""

from lexicoIgor import TipoToken as tt, Token, Lexico
from tabelaIgor import TabelaSimbolos
from semanticoIgor import Semantico

class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.erro = False
        self.variaveis = open("variaveis.txt", "w")

    

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.erro = False
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.tabela = TabelaSimbolos()
            self.semantico = Semantico()
            self.PROG()

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual( token ):
            (const, msg) = token
            # Print para faciliatr o entendimento.
            # print('[linha %d]: era esperado "%s" e veio "%s"'
            #    % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            
            ultimoLex = self.tokenAtual
            self.tokenAtual = self.lex.getToken()

            return ultimoLex
            
        else:
            self.erro = True
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    #Regras de execução:
    def PROG(self):
        self.consome(tt.PROGRAMA)
        self.consome(tt.IDENT)
        self.consome(tt.PVIRG)
        self.DECLS()
        self.C_COMP()
        # Depois de execultar tudo, fecha o arquivo.
        self.variaveis.close()   

    def DECLS(self):
        if self.atualIgual( tt.VARIAVEIS ):
            self.consome(tt.VARIAVEIS)
            self.LIST_DECLS()
        else:
            pass

    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()

    def D(self):
        if self.atualIgual( tt.IDENT ):
            self.LIST_DECLS()
        else:
            pass
    
    def DECL_TIPO(self):
        token = self.LIST_ID()
        self.consome( tt.DPONTOS)
        tipo = self.TIPO()
        self.consome(tt.PVIRG)
        
        if type(token) == list:
            for i in token:
                # print('Token: ',i)
                # print('Tipo: ',tipo)
                if i in self.tabela.tabela:
                    print("Erro variavel já declarada")
                    quit()
                self.tabela.declaraIdent(i,tipo.tipo)
                self.variaveis.write(f"{tipo.tipo} {i}\n")
        else:
            # print('Token: ',token)
            # print('Tipo: ',tipo)
            if token in self.tabela.tabela:
                print("Erro variavel já declarada")
                quit()
            self.tabela.declaraIdent(token,tipo.tipo)
            self.variaveis.write(f"{tipo.tipo} {token}\n")
    
    def LIST_ID(self):
        token = self.consome(tt.IDENT)
        e = self.E()
        if(e != None):
            listaLex = []
            listaLex.append(token.lexema)
            listaLex.extend(e)
            return listaLex
        return token.lexema

    def E(self):
        if self.atualIgual( tt.VIRG ):
            self.consome(tt.VIRG)
            return self.LIST_ID()
        else:
            pass
    
    def TIPO(self):
        if self.atualIgual( tt.INTEIRO ):
            return self.consome(tt.INTEIRO)
        elif self.atualIgual( tt.REAL ):
            return self.consome(tt.REAL)
        elif self.atualIgual( tt.LOGICO ):
            return self.consome(tt.LOGICO)
        elif self.atualIgual( tt.CARACTER ):
            return self.consome(tt.CARACTER)
    
    def C_COMP(self):
        self.consome(tt.ABRECH)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH)

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    def G(self):
        if self.atualIgual( tt.SE ) or self.atualIgual( tt.ENQUANTO ) or self.atualIgual( tt.LEIA ) or self.atualIgual( tt.ESCREVA ) or self.atualIgual( tt.IDENT ):
            self.LISTA_COMANDOS()
        else:
            pass

    def COMANDOS(self):
        if self.atualIgual( tt.SE ):
            self.SE()
        elif self.atualIgual( tt.ENQUANTO ):
            self.ENQUANTO()
        elif self.atualIgual( tt.LEIA ):
            self.LEIA()
        elif self.atualIgual( tt.ESCREVA ):
            self.ESCREVA()
        elif self.atualIgual (tt.IDENT):
            self.ATRIB()
    
    def SE(self):
        self.consome( tt.SE )
        self.consome( tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.C_COMP()
        self.H()

    def H(self):
        if self.atualIgual (tt.SENAO):
            self.consome(tt.SENAO)
            self.C_COMP()
        else:
            pass
    
    def ENQUANTO(self):
        self.consome( tt.ENQUANTO )
        self.consome( tt.ABREPAR )
        self.EXPR()
        self.consome( tt.FECHAPAR )
        self.C_COMP()
    
    def LEIA(self):
        self.consome( tt.LEIA )
        self.consome( tt.ABREPAR )
        variaveis = self.LIST_ID()
        if (not self.tabela.existeIdent(variaveis)):
            self.semantico.erroSemantico("Variável '{}' não declarada".format(variaveis), self.tokenAtual.linha)
            quit()
        self.consome( tt.FECHAPAR )
        self.consome( tt.PVIRG )
    
    def ATRIB(self):
        lexAtual = self.consome( tt.IDENT )
        if (not self.tabela.existeIdent(lexAtual.lexema)):
            self.semantico.erroSemantico("Variável '{}' não declarada".format(lexAtual.lexema), self.tokenAtual.linha)
            quit()
        self.consome( tt.ATRIB )
        self.EXPR()
        self.consome( tt.PVIRG )
    
    def ESCREVA(self):
        self.consome( tt.ESCREVA )
        self.consome( tt.ABREPAR )
        self.LIST_W()
        self.consome( tt.FECHAPAR )
        self.consome( tt.PVIRG )

    def LIST_W(self):
        self.ELEM_W()
        self.L()
    
    def L(self):
        if self.atualIgual (tt.VIRG):
            self.consome( tt.VIRG )
            self.LIST_W()
        else:
            pass

    def ELEM_W(self):
        if self.atualIgual( tt.CADEIA):
            self.consome( tt.CADEIA )
        else:
            self.EXPR()
    
    def EXPR(self):
        fat = self.SIMPLES()
        oprel = self.P()
        if oprel is not None:
            if oprel.lexema != '=':
                tipo = self.tabela.tabela[fat.lexema]
                    # print(type(tipo))
                if 'logico' in tipo:
                    self.semantico.erroSemantico("Variável '{}' não é compativel com operações de '*' e '/'.".format(fat.lexema), self.tokenAtual.linha)
                    quit()
    
    def P(self):
        if self.atualIgual( tt.OPREL ):
            oprel = self.consome( tt.OPREL )
            self.SIMPLES()
            return oprel
        else:
            pass
    
    def SIMPLES(self):
        fat = self.TERMO()
        opad = self.R()
        if opad is not None:
            tipo = self.tabela.tabela[fat.lexema]
            # print(type(tipo))
            if 'logico' in tipo:
                self.semantico.erroSemantico("Variável '{}' não é compativel com operações de '*' e '/'.".format(fat.lexema), self.tokenAtual.linha)
                quit()
        return fat
    
    def R(self):
        if self.atualIgual( tt.OPAD ):
            opad = self.consome( tt.OPAD )
            self.SIMPLES()
            return opad
        else:
            pass

    def TERMO(self):
        fat = self.FAT()
        opmul = self.S()
        if opmul is not None:
            tipo = self.tabela.tabela[fat.lexema]
            # print(type(tipo))
            if 'logico' in tipo:
                self.semantico.erroSemantico("Variável '{}' não é compativel com operações de '*' e '/'.".format(fat.lexema), self.tokenAtual.linha)
                quit()
        return fat
        
    
    def S(self):
        if self.atualIgual( tt.OPMUL ):
            opmul = self.consome( tt.OPMUL )
            self.TERMO()
            return opmul
        else:
            pass
    
    def FAT(self):
        if self.atualIgual( tt.IDENT ):
            lexAtual = self.consome( tt.IDENT )
            if (not self.tabela.existeIdent(lexAtual.lexema)):
                self.semantico.erroSemantico("Variável '{}' não declarada".format(lexAtual.lexema), self.tokenAtual.linha)
                quit()
            return lexAtual
        elif self.atualIgual( tt.CTE ):
            lexAtual = self.consome( tt.CTE )
            return lexAtual
        elif self.atualIgual( tt.ABREPAR ):
            self.consome( tt.ABREPAR )
            self.EXPR()
            self.consome( tt.FECHAPAR )
        elif self.atualIgual( tt.VERDADEIRO ):
            lexAtual = self.consome( tt.VERDADEIRO )
            return lexAtual
        elif self.atualIgual( tt.FALSO ):
            lexAtual = self.consome( tt.FALSO )
            return lexAtual
        elif self.atualIgual( tt.OPNEG ):
            self.consome( tt.OPNEG )
            self.FAT()


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo1.txt'
   parser = Sintatico()
   parser.interprete(nome)
