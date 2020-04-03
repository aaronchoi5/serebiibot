from lxml import html
import requests
import sys
import pickle
import os

import discord
from dotenv import load_dotenv
class Post:

	def __init__(self, uID, content):
		self.id = uID
		self.content = content

path = sys.argv[1]

try :
	history = pickle.load(open(path, "rb"))
except (OSError, IOError) as e:
	history = set()    

#TODO split out into subcatagories
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')
client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	page = requests.get('https://serebii.net/index2.shtml')
	tree = html.fromstring(page.content)

	dates = tree.xpath('//div[@class="post"]/h2/a/@id')
	posts = tree.xpath('//div[@class="post"]')

	listOfPosts = []
	for post, date in zip(posts, dates):
		listOfPosts.append(Post(date, post.text_content()))

	await client.wait_until_ready()
	channel = client.get_channel(int(CHANNEL))
	#if date in pickle of dates read then don't post it in discord
	for k in reversed(range(len(listOfPosts))):
		if listOfPosts[k].id not in history:
			#print to discord
			print(listOfPosts[k].id + " " + listOfPosts[k].content)
			await channel.send(listOfPosts[k].id + " " + listOfPosts[k].content)
			history.add(listOfPosts[k].id)

client.run(TOKEN)
pickle.dump(history, open(path, "wb"))

