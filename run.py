from my_parser import MyParser
from aro_lookup import AroLookup
from api_calls import tagSearch
import semantics
import sys

genresUrl = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_terms.txt'
testUrl = 'http://www.bbc.com/news/technology-31552029'
testSentence = "This is an ultimate, to beat Chelsea, who I think will go on and win the Champion's League - it really is."

lookup = AroLookup()
tag_dict = {}


def main(url):
    parser = MyParser(url)
    text = parser.bpArtGetText()
    print(text)
    pos_tagged = semantics.text_to_pos_tags(text)
    entities = semantics.entities(pos_tagged, "PERSON", "ORGANIZATION", "LOCATION", "DATE", "FACILITY", "GPE")
    entities = semantics.ordered_set_of_tags(entities)
    adjectives = semantics.adjectives(pos_tagged)
    adjectives = semantics.ordered_set_of_tags(adjectives)
    for tag in entities and adjectives:
        print(tag)
    for ent in entities:
        tag_dict[ent] = "ENT"
    print(entities)
    for adj in adjectives:
        tag_dict[adj] = "ADJ"
    print(adjectives)
    mean_arousal = lookup.mean(pos_tagged)
    print(mean_arousal)






if __name__ == '__main__':
    main(sys.argv[1])
