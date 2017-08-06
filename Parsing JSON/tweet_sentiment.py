import sys
import json
import re
import string

def create_sentiment_dict(pFile):
    """This will return a dictionary
    of words:sentiment scores"""
    snt_file = open(pFile)
    snt_dict = {}
    """Loop through tab delimited file"""
    for line in snt_file:
        word, score = line.split("\t")
        snt_dict[word] = int(score)
    return snt_dict

def extract_text(somedict):
    try:
        raw_string = somedict.get('text','').encode('ascii','ignore')
        raw_string = raw_string.translate(None, string.punctuation)
        raw_string = raw_string.lower()
        return raw_string
    except:
        return ''
	
def get_tweet_score(tweet,scores_dict):
    tweet_score=0
    if isinstance(tweet,basestring):
        for word in tweet.split(' '):   
            tweet_score += int(scores_dict.get(word,0))
    return tweet_score

def main():
    scores_dict = create_sentiment_dict(sys.argv[1])
    datafile = open(sys.argv[2])
    for line in datafile:
        j = json.loads(line)
        tweet = extract_text(j)
        #print score to stdout
        print(get_tweet_score(tweet,scores_dict))
        
        

if __name__ == '__main__':
    main()
