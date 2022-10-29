from tokenize import Token
from Tokens import Tokens
from Errors import Errors
from Colors import Colors
from Tokens import Tokens


class Node:
    def __init__(self, term, token=None, isTerminal=False) -> None:
        self.term = term
        self.token = token
        self.isTerminal = isTerminal
        self.children = []

    def addChild(self, childNode):
        self.children.append(childNode)

    def __str__(self) -> str:
        return f'{self.term}'


class Parser:
    errs = Errors().instance()

    def __init__(self, tokenTable) -> None:
        self.tokenTable = tokenTable.copy()
        self.currentToken = 0
        self.tree = None
        self.isEnd = True
        self.init()

    def isTerminal(self, token) -> bool:
        # Evita busca de token em index inexistente
        if self.isEnd:
            # verfica se o token corresponde 
            if self.tokenTable[self.currentToken][2] in token:
                return True
        
        # False se já chegou ao fim ou o token não corresponde 
        return False        

    def errorMessage(self, msg):
        # 2 tipos de erros: Não tem token ou o Token não corresponde
    
        line = self.tokenTable[self.currentToken][3]
        column = self.tokenTable[self.currentToken][4]

        position = f', line {line}, column {column}.{Colors.END}'
        msg = f'{Colors.ERR}Missing {msg}{position}'
        raise self.errs.addError(f'{Colors.SIN}[Syntactic Error] {msg}')

    def init(self):
        # Root
        root = Node('init')

        # Verifica se existe função(InventaModa)
        if self.tokenTable[self.currentToken] != Tokens.TK_RW_MAIN:
            self.functionDeclaration(root)
        
        self.mainFunction(root)

        print('End parsing!')

        # Conforme vai para as próximas etapas muda disparo de erro
        if self.errs.hasError():
            raise

        # Save tree
        self.tree = root

    def functionDeclaration(self, previousNode):
        currentNode = Node('functionDeclaration')

        self.functionIndicator(currentNode)
        self.dataType(currentNode)
        self.identifier(currentNode)
        self.openParentheses(currentNode)
        self.functionParameters(currentNode)
        self.closeParentheses(currentNode)
        self.openKey(currentNode)
        # self.content(currentNode)
        self.closeKey(currentNode)
        
        previousNode.addChild(currentNode)

    def mainFunction(self, previousNode):
        currentNode = Node('mainFunction')

        self.main(currentNode)
        self.openParentheses(currentNode)
        self.closeParentheses(currentNode)
        self.openKey(currentNode)
        self.content(currentNode)
        self.closeKey(currentNode)

        previousNode.addChild(currentNode)

    def main(self, previousNode):
        if self.isTerminal([Tokens.TK_RW_MAIN]):
            currentNode = Node('main')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\'Uai\'')

    def functionIndicator(self, previousNode):
        if self.isTerminal([Tokens.TK_RW_FUNCTION]):
            currentNode = Node('functionIndicator')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\'InventaModa\'')

    def dataType(self, previousNode):
        if self.isTerminal([Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL, Tokens.TK_RW_STRING]):
            currentNode = Node('dataType')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\'dataType\'')

    def identifier(self, previousNode):
        if self.isTerminal([Tokens.TK_INDETINFIER]):
            currentNode = Node('identifier')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\'identifier\'')

    def openParentheses(self, previousNode):
        if self.isTerminal([Tokens.TK_OP]):
            currentNode = Node('openParentheses')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\'(\'')

    def functionParameters(self, previousNode):
        if self.isTerminal([Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL, Tokens.TK_RW_STRING]):
            currentNode = Node('functionParameters')
            
            while True:
                self.dataType(currentNode)
                self.identifier(currentNode)

                if self.isTerminal([Tokens.TK_COMMA]):
                    self.comma(currentNode)
                elif self.isTerminal([Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL, Tokens.TK_RW_STRING]):
                    self.errorMessage('\',\'')
                else:
                    break

            previousNode.addChild(currentNode)

    def comma(self, previousNode):
        currentNode = Node('comma')
        self.terminal(currentNode)
        previousNode.addChild(currentNode)

    def closeParentheses(self, previousNode):
        if self.isTerminal([Tokens.TK_CP]):
            currentNode = Node('closeParentheses')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\')\'')

    def openKey(self, previousNode):
        if self.isTerminal([Tokens.TK_OK]):
            currentNode = Node('openKey')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\'{\'')

    def content(self, previousNode):
        currentNode = Node('content')

        hasContente = False

        while True:
            if self.isTerminal([Tokens.TK_RW_INTEGER, Tokens.TK_RW_REAL, Tokens.TK_RW_STRING]): 
                # Declaração de variáveis
                self.variableDeclaration(currentNode)
                hasContente = True
                continue
            else:
                break

        if hasContente:
            previousNode.addChild(currentNode)
    
    def variableDeclaration(self, previousNode):
        currentNode = Node('variableDeclaration')

        self.dataType(currentNode)
        self.identifier(currentNode)

        if self.isTerminal([Tokens.TK_ASSIGNMENT]):
            self.assignment(currentNode)
            if self.isTerminal([Tokens.TK_STRING]):
                self.string(currentNode)
            else:
                self.mathExpression(currentNode)

        self.end(currentNode)

        previousNode.addChild(currentNode)

    def assignment(self, previousNode):
        currentNode = Node('assignment')
        self.terminal(currentNode)
        previousNode.addChild(currentNode)

    def mathExpression(self, previousNode):
        currentNode = Node('mathExpression')

        self.term(currentNode)
        # Se houver + ou -
        if self.isTerminal([Tokens.TK_MATH_ADD, Tokens.TK_MATH_MUL]):
            self.mathOperator(currentNode)
            self.term(currentNode)
        
        previousNode.addChild(currentNode)

    def term(self, previousNode):
        currentNode = Node('term')

        self.factor(currentNode)
        # Se houver * ou /
        if self.isTerminal([Tokens.TK_MATH_MUL, Tokens.TK_MATH_DIV]):
            self.mathOperator(currentNode)
            self.factor(currentNode)

        previousNode.addChild(currentNode)

    def factor(self, previousNode):
        currentNode = Node('fator')

        if self.isTerminal([Tokens.TK_OP]):
            self.openParentheses(currentNode)
            self.mathExpression(currentNode)
            self.closeParentheses(currentNode)
        elif self.isTerminal([Tokens.TK_INDETINFIER]):
            self.identifier(currentNode)
        elif self.isTerminal([Tokens.TK_REAL, Tokens.TK_INTEGER]):
            self.number(currentNode)
        else:
            self.errorMessage('\'attribution value\'')
        
        previousNode.addChild(currentNode)

    def mathOperator(self, previousNode):
        currentNode = Node('mathOperator')
        self.terminal(currentNode)
        previousNode.addChild(currentNode)
    
    def number(self, previousNode):
        currentNode = Node('number')
        self.terminal(currentNode)
        previousNode.addChild(currentNode)

    def string(self, previousNode):
        currentNode = Node('string')
        self.terminal(currentNode)
        previousNode.addChild(currentNode)

    def end(self, previousNode):
        if self.isTerminal([Tokens.TK_END]):
            currentNode = Node('end')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\';\'')

    def closeKey(self, previousNode):
        if self.isTerminal([Tokens.TK_CK]):
            currentNode = Node('closeKey')
            self.terminal(currentNode)
            previousNode.addChild(currentNode)
        else:
            self.errorMessage('\'}\'')

    def terminal(self, previousNode):
        # Armazena terminal
        token = self.tokenTable[self.currentToken]
        currentNode = Node(f'{token}', token, True)
        previousNode.addChild(currentNode)

        # print(token)
        
        # Verifica se já chegou no fim da tabela de tokens
        if self.currentToken == len(self.tokenTable)-1:
            self.isEnd = False
        else:
            self.currentToken += 1
