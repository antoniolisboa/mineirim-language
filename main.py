import sys
from time import time
from Colors import Colors
from Errors import Errors
from Scanner import Scanner

def main(file):

    errs = Errors().instance() # Singleton para armazenar todos os erros
    try:
        '''Lex Analise (Scanner)'''
        token_table = Scanner(file).table # Análise Léxica → Retorna tabela de tokens
        print(token_table)
    except:
        for err in errs.listErrors:
            print(err)

if __name__ == '__main__':
    arg = sys.argv

    init = time()
    main('main.mm')
    finish = time()

    print(f'{Colors.TCM}Compile Time: {(finish - init):.3e} sec.{Colors.END}')
