from csv import DictReader
from semantics import stem, tuple_check

__author__ = 'Damon Hayhurst'

class AroLookup():

    def __init__(self, filter_bounds = [40, 60]):
        emo_file = 'emo_file.txt'
        self.lookup = self.read_arousal(emo_file)
        low_percent_bound = filter_bounds[0]
        high_percent_bound = filter_bounds[1]
        self.lookup = self.filter_lookup(self.lookup, low_percent_bound, high_percent_bound)

    def read_arousal(self, file):
        file = open(self.file, 'r')
        file_reader = DictReader(file, delimiter='\t')
        lookup = {}
        for row in file_reader:
            lookup.update({row['Word']: float(row['AroMn'])})
        return lookup

    def filter_lookup(self, lookup, low_percent_bound, high_percent_bound):
        lookup_list = lookup.items()
        sorted_lookup_list = sorted(lookup_list, key=lambda x: x[1])
        total = len(sorted_lookup_list)
        percent = int(total / 100)
        mid_low = int(low_percent_bound * percent)
        mid_high = int(high_percent_bound * percent)
        count = 0
        #print(total)
        for tuple in sorted_lookup_list:
            if mid_low < count < mid_high:
                del lookup[tuple[0]]
            count += 1
        #print(len(lookup.items()))
        return lookup

    def mean(self, tokenized):
        total = 0
        count = 0
        lookup = self.lookup
        for word in tokenized:
            if word in lookup:
                total += lookup[word]
                count += 1
            elif stem(word) in lookup:
                total += lookup[word]
                count += 1
            else:
                continue
        return total / count

    def get_words(self, tokenized):
        word_list = []
        lookup = self.lookup
        for word in tokenized:
            word = tuple_check(word)
            if word in lookup:
                word_list.append((word, lookup[word]))
            elif stem(word) in lookup:
                word_list.append((stem(word), lookup[stem(word)]))
            else:
                continue
        tuples = sorted(word_list, key=lambda x: x[1], reverse=True)
        return tuples