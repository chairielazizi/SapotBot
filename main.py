import discord
import os

#connection to the discord
client = discord.Client()

#register an event
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

#if receive a message
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startsWith("$hello"):
    await message.channel.send("Hello")

client.run(os.getenv("TOKEN"))