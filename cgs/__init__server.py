import discord
from discord.ext import commands
import datetime
import json
import os


class test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        home = os.getcwd()
        try:
            path1 = f'{home}/servers/{guild.id}'
            os.mkdir(path1)
            os.chdir(path1)
        except OSError:
            os.chdir(path1)

        Id = guild.id
        Name = guild.name
        Icon = guild.icon
        Region = guild.region

        server={
        'ID': Id,
        'NAME':  Name,
        'ICON': Icon,
        'REGION': Region,
        'Premium': 'N'
        }



        with open('server.txt', 'w', encoding='Latin-1') as w:
            json.dump(server,w)


        config ={
        'Language': 'ENG',
        'Prefix': 'm.'
        }
        with open('config.json', 'w',  encoding='Latin-1') as w:
            json.dump(config,w)

        open('music_queue.txt', 'tw',  encoding='Latin-1').close()
        os.chdir(home)






def setup(bot):
    bot.add_cog(test(bot))

