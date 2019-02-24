import urllib2
import re
import csv

''' Dictionary that contains all information to be written to a csv file. '''
data = {}

'''
Dictionary with Drake's albums as keys and songs in that album as values.
The song names are formatted in a way that's consistent with the genius url
for that song
'''
songdict = {'So Far Gone': ['houstatlantavegas', 'successful', 'best-i-ever-had',
                            'uptown', 'im-goin-in', 'the-calm', 'fear'],
            'Thank Me Later': ['fireworks', 'karaoke', 'the-resistance',
                               'over', 'show-me-a-good-time', 'up-all-night',
                               'fancy', 'shut-it-down', 'unforgettable',
                               'light-up', 'miss-me', 'ceces-interlude',
                               'find-your-love', 'thank-me-now'],
            'Take Care': ['over-my-dead-body', 'shot-for-me', 'headlines',
                          'crew-love', 'take-care', 'marvins-room',
                          'buried-alive-interlude', 'under-ground-kings',
                          'well-be-fine', 'make-me-proud', 'lord-knows',
                          'cameras', 'doing-it-wrong', 'the-real-her',
                          'look-what-youve-done', 'hyfr', 'practice',
                          'the-ride', 'the-motto'],
            'Nothing Was The Same': ['tuscan-leather', 'furthest-thing',
                                     'started-from-the-bottom', 'wu-tang-forever',
                                     'own-it', 'worst-behavior', 'from-time',
                                     'hold-on-were-going-home', 'connect',
                                     'the-language', '305-to-my-city', 'too-much',
                                     'pound-cake-paris-morton-music-2',
                                     'come-thru', 'all-me'],
            'If You\'re Reading This It\'s Too Late': ['legend', 'energy',
                                                       '10-bands', 'know-yourself',
                                                       'no-tellin', 'madonna',
                                                       '6-god', 'star67', 'preach',
                                                       'wednesday-night-interlude',
                                                       'used-to', '6-man',
                                                       'now-and-forever', 'company',
                                                       'you-and-the-6', 'jungle',
                                                       '6pm-in-new-york'],
            'What A Time To Be Alive': ['and-future-digital-dash',
                                        'and-future-big-rings',
                                        'and-future-live-from-the-gutter',
                                        'and-future-diamonds-dancing',
                                        'and-future-scholarships',
                                        'and-future-plastic-bag',
                                        'and-future-im-the-plug',
                                        'and-future-change-locations',
                                        'and-future-jumpman', 'and-future-jersey',
                                        'and-future-30-for-30-freestyle'],
            'Views': ['keep-the-family-close', '9', 'u-with-me', 'feel-no-ways',
                      'hype', 'weston-road-flows', 'redemption', 'with-you',
                      'faithful', 'still-here', 'controlla', 'one-dance', 'grammys',
                      'childs-play', 'pop-style', 'too-good', 'summers-over-interlude',
                      'fire-and-desire', 'views', 'hotline-bling'],
            'More Life': ['free-smoke', 'no-long-talk', 'passionfruit',
                          'jorja-interlude', 'get-it-together', 'madiba-riddim',
                          'blem', '4422', 'gyalchester', 'skepta-interlude',
                          'portland', 'sacrifices', 'nothings-into-somethings',
                          'teenage-fever', 'kmt', 'lose-you',
                          'cant-have-everything', 'glow', 'since-way-back',
                          'fake-love', 'ice-melts', 'do-not-disturb'],
            'Scorpion B': ['peak', 'summer-games', 'jaded', 'nice-for-what',
                           'finesse', 'ratchet-happy-birthday', 'thats-how-you-feel',
                           'blue-tint', 'in-my-feelings', 'dont-matter-to-me',
                           'after-dark', 'final-fantasy', 'march-14'],
            'Scorpion A': ['survival', 'nonstop', 'elevate', 'emotionless',
                           'gods-plan', 'im-upset', '8-out-of-10', 'mob-ties',
                           'cant-take-a-joke', 'sandras-rose', 'talk-up',
                           'is-there-more']}

''' Words chosen to be ignored when creating a word frequency dictionary. '''
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
             "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
             "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
             "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
             "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
             "being", "have", "has", "had", "having", "do", "does", "did", "doing",
             "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
             "while", "of", "at", "by", "for", "with", "about", "against", "between",
             "into", "through", "during", "before", "after", "above", "below", "to",
             "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
             "further", "then", "once", "here", "there", "when", "where", "why", "how",
             "all", "any", "both", "each", "few", "more", "most", "other", "some",
             "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
             "very", "can", "will", "just", "dont", "should", "now"]

'''
Dictionary with song names as keys and Spotify plays, duration of song,
and binary indicator of whether the song is explicit or not as values.
'''
stats = {'houstatlantavegas': [18326460, 290, 1], 'successful': [25909079, 352, 1],
         'best-i-ever-had': [156391937, 258, 1], 'uptown': [23870145, 381, 1],
         'im-goin-in': [43785506, 225, 1], 'the-calm': [8186271, 246, 1],
         'fear': [15212814, 281, 1], 'fireworks': [25231337, 313, 1], 'karaoke': [16060829, 228, 0],
         'the-resistance': [21815228, 225, 1], 'over': [78784512, 234, 1],
         'show-me-a-good-time': [26548810, 210, 1], 'up-all-night': [79701984, 234, 1],
         'fancy': [34531835, 319, 1], 'shut-it-down': [33194793, 419, 1],
         'unforgettable': [22813752, 214, 1], 'light-up': [17096112, 274, 1],
         'miss-me': [36272231, 306, 1], 'ceces-interlude': [10242737, 154, 0],
         'find-your-love': [58761724, 209, 0], 'thank-me-now': [22642519, 329, 1],
         'over-my-dead-body': [61963848, 273, 1], 'shot-for-me': [99905067, 225, 1],
         'headlines': [216878305, 236, 1], 'crew-love': [141399152, 209, 1],
         'take-care': [251893511, 273, 1], 'marvins-room': [212697266, 347, 1],
         'buried-alive-interlude': [34887446, 151, 1], 'under-ground-kings': [54409386, 213, 1],
         'well-be-fine': [46529978, 248, 1], 'make-me-proud': [120248309, 220, 1],
         'lord-knows': [35859102, 308, 1], 'cameras': [44397724, 435, 1],
         'doing-it-wrong': [81803835, 245, 1], 'the-real-her': [43888196,  321, 1],
         'look-what-youve-done': [41442718, 302, 1], 'hyfr': [132216435, 207, 1],
         'practice': [77004118, 238, 1], 'the-ride': [27226037, 351, 1],
         'the-motto': [203056768, 182, 1], 'tuscan-leather': [59095077, 306, 0],
         'furthest-thing': [85543191, 287, 1], 'started-from-the-bottom': [241806922, 174, 1],
         'wu-tang-forever': [73829464, 218, 1], 'own-it': [76910875, 252, 1],
         'worst-behavior': [104001747, 270, 1], 'from-time': [169040334, 322, 1],
         'hold-on-were-going-home': [427292782, 228, 1], 'connect': [53758681, 296, 0],
         'the-language': [101909959, 224, 1], '305-to-my-city': [48081706, 256, 1],
         'too-much': [97001502, 262, 1], 'pound-cake-paris-morton-music-2': [108694523, 433, 1],
         'come-thru': [66229521, 236, 1], 'all-me': [202453782, 271, 1],
         'legend': [243588375, 242, 1], 'energy': [267928900, 182, 1],
         '10-bands': [180257154, 178, 1], 'know-yourself': [238989378, 276, 1],
         'no-tellin': [96752701, 311, 1], 'madonna': [59415325, 178, 1],
         '6-god': [106732054, 181, 1], 'star67': [70047283, 296, 1],
         'preach': [84394488, 237, 1], 'wednesday-night-interlude': [49742611, 212, 1],
         'used-to': [70733931, 268, 1], '6-man': [74336521, 168, 1],
         'now-and-forever': [70866760, 281, 1],
         'company': [64129329, 253, 1], 'you-and-the-6': [50747858, 265, 1],
         'jungle': [130100824, 320, 1], '6pm-in-new-york': [41227801, 283, 1],
         'and-future-digital-dash': [76566383, 231, 1], 'and-future-big-rings': [165329967, 218, 1],
         'and-future-live-from-the-gutter': [72042186, 212, 1],
         'and-future-diamonds-dancing': [104043998, 315, 1],
         'and-future-scholarships': [76445023, 209, 1],
         'and-future-plastic-bag': [58891812, 202, 1],
         'and-future-im-the-plug': [59996107, 180, 1],
         'and-future-change-locations': [59690860, 221, 1],
         'and-future-jumpman': [526694212, 206, 1], 'and-future-jersey': [66999845, 189, 1],
         'and-future-30-for-30-freestyle': [38815834, 254, 1],
         'keep-the-family-close': [60522626, 329, 1], '9': [85618142, 256, 1],
         'u-with-me': [75325528, 297, 1], 'feel-no-ways': [116960777, 241, 1],
         'hype': [120931606, 209, 1], 'weston-road-flows': [62995808, 254, 1],
         'redemption': [88599470, 334, 1], 'with-you': [122987244, 195, 1],
         'faithful': [61263568, 290, 1], 'still-here': [181940608, 190, 1],
         'controlla': [506354966, 245, 1], 'one-dance': [1586696075, 174, 0],
         'grammys': [118190841, 280, 1], 'childs-play': [158652561, 241, 1],
         'pop-style': [265912291, 233, 1], 'too-good': [693625202, 263, 1],
         'summers-over-interlude': [43361980, 106, 1], 'fire-and-desire': [120167651, 138, 1],
         'views': [56883809, 312, 1], 'hotline-bling': [766742156, 267, 1],
         'free-smoke': [123998370, 219, 1], 'no-long-talk': [88278950, 150, 1],
         'passionfruit': [584919518, 299, 1], 'jorja-interlude': [73253253, 168, 1],
         'get-it-together': [113017553, 250, 1], 'madiba-riddim': [91934606, 205, 0],
         'blem': [156923340, 217, 0], '4422': [82124888, 186, 0],
         'gyalchester': [216465651, 189, 1],
         'skepta-interlude': [55865888, 143, 1], 'portland': [308093495, 237, 1],
         'sacrifices': [92762820, 308, 1], 'nothings-into-somethings': [53705905, 154, 0],
         'teenage-fever': [170190155, 220, 1], 'kmt': [105452877, 163, 1],
         'lose-you': [50741104, 305, 1], 'cant-have-everything': [59829099, 228, 1],
         'glow': [53516686, 206, 1], 'since-way-back': [49226022, 368, 0],
         'fake-love': [293166379, 211, 1], 'ice-melts': [74721074, 251, 1],
         'do-not-disturb': [138430512, 284, 1], 'peak': [41819013, 206, 1],
         'summer-games': [51420680, 248, 0], 'jaded': [48576653, 262, 1],
         'nice-for-what': [545129698, 211, 1], 'finesse': [47899509, 182, 0],
         'ratchet-happy-birthday': [34958925, 207, 1], 'thats-how-you-feel': [46923264, 158, 1],
         'blue-tint': [56903209, 163, 1], 'in-my-feelings': [645696513, 218, 1],
         'dont-matter-to-me': [229154699, 246, 0], 'after-dark': [52000292, 290, 1],
         'final-fantasy': [31757806, 220, 1], 'march-14': [30076071, 310, 1],
         'survival': [63300529, 136, 1], 'nonstop': [293889114, 239, 1],
         'elevate': [77574969, 185, 1], 'emotionless': [84441837, 302, 1],
         'gods-plan': [1092848186, 299, 1], 'im-upset': [199241748, 214, 1],
         '8-out-of-10': [62127410, 196, 1], 'mob-ties': [122923810, 205, 1],
         'cant-take-a-joke': [74232844, 164, 1], 'sandras-rose': [50147558, 216, 1],
         'talk-up': [57385371, 223, 1], 'is-there-more': [37178759, 227, 1]}

''' Dictionary with album name as key and release year as value. '''
releasedOn = {"Thank Me Later": 2010, "Take Care": 2011, "Nothing Was The Same": 2013,
              "Views": 2016, "Scorpion A": 2018, "Scorpion B": 2018, "More Life": 2017,
              "What A Time To Be Alive": 2015, "If You\'re Reading This It\'s Too Late": 2015,
              "So Far Gone": 2009}

'''
Parses HTML from Genius URL's and returns text with removed non-alphanumeric
characters.
'''


def parseHTMLforLyrics(pageContents):
    startAt = pageContents.find("<p>")
    endAt = pageContents.find("</p>", startAt + 3)
    pageContents = pageContents[startAt: endAt]

    ignore = 0
    text = ''

    for char in pageContents:
        if char == '<' or char == '[':
            ignore = 1
        elif (ignore == 1 and (char == '>' or char == ']')):
            ignore = 0
        elif ignore == 1:
            continue
        else:
            text += char

    removeNL = text.replace('\n', ' ').lower()
    removeNL.split(" ")
    removeNonAlphaNum = re.sub(r'[^a-zA-Z\ ]', "", removeNL)
    return removeNonAlphaNum.split()


'''
Create a frequency dictionary given an array of strings.
'''


def textToFreqDict(wordArr):
    wordfreq = [wordArr.count(p) for p in wordArr]
    freqdict = dict(zip(wordArr, wordfreq))
    return freqdict


''' Create a frequency dictionary given a url.'''


def URLtoFreqDict(url):
    request = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    response = urllib2.urlopen(request)
    html = response.read()
    wordArr = parseHTMLforLyrics(html)
    return textToFreqDict(wordArr)


'''
Creates a word frequency dictionary for each song in each album and:
1. adds the word count for each song to the stats dictionary
2. adds the word frequency to a metadata dictionary in order to retrieve the top
   15 most frequent words.
'''


def getTop15():
    metadata = {}
    for albums, songs in songdict.iteritems():
        for i in range(len(songs)):
            url = 'https://genius.com/Drake-'+songs[i]+'-lyrics'
            print(songs[i])  # keeps track of progress
            freqDict = URLtoFreqDict(url)
            totalWords = 0
            for key, value in freqDict.iteritems():
                totalWords += value
            stats[songs[i]].append(totalWords)
            for key, value in freqDict.iteritems():
                if key in metadata:
                    metadata[key] += value
                else:
                    metadata[key] = value

    filtered = removeStopWords(metadata)
    tuples = [(filtered[key], key) for key in filtered]
    tuples.sort()
    tuples.reverse()
    words = [tuple[1] for tuple in tuples]
    return words[: 15]


''' This method removes all stopwords from a given word frequency dictionary.
    Could not use the 'not in' operator for some reason.'''


def removeStopWords(wordDict):
    stopwordDict = dict(zip(stopwords, stopwords))
    for key, stopword in stopwordDict.iteritems():
        if stopword in wordDict:
            del wordDict[stopword]
    return wordDict


'''
Populates the rows of our data dictionary in order to later create a csv file.
Rows are populated first with release date, and then the 15 most frequent words
from each song are retrieved. Given these words, their word frequency is recorded
in the data dictionary.
'''


def populateRows():
    addYears()
    print(mostFreq)
    for albums, songs in songdict.iteritems():
        for i in range(len(songs)):
            data[songs[i]] = []
            url = 'https://genius.com/Drake-'+songs[i]+'-lyrics'
            print(songs[i])
            freqDict = URLtoFreqDict(url)
            data[songs[i]].append(albums)
            for word in mostFreq:
                if word in freqDict:
                    data[songs[i]].append(freqDict[word])
                else:
                    data[songs[i]].append(0)
    for songs, info in stats.iteritems():
        for j in range(len(info)):
            data[songs].append(info[j])


''' Adds the released years to the stats dictionary.'''


def addYears():
    for albums, songs in songdict.iteritems():
        for i in range(len(songs)):
            stats[songs[i]].append(releasedOn[albums])


'''
After populating the data dictionary, this method creates a csv file that records
all the elements in 'myFields' as columns and their corresponding data for each
song.
'''


def makeCSV():
    populateRows()
    myFile = open('unfiltered.csv', 'w')
    with myFile:
        myFields = ['song', 'album']
        myFields.extend(mostFreq)
        myFields.extend(['spotifyPlays', 'duration', 'explicit', 'wordCount', 'yearReleased'])
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writeheader()
        for songs, songAttributes in data.iteritems():
            row = {}
            row[myFields[0]] = songs
            for i in range(len(songAttributes)):
                print(i)
                print(myFields[i])
                row[myFields[i+1]] = songAttributes[i]
            writer.writerow(row)


mostFreq = getTop15()
makeCSV()
