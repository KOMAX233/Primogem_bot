import discord
import os
import random
import datetime
from backports.zoneinfo import ZoneInfo
# from keep_alive import keep_alive
from discord.ext import commands

token = os.getenv('TOKEN')
id = "1025615784170487809"

intents = discord.Intents.all()
intents.message_content = True

# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='/',
                      intents=intents,
                      help_command=None,
                      description="This is a command that sends current time")

greeting = [
  "···喝！", "···哈！", "蔓延！", "散！", "昼夜时空皆为虚像，命运的纽带却再次将你带到了我的永恒长夜中。",
  "···咳，有何贵干？", "我听见命运的嚅嗫，低声呼唤我之尊名···", "你的深眠将平安无梦。",
  "此间须臾的霁月光风，就如命运的转折点一般呢！愉快！", "我与你在此相遇。错不了，想必是命运的意志吧。"
]

timezones = [
  "America/Chicago", "Canada/Eastern", "Canada/Mountain", "Asia/Shanghai"
]


### commands
@client.command()
async def hello(ctx, arg):
  await ctx.send(ctx.author.mention + arg)


# what does context mean?
@client.command(name='now', aliases=['t1'])
async def test(ctx):
  await ctx.send(r'''Please select timezone:
    [1] "America/Chicago"
    [2] "Canada/Eastern"
    [3] "Canada/Mountain"
    [4] "Asia/Shanghai"
  ''')
  msg = await client.wait_for("message")
  if msg:
    await ctx.send(
      datetime.datetime.now(tz=ZoneInfo(timezones[int(msg.content) - 1])))


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


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

  if client.user.mentioned_in(message) or message.content.find('上班了') != -1:
    await message.channel.send(greeting[random.randrange(1, len(greeting), 1)])
  await client.process_commands(message)

  # if client.user.mentioned_in(message):
  #   await message.channel.send("距离每日委托ddl还有" + "")

  # client id after applications/


# keep_alive()
client.run(token)
