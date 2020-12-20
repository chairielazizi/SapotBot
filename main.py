import discord
import os
#allow http request to get data from zenquotes api
import requests
import json

import random
from replit import db

from keep_alive import keep_alive

#connection to the discord
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#add msg to database
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

#delete msg in database
def delete_encouragement(index):
  #get list of encouragementsform the database
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

sad_words = ["sad","depressed","unhappy","angry","sedih","nangis","marah","miserable","depressing"]

starter_encouragements = ["Hang in  there!","Cheer up!","You are a great person"]

if "responding" not in db.keys():
  db["responding"] =True

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

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

#shows the list of added encouragement  message
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

#change whether bots will response to sad words or not
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] =True
      await message.channel.send("Responding is on")
    else:
      db["responding"] =False
      await message.channel.send("Responding is off")

#connect to uptimerobot.com to ping the bot every 5 minutes
keep_alive()
client.run(os.getenv("TOKEN"))