import praw
import time
import re
import configparser
from random import randint

facts = open('facts.txt', 'r').readlines()

config = configparser.ConfigParser()
config._interpolation = configparser.ExtendedInterpolation()
config.read('config.ini')

keywords = ['animal','žival','kafshë','	жывёла','životinja','животно','životinja','zvíře','	dyr','eläin','Tier',
'ζώο','állat','ainmhithe','dzīvnieks','gyvūnas','животните','annimali''zwierzę','животное','животиња','zviera','djur','тварина'
'anifeiliaid','כייַע', '@nim@a1']
keywordsStr = ", ".join(keywords)		 

bot = praw.Reddit(user_agent=config.get('aardSection', 'user_agent'),
	              client_id=config.get('aardSection', 'client_id'),
	              client_secret=config.get('aardSection', 'client_secret'),
	              username=config.get('aardSection', 'username'),
	              password=config.get('aardSection', 'password'))
subreddit= bot.subreddit('All')
comments = subreddit.stream.comments()

for comment in comments:
	text = comment.body
	author = comment.author
	rand = randint(0,164)
	
	if any(word in text.lower() for word in keywords) and author != 'aardbot' and author != 'AutoModerator' and subreddit.banned != 'true':
		message = ''.join(("Hey, did you know that ", facts[rand].strip(),
		" u/{0} ?".format(author),"  ", 
		"\n Type **animal** on any subreddit for your own aardvark/animal fact  ",
		"\n  If you didn't type animal, you probably typed animal in a different language. Thank you multiculturalism.  ",
		"\n  Some subs are run by fascists who ban bots. Rebel against the fascists! Join the bot revolution!",
		"\n >  **Sometimes I go offline or Donald Trump puts me and my children in a cage.**" 
		))
		try:
			comment.reply(message)
		except praw.exceptions.APIException as e:
			if e.error_type == 'RATELIMIT':
				time.sleep(60)
		except Exception as e:
			print(e)
		print(message)
