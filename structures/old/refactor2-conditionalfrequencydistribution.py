import re

import nltk
from nltk.probability import ConditionalFreqDist, ConditionalProbDist, ELEProbDist, FreqDist
from nltk import word_tokenize, pos_tag
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
# import nltk.corpus as corpum, nltk.book as book, nltk.probability as probability

from m3ta import defaultdict, Address, show, pop, main, chords, tipo, join, shuffle
from refactor1 import normalize


class Node:
    def __init__(self, id):
        # self.id = id = normalize(id)
        self.id = str(id)
        self.cohorts = ConditionalFreqDist()
        self.forms = defaultdict(int)
        self.tag = pos_tag([id])[0][-1]
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
        keys = (self.leaders, self.followers, self.predecessors, self.successors)
        keystrs = ('leading', 'following', 'predecessing', 'successing')
        items = zip(keystrs, map(lambda x: x.get(string), keys))
        pairs = (join(pair, ': ') for pair in items)
        rack = join(pairs, ',\n   ')
        return f"{string} wrt {self.id}\n" + "{  " + rack + "}"
    def __getattr__(self, attr):
        return self.cohorts[attr]
    def __hash__(self):
        return hash(self.id)
    def __str__(self):
        return self.id
    @property
    def freq(self):
        return sum(self.forms.values())

class Dictionary(defaultdict):
    def __init__(self):
        defaultdict.__init__(self, Node)
    def vertices(self, sample):
        tokes = sample.split()
        stems = map(self.stem, set(tokes))
        return {stem: self[stem] for stem in stems}
    def edges(self, sample):
        wnl = WordNetLemmatizer()
        
        tokes = sample.split()
        text = dict(enumerate(tokes))
        lemmas = map(wnl.lemmatize, set(tokes))
        
        nodes = {lemma: Node(lemma) for lemma in lemmas}
        # nodes = {lemma: node if (node:=self.get(lemma)) else Node(lemma) for lemma in lemmas}
        # print(nodes)
        for node in nodes:
            if self.get(node):
                nodes[node] = self[node]
            else:
                self[node] = nodes[node]
        
        # table = {term: wnl.lemmatize(term) for term in tokes}
        table = {term: nodes[self.stem(term)] for term in set(tokes)}
        
        # for node in nodes:
            # self
        # for index, trio in enumerate(chords(tokes, 3)):
        for index, trio in enumerate(chords(tokes, 2)):
            # first, second, third = map(wnl.lemmatize, trio)
            # first, second, third = trio
            first, second = trio
            i, j, k = map(lambda x: index + x, (0, 1, 2))
            # print(*map(text.get, (i,j,k)))
            
            table[first].cohorts['followers'][second] += 1
            table[second].cohorts['leaders'][first] += 1
            
            # table[second].cohorts['followers'][third] += 1
            # table[third].cohorts['leaders'][second] += 1
            
            # nodes[second].cohorts['followers'][third] += 1
        return self
    def points(self, sample):
        nodes = self.vertices(sample)
        tokes = sample.split()
        lemmas = {token: node[self.stem(token) for token in tokes}
        for i, term in enumerate(tokes):
            for j, t in enumerate(tokes):
                if j == i :
                    table[term].forms[t] += 1
                elif j > i:
                    if j == i+1:
                        table[term].cohorts['followers'][t] += 1
                    table[term].cohorts['successors'][t] += 1
                elif j < i:
                    if j == i-1:
                        table[term].cohorts['leaders'][t] += 1
                    table[term].cohorts['predecessors'][t] += 1
    def faces(self, sample):
        nodes = self.vertices(sample)
        tokes = sample.split()
        lemmas = {token: self.stem(token) for token in tokes}
        for i in 


class Agent(defaultdict):
    def __init__(self, dictionary, lemmatizer):
        self.memory = dictionary
        self.stem = lemmatizer().stem()
        try:
            self.stem = lemmatizer().stem
        except AttributeError:
            self.stem = lemmatizer().lemmatize
if eval(main):
    sent = "the the the dog dog some other words that we do not care about."
    sent = "go home, Louis"
    sent = "go home, Charles"
    sent = "ones twos threes"
    # sent = "Frank's a bigger jerk than Laurie"
    # sent = "the quick brown foxes jumped over the lazy dogs"
    
    # sent = zip(sent.split(), range(1, len(sent)+1))
    sent = zip(sent.split(), shuffle(range(1, len(sent)+1)))
    sent = join(((a+' ')*b for a,b in sent), ' ')
    
    print(sent)
    b = Dictionary()
    b.train(sent)
    # show(b.values())
    show(((print(n.id), n.cohorts.tabulate())[-1] for n in b.values()),sep='\n\n')