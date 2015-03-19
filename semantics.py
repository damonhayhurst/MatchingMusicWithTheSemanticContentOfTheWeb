__author__ = 'Damon Hayhurst'
from __future__ import division
import nltk
from nltk.corpus import stopwords


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


genresUrl = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_terms.txt';
testUrl = 'http://www.bbc.co.uk/sport/0/football/30970439'
testSentence = 'This is an ultimate, to beat Chelsea, who I think will go on and win the Champions League - it really is.'

# print(verbs(tuples)) 
