from itertools import chain
from string import punctuation
import re, random

# import nltk
from nltk.probability import ConditionalFreqDist
from nltk import pos_tag
# from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
# import nltk.corpus as corpum, nltk.book as book, nltk.probability as probability

from m3ta import defaultdict, Address, show, pop, main, walks, tipo, join, shuffle, freq
# from refactor1 import normalize


ignorables = '-'
punctuation = join(i for i in punctuation if not i in ignorables)
_special_endings = "mars ver ther ter fer".split()

special_endings = map(re.escape, _special_endings)
special_endings = [i+"$" for i in special_endings]
special_endings = join(special_endings, '|')
special_endings = re.compile(special_endings, re.I)
_extensions = "es s ies ing er ers ly ive ish esque ed 's 've 're 'll 'm 'd , .".split()
extensions = map(re.escape, _extensions)
extensions = [i+"$" for i in extensions]
extensions = re.compile(join(extensions, '|'), re.I)

def normalize(term):
    while extensions.search(term) and not special_endings.search(term):
        term = join(extensions.split(term))
    return term.lower()


class UntrainedException(Exception):
    def __init__(self, *args, **kwargs):
        self.msg = "I have not been trained yet. Please train me before attempting to generate text."
        Exception.__init__(self, msg, *args, **kwargs)


class Node:
    def __init__(self, id):
        self.id = id #= normalize(id)
        self.cohorts = ConditionalFreqDist()
        self.forms = defaultdict(int)
        self.tag = pos_tag([id])[0][-1]
    def __iter__(self):
        yielded = set()
        rack = chain(self.predecessors, self.successors, self.leaders, self.followers)
        for i in rack:
            if not i in yielded:
                yield i
                yielded.add(i)            
    def __repr__(self):
        t = tipo(self).split('.')[-1]
        return f"{t}(id={self.id}, freq={self.freq})"
    def __eq__(self, other):
        if isinstance(other, str):
            return self.id == other
        return self.id == other.id
    def __add__(self, other):
        self.cohorts += other.cohorts
        return self
    def __len__(self):
        return len(self.id)
    def __getitem__(self, other):
        if isinstance(other, str):
            string = other
        elif isinstance(other, type(self)):
            string = other.id
        keys = (self.predecessors, self.successors, self.leaders, self.followers)
        keystrs = ('"predecessors"', '"successors"', '"leaders"', '"followers"')
        items = zip(keystrs, map(lambda x: x.get(string), keys))
        pairs = (join(pair, ': ') for pair in items)
        rack = join(pairs, ',\n   ')
        # return f"{string} wrt {self.id}\n" + "{  " + rack + "}"
        return eval("{  " + rack + "}")
    def __getattr__(self, attr):
        return self.cohorts[attr]
    def __hash__(self):
        return hash(self.id)
    def __str__(self):
        return self.id
    @property
    def freq(self):
        return sum(self.forms.values())


class Agent(dict):
    def __init__(self, lemmatizer=lambda x: x.lower()):
        dict.__init__(self)
        try:
            self.stem = lemmatizer().stem
        except AttributeError:
            self.stem = lemmatizer().lemmatize
        except TypeError:
            self.stem = lemmatizer
    
    def vertices(self, sample, sep=None):
        tokens = sample.split(sep) if sep!="#lines" else sample.splitlines()
        stems = map(self.stem, set(tokens))
        nodes = {stem: Node(stem) for stem in stems}
        for node in nodes:
            if self.get(node):
                nodes[node] = self[node]
            else:
                self[node] = nodes[node]
        return nodes
    
    def step(self, sample, sep=None):
        nodes = self.vertices(sample)
        tokens = sample.split()
        table = {term: nodes[self.stem(term)] for term in set(tokens)}
        for index, duo in enumerate(walks(tokens, 2)):
            first, second = duo
            table[first].cohorts['successors'][second] += 1
            table[second].cohorts['predecessors'][first] += 1
        return self
        
    def cohort(self, sample, sep=None):
        tokens = sample.split(sep) if sep!="#lines" else sample.splitlines()
        table = {term: self[self.stem(term)] for term in set(tokens)}
        for token in set(tokens):
            match = re.search(re.escape(token), sample, re.I)
            start, end = match.span()
            for term in sample[:start].split():
                table[token].cohorts['leaders'][term] += 1
            for term in sample[end:].split():
                table[token].cohorts['followers'][term] += 1
            if (ctr := (freq(token, tokens) - 1)):
                table[token].cohorts['leaders'][token] += ctr    
        return self
    
    def faces(self, sample, minimal_length=2, sep=None):
        nodes = self.vertices(sample)
        tokens = sample.split(sep) if sep!="#lines" else sample.splitlines()
        lemmas = {token: self.stem(token) for token in tokens}
        counter = 0
        for i in range(minimal_length, len(tokens)):
            for chord in walks(tokens, i):
                first, *middle, last = chord
                if first == last:
                    counter += 1
        return counter
    
    def characteristic(self, sample, minimal_length=2, sep=None):
        vertices = len(sample.split(sep))
        edges = len([*walks(sample.split(sep), 2)])
        faces = self.faces(sample)
        return vertices - edges + faces
    
    def train(self, sample, sep=None):
        tokens = sample.split()
        nodes = self.vertices(sample, sep)
        for token in tokens:
            nodes[self.stem(token)].forms[token] += 1
        self.step(sample)
        self.cohort(sample)
        return self
    
    def speak(self, length, sample='', sep=None):
        if len(self):
            if not sample:
                out = self[random.choice(self.keys())]
                length -= 1
            else:
                out = sample
            last = sample.split(sep)[-1]
            while length:
                new = str(self.nextword(out))
                new = new.title() if last.endswith('.') else new
                length -= 1
                out += ' ' + new
                last = new
            return out
        else:
            raise UntrainedException()
    
    def nextword(self, sample, sep=None, flags=re.I):
        """
        Look for nodes which have the last word in predecessors
        Else:
            look for nodes which have the most terms from the sample in their leaders
            Else:
                choose a random node
        """
        if len(self):
            prd = lambda token, term: re.search(re.escape(token), term, flags)
            tokens = sample.split(sep) if sep!="#lines" else sample.splitlines()
            matches = [node for node in self.values() if any(prd(tokens[-1], pred) for pred in node.predecessors)]
            if not matches:
                matches = [node for node in self.values() if any(prd(token, term) for term in node.leaders for token in tokens)]
            if matches:
                weights = [
                    sum(int(token in node.leaders) for token in tokens) for node in matches
                ]
                match = random.choices(matches, weights=weights, k=1)[0]
            else:
                weights = [len(node.leaders) for node in self.values()]
                match = random.choices(self.values(), weights=weights, k=1)[0]
            return match
        else:
            raise UntrainedException()

if eval(main):
    sents = [
        "Frank is a bigger jerk than Laurie",
        "the the the dog dog some other words that we do not care about.",
        "the quick brown foxes jumped over the lazy dogs",
        "go home, Louis",
        "go home, Charles",
        "to be or not to be",
        "this statement is false"
    ]
    
    sent = "ones twos threes"
    sent = zip(sent.split(), range(1, len(sent.split())+1))
    sent = join((join([a for i in range(b)], ' ') for a, b in sent), ' ')
    sents.append(sent)
    
    
    print(sent)
    # print(len(sent.split()), len([*walks(sent.split(), 2)]), len(sent.split()), len([*walks(sent.split(), 2)])/len(sent.split()), len([*walks(sent.split(), 2)]), sep='\n')
    b = Agent(WordNetLemmatizer)
    # b = Agent()
    print(b.characteristic(sent))
    for sent in sents:
        b.train(sent)
    for i in range(10):
        print(b.speak(i, "Things that aren't can't be, but Frank is so he must be"))
    
    # for i in b.values():
        # print(i)
        # print(i.tag)
        
    # print(b)
    # show(b.items())
    
    # b.vertices(sent)
    # show(b.items())
    
    # b.edges(sent)
    # show(b.items())
    
    # b.points(sent)
    # show(b.items())
    
    # b.faces(sent)
    # show(b.items())
    
    # show(b.values())
    # show(((print(n.id), n.cohorts.tabulate())[-1] for n in b.values()),sep='\n\n')