import discord
import os
#allow http request to get data from zenquotes api
import requests
import json

#connection to the discord
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#register an event
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

#if receive a message
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("hello"):
    await message.channel.send("Hello!")

client.run(os.getenv("TOKEN"))