from m3ta import alphabet, primes1

letters = alphabet
primes = primes1(len(alphabet))

class Word:
    def __init__(self,string):
        self.id = string
        self.transmorphs = []
        self.sequence = tuple(primes[letters.index(letter)] for letter in self.id)
        self.base = (set(self.id),set(self.sequence))
        self.successors = {}
        self.antecedents = {}
        self.cohort = {
            'pred':{},
            'succ':{}
        }
        self.samples = 0
        self.cases = {'lower':0,'upper':0,'mixed':0}
    def __repr__(self):
        return self.id
    def __str__(self):
        return self.id
    def _dumpCohort(self,iterable,att=None):
        assert att != None, f"Target attribute is undefined:\n\t\t{att=}"
        if iterable==None:
            if iterable not in self.cohort[att].keys():
                self.cohort[att][iterable] = 0
            self.cohort[att][iterable] += 1
        else:
            for i in range(len(iterable)):
                if iterable[i] not in self.cohort[att].keys():
                    self.cohort[att][iterable[i]] = 0
                self.cohort[att][iterable[i]] += 1
    def _getNeighbors(self,phrase):
        phrase = phrase.split() if isinstance(phrase,str) else phrase
        while self.id in phrase:
            position = phrase.index(self.id)
            pred = phrase[position-1] if position!=0 else None
            succ = phrase[position+1] if position!=len(phrase)-1 else None
            if pred not in self.antecedents.keys():
                self.antecedents[pred] = 0
            if succ not in self.successors.keys():
                self.successors[succ] = 0
            self.antecedents[pred] += 1
            self.successors[succ] += 1
            del phrase[position]
            # self.neighborSamples += 1
    def _getCohort(self,phrase):
        phrase = phrase.split() if isinstance(phrase,str) else phrase
        while self.id in phrase:
            position = phrase.index(self.id)
            pred = phrase[:position] if position!=0 else None
            succ = phrase[position+1:] if position!=len(phrase)-1 else None
            # print(f'{pred=}\n{succ=}')
            self._dumpCohort(pred,'pred')
            self._dumpCohort(succ,'succ')
            del phrase[position]
            # self.cohortSamples += 1
    def sample(self,phrase):
        self._getNeighbors(phrase)
        self._getCohort(phrase)
        self.samples += 1

if __name__ == '__main__':
    test = f'the quick bown fox jumps over the lazy dog'
    for word in set(test[:].split()):
        w = Word(word)
        w.sample(test)
        print(f'{w}\n{w.antecedents=}\n{w.successors=}\n{w.samples=}\n{w.cohort=}\n')
        print()
