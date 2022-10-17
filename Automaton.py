from ast import Raise
from Colors import Colors
from Errors import Errors
from ReservedWords import ReservedWords
from Tokens import Tokens
import string

class State:
    '''Simboliza um estado do autômato'''
    def __init__(self, id, transitions=None, condition=None, token=None, info=None) -> None:
        self.id = id                    # Idenficador do estado
        self.transitions = transitions  # Armazena as transições para outros estados
        self.condition = condition      # Indica se o estado é FINAL
        self.token = token              # Se for estado final indica o token do lexema
        self.info = info                # Uma breve descrição do estado se for FINAL (Isso não é necessário)

    def __str__(self) -> str:
        return f'id: {self.id}\ncondition: {self.condition}\ntransitions: {self.transitions}'


class Automaton:
    '''Autômato finito utilizado no Scanner'''

    # Alfabeto
    uppercase_AZ = string.ascii_uppercase
    lowercase_ab = string.ascii_lowercase
    digits = string.digits
    whitespace = string.whitespace
    point = '.'
    op = '('
    cp = ')'
    ok = '{'
    ck = '}'
    comma = ','
    math_add = '+'
    math_sub = '-'
    math_mul = '*'
    math_div = '/'
    pipe = '|'
    ampersand = '&'
    logic_not = '!'
    logic_g = '>'
    logic_l = '<'
    assignment = '='
    semicolon = ';'
    quotation_mark = '"'
    alphabet_aZ = lowercase_ab + uppercase_AZ
    ascii_table = ''
    for i in range(0, 256):
        ascii_table += chr(i)

    errs = Errors().instance()
    table = [] # Tabela de Tokens
    is_str = False # Flag de string

    def __init__(self) -> None:
        self.states = {} # Armazena todos os estados do autômato
        self.generate()  # Gera o autômato finito

    def validate(self, code) -> list:
        if code == []:
            self.errs.addError(f'{Colors.ERR}Null file!{Colors.END}')
            raise

        # Localização do token
        line_n = 0
        column_n = 0

        for line in code:
            line_n += 1
            column_n = 0

            state = 0
            lexeme = ''

            for char in line:
                column_n += 1
                
                # Verificar se é comentário (Se for ignora)
                if char == '#':
                    break

                if char == '"' and not is_str: # Verifica se é string
                    is_str = True

                # Verifica se o caracter é um espaço em branco (Se for ignora)
                if char in self.whitespace and not is_str: # Caso for um espaço em branco em string pula
                    continue

                # Próximo caracter a ser validado
                next_c = self.nextCharacter(line, column_n) 

                # Leitura e validação do token
                if char in self.states[state].transitions.keys(): # Existe transição?
                    lexeme += char

                    state = self.states[state].transitions[char]  # Se existir faz transição

                    if next_c in self.states[state].transitions.keys(): # O próximo caracter apresenta transição?
                        continue                                        # Se existir continua leitura

                    if self.states[state].condition == 'FINAL':
                        print(lexeme)
                        self.addToken(state, lexeme, line_n, column_n)
                        state = 0
                        lexeme = ''
                        is_str = False
                    else:
                        self.errs.addError(f'{Colors.ERR}[Lexical Error] No transition from \'{char}\' to \'{next_c}\', line {line_n}, column {column_n}.{Colors.END}')
                        break
                else:
                    self.errs.addError(f'{Colors.ERR}[Lexical Error] {Colors.ERR}Inavalid token → \'{char}\', line {line_n}, column {column_n}.{Colors.END}')
                    break
        
        # Conforme vai para as próximas etapas muda disparo de erro
        if self.errs.hasError():
            raise

        return self.table

    def nextCharacter(self, line, index):
        next_c = None
        if index < len(line):
            next_c = line[index]
        return next_c

    def addToken(self, state, lexeme, line_n, column_n) -> None:
        # Verifica se é identificador (Se for verfica se é palavra reservada)
        if self.states[state].token == Tokens.TK_INDETINFIER:
            if lexeme in ReservedWords.rws.keys():
                self.table.append((lexeme, 'RESERVED WORD', ReservedWords.rws[lexeme], line_n, column_n))
            else:
                self.table.append((lexeme, self.states[state].info, self.states[state].token, line_n, column_n))
        else:
            self.table.append((lexeme, self.states[state].info, self.states[state].token, line_n, column_n))

    def generate(self) -> None:
        '''Gera as transições utilizadas para validar os lexemas das linguagem'''

        # Formato transições { transição: novo estado }
        # Formato do autômato { estado: State(id, transições, condição, token, descrição) } 

        # Transições do estado 0
        transitions_0 = {}
        transitions_0.update({i: 0 for i in self.whitespace})       # 0 → 0
        transitions_0.update({i: 74 for i in self.alphabet_aZ})     # 0 → 74
        transitions_0.update({i: 75 for i in self.digits})          # 0 → 75
        transitions_0.update({i: 78 for i in self.quotation_mark})  # 0 → 78
        transitions_0.update({i: 80 for i in self.op})              # 0 → 80
        transitions_0.update({i: 81 for i in self.cp})              # 0 → 81
        transitions_0.update({i: 82 for i in self.ok})              # 0 → 82
        transitions_0.update({i: 83 for i in self.ck})              # 0 → 83
        transitions_0.update({i: 84 for i in self.comma})           # 0 → 84
        transitions_0.update({i: 85 for i in self.math_add})        # 0 → 85
        transitions_0.update({i: 86 for i in self.math_sub})        # 0 → 86
        transitions_0.update({i: 87 for i in self.math_mul})        # 0 → 87
        transitions_0.update({i: 88 for i in self.math_div})        # 0 → 88
        transitions_0.update({i: 89 for i in self.pipe})            # 0 → 89
        transitions_0.update({i: 91 for i in self.ampersand})       # 0 → 91
        transitions_0.update({i: 93 for i in self.logic_not})       # 0 → 93
        transitions_0.update({i: 95 for i in self.logic_l})         # 0 → 95
        transitions_0.update({i: 97 for i in self.logic_g})         # 0 → 97
        transitions_0.update({i: 99 for i in self.assignment})      # 0 → 99
        transitions_0.update({i: 101 for i in self.semicolon})      # 0 → 101

        # Transições do estado 74
        transitions_74 = {}
        transitions_74.update({i: 74 for i in self.alphabet_aZ})    # 74 → 74
        transitions_74.update({i: 74 for i in self.digits})         # 74 → 74

        # Transições do estado 75
        transitions_75 = {}
        transitions_75.update({i: 75 for i in self.digits})         # 74 → 75
        transitions_75.update({i: 76 for i in self.point})          # 74 → 76

        # Transições do estado 76
        transitions_76 = {}
        transitions_76.update({i: 77 for i in self.digits})         # 76 → 77

        # Transições do estado 77
        transitions_77 = {}
        transitions_77.update({i: 77 for i in self.digits})         # 77 → 77

        # Transições do estado 78
        transitions_78 = {}
        transitions_78.update({i: 78 for i in self.ascii_table})    # 78 → 78
        transitions_78.update({i: 79 for i in self.quotation_mark}) # 78 → 79

        # Transições do estado 79
        transitions_79 = {}

        # Transições do estado 80
        transitions_80 = {}

        # Transições do estado 81
        transitions_81 = {}

        # Transições do estado 82
        transitions_82 = {}

        # Transições do estado 83
        transitions_83 = {}

        # Transições do estado 84
        transitions_84 = {}

        # Transições do estado 85
        transitions_85 = {}

        # Transições do estado 86
        transitions_86 = {}

        # Transições do estado 87
        transitions_87 = {}

        # Transições do estado 88
        transitions_88 = {}

        # Transições do estado 89
        transitions_89 = {}
        transitions_89.update({i: 90 for i in self.pipe})           # 89 → 90

        # Transições do estado 90
        transitions_90 = {}

        # Transições do estado 91
        transitions_91 = {}
        transitions_91.update({i: 92 for i in self.ampersand})      # 92 → 93

        # Transições do estado 92
        transitions_92 = {}

        # Transições do estado 93
        transitions_93 = {}
        transitions_93.update({i: 94 for i in self.assignment})     # 93 → 94

        # Transições do estado 94
        transitions_94 = {}

        # Transições do estado 95
        transitions_95 = {}
        transitions_95.update({i: 96 for i in self.assignment})     # 95 → 96

        # Transições do estado 96 
        transitions_96 = {}

        # Transições do estado 97
        transitions_97 = {}
        transitions_97.update({i: 98 for i in self.assignment})     # 97 → 98

        # Transições do estado 98
        transitions_98 = {}

        # Transições do estado 99
        transitions_99 = {}
        transitions_99.update({i: 100 for i in self.assignment})   # 99 → 100

        # Transições do estado 100
        transitions_100 = {}

        # Transições do estado 101
        transitions_101 = {}

        # Gerando autômaro
        self.states[0] = State(0, transitions_0, 'INITIAL')
        self.states[74] = State(74, transitions_74, 'FINAL', Tokens.TK_INDETINFIER, 'IDENTIFIER')
        self.states[75] = State(75, transitions_75, 'FINAL', Tokens.TK_INTEGER, 'INTEGER')
        self.states[76] = State(76, transitions_76)
        self.states[77] = State(77, transitions_77, 'FINAL', Tokens.TK_REAL, 'REAL')
        self.states[78] = State(78, transitions_78)
        self.states[79] = State(79, transitions_79, 'FINAL', Tokens.TK_STRING, 'STRING')
        self.states[80] = State(81, transitions_80, 'FINAL', Tokens.TK_OP, 'OP')
        self.states[81] = State(82, transitions_81, 'FINAL', Tokens.TK_CP, 'CP')
        self.states[82] = State(83, transitions_82, 'FINAL', Tokens.TK_OK, 'OK')
        self.states[83] = State(84, transitions_83, 'FINAL', Tokens.TK_CK, 'CK')
        self.states[84] = State(85, transitions_84, 'FINAL', Tokens.TK_COMMA, 'COMMA')
        self.states[85] = State(86, transitions_85, 'FINAL', Tokens.TK_MATH_ADD, 'ADD')
        self.states[86] = State(87, transitions_86, 'FINAL', Tokens.TK_MATH_SUB, 'SUB')
        self.states[87] = State(88, transitions_87, 'FINAL', Tokens.TK_MATH_MUL, 'MUL')
        self.states[88] = State(89, transitions_88, 'FINAL', Tokens.TK_MATH_DIV, 'DIV')
        self.states[89] = State(90, transitions_89)
        self.states[90] = State(91, transitions_90, 'FINAL', Tokens.TK_LOGIC_OR, 'OR')
        self.states[91] = State(92, transitions_91)
        self.states[92] = State(93, transitions_92, 'FINAL', Tokens.TK_LOGIC_AND, 'AND')
        self.states[93] = State(94, transitions_93, 'FINAL', Tokens.TK_LOGIC_NOT, 'NOT')
        self.states[94] = State(95, transitions_94, 'FINAL', Tokens.TK_LOGIC_DIF, 'DIFFERENT')
        self.states[95] = State(96, transitions_95, 'FINAL', Tokens.TK_LOGIC_LT, 'LT')
        self.states[96] = State(97, transitions_96, 'FINAL', Tokens.TK_LOGIC_LTE, 'LTE')
        self.states[97] = State(98, transitions_97, 'FINAL', Tokens.TK_LOGIC_GT, 'GT')
        self.states[98] = State(99, transitions_98, 'FINAL', Tokens.TK_LOGIC_GTE, 'GTE')
        self.states[99] = State(100, transitions_99, 'FINAL', Tokens.TK_ASSIGNMENT, 'ASSIGNMENT')
        self.states[100] = State(101, transitions_100, 'FINAL', Tokens.TK_LOGIC_EQ, 'EQUAL')
        self.states[101] = State(102, transitions_101, 'FINAL', Tokens.TK_END, 'END')
