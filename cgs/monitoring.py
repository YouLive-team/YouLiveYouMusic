import os
import json
import discord
from discord.ext import commands
import datetime
from colorama import init
from termcolor import colored
try:
    import MusicBot
except:pass

class test(commands.Cog):
    init()
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global today, now
        timedelta = datetime.timedelta(hours=1)
        today = datetime.datetime.today() +timedelta

        now = today.strftime("%Y/%m/%d %H:%M:%S")
        print(colored(f'{now}:  «Я готов»', 'blue'))
        _type = discord.ActivityType.listening
        activity = discord.Activity(name=f"{len(self.bot.guilds)} servers", type=_type)
        status = discord.Status.online
        await self.bot.change_presence(activity=activity, status=status)

    @commands.Cog.listener()
    async def on_connect(self):
        timedelta = datetime.timedelta(hours=1)
        today = datetime.datetime.today() +timedelta
        now = today.strftime("%Y/%m/%d %H:%M:%S")
        print(colored(f'{now}:  «Присоединился»', 'blue'))

    @commands.Cog.listener()
    async def on_disconnect(self):
        today = datetime.datetime.today()
        now = today.strftime("%Y/%m/%d %H:%M:%S")
        print(colored(f'{now}:  «Отсоединился»', 'blue'))

    @commands.Cog.listener()
    async def on_resumed(self):
        today = datetime.datetime.today()
        now = today.strftime("%Y/%m/%d %H:%M:%S")
        print(colored(f'{now}:  «Возобновил работу»', 'blue'))

    @commands.Cog.listener()
    async def on_message(self,message):
        home = os.getcwd()
    
        path1 = (f'{home}/servers/{message.guild.id}')
        with open(f'{path1}/config.json', 'r') as f:
            prefixes = json.load(f)#тут я прочитал то что там есть
            prefixes = prefixes["Prefix"]
        if message.content == "prefix" or message.content == "префикс":
            if await MusicBot.langueg(message) == "RUS":
                embed=discord.Embed(title=f"Префикс на сервер __`{message.guild.name}`__: `{prefixes}`",color=0xff7606)
            elif await MusicBot.langueg(message) == "ENG":
                embed=discord.Embed(title=f"Server prefix __`{message.guild.name}`__: `{prefixes}`",color=0xff7606)
            await message.channel.send(embed=embed)





def setup(bot):
    bot.add_cog(test(bot))
