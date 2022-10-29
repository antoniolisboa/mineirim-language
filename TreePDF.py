from cProfile import label
import graphviz


class TreePDF:
    def __init__(self, syntacticTree) -> None:
        self.syntacticTree = syntacticTree
        self.level = 0
        self.id = 0
        self.tree = graphviz.Digraph(comment='Syntactic Tree')

    def generate(self, currentNode=None):
        if self.level == 0:
            currentNode = self.syntacticTree
        
        label = f'[{self.id}] {currentNode}'

        self.tree.node(label, label)
            
        print(currentNode)

        self.level += 1

        for child in currentNode.children:
            self.id += 1
            labelChild = f'[{self.id}] {child}'
            self.tree.edge(label, labelChild, constraint='true')
            self.generate(currentNode=child)
        
        self.level -= 1

        if self.level == 0:
            self.tree.render('SyntaticTree', view=True)
