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
        # 3 → Incompatibilidade entre operações

        line = self.tokenTable[self.indexTK][3]
        column = self.tokenTable[self.indexTK][4]   

        position = f', line {line}, column {column}.{Colors.END}'

        if self.errorType == 1:
            msg = f'{Colors.ERR}In function \'{function}\': {msg} undeclared{position}'
        elif self.errorType == 2:
            msg = f'{Colors.ERR}In function \'{function}\': implicit declaration of function {msg}{position}'
        elif self.errorType == 3:
            msg = f'{Colors.ERR}In function \'{function}\': operation incompatible with {msg}{position}'
        
        raise self.errs.addError(f'{Colors.SEM}[Semantic Error] {msg}')

    def check(self):
        self.checkVariables()

    def checkVariables(self):
        identifierType = {}
        declared = []
        function = ''
        functions = []
        for token in self.tokenTable:
            if token[2] in self.variableType:
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
                if identifierType[self.idToCheck] in self.variableType[0:2]:
                    print(self.idToCheck)
                    print(identifierType)
                    print(token[0])
                    if token[0] in identifierType:
                        if token[2] == Tokens.TK_STRING or identifierType[token[0]] == Tokens.TK_RW_STRING:
                            print(token[0])
                            self.errorType = 3
                            self.errorMessage(f'{function}', f'\'{token[0]}\'')

                if token[2] == Tokens.TK_END:
                    self.isAttribution = False
                    self.idToCheck = ''

            if token[2] in [Tokens.TK_RW_FUNCTION, Tokens.TK_RW_MAIN]:
                if token[2] == Tokens.TK_RW_FUNCTION:
                    function = self.tokenTable[self.indexTK+2][0]
                    functions.append(function)
                else:
                    function = token[0]
                declared.clear()

            self.indexTK += 1
