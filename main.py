import sys
from time import time
from Scanner import Scanner

def main(file):
    '''Lex Analise (Scanner)'''
    # Return list of tokens
    Scanner(file)

if __name__ == '__main__':
    arg = sys.argv

    init = time()
    main('main.mm')
    finish = time()

    print(f'\033[1;33m Compile Time: {(finish - init):.3e} sec')
