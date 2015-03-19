from gensim.models import word2vec
import logging
import csv
import os
import urllib3
import nltk.data
from bs4 import BeautifulSoup
import MyParser

_author_ = 'Damon Hayhurst'

reviews = "pitchfork-reviews.csv"
review_sent = "artSentences.txt"
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
model_path = "rModel"
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def read_reviews():
    file = open(reviews, 'r')
    reader = csv.DictReader(file)
    return reader

def scrape_reviews(reader):
    count = 0
    for row in reader:
        url = row['url']
        parser = MyParser(url)
        article = parser.getEditorial()
        article = article.getText()
        review_sent += article.replace(row['artist'], "ARTIST")
        output = open(review_sent, 'w')
        # 		print(reviewSent, file=output)
        print(review_sent)
        count += 1
        print("%d/6886" % count)
    output.close()

def sentenize(path):
    file = open(path, 'r')
    data = file.read()
    sentences = tokenizer.tokenize(data)
    file.close()
    return sentences

def line_sentences(sentences):
    output = open(review_sent, 'w')
    for sentence in sentences:
        # 		print("%s\n" % sentence, file=output)
        print("%s\n" % sentence)
    output.close()

class Sentences(object):

    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        file = open(self.dirname, 'r')
        for i, line in enumerate(file):
            line = line.lower()
            line = tokenize(line)
            line = removeStops(line)
            if line:
                print(line)
                yield line
        file.close()


def save_model(sentences_file):
    sentences = Sentences(sentences_file)
    model = word2vec.Word2Vec(sentences, size=20, workers=2, min_count=50, sample=1e-5)
    model.save(model_path)

def model():
    model = word2vec.Word2Vec.load(model_path)
    return model

save_model(review_sent)
# print(model()['music'])
