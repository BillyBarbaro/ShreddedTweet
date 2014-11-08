#! /usr/bin/python
import random
from twython import Twython
import time

# List of bad words so I don't accidentally tweet anything I'm calling people out for
badWords = ['damn', 'shit', 'fuck', 'bitch', 'ass', 'asshole', 'hell', 'goddamn', 'dammit']


# Searches for tweets using the bad word and returns the dictionary object containing a random one's information
def getTweet(searchWord):
	while True:
		# Queries for 30 tweets
		search = twitter.search(q=searchWord, count='30', lang='en')

		# Chooses a random one
		index = random.randint(0, len(search) - 1)
		result = search['statuses'][index]

		# Checks to make I'm not tweeting at anyone and that it doesn't have any bad words in it
		for entry in search['statuses']:
			if '@' not in entry['text']:
				if not any(word in entry for word in badWords):
					return entry

# Appends the given output to "report.txt"
def writeToReport(output):
	with open("ReportTweet.txt", "a") as myfile:
		myfile.write(output + '\n')


# All 4 keys were pulled from the developer page on Twitter's Website. Custom to account and allow us to authorize ourself to tweet
APP_KEY = 'APPKEY'
APP_SECRET = 'APPSECRET'

OAUTH_TOKEN = 'OAUTHTOKEN'
OAUTH_TOKEN_SECRET = 'OAUTHTOKENSECRET'

# Opens a connection with twitter and verifies the user
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Clears the reporting file and writes a message to indicate the start
f = open('ReportTweet.txt','w')
f.write("Beginning Tweets" + '\n')
f.close()

# Continuously loops through the script to tweet. Sleeps 15 minutes to 75 minutes and then tweets again
while True:

	try:

		# Finds a tweet to copy just using the letter a as a search term
		result = getTweet('a')

		# Grabs the data from the dictionary containing the tweet
		tweet = result['text']

		# Posts the tweet to twitter
		twitter.update_status(status=tweet)
	
	except Exception, ex:
		writeToReport("Error. Will try again later")
		writeToReport(str(ex))

	for i in range(0,5):
		time.sleep(random.randint(150,750))
		writeToReport("Still Running Tweeter")
