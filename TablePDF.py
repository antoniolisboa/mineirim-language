from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class TablePDF:
    def __init__(self, symbolTable) -> None:
        self.symbolTable = symbolTable
        self.doc = None

    def generate(self):
        self.doc = SimpleDocTemplate("SymbolTable.pdf", pagesize=letter)
        elements = []

        data = [['Lexema', 'Descrição', 'Token', 'Linha', 'Coluna']]
        data += self.symbolTable

        print(data)

        table = Table(data)
        tableStyle = TableStyle([
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
        table.setStyle(tableStyle)

        elements.append(table)
        print(elements)
        self.doc.build(elements)
