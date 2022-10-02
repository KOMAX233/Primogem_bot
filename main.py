import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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

  if message.content.startswith('这么好笑') or message.content.startswith(
      '<:grass:1025233778949492806>'):
    await message.channel.send('<:grass:1025233778949492806>')


client.run(os.getenv('TOKEN'))
