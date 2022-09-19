import sys
from time import time
from Colors import Colors
from Scanner import Scanner

def main(file):

    try:
        '''Lex Analise (Scanner)'''
        # Return list of tokens
        print(Scanner(file).table)
    except BaseException as err:
        print(err)

if __name__ == '__main__':
    arg = sys.argv

    init = time()
    main('main.mm')
    finish = time()

    print(f'{Colors.TCM}Compile Time: {(finish - init):.3e} sec.{Colors.END}')
