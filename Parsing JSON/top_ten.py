"""
This small script will parse a flat file of JSON from Twitter feed
And it will Find the top ten tweets
Parameter Files: 
    Twitter Tweets (raw json, no upfront cleansing)
"""
import sys
import json
import string
import operator
  
def get_hashtags(twitter_dict, hash_dict):
    #get hashtags from twitter JSON
    try:
        for itm in twitter_dict.get('entities','').get('hashtags',''):
            raw_string = itm.get('text','').encode('ascii','ignore')
            raw_string = raw_string.upper()
            if raw_string in hash_dict:
                hash_dict[raw_string] += 1 
            else:
                hash_dict[raw_string] = 1
    except:
        pass
    return hash_dict

def main():
    datafile = open(sys.argv[1])
    hash_dict = {}
    for line in datafile:
        j = json.loads(line)
        hash_dict = get_hashtags(j, hash_dict)
        
    hash_dict.pop('',None)
    top_tweets = dict(sorted(hash_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    
    for key in top_tweets:
        print "{} {}".format(key, top_tweets[key])

if __name__ == '__main__':
    main()
