"""
This small script will parse a flat file of JSON from Twitter feed
And it will evaluate the users' locations and the sentiments of their
tweets. This script is graded on an autograder and does not have internet
access so I will simply use the users' registered locations rather
than encoded twitter lat/long and a third party service/module to
get US states from them.
Parameter Files: 
    Sentiment file (space delimimted)
    Twitter Tweets (raw json, no upfront cleansing)
"""
import sys
import json
import string
import operator

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

def extract_text(twitter_dict):
    #this function gets the text of a given tweet
    #Cleansing applied: lower-cased and punctuation removed
    try:
        raw_string = twitter_dict.get('text','').encode('ascii','ignore')
        raw_string = raw_string.translate(None, string.punctuation)
        raw_string = raw_string.lower()
        return raw_string
    except:
        return ''
        
def get_location(twitter_dict, state_abbr_dict, states_tuple):
    #this function gets the location of a twitter user.
    #cleansing rules: take only values with the final four
    #characters ", XX" Where XX is a known US State/territory
    #if no state is found, scrub for a state's long name
    try:
        raw_string = twitter_dict.get('user','').get('location').encode('ascii','ignore')
        raw_string = raw_string.upper()
        if raw_string.endswith(states_tuple):
            return raw_string[-2:]
        else:
            return ''
    except:
        return ''
	
def get_tweet_score(tweet,scores_dict):
    tweet_score=0
    if isinstance(tweet,basestring):
        for word in tweet.split(' '):   
            tweet_score += int(scores_dict.get(word,0))
    return tweet_score

def wish_i_had_numpy(num,div):
    #return 0 if you get
    #divide by zero error
    try:
        res = float(num)/div
        return res
    except:
        return 0

def get_states():
    """returns Tuple of...
       {Abbr: State_Name} Dict
       {State Name:Abbr} Dict
       (', Abbr') Tuple
       {State_Abbr:0} Dict
    """
    state_abbr_dict = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'}
    #since python tuples are immutable,
    #create a list firsts then convert to tuple at the endswith
    state_abbr_list = []
    state_abbr_num_dict = {}
    for key in state_abbr_dict:
        state_abbr_list.append(', ' + key)
        state_abbr_num_dict[key] = 0
    return (state_abbr_dict, tuple(state_abbr_list), state_abbr_num_dict)
    

def main():
    scores_dict = create_sentiment_dict(sys.argv[1])
    datafile = open(sys.argv[2])
    state_abbr_dict, states_tuple, state_scores_dict = get_states()
    state_counts_dict = state_scores_dict.copy()
    for line in datafile:
        j = json.loads(line)
        tweet = extract_text(j)
        tweet_location = get_location(j, state_abbr_dict, states_tuple)
        tweet_sentiment_score = get_tweet_score(tweet,scores_dict)
        if tweet_location <> '':
            state_counts_dict[tweet_location] += 1
            state_scores_dict[tweet_location] += tweet_sentiment_score
    #print scores to stdout
    state_avgs = {}
    for key in state_counts_dict:
        state_avgs[key] = wish_i_had_numpy(state_scores_dict[key], state_counts_dict[key])
    
    top_state = dict(sorted(state_avgs.iteritems(), key=operator.itemgetter(1), reverse=True)[:1])
    for key in top_state:
        print key

if __name__ == '__main__':
    main()
