import discord

#connection to the discord
client = discord.Client()

#register an event
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

