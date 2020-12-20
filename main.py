import discord
import os
#allow http request to get data from zenquotes api
import requests
import json

import random
from replit import db

#connection to the discord
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#add msg to database
def update_encouragements(msg):
  if "encouragements" in db.key():
    encouragements = db["encouragements"]
    encouragements.append(msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [msg]

#delete msg in database
def delete_encouragement(index):
  #get list of encouragementsform the database
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

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

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

client.run(os.getenv("TOKEN"))