from Automaton import Automaton

class Scanner:
    
    table = []

    def __init__(self, filename) -> None:
        with open(filename, 'r') as file:
            self.content = [line.rstrip() for line in file]

        self.table = Automaton().validate(self.content)
