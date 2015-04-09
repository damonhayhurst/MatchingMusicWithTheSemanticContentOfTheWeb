__author__ = 'Damon Hayhurst'

from boilerpipe.extract import Extractor
from bs4 import BeautifulSoup
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import urllib3
import json
import re


class MyParser:

    def __init__(self, url):
        http = urllib3.PoolManager()
        self.url = url
        page = http.request('GET', url) #retrieve content from html
        self.source = page.data
        self.soup = BeautifulSoup(self.source)
        self.result_count = None
        #BeautifulSoup - Html Parser http://www.crummy.com/software/BeautifulSoup/bs4/doc/
        self.text = self.soup.get_text()

    def getSoup(self):#return parsed html
        return self.soup

    def getText(self):#return plain text
        text = self.text
        return text

    def getTitle(self):#get header
        title_tag = self.soup.title
        return title_tag.contents

    # return all text contained in body tags
    def getBody(self):
        body_tag = self.soup.find_all("p")
        text = ""
        for child in body_tag:
            text += str(child.contents)
        return text

    def bpLargGetText(self):
        extractor = Extractor(extractor='LargestContentExtractor', url=self.url)
        extracted = extractor.getText()
        return extracted

    def bpArtGetText(self):
        extractor = Extractor(extractor='ArticleExtractor', url=self.url)
        extracted = extractor.getText()
        return extracted

    def getEditorial(self):
        soup = self.soup
        edit_tag = soup.find("div", {"class": "editorial"})
        return edit_tag

    def getSummary(self, num_sentences):
        lex_rank = LexRankSummarizer()
        text = str(self.bpLargGetText())
        parser = PlaintextParser.from_string(text, Tokenizer('english'))
        summary = lex_rank(parser.document, num_sentences)
        sentences = []
        for sent in summary:
            sentences.append(str(sent))
        return sentences


    def getUrls(self):
        text = self.getText()
        results = json.loads(text)
        url_results = results['responseData']['results']
        urls = []
        head = len('http://www.last.fm/music/')
        tail = len('/%2Btags')
        reg = re.compile('/')
        self.result_count = int(results['responseData']['cursor']['estimatedResultCount'])
        for result in url_results:
            url = result['url']
            url = url[head:-tail]
            url = url.replace('%2B', ' ')
            match = reg.search(url)
            if match is not None:
                slash = match.start()
                url = (url[:slash], url[(slash + 1):])
            else:
                url = (url, None)
            urls.append(url)
        return urls





