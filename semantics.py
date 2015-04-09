from __future__ import division
import collections
import nltk
from nltk.tag import map_tag
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import csv
from reviews import get_model

__author__ = 'Damon Hayhurst'

stemmer = SnowballStemmer("english")
punct = ['``', "''", '""', '!', '"', '#', '$', '%', '&', '\\', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']

def tokenize(document):
    if type(document) is list:
        for sent in document:
            tokenized = nltk.word_tokenize(sent)
            return tokenized
    else:
        tokenized = nltk.word_tokenize(document)
        return tokenized

def pos_tag(tokenized, simplified=True):
    tuples = nltk.pos_tag(tokenized)
    if simplified:
        tuples = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in tuples]
    return tuples

def remove_stops(document):
    stops = set(stopwords.words("english"))
    text = []
    for word in document:
        if type(word) is tuple:
            if word[0] not in stops:
                text.append(word)
        else:
            if word not in stops:
                text.append(word)
    return text

def entities(tuples):
    chunky = nltk.ne_chunk(tuples)
    entities = [' '.join([y[0] for y in chunk.leaves()]) for chunk in chunky.subtrees() if chunk.label() == "PERSON" or chunk.label() == "ORGANIZATION" or chunk.label() == "LOCATION" or chunk.label() == "DATE" or chunk.label() == "FACILITY" or chunk.label() == "GPE"]
    return entities

def verbs(tuples):
    ignored = ['is', 'am', 'are', 'was', 'were', 'be', 'being', 'been', 'would', 'will', 'go', 'going', 'goes', 'has', 'have', 'went']
    verbs = [tuple[0] for tuple in tuples if tuple[1] == 'VERB' and tuple[0] not in ignored]
    count = collections.Counter(verbs)
    return sorted(count.items(), key=lambda x: x[1], reverse=True)


def stem(word):
    word = tuple_check(word)
    stemmed = stemmer.stem(word)
    return stemmed


def stems(tokenized):
    stems = []
    for word in tokenized:
        stemmed = stem(word)
        stems.append(stemmed)
    return stems

def adjectives(tuples):
    ignored = ['very', 'many', 'much', 'all', 'another', 'any', 'both', 'each', 'entire', 'every', 'few', 'first', 'likely', 'last', 'many', 'only', 'other', 'our', 'same', 'single', 'some', 'second', 'that', 'these', 'those', 'total', 'used', 'valid', 'which', 'whole', ]
    adjectives = [tuple[0] for tuple in tuples if tuple[1] == 'ADJ' and stem(tuple[0]) not in ignored]
    count = collections.Counter(adjectives)
    return sorted(count.items(), key=lambda x: x[1], reverse=True)

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

def get_aro_words(tokenized):
    word_list = []
    for word in tokenized:
        word = tuple_check(word)
        if word in aro_lookup:
            word_list.append((word, aro_lookup[word]))
        elif stem(word) in aro_lookup:
            word_list.append((stem(word), aro_lookup[stem(word)]))
        else:
            continue
    return sorted(word_list, key=lambda x: x[1], reverse=True)


def lookup_arousal(tokenized):
    total = 0
    count = 0
    for word in tokenized:
        if word in aro_lookup:
            total += aro_lookup[word]
            count += 1
        elif stem(word) in aro_lookup:
            total += aro_lookup[word]
            count += 1
        else:
            continue
    return total / count

def tagSearch(*tags):
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='
    query = 'site:last.fm%2Fmusic+intitle:"tags+for"'
    for tag in tags:
        tag = '+' + '"' + tag + '"'
        query += tag
    url = url + query
    return str(url)

def similarWords(tokenized):
    for word in tokenized:
        model = get_model()
        word = tuple_check(word)
        try:
            similar = model.most_similar(positive=[word, 'music'])
            print('\n' + word + str(similar))
        except KeyError:
            continue

def common_words(*sentences):
    words = {}
    mut_words = []
    ignored = ['the', "'s", 'in', 'is', 'it']
    for sentence in sentences:
        for word in sentence:
            word = tuple_check(word)
            if word not in words:
                words[word] = 1
            else:
                words[word] += 1
    for key in words.keys():
        if words[key] > 1:
            mut_words.append((key, words[key]))
    mut_words = [word for word in mut_words if word[0].lower() not in punct or ignored]
    return sorted(mut_words, key=lambda x: x[1], reverse=True)

def tuple_check(word):
    if type(word) is tuple:
        return word[0]
    else:
        return word




aro_lookup = filter_lookup(read_arousal())

genresUrl = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_terms.txt'
testUrl = 'http://www.bbc.co.uk/sport/0/football/30970439'
testSentence = 'This is an ultimate, to beat Chelsea, who I think will go on and win the Champions League - it really is.'


