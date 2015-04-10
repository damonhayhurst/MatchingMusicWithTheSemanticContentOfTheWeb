from __future__ import division
import collections
import nltk
from nltk.tag import map_tag
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from reviews import model

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
        model = model()
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