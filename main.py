import discord
import os
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

greeting = ["···喝！", "···哈！", "蔓延！", "散！"]


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('蛤'):
    await message.channel.send('这么强!')

  if message.content.startswith('还有什么'):
    await message.channel.send('没了!')

  if message.content.startswith('这么好笑'):
    await message.channel.send('<:grass:1025233778949492806>')

  if message.content.find('<:grass:1025233778949492806>') != -1:
    await message.channel.send('<:grass:1025233778949492806>')

  if client.user.mentioned_in(message):
    await message.channel.send(greeting[random.randrange(1, len(greeting), 1)])


client.run(os.getenv('TOKEN'))
