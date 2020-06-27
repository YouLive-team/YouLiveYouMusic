import discord
import json
import re
import os
import MusicBot
from discord.ext import commands

class langue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["lang"])
    @commands.has_permissions(administrator=True)
    async def set_lang(self, ctx, langue: str=None):
        if langue == None:
            await ctx.send("ENG or RUS")
        else:
            if langue == 'ENG' or langue == "RUS":
                home = os.getcwd()
                path1 = f'{home}/servers/{ctx.guild.id}'
                with open(f'{path1}/config.json','r') as f:
                    data1 = json.load(f)
                with open(f'{path1}/config.json','w') as f:
                    data1["Language"] = langue
                    json.dump(data1, f)
                await ctx.send(f"__**{langue}**__")
            else:
                if await MusicBot.langueg == "RUS":
                    await ctx.send(f"Извините но я не знаю такой язык, если вы хотите что б он появился в списке языков напишите об этом создателям меня")
                elif await MusicBot.langueg == "ENG":
                    await ctx.send(f"Sorry, but I don’t know such a language, if you want it to appear in the list of languages, write to the creators about it")



    @set_lang.error
    async def set_lang_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            if Green.langue(ctx) == 'RUS':
                await ctx.send(f'**{ctx.author.mention} у вас не достаточно прав**')
            elif Green.langue(ctx) == 'ENG':
                await ctx.send(f'**{ctx.author.mention} you do not have enough rights**')

def setup(bot):
    bot.add_cog(langue(bot))
