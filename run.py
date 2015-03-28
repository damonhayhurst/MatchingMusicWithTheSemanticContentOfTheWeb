import MyParser, semantics, api_calls, reviews

genresUrl = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_terms.txt'
testUrl = 'http://www.bbc.com/news/technology-31552029'
testSentence = "This is an ultimate, to beat Chelsea, who I think will go on and win the Champion's League - it really is."

parser = MyParser.MyParser(testUrl)
# tuples = preprocess(parser.getText(), True)
# reader = readEmoData()
# reader = nameVsArousal(reader)
# reader = sliceDict(reader)
#text = parser.bpLargGetText()
#text = tokenize(text)
#model = model()
#for word in text:
    #print(model[word])
# print(sorted(reader, key=reader.get))
# print(parser.getText())

# print(scoreWords(parser.bpGetText(), reader))

# tokenized = tokenize(parser.bpgetText())
#postagged = posTags(tokenized)
#entities = entities2(postagged)
#print(entities)
#artists = searchTags(entities)
#print(artists)
#songs = getEnSongs(artists[0], 0.3)
#print(songs)

text = parser.bpArtGetText()
tokenized = semantics.tokenize(text)
aro_score = semantics.lookup_arousal(tokenized)
print(aro_score)
