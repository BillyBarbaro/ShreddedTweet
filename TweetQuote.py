import urllib
import re
from twython import Twython
import time
import random

# All 4 keys were pulled from the developer page on Twitter's Website. Custom to account and allow us to authorize ourself to tweet
APP_KEY = 'APPKEY'
APP_SECRET = 'APPSECRET'

OAUTH_TOKEN = 'OAUTHTOKEN'
OAUTH_TOKEN_SECRET = 'OAUTHTOKENSECRET'

# Opens a connection with twitter and verifies the user
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Appends the given output to "report.txt"
def writeToReport(output):
	with open("QuoteTweet.txt", "a") as myfile:
		myfile.write(output + '\n')

# Clears the reporting file and writes a message to indicate the start
f = open('QuoteTweet.txt','w')
f.write("Beginning Tweets" + '\n')
f.close()

while True:

	try:
		# Here we grab the html from a page containing a collection of random quotes. These quotes change each time the page is loaded
		html = urllib.urlopen('http://www.quotationspage.com/random.php3')

		webpage = html.read()

		html.close()

		# We find the first quote on the page based on context the truncate what we've found to just inculde the quote
		findQuote = re.search(r'([0-9]+.html">.*</a>\ <)', webpage)

		quote = findQuote.group()
		start = quote.find('>') + 1
		stop = quote.find('<')

		quote = quote[start:stop]

		# We do the same for the author
		findAuthor = re.search(r'(</div><b><a href=".*">.*?</a>.*</b></dd>)', webpage)

		author = findAuthor.group()

		start = author.find('">') + 2
		stop = author.find('</a')

		author = author[start:stop]

		# Assures the tweet will be less than 140 characters. If not, we modifiy it a bit
		if (len(quote) + len(author) < 136):

			tweet = '"' + quote + '" --' + author
		else:
			if (len(quote) < 139):
				tweet = '"' + quote +'"'
			else:
				tweet = 'Check out some of ' + author + "'s quotes. Quality stuff."

		# Posts the tweet to twitter
		twitter.update_status(status=tweet)
		#print(tweet)

	except Exception, ex:
		writeToReport("Error. Will try again later")
		writeToReport(str(ex))

	for i in range(0,5):
		time.sleep(random.randint(60,900))
		writeToReport("Still Quoting Famous People")
