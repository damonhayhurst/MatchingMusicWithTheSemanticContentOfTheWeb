import pylast
import urllib
import requests

echoKey =
lastKey = 
lastSecret =
lastUser =
lastPass = 

#code from getgenres.py by nickjevershed, url: https://gist.github.com/nickjevershed/8589517

def getEnTerms3(artist):

    #Echonest API call

    baseURL = 'http://developer.echonest.com/api/v4/artist/terms?api_key='
    #EchoNest API key
    searchQuery = baseURL + echoKey + '&name=' + urllib.quote_plus(artist) + '&format=json'
    searchSong = requests.get(searchQuery)
    enTerms = searchSong.json()

    if enTerms['response']['status']['message'] == 'Success':

        try:
            term1 = enTerms['response']['terms'][0]['name']
        except:
            term1 = "na"

        try:
            term2 = enTerms['response']['terms'][1]['name']
        except:
            term2 = "na"

        try:
            term3 = enTerms['response']['terms'][2]['name']
        except:
            term3 = "na"
    else:
        term1 = "na"
        term2 = "na"
        term3 = "na"

    return {'term1':term1,'term2':term2,'term3':term3}


def getEnSongs(artist, energy):
    maxE = 1.0
    minE = 0.0
    results = 100
    baseUrl = 'http://developer.echonest.com/api/v4/song/search?api_key='
    searchQuery = baseUrl + echoKey + '&artist=' + artist + '&results=' + str(results) + '&song_type=live:false^2' + '&max_energy=' + str(maxE) + '&min_energy=' + str(minE) + '&bucket=song_type' + '&format=json'
    searchSongs = requests.get(searchQuery)
    enSongs = searchSongs.json()
    songs = []

    if enSongs['response']['status']['message'] == 'Success':

        size = len(enSongs['response']['songs'])

        for x in range(0, size-1):
            songs.append(enSongs['response']['songs'][x]['title'])



    else:

        print('na')


    return songs

def getEnTerms(artist):

    #Echonest API call
    baseURL = 'http://developer.echonest.com/api/v4/artist/terms?api_key='
    searchQuery = baseURL + echoKey + '&name=' + urllib.quote_plus(artist) + '&results=' + results + '&format=json'
    searchSong = requests.get(searchQuery)
    enTerms = searchSong.json()
    terms = []

    if enTerms['response']['status']['message'] == 'Success':

        size = len(enTerms['response']['terms'])

        for x in xrange(0, size-1):
            terms.append(enTerms['response']['terms'][x]['name'])



    else:

        terms[0] = 'na'


    return terms

def getTracks(artist):
    network = pylast.LastFMNetwork(api_key=lastKey, api_secret=lastSecret, username = lastUser, password_hash = lastPass)
    tracks = []
    artistLF = network.get_artist(artist)
    tracks = artistLF.get_top_tracks()
    return tracks


def getLastFM(artist, song):

    network = pylast.LastFMNetwork(api_key = lastKey, api_secret = lastSecret, username = lastUser, password_hash = lastPass)
    tags = []

    try:
        track = network.get_track(artist, song)
        topItems = track.get_top_tags(limit=50)
        size = len(topItems)

        if len(topItems) > 0:
            for x in xrange(0, size-1):
                tags.append(topItems[x].item.get_name())

        else:
            tags[0] = 'na'


        return tags

    except:
        print("last fm call failed")
        return {'na'}

#Formats a Google Search Url for internal search of Last.Fm. The site is queried with multiple tags.

def tagSearch(*tags):
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='
    query = 'site:last.fm%2Fmusic+intitle:"tags+for"'
    for tag in tags:
        tag = '+' + '"' + tag + '"'
        query += tag
    url = url + query
    return str(url)
