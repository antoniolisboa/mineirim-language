from Errors import Errors
from Tokens import Tokens
from Colors import Colors

class Semantic:
    errs = Errors().instance()

    variableType = [
        Tokens.TK_RW_INTEGER,
        Tokens.TK_RW_REAL,
        Tokens.TK_RW_STRING
    ]

    dataType = [
        Tokens.TK_INTEGER,
        Tokens.TK_REAL,
        Tokens.TK_STRING
    ]

    unsupported = [
        Tokens.TK_LOGIC_LT,   # a < b
        Tokens.TK_LOGIC_LTE,  # a <= b
        Tokens.TK_LOGIC_GT,   # a > b
        Tokens.TK_LOGIC_GTE,  # a >= b
        Tokens.TK_LOGIC_EQ,   # a == b
        Tokens.TK_LOGIC_DIF,  # a != b
        Tokens.TK_LOGIC_AND,  # a && b
        Tokens.TK_LOGIC_OR,   # a || b
        Tokens.TK_LOGIC_NOT,  # !a
        # Tokens.TK_MATH_ADD,   # +
        # Tokens.TK_MATH_SUB,   # -
        Tokens.TK_MATH_MUL,   # *
        Tokens.TK_MATH_DIV    # /
    ]

    def __init__(self, tokenTable, tree) -> None:
        self.tokenTable = tokenTable
        self.tree = tree
        self.indexTK = 0
        self.errorType = 0
        self.isAttribution = False
        self.idToCheck = ''

    def errorMessage(self, function, msg):
        # Error
        # 1 → Variável não declarada
        # 2 → Chamada de função não declarada
        # 3 → Incompatibilidade entre elementos de uma operação
        # 4 → Operadores não suportados pelo tipo string
        # 5 → Identificador já está em uso
        # 6 → Retorno compatível com o tipo da função
        # 7 → Quantidade de parâmetros em chamada de função

        line = self.tokenTable[self.indexTK][3]
        column = self.tokenTable[self.indexTK][4]   

        position = f', line {line}, column {column}.{Colors.END}'

        if self.errorType == 1:
            msg = f'{Colors.ERR}In function \'{function}\': {msg} undeclared{position}'
        elif self.errorType == 2:
            msg = f'{Colors.ERR}In function \'{function}\': implicit declaration of function {msg}{position}'
        elif self.errorType == 3:
            msg = f'{Colors.ERR}In function \'{function}\': operation incompatible with {msg}{position}'
        elif self.errorType == 4:
            msg = f'{Colors.ERR}In function \'{function}\': string does not support this operation {msg}{position}'
        elif self.errorType == 5:
            msg = f'{Colors.ERR}In function \'{function}\': identifier {msg} has already been declared{position}'
        elif self.errorType == 6:
            msg = f'{Colors.ERR}In function \'{function}\': return incompatible with {msg}{position}'
        elif self.errorType == 7:
            msg = f'{Colors.ERR}In function \'{function}\': Incompatible number arguments in {msg}{position}'
        
        raise self.errs.addError(f'{Colors.SEM}[Semantic Error] {msg}')

    def check(self):
        self.checkVariables()

    def checkVariables(self):
        identifierType = {}
        functionParameters = {}
        callFunctionParameters = {}
        checkParameters = False
        checkParameterPassing = False
        functionType = {}
        checkReturn = False
        declared = []
        function = ''
        functions = []
        for token in self.tokenTable:
            if token[2] in self.variableType:
                if self.tokenTable[self.indexTK+1][0] in (declared+functions[0:-1:1]): 
                    self.errorType = 5
                    self.errorMessage(f'{function}', f'\'{self.tokenTable[self.indexTK+1][0]}\'')

                declared.append(self.tokenTable[self.indexTK+1][0])
                identifierType[self.tokenTable[self.indexTK+1][0]] = token[2]

            if token[2] == Tokens.TK_INDETINFIER:
                if self.tokenTable[self.indexTK+1][2] == Tokens.TK_OP:
                    if not (token[0] in functions):
                        self.errorType = 2
                        self.errorMessage(f'{function}', f'\'{token[0]}\'')
                else:
                    if not (token[0] in declared):
                        self.errorType = 1
                        self.errorMessage(f'{function}', f'\'{token[0]}\'')

                if self.tokenTable[self.indexTK+1][2] == Tokens.TK_ASSIGNMENT:
                    self.idToCheck = token[0]
                    self.isAttribution = True

            if self.isAttribution:
                # Presença de string em operação entre interger e real
                if identifierType[self.idToCheck] in [Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL]:
                    if token[2] != Tokens.TK_INDETINFIER:
                        if token[2] == Tokens.TK_STRING:
                            self.errorType = 3
                            self.errorMessage(f'{function}', f'\'integer or real\'')
                    elif identifierType[token[0]] == Tokens.TK_RW_STRING:
                        self.errorType = 3
                        self.errorMessage(f'{function}', f'\'integer or real\'')
                # Presença de integer e real em operação entre strings
                elif identifierType[self.idToCheck] == Tokens.TK_RW_STRING:
                    if token[2] != Tokens.TK_INDETINFIER:
                        if token[2] in [Tokens.TK_INTEGER, Tokens.TK_REAL]:
                            self.errorType = 3
                            self.errorMessage(f'{function}', f'\'string\'')
                    elif identifierType[token[0]] in [Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL]:
                        self.errorType = 3
                        self.errorMessage(f'{function}', f'\'string\'')

                    # Verifica ocorrência de operações não suportadas por string
                    if token[2] in self.unsupported:
                        self.errorType = 4
                        self.errorMessage(f'{function}', f'\'{token[0]}\'')

                if token[2] == Tokens.TK_END:
                    self.isAttribution = False
                    self.idToCheck = ''

            if token[2] in [Tokens.TK_RW_FUNCTION, Tokens.TK_RW_MAIN]:
                if token[2] == Tokens.TK_RW_FUNCTION:
                    function = self.tokenTable[self.indexTK+2][0]
                    functionType[function] = self.tokenTable[self.indexTK+1][2]
                    checkParameters = True
                    functionParameters[function] = -1
                    
                    if function in (functions+declared):
                        self.errorType = 5
                        self.errorMessage(f'{function}', f'\'{self.tokenTable[self.indexTK+1][0]}\'')
                    functions.append(function)
                else:
                    function = token[0]
                declared.clear()

            if token[2] == Tokens.TK_RW_RETURN:
                checkReturn = True

            if checkReturn:
                # Presença de string em retorno de interger e real
                if functionType[functions[-1]] in [Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL]:
                    if token[2] != Tokens.TK_INDETINFIER:
                        if token[2] == Tokens.TK_STRING:
                            print(token[0])
                            self.errorType = 6
                            self.errorMessage(f'{function}', f'\'integer or real\'')
                    elif identifierType[token[0]] == Tokens.TK_RW_STRING:
                        self.errorType = 6
                        self.errorMessage(f'{function}', f'\'integer or real\'')
                # Presença de integer e real em retorno de strings
                elif functionType[functions[-1]] == Tokens.TK_RW_STRING:
                    if token[2] != Tokens.TK_INDETINFIER:
                        if token[2] in [Tokens.TK_INTEGER, Tokens.TK_REAL]:
                            self.errorType = 6
                            self.errorMessage(f'{function}', f'\'string\'')
                    elif identifierType[token[0]] in [Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL]:
                        self.errorType = 6
                        self.errorMessage(f'{function}', f'\'string\'')

                    # Verifica ocorrência de operações não suportadas por string
                    if token[2] in self.unsupported:
                        self.errorType = 4
                        self.errorMessage(f'{function}', f'\'{token[0]}\'')

                if token[2] == Tokens.TK_END:
                    checkReturn = False

            if (token[0] in functions) and not checkParameters:
                callFunction = token[0]
                callFunctionParameters[callFunction] = 0
                checkParameterPassing = True

            if checkParameters:
                if token[2] == Tokens.TK_INDETINFIER:
                    functionParameters[function] += 1
                
                if token[2] == Tokens.TK_CP:
                    checkParameters = False

            if checkParameterPassing:
                
                if token[2] in [Tokens.TK_COMMA, Tokens.TK_CP] and not (self.tokenTable[self.indexTK-1][2] in [Tokens.TK_OP, Tokens.TK_COMMA]):
                    callFunctionParameters[callFunction] += 1

                if token[2] == Tokens.TK_CP:
                    if callFunctionParameters[callFunction] != functionParameters[callFunction]:
                        self.errorType = 7
                        self.errorMessage(f'{function}', f'\'{callFunction}\'')

                    checkParameterPassing = False

            self.indexTK += 1
