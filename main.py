import sys
from time import time

def main(file):
    '''Lex Analise (Scanner)'''
    # Return list of tokens
    pass

if __name__ == '__main__':
    arg = sys.argv

    init = time()
    main('main.mm')
    finish = time()

    print(f'\033[1;33m Compile Time: {(finish - init):.3e} sec')
