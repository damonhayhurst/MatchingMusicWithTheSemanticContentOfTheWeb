__author__ = 'Damon Hayhurst'

from boilerpipe.extract import Extractor
from bs4 import BeautifulSoup
import urllib3


class MyParser:

    def __init__(self, url):
        self.url = url
        http = urllib3.PoolManager()
        page = http.request('GET', url) #retrieve content from html
        self.source = page.data
        self.soup = BeautifulSoup(self.source)
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

