from __future__ import division
import collections
import nltk
from nltk.tag import map_tag
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

__author__ = 'Damon Hayhurst'

#A list of methods to do with the manipulation and extractionof the semantics of a web page

stemmer = SnowballStemmer("english")
punct = ['``', "''", '""', '!', '"', '#', '$', '%', '&', '\\', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']

#Splits passage of text into list of word strings

def tokenize(document):
    if type(document) is list:
        for sent in document:
            tokenized = nltk.word_tokenize(sent)
            return tokenized
    else:
        tokenized = nltk.word_tokenize(document)
        return tokenized

#Adds "part of speech" tags to words, returns a list of tuples. PoS tags describe the word as a category. These categories include DET (Determiner), ADJ (Adjective)

def pos_tag(tokenized, simplified=True):
    tuples = nltk.pos_tag(tokenized)
    if simplified:
        tuples = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in tuples]
    return tuples

#Removes stop words from a passage of text

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

def text_to_pos_tags(text):
    tokenized = tokenize(text)
    tuples = pos_tag(tokenized)
    return tuples

#Uses nltk's named entity recognition in order to return a list of proper nouns extracted from the text
#Default label values "PERSON", "ORGANIZATION". "LOCATION", "DATE", "FACILITY", "GPE"

def entities(tuples, *labels):
    chunky = nltk.ne_chunk(tuples)
    entities = []
    if "PER" in labels:
        entities.extend([' '.join([y[0] for y in chunk.leaves()]) for chunk in chunky.subtrees() if chunk.label() == "PERSON"])
    if "ORG" in labels:
        entities.extend([' '.join([y[0] for y in chunk.leaves()]) for chunk in chunky.subtrees() if chunk.label() == "ORGANIZATION"])
    if "LOC" in labels:
        entities.extend([' '.join([y[0] for y in chunk.leaves()]) for chunk in chunky.subtrees() if chunk.label() == "LOCATION"])
    if "DAT" in labels:
        entities.extend([' '.join([y[0] for y in chunk.leaves()]) for chunk in chunky.subtrees() if chunk.label() == "DATE"])
    if "FAC" in labels:
        entities.extend([' '.join([y[0] for y in chunk.leaves()]) for chunk in chunky.subtrees() if chunk.label() == "FACILITY"])
    if "GPE" in labels:
        entities.extend([' '.join([y[0] for y in chunk.leaves()]) for chunk in chunky.subtrees() if chunk.label() == "GPE"])
    print(entities)
    count = collections.Counter(entities)
    return sorted(entities, key=count.get, reverse=True)

#Extracts any verbs from a PoS tagged list of words. Verbs that do not convey an emotion are ignored in a manual list, such as the verb to be. Returns
#a list of tuples sorted in by number of occurences. (x,y) y being number of occurences.

def verbs(tuples):
    ignored = ['is', 'am', 'are', 'was', 'were', 'be', 'being', 'been', 'would', 'will', 'go', 'going', 'goes', 'has', 'have', 'went']
    verbs = [tuple[0] for tuple in tuples if tuple[1] == 'VERB' and tuple[0] not in ignored]
    count = collections.Counter(verbs)
    return sorted(count.items(), key=lambda x: x[1], reverse=True) #sorted in descending order of number of occurences

#Stems a word to remove any suffix, such as -ing

def stem(word):
    word = tuple_check(word)
    stemmed = stemmer.stem(word)
    return stemmed

#Stems a tokenized list of words

def stems(tokenized):
    stems = []
    for word in tokenized:
        stemmed = stem(word)
        stems.append(stemmed)
    return stems

#Extracts any adjectives from a PoS tagged list of words. Adjectives that convey multiplicity are ignored. Returns
#a list of tuples sorted in by number of occurences. (x,y) y being number of occurences.

def adjectives(tuples):
    ignored = ['very', 'many', 'much', 'all', 'another', 'any', 'both', 'each', 'entire', 'every', 'few', 'first', 'likely', 'last', 'many', 'only', 'other', 'our', 'same', 'single', 'some', 'second', 'that', 'these', 'those', 'total', 'used', 'valid', 'which', 'whole', ]
    adjectives = [tuple[0] for tuple in tuples if tuple[1] == 'ADJ' and stem(tuple[0]) not in ignored and tuple[0] not in ignored]
    count = collections.Counter(adjectives)
    return sorted(count.items(), key=lambda x: x[1], reverse=True)

#Queries the word2vec model, trained on album reviews (reviews.py). Accepts a tokenized list of words.

def similarWords(tokenized):
    for word in tokenized:
        model = model()
        word = tuple_check(word)
        try:
            similar = model.most_similar(positive=[word, 'music'])
            print('\n' + word + str(similar))
        except KeyError:
            continue

#Queries a document/list of sentences, for words which appear multiple times. Returns a list of tuples (x,y) with y being number of occurences

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

#Creates reference to first element of tuple, if parameterised object is tuple

def tuple_check(word):
    if type(word) is tuple:
        return word[0]
    else:
        return word

def ordered_set_of_tags(words):
    set_words = []
    lower_words = []
    for word in words:
        if word.lower() not in lower_words:
            lower_words.append(word.lower())
            set_words.append(word)
    return set_words