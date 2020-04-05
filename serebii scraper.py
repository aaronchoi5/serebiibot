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
	subcats = []
	subcatTitles = []
	for x in range(len(dates)):
		subcats.append(tree.xpath('(//div[@class="post"]/h2/a[@id="' + dates[x] + '"]/parent::h2/parent::div/div[@class="subcat"]/p[2])'))
		subcatTitles.append(tree.xpath('(//div[@class="post"]/h2/a[@id="' + dates[x] + '"]/parent::h2/parent::div/div[@class="subcat"]/p[1])'))

	listOfPosts = []
	for date, subcat in zip(dates, subcats):
		listOfPosts.append(Post(date, subcat))
	listOfPosts = reversed(listOfPosts)
	subcatTitles = reversed(subcatTitles)

	await client.wait_until_ready()
	channel = client.get_channel(int(CHANNEL))
	#if date in pickle of dates read then don't post it in discord

	for post, subcatTitle in zip(listOfPosts, subcatTitles):
		if post.id not in history:
			for z, s in zip(reversed(range(len(post.content))), reversed(subcatTitle)):
				print(post.id + " " + s.text_content() + "\n" + post.content[z].text_content())
				await channel.send(post.id + " **" + s.text_content() + "**\n" + post.content[z].text_content())
		history.add(post.id)
	pickle.dump(history, open(path, "wb"))

client.run(TOKEN)


