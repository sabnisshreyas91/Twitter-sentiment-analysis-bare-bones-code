
import tweepy
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
print('imported necessary libraries')
print('')

query='' #The topic you are looking to extract tweets about.
print('search query is : {}'.format(query))
rows=0 #enter value
print('number of tweets being pulled : {}'.format(rows))
ckey = ''
csecret = ''
atoken = ''
asecret = ''
relevant_words=[] #searching for tweets by key word can result in unrelated tweets containing the search term. This list of words can be used to filter out such noise.
print('tweet should have atleast one of the following words : {}'.format(relevant_words))
print('')

OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)

list_of_tweets=list()
row_list=list()
tweets = tweepy.Cursor(api.search, q=query,lang='en',geocode='12.972442,77.580643,30km').items(rows) #Co-ordinates of Bangalore. So tweets within a 30 km radius of the co-ordinates will be collected.
	  
for tweet in tweets:
    flg=0
    for word in relevant_words:
        if(word in tweet.text):
            flg=1 #filters out unrelated tweets that may still contain the query keyword
    if(flg>0):
        clean_tweet=' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet.text).split()) #strips the tweet of any special characters, link etc.
        row_list=[tweet.created_at,clean_tweet,TextBlob(clean_tweet).sentiment.polarity] # Assigns polarity to tweet. Values range from -1 to +1
        list_of_tweets.append(row_list)
print('checked tweets for relevancy, removed special characters from tweets')
print('')
gst_df=pd.DataFrame(data=list_of_tweets,columns=['date','tweet','polarity'])
print('tweets loaded to dataframe')
print('')
gst_df['date']=pd.to_datetime(gst_df['date'])

