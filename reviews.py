from gensim.models import word2vec
import logging
import csv
from semantics import tokenize, remove_stops
import nltk.data
import my_parser

_author_ = 'Damon Hayhurst'

reviews = "pitchfork-reviews.csv"
review_sent = "artSentences.txt"
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
model_path = "rModel"
model = word2vec.Word2Vec.load(model_path)


def read_reviews():
    file = open(reviews, 'r')
    reader = csv.DictReader(file)
    return reader


def scrape_reviews(reader):
    count = 0
    for row in reader:
        url = row['url']
        parser = parser(url)
        article = parser.getEditorial()
        article = article.getText()
        article += article.replace(row['artist'], "ARTIST")
        output = open(review_sent, 'w')
        # print(reviewSent, file=output)
        print(article)
        count += 1
        print("%d/6886" % count)
    output.close()


def line_sentences(sentences):
    output = open(review_sent, 'w')
    for sentence in sentences:
        # print("%s\n" % sentence, file=output)
        print("%s\n" % sentence)
    output.close()

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


def save_model(sentences_file):
    sentences = Sentences(sentences_file)
    model = word2vec.Word2Vec(sentences, size=20, workers=2, min_count=50, sample=1e-5)
    model.save(model_path)



