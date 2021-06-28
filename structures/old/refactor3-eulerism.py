import re

from m3ta import defaultdict, Address, show, pop, main, chords, tipo, join

pat = lambda pred: '^ | $|^ $| '.replace(' ', re.escape(pred))
mob = lambda pred, term: re.search(pat(pred), term)

class Vertex:
    def __init__(self, id):
        self.id = str(id)
        self.freq = 0
    def __str__(self):
        return self.id
    def __eq__(self, other):
        pattern = join("^$", sep=re.escape(id))
        return bool(re.match(pattern, str(other), re.I))
    def __ge__(self, other):
        return bool(re.search(re.escape(str(other)), self.str))
    def __le__(self, other):
        return bool(re.search)
    def pattern(self):
        return
        

class Edge:
    def __init__(self, vertex1, vertex2):
        self.verices = vertex1, vertex2
        self.freq = 1
    