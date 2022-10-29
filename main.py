import sys
from time import time
from Colors import Colors
from Errors import Errors
from Scanner import Scanner
from Parser import Parser
from TreePDF import TreePDF
from TablePDF import TablePDF

def main(file):

    # Singleton para armazenar todos os erros
    errs = Errors().instance() 
    
    try:
        '''Front-end Compiler'''
        
        # Análise Léxica → Retorna tabela de símbolos
        symbolTable = Scanner(file).table 
        # Análise Sintática → Retorna árvore sintática
        syntacticTree = Parser(symbolTable).tree

        # Gera PDF da tabela de simbolos
        TablePDF(symbolTable).generate()
        # Gerar PDF da árvore sintática
        TreePDF(syntacticTree).generate()
    except:
        # Se existir erros os mostra na tela
        for err in errs.listErrors: 
            print(err)

if __name__ == '__main__':
    arg = sys.argv

    init = time()
    main('main.mm')
    finish = time()

    print(f'{Colors.TCM}Compile Time: {(finish - init):.3e} sec.{Colors.END}')
