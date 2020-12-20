import discord
import os
#allow http request to get data from zenquotes api
import requests
import json

import random

#connection to the discord
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

sad_words = ["sad","depressed","unhappy","angry","sedih","nangis","marah","miserable","depressing"]

starter_encouragements = ["Hang in  there!","Cheer up!","You are a great person"]

#register an event
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

#if receive a message
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith("hmm"):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

client.run(os.getenv("TOKEN"))