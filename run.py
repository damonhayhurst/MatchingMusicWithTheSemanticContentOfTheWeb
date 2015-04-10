from my_parser import MyParser
from aro_lookup import AroLookup
import semantics, api_calls
import sys

genresUrl = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_terms.txt'
testUrl = 'http://www.bbc.com/news/technology-31552029'
testSentence = "This is an ultimate, to beat Chelsea, who I think will go on and win the Champion's League - it really is."

lookup = AroLookup()

def main(url):
    parser = MyParser(url)




if __name__ == '__main__':
    main(sys.argv[1])
