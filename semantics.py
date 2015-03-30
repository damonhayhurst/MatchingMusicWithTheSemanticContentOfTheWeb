from __future__ import division
import nltk
from nltk.corpus import stopwords
import csv

__author__ = 'Damon Hayhurst'

def tokenize(document):
    tokenized = nltk.word_tokenize(document)
    return tokenized

def pos_tag(tokenized):
    tuples = nltk.pos_tag(tokenized, tagset='universal')
    return tuples

def remove_stops(document):
    stops = set(stopwords.words("english"))
    tuples = [w for w in document if not w in stops]
    return tuples

def entities(tuples):
    chunky = nltk.ne_chunk(tuples)
    return chunky

def verbs(tuples):
    verbs = [wt[0] for (wt, _) in tuples if wt[1] == 'VERB']
    return verbs

def read_arousal():
    file = open('emoFile.txt', 'r')
    file_reader = csv.DictReader(file, delimiter='\t')
    lookup = {}
    for row in file_reader:
        lookup.update({row['Word']: float(row['AroMn'])})
    return lookup

class Sentences(object):
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        file = open(self.path, 'r')
        for i, line in enumerate(file):
            line = line.lower()
            line = tokenize(line)
            line = remove_stops(line)
            if line:
                yield line
        file.close()

def filter_lookup(lookup):
    lookup_list = lookup.items()
    sorted_lookup_list = sorted(lookup_list, key=lambda x: x[1])
    mid_low_percent = 40
    mid_high_percent = 60
    total = len(sorted_lookup_list)
    percent = int(total / 100)
    mid_low = int(mid_low_percent * percent)
    mid_high = int(mid_high_percent * percent)
    count = 0
    #print(total)
    for tuple in sorted_lookup_list:
        if mid_low < count < mid_high:
            del lookup[tuple[0]]
        count += 1
    #print(len(lookup.items()))
    return lookup


def lookup_arousal(tokenized):
    total = 0
    count = 0
    for word in tokenized:
        if word in aro_lookup:
            total += aro_lookup[word]
            count += 1
        else:
            continue
    return total / count




aro_lookup = filter_lookup(read_arousal())

genresUrl = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_terms.txt';
testUrl = 'http://www.bbc.co.uk/sport/0/football/30970439'
testSentence = 'This is an ultimate, to beat Chelsea, who I think will go on and win the Champions League - it really is.'


