import discord
import os
import random
import datetime
from backports.zoneinfo import ZoneInfo
from keep_alive import keep_alive
# from discord.ext import commands
from discord import app_commands
from typing import List
from discord.ext import tasks
import sqlite3

token = os.getenv('TOKEN')
user = os.getenv('USER')
pw = os.getenv('PW')
id = "1025615784170487809"
guild_id = 710874067036536882
status_index = 1
status = ['你的老婆', '我的老婆']

intents = discord.Intents.default()
intents.message_content = True


class aclient(discord.Client):

  def __init__(self):
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync(guild=discord.Object(id=guild_id))
      self.synced = True
    print(f'We have logged in as {self.user}')
    channel = self.get_channel(1025128006634713208)
    change_status.start()
    await channel.send("上班了!")
    voice_channel = self.get_channel(710874067581796365)
    await voice_channel.connect()
    await scheduled_greets()


#   async def on_ready():
#     await wait_until_ready()

# client = discord.Client(intents=intents)
# client = commands.Bot(command_prefix='/',
#                       intents=intents,
#                       help_command=None,
#                       description="This is a command that sends current time")

client = aclient()
tree = app_commands.CommandTree(client)

connection = sqlite3.connect('ddl.db')
cursor = connection.cursor()
cursor.execute(
  '''CREATE TABLE IF NOT EXISTS ddl_table(Task TEXT, User TEXT, Year INT, Month INT, Day INT, Hour INT, Minute INT, Timezone INT)'''
)

sleep = ["你的深眠将平安有梦。"]

greeting = [
  "···喝！", "···哈！", "蔓延！", "散！", "昼夜时空皆为虚像，命运的纽带却再次将你带到了我的永恒长夜中。",
  "···咳，有何贵干？", "我听见命运的嚅嗫，低声呼唤我之尊名···", "你的深眠将平安有梦。",
  "此间须臾的霁月光风，就如命运的转折点一般呢！愉快！", "我与你在此相遇。错不了，想必是命运的意志吧。", "赞颂我的降临吧!"
]

timezones = [
  "America/Chicago", "Canada/Eastern", "Canada/Mountain", "Asia/Shanghai"
]

nekos = [
  "(ФωФ)", "#(ФωФ)", "\\(ФωФ)/", "(ФωФ*)", "(Ф∀Ф)", "(ФДФ)", "( ↀДↀ)✧",
  "Σ(;ФωФ)", "（งФДФ）ง", "(˵ФωФ˵)", "(ﾐФﻌФﾐ)∫", "(ﾐФᆽФﾐ)✧", "(ﾐФᆽФﾐ)",
  "/ᐠ｡ꞈ｡ᐟ\\", "/ᐠ｡ꞈ｡ᐟ✿\\", "/ᐠ｡ꞈ｡ᐟ❁ \\∫", "/ᐠ｡▿｡ᐟ\\*ᵖᵘʳʳ*", "/ᐠ｡ﻌ｡ᐟ\\",
  "/ᐠ.ꞈ.ᐟ\\", "✧/ᐠ-ꞈ-ᐟ\\", "/ᐠ –ꞈ –ᐟ\\", "/ᐠ_ ꞈ _ᐟ\\ɴʏᴀ~", "/ᐠ.ﮧ.ᐟ\\",
  "/ᐠ ._. ᐟ\\ﾉ", "/ᐠ .⋏. ᐟ\\ﾉ", "/ᐠ .ᆺ. ᐟ\\ﾉ", "/ᐠ ._. ᐟ\\ﾉ"
]


@tasks.loop(seconds=10)
async def change_status():
  global status_index
  status_index = 1 - status_index
  await client.change_presence(activity=discord.Game(status[status_index]))
  # print(status_index)


### commands
@tree.command(name="test",
              description="test command",
              guild=discord.Object(id=guild_id))
async def test(interaction: discord.Interaction):
  await interaction.response.send_message("哦嗨哟!")


@tree.command(name="hello",
              description="hello command",
              guild=discord.Object(id=guild_id))
async def hello(interaction: discord.Interaction, input: str):
  await interaction.response.send_message(input)


@tree.command(name="neko",
              description="neko print command",
              guild=discord.Object(id=guild_id))
async def neko(interaction: discord.Interaction):
  await interaction.response.send_message(nekos[random.randrange(
    1, len(nekos), 1)])


  # # what does context mean?
class Now(app_commands.Group):

  @app_commands.command(name='now')
  @app_commands.choices(timezone=[
    app_commands.Choice(name='America/Chicago', value=0),
    app_commands.Choice(name='Canada/Eastern', value=1),
    app_commands.Choice(name='Canada/Mountain', value=2),
    app_commands.Choice(name='Asia/Shanghai', value=3)
  ])
  async def now(self, interaction: discord.Interaction,
                timezone: app_commands.Choice[int]):
    await interaction.response.send_message(
      datetime.datetime.now(tz=ZoneInfo(timezones[timezone.value])))


tree.add_command(Now(), guild=discord.Object(id=guild_id))


class ddl_helper(app_commands.Group):
  choice_list = []

  @app_commands.choices(timezone=[
    app_commands.Choice(name='America/Chicago', value=0),
    app_commands.Choice(name='Canada/Eastern', value=1),
    app_commands.Choice(name='Canada/Mountain', value=2),
    app_commands.Choice(name='Asia/Shanghai', value=3)
  ])
  @app_commands.command(name="set-ddl")
  async def set_ddl(self, interaction: discord.Interaction, task: str,
                    ddl_year: int, month: int, day: int, hour: int,
                    minute: int, timezone: app_commands.Choice[int]):

    cursor.execute('''DELETE FROM ddl_table WHERE Task=? AND User=?''',
                   (task, interaction.user.id))
    cursor.execute(
      '''INSERT INTO ddl_table(Task, User, Year, Month, Day, Hour, Minute, Timezone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
      (task, interaction.user.id, ddl_year, month, day, hour, minute,
       timezone.value))
    connection.commit()
    now = datetime.datetime.now(tz=ZoneInfo(timezones[timezone.value]))
    ddl = datetime.datetime(ddl_year,
                            month,
                            day,
                            hour,
                            minute,
                            0,
                            tzinfo=ZoneInfo(timezones[timezone.value]))
    ddl_time = "距离" + task + "还有" + str(ddl - now)
    await interaction.response.send_message(ddl_time)

  async def get_user_tasks(user):
    cursor.execute('''SELECT * FROM ddl_table WHERE User=?''', ([user]))
    tasks_info = cursor.fetchall()
    ddl_helper.choice_list = [item[0] for item in tasks_info]
    return ddl_helper.choice_list

  # item_names = item[0] for item in ddl_helper.get_user_tasks(interaction.user.id)

  async def task_autocomplete(
    self,
    interaction: discord.Interaction,
    current: str,
  ) -> List[app_commands.Choice[str]]:
    choices = await ddl_helper.get_user_tasks(interaction.user.id)
    return [
      app_commands.Choice(name=choice, value=choice) for choice in choices
      # if current.lower() in choice.lower()
    ]

  # set task to done and delete from ddl.db
  @app_commands.command(name="get-ddl")
  @app_commands.autocomplete(choices=task_autocomplete)
  async def get_ddl(self, interaction: discord.Interaction, choices: str):
    cursor.execute(
      '''SELECT Year, Month, Day, Hour, Minute, Timezone FROM ddl_table WHERE Task=? AND User=?''',
      (choices, interaction.user.id))
    ret = cursor.fetchone()
    now = datetime.datetime.now(tz=ZoneInfo(timezones[ret[5]]))
    ddl = datetime.datetime(ret[0],
                            ret[1],
                            ret[2],
                            ret[3],
                            ret[4],
                            0,
                            tzinfo=ZoneInfo(timezones[ret[5]]))
    ddl_time = "距离" + choices + "还有" + str(ddl - now)
    await interaction.response.send_message(ddl_time)

  # set task to done and delete from ddl.db
  @app_commands.command(name="done")
  @app_commands.autocomplete(choices=task_autocomplete)
  async def done(self, interaction: discord.Interaction, choices: str):
    await interaction.response.send_message(choices + ", 完成!")
    cursor.execute('''DELETE FROM ddl_table WHERE Task=? AND User=?''',
                   (choices, interaction.user.id))
    connection.commit()


tree.add_command(ddl_helper(), guild=discord.Object(id=guild_id))

# await ctx.send(r'''Please select timezone:
# [1] "America/Chicago"
# [2] "Canada/Eastern"
# [3] "Canada/Mountain"
# [4] "Asia/Shanghai"''')
# temp_tz = await client.wait_for("message")

#   if msg:
#     now = datetime.datetime.now(tz=ZoneInfo(timezones[int(msg.content) - 1]))
#     await ctx.send(now)


@tree.command(name='daily',
              description="daily comission countdown command",
              guild=discord.Object(id=guild_id))
async def quest(interaction: discord.Interaction):
  beijing = datetime.datetime.now(tz=ZoneInfo(timezones[3]))
  ddl = datetime.datetime(beijing.year,
                          beijing.month,
                          beijing.day,
                          4,
                          0,
                          0,
                          tzinfo=ZoneInfo(timezones[3]))
  if beijing.hour >= 4:
    # date add 1
    ddl += datetime.timedelta(days=1)
  quest_time = "距离每日委托ddl还有" + str(ddl - beijing)
  await interaction.response.send_message(quest_time)


@tree.command(name='map',
              description="Teyvat map command",
              guild=discord.Object(id=guild_id))
async def map(interaction: discord.Interaction):
  await interaction.response.send_message(
    f"https://webstatic.mihoyo.com/ys/app/interactive-map/")


@tree.command(name='gacha',
              description="gacha simulation",
              guild=discord.Object(id=guild_id))
async def gacha(interaction: discord.Interaction):
  await interaction.response.send_message(
    f"https://wiki.biligame.com/ys/%E6%8A%BD%E5%8D%A1%E6%A8%A1%E6%8B%9F%E5%99%A8"
  )


@tree.command(name='chinese',
              description="pinyin to Chinese ",
              guild=discord.Object(id=guild_id))
async def chinese(interaction: discord.Interaction):
  # TODO: hyperlink
  await interaction.response.send_message(
    "我可以输入中文了!(https://www.archchinese.com/type_chinese.html)")


@tree.command(name='primo_calc',
              description="calculate how many wishes you can get",
              guild=discord.Object(id=guild_id))
async def primoCalc(interaction: discord.Interaction, primogem: int,
                    interwined_fate: int):
  await interaction.response.send_message("你还有" + str(primogem // 160 +
                                                      interwined_fate) + "抽")


@tree.command(name='join',
              description="join author's voice channel command",
              guild=discord.Object(id=guild_id)
              )  # CREATING COMMAND "JOIN" WITH ALIAS SUMMON
async def _join(
  interaction: discord.Interaction
):  # TAKING ARGUMENT CHANNEL SO PPL CAN MAKE THE BOT JOIN A VOICE CHANNEL THAT THEY ARE NOT IN
  """Joins a voice channel."""
  channel = discord.VoiceChannel = None
  destination = channel if channel else interaction.user.voice.channel  # CHOOSING THE DESTINATION, MIGHT BE THE REQUESTED ONE, BUT IF NOT THEN WE PICK AUTHORS VOICE CHANNEL

  # if ctx.voice_client:  # CHECKING IF THE BOT IS PLAYING SOMETHING
  #   await ctx.voice_state.voice.move_to(
  #     destination
  #   )  # IF THE BOT IS PLAYING WE JUST MOVE THE BOT TO THE DESTINATION
  #   return

  await destination.connect()  # CONNECTING TO DESTINATION
  await interaction.response.send_message(
    f"Succesfully joined the voice channel: {destination.name} ({destination.id})."
  )


@client.event
async def scheduled_greets():
  now2 = datetime.datetime.now(tz=ZoneInfo(timezones[2 - 1]))
  print(now2.hour)
  channel = client.get_channel(1025128006634713208)
  if 7 <= now2.hour and now2.hour <= 10:
    await channel.send("哦嗨哟 ~~~ヾ(＾∇＾)!")
  elif 19 <= now2.hour and now2.hour <= 22:
    await channel.send("(*´△｀*)哦(*＾д＾*)呀(*´ε｀*)斯(*´～｀*)密!")


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('蛤') or message.content.startswith('这么强'):
    await message.channel.send('这么强!')

  if message.content.startswith('还有什么'):
    await message.channel.send('没了!')

  if message.content.startswith('这么好笑'):
    await message.channel.send('<:grass:1025233778949492806>')

  if message.content.find('<:grass:1025233778949492806>') != -1:
    await message.channel.send('<:grass:1025233778949492806>')

  if client.user.mentioned_in(message) or message.content.find('上班了') != -1:
    await message.channel.send(greeting[random.randrange(1, len(greeting), 1)])
  # await client.process_commands(message)
  if message.content.find('睡') != -1 or message.content.find(
      '困') != -1 or message.content.find('sleep') != -1:
    await message.channel.send(sleep[0])

  if message.content.find("哦嗨哟") != -1:
    await message.channel.send("哦嗨哟 ~~~ヾ(＾∇＾)!")
  if message.content.find("哦呀斯密") != -1:
    await message.channel.send("(*´△｀*)哦(*＾д＾*)呀(*´ε｀*)斯(*´～｀*)密!")


#   # client id after applications/

keep_alive()
client.run(token)
