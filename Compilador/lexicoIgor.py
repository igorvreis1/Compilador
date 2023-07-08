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
COMANDOS → IF | WHILE | READ | WRITE | ATRIB
IF → se abrepar EXPR fechapar C-COMP H
H → _ | senao C-COMP
WHILE → enquanto abrepar EXPR fechapar C-COMP
READ → leia abrepar LIST-ID fechapar pvirg
ATRIB → id atrib EXPR pvirg
WRITE → escreva abrepar LIST-W fechapar pvirg
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

from os import path


class TipoToken: #Todas os Tokens da linguagem miniPascal
    PROGRAMA = (1, 'programa')
    VARIAVEIS = (2, 'variaveis')
    INTEIRO = (3, 'inteiro')
    REAL = (4, 'real')
    LOGICO = (5, 'logico')
    CARACTER = (6, 'caracter')
    SE = (7, 'se')
    SENAO = (8, 'senao')
    ENQUANTO = (9, 'enquanto')
    LEIA = (10, 'leia')
    ESCREVA = (11, 'escreva')
    FALSO = (12, 'falso')
    VERDADEIRO = (13, 'verdadeiro')
    ATRIB = (14, ':=')
    OPREL = (15,  'oprel')
    OPAD = (16,  ('+', '-'))
    OPMUL = (17,  ('*', '/'))
    OPNEG = (18, '!')
    PVIRG = (19, ';')
    DPONTOS = (20, ':')
    VIRG = (21, ',')
    ABREPAR = (22, '(')
    FECHAPAR = (23, ')')
    ABRECH = (24, '{')
    FECHACH = (25, '}')
    IDENT = (26, 'ident')
    ASPAS = (27, '"')
    CTE = (28, 'cte')
    CADEIA = (29, 'cadeia')
    ERRO = (30,"ERRO")
    FIMARQ = (31, '<eof>')


class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema 
        self.linha = linha
        # self.abrech = abrech # numero de {
        # self.fechach = fechach # numero de  }
        # self.abrepar = abrepar # numero de  (
        # self.fechapar = fechapar # numero de  )

class Lexico:
    # dicionario de palavras reservadas
    reservadas = { 'programa': TipoToken.PROGRAMA, 'variaveis': TipoToken.VARIAVEIS, 'inteiro': TipoToken.INTEIRO, 'real': TipoToken.REAL, 'logico': TipoToken.LOGICO, 'caracter': TipoToken.CARACTER, 'se': TipoToken.SE, 'senao': TipoToken.SENAO, 'enquanto': TipoToken.ENQUANTO, 'escreva': TipoToken.ESCREVA, 'leia': TipoToken.LEIA,'falso': TipoToken.FALSO,'verdadeiro': TipoToken.VERDADEIRO }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self): #abre arquivo
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists('exemplos/'+self.nomeArquivo):
            nome = self.nomeArquivo
            self.arquivo = open('exemplos/'+nome, "r")
            self.arquivo = self.arquivo
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
            
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()                 
                if car == '/':#trata comentario
                    car = self.getChar()
                    if car == '/' or car == '*':
                        estado = 5
                    else:
                        car = '/'
                        estado = 4
                elif car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1                
                elif car in {':', ';',',', '!', '+','-','/', '*', '(', ')','=', '<', '>', '{', '}','"'}:
                    estado = 4
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 3
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isalnum()) :
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        if len(lexema) <= 16:
                            return Token(TipoToken.IDENT, lexema, self.linha)
                        else:
                            print(f"Erro: O {lexema} tem mais de 16 caracteres")
                            quit()
            elif estado == 3:

                if lexema.count('.') > 1: #verificando se o Float tem mais de um '.'
                        print("Erro!! Numero invalido.")
                        quit()
                        
                if car.isdigit() or car == '.':
                    lexema = lexema + car
                    car = self.getChar()

                elif car is None or (not car.isdigit()):
                    self.ungetChar(car)
                    return Token(TipoToken.CTE, lexema, self.linha)
                
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == ':':
                    proxCar = self.getChar()
                    if proxCar == '=':
                        lexema = car+proxCar
                        return Token(TipoToken.ATRIB, lexema, self.linha)
                    else:
                        return Token(TipoToken.DPONTOS, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PVIRG, lexema, self.linha)
                elif car in ('+','-'):
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car in ('*','/'):
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '(': #ABREPAR = (22, '(')
                    return Token(TipoToken.ABREPAR, lexema, self.linha)
                elif car == ')': #fechaPAR
                    return Token(TipoToken.FECHAPAR, lexema, self.linha)
                elif car == ',': #VIRG = (21, ',')
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == '{': # ABRECH = (24, '{')
                    return Token(TipoToken.ABRECH, lexema, self.linha)
                elif car == '}': #FECHACH = (25, '}')
                    return Token(TipoToken.FECHACH, lexema, self.linha)
                elif car == '(': # ABRECH = (24, '{')
                    return Token(TipoToken.ABREPAR, lexema, self.linha)
                elif car == ')': #FECHACH = (25, '}')
                    return Token(TipoToken.FECHAPAR, lexema, self.linha)
                elif car == '"':
                    lexema = car
                    while True:
                        car = self.getChar()
                        if car == '"':
                            lexema = lexema + car
                            break
                        else:
                            lexema = lexema + car
                    return Token(TipoToken.CADEIA, lexema, self.linha)
                
                # '=', '<', '>', '<=', '>=', '<>'
                elif car in ('=', '<', '>'):
                # Tratando os OP logicos
                    if car == '<':
                        car = self.getChar()
                        print('ProxCar: '+car)
                        if car == '=':
                            lexema = lexema+car
                            return Token(TipoToken.OPREL, lexema, self.linha)
                        elif car == '>':
                            lexema = lexema+car
                            return Token(TipoToken.OPREL, lexema, self.linha)
                        else:
                            self.ungetChar(car)
                            return Token(TipoToken.OPREL, lexema, self.linha)
                    elif car == '>':
                        car = self.getChar()
                        if car == '=':
                            lexema = car+proxCar
                            return Token(TipoToken.OPREL, lexema, self.linha)
                        else:
                            self.ungetChar(car)
                            return Token(TipoToken.OPREL, lexema, self.linha)
                    else:
                        return Token(TipoToken.OPREL, lexema, self.linha)
            elif estado == 5:
            # Tratamento de comentario
                if car == '*':
                    lex = ''
                    while True:
                        car = self.getChar()
                        # print(f"Car: {car}")
                        if car == '*':
                            lex = car
                        elif car == '/' and lex == '*':
                            lex = lex+car
                            # print(lex)
                            break
                        elif car ==  None:
                            print(f"Erro  não fechou comentario: '*/'. Linha: {self.linha}")
                            exit()
                else:
                    while (not car is None) and (car != '\n'):
                        car = self.getChar()
                
                self.ungetChar(car)
                estado = 1


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo1.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s || lexema= (%s) || linha= %d" % (token.msg, token.lexema, token.linha))
    #    print("token= %s || lexema= (%s) || linha= %d // AbrCH = %d FechaCH = %d" % (token.msg, token.lexema, token.linha, token.abrch, token.fechapar))
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()
