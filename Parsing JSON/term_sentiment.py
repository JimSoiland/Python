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

def get_avg_score(score, num_words):
    if score == 0:
        return 0
    else:
        return score/num_words

def main():
    scores_dict = create_sentiment_dict(sys.argv[1])
    datafile = open(sys.argv[2])
    unknown_dict_values = {}
    unknown_dict_counts = {}
    #create an empty data frame and load it up with
    #the contents of the datafile
    for line in datafile:
        j = json.loads(line)
        tweet = extract_text(j)
        tweet_score = get_tweet_score(tweet,scores_dict)
        tweet_words = float(len(tweet.split()))
        avg_term_score = get_avg_score(tweet_score, tweet_words)
        
        #iterate through the words in the string
        for word in tweet.split():
            if word not in scores_dict:
                if word in unknown_dict_values:
                    unknown_dict_values[word] += avg_term_score
                    unknown_dict_counts[word] += 1
                else:
                    unknown_dict_values[word] = avg_term_score
                    unknown_dict_counts[word] = 1
    
    #iterate through dict of unknown words
    for key in sorted(unknown_dict_values.iterkeys()):
        this_count = unknown_dict_counts[key]
        this_value = unknown_dict_values[key]
        print "{} {}".format(key, float(this_value)/this_count)
        
if __name__ == '__main__':
    main()
