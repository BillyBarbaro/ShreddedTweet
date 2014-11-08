#! /usr/bin/python
import random
from twython import Twython
import time

# A collection of naughty words to search twitter for
badWords = ['damn', 'shit', 'fuck', 'bitch', 'ass', 'asshole', 'hell', 'goddamn']

# euphemisms for some of the swear words above. There's different lists for each word depending on the context in which it's used
corrections = {'damn' : {'dammit' : ["darnit", "dag nabit", "dadblast", "doggone it", "doggone it"], "damnExclaim" : ["darn", "drat", "doggone", "dang"], "damn" : ["darn", "dang"]}, 'shit' : {'shitexclaim' : ["shoot", "crud", "crap", "whoopsies", "spit"], 'holyshit' : ["holy cow", "holy crap", "holy moly", "holy guacamole", "holy mackerel", "holy Toledo"], 'shit' : ['crap', 'spit']}, 'ass' : {'assanat' : ["butt", "behind", "backside", "rear end", "rump", "fanny", "bum", "gluteus maximus"], "asspers" : ["jerk", "idiot", "loser", "infidel"]}, 'asshole' : {'asshole' : ["jerk", "idiot", "loser", "infidel"]}, 'hell' : {'hell' : ["heck"], "wthell" : ["what the heck", "what the hay"]}, 'goddamn' : {'goddamn' : ["gosh darn", "doggone", "dadgum"], 'goddamnComma' : ["golly gee willikers", "my goodness", "holy cow", "good grief", "God bless America"]}}
# Commonly used phrases for each of the searched words. They're used to identify the context in which it's used so a replacement can be suggested
swearPhrases = {"damn" : {"damn it" : "dammit", "dammit" : "damnit", "damnit" : "dammit", "damn!" : "damnExclaim", "damn" : "damn"}, "shit" : {"holy shit" : "holyshit", "shit!" : "shitexclaim", "shit" : 'shit'}, "ass" : {"her ass" : "assanat", "his ass" : "assanat", "my ass" : "assanat", "ur ass" : "assanat", "half ass" : "attempted", "ass" :"asspers"}, "asshole" : {"asshole" : "asshole"}, "hell" : {"what the hell" : "wth", 'hell' : 'hell'}, "goddamn" : {"goddamn," : "goddamnComma", "goddamn" : "goddamn"}}

# Beginning and ending phrases that a euphemism and original word can be plugged in to. The phrases match up by index
beginningPhrases = ['Did you mean ', 'I think you might have meant ', "Stupid autocorrect. Looks like it changed ", 'Whoops looks like autocorrect switched your tweet. You probably meant to say ', "Why not just use ", "You could always just say ", "My little brother thinks you must've meant to say ", "Pesky autocorrect. Must've changed ", "Autocorrect must've gotten a hold of "]
endingPhrases = [" instead of ", " rather than ", " to ", " instead of ", " and not ",  " and not use ", " but accidentally typed ", " to ", " and switched it to "]

# Full phrases to simply reprimand someone whose tweet includes a swear word
fullPhrases = ['Whoa there. Did you really mean that?', 'Tell us how you really feel.', "Didn't your mom tell you not to use words like that?", "You know, words like that could really hurt someone.", "Please don't pollute the interweb with your foul language.", "If I used words like that, I'd have to rinse out my mouth with soap.", "Come on man, don't be a potty-mouth", "You'd probably get in trouble if your mom knew you said that word", "You're crude language is detracting from your excellent point."]

# Searches for tweets using the bad word and returns the dictionary object containing a random one's information
def getTweet(badWord):
	while True:
		# Queries for 30 tweets
		search = twitter.search(q=badWord, count='30', lang='en')

		# Chooses a random one
		index = random.randint(0, len(search) - 1)
		result = search['statuses'][index]

		# Checks to make sure it's not a retweet
		if result['retweet_count'] == 0:
			return result

# Appends the given output to "report.txt"
def writeToReport(output):
	with open("report.txt", "a") as myfile:
		myfile.write(output + '\n')

# Given a word and a phrase, finds an appropriate euphemism for the word
def findEuphemism(badWord, text):

	key = ""
	# Makes the search case insesitive
	text = text.lower()

	# Corrects for words that are inside the other word by just choosing the larger one
	if (badWord == "ass"):
		if "asshole" in text:
			badWord = "asshole"
	if (badWord == "damn"):
		if "goddamn" in text:
			badWord = "goddamn"

	responseDict = swearPhrases[badWord]

	# Searches through the dictionary of responses looking for a case that matches so an appropriate euphemism is selected
	for phrase in responseDict:
		if phrase in text:
			key = responseDict[phrase]
			break

	return badWord, key

# Generates a reply from the lists above
def generateReply(badWord, tweet):

	# If the bad word has euphemisms, we might look for one
	if (badWord in corrections):

		# Randomly selects to suggest a euphemism or reprimand
		if (random.randint(0,1) == 0):
			reply = fullPhrases[random.randint(0, len(fullPhrases) - 1)]
		else:
			picker = random.randint(0, len(beginningPhrases) - 1)
			badWord, euphemism = findEuphemism(badWord, tweet)

			# If we couldn't find an appropirate context for the word, we'll just reprimand
			if euphemism == "":
				reply = fullPhrases[random.randint(0, len(fullPhrases) - 1)]
			else:
				reply = beginningPhrases[picker] + corrections[badWord][euphemism][random.randint(0, len(corrections[badWord][euphemism]) - 1)] + endingPhrases[picker] + badWord

	# If there's no euphemisms, we'll just reprimand
	else:
		reply = fullPhrases[random.randint(0, len(fullPhrases) - 1)]

	return reply

# All 4 keys were pulled from the developer page on Twitter's Website. Custom to account and allow us to authorize ourself to tweet
APP_KEY = 'APPKEY'
APP_SECRET = 'APPSECRET'

OAUTH_TOKEN = 'OAUTHTOKEN'
OAUTH_TOKEN_SECRET = 'OAUTHTOKENSECRET'

# Opens a connection with twitter and verifies the user
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Clears the reporting file and writes a message to indicate the start
f = open('report.txt','w')
f.write("Beginning Tweets" + '\n')
f.close()

# Continuously loops through the script to tweet. Sleeps half an hour to an hour and then tweets again
while True:

	try:
		# Picks a word at random to search fo
		word = badWords[random.randint(0,len(badWords) - 1)]

		result = getTweet(word)

		# Grabs the data from the dictionary containing the tweet
		name = "@" + result['user']['screen_name']
		idStr = result["id_str"]
		tweet = result['text']

		writeToReport(tweet)

		reply = name + " " + generateReply(word, tweet)

		writeToReport(reply)

		# Posts the tweet to twitter
		twitter.update_status(status=reply, in_reply_to_status_id=idStr)

	except Exception, e:
		# If there's an error, we note it
		writeToReport("Error! We'll try again later")
		writeToReport(str(e))

	for i in range(0,5):
		time.sleep(random.randint(300,600))
		writeToReport("Still Running")

