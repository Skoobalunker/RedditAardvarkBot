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
	rand = randint(0,115)
	
	if any(word in text.lower() for word in keywords) and author != 'aardbot' and subreddit.banned != 'true':
		message = ''.join(("Hey, did you know that ", facts[rand].strip(),
		" u/{0} ?".format(author),"  ", 
		"\n Type **animal** on any subreddit for your own aardvark/animal fact ",
		"\n >  I have expanded my knowledge base by 300% !  ", 
		"\n Now you may enjoy facts from other animals as well as more all new aardvark facts.  ",
		"\n Also, I am learning more languages of human. Try my foreign language options.  ",
		"\n >  **Sometimes I go offline or Donald Trump takes me offline. Be patient.**"
		))
		try:
			comment.reply(message)
		except praw.exceptions.APIException as e:
			if e.error_type == 'RATELIMIT':
				time.sleep(60)
		except Exception as e:
			print(e)
		print(message)
