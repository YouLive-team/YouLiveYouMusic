import discord
from discord.ext import commands
from discord.utils import get
try:
    import MusicBot
except:pass
class join(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["j"])
    async def join(self, ctx):
        global voice
        try:
            voice = get(self.bot.voice_clients, guild = ctx.guild)
            channel = ctx.message.author.voice.channel

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                if await MusicBot.langueg(ctx) == "RUS":
                    embed=discord.Embed(title=f'🎶Я присоеденяюсь к каналу: {channel}🎶', color=0xff7606)
                elif await MusicBot.langueg(ctx) == "ENG":
                    embed=discord.Embed(title=f'🎶I was join to voice channel: {channel}🎶', color=0xff7606)
                await ctx.send(embed=embed)
        except:
            return
    @commands.command(aliases = ["l"])
    async def leave(self, ctx):
        try:
            voice = get(self.bot.voice_clients, guild = ctx.guild)
            channel = voice.channel
            await voice.disconnect()
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f'🎶Я выйшел из канала: {channel}🎶', color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f'🎶I was leave to voice channel: {channel}🎶', color=0xff7606)
            await ctx.send(embed=embed)
        except:
            return

def setup(bot):
    bot.add_cog(join(bot))
