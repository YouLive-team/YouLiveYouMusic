import discord
from discord.ext import commands
import asyncio

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        if ctx.member.id == 398538710993600523 and ctx.member.id == 501089151089770517:
            msg = await ctx.send('.')
            await asyncio.sleep(1)
            await msg.delete()
            msg = await ctx.send('..')
            await asyncio.sleep(1)
            await msg.delete()
            msg = await ctx.send('...')
            await asyncio.sleep(1)
            await msg.delete()
            msg = await ctx.send('....')
            await asyncio.sleep(1)
            await msg.delete()
            msg = await ctx.send('.....')
            await asyncio.sleep(1)
            await msg.delete()

def setup(bot):
    bot.add_cog(test(bot))

