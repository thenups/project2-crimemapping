# Dependencies
import tweepy
import json
import numpy as np
import schedule
import time

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def social():
	# Twitter API Keys
	consumer_key = 'ibYsFmAdHS8fhnupeA3opTRHN'
	consumer_secret = 'cSfliluzlYkSJ8EPJEOvQA5kKG9BE6MG1ddF8kHAyNc5ZJ6601'
	access_token = '943311356534472704-3tToKzZ2RMDtNOo4frlY6IEAg6iWGL1'
	access_token_secret = '42jS6EeOwV5ZaWde0LwxpL4dPyozVt5rv3URu7ZlP9m17'

	# Setup Tweepy API Authentication
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

	# Search Term
	# search_term = input("what term do you want to search for? ")
	search_term = 'school shooting'

	# Search for 5 popular tweets
	# public_tweets = api.search(search_term, count=5, result_type='popular')
	# Search for 5 recent tweets
	public_tweets = api.search(search_term, count=5, result_type='recent')

	# View Search Object
	# print(public_tweets)

	compound_list = []
	positive_list = []
	negative_list = []
	neutral_list = []
	tweet_id = []
	tweet_text = []

	# Loop through all tweets
	for tweet in public_tweets["statuses"]:

		# Utilize JSON dumps to generate a pretty-printed json
    	# print(json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ': ')))
		tweet_id.append(tweet['id'])
		tweet_text.append(tweet["text"])
    
    	# Run Vader Analysis on each tweet
		compound = analyzer.polarity_scores(tweet['text'])["compound"]
		pos = analyzer.polarity_scores(tweet['text'])["pos"]
		neu = analyzer.polarity_scores(tweet['text'])["neu"]
		neg = analyzer.polarity_scores(tweet['text'])["neg"]

    	# Add each value to the appropriate array
		compound_list.append(compound)
		positive_list.append(pos)
		negative_list.append(neg)
		neutral_list.append(neu) 

	return tweet_id, tweet_text

	#print(tweet_text)
# Print the Averages
#print("")
#print("Compound: %s" % np.mean(compound_list))
#print("Positive: %s" % np.mean(positive_list))
#print("Neutral: %s" % np.mean(neutral_list))
#print("Negative: %s" % np.mean(negative_list))

schedule.every(.5).minutes.do(social)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(.5)
