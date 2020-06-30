## -*- coding: utf-8 -*-
import discord
import re
import json
from urllib.parse import quote
import urllib.request
import pafy
import asyncio
import ffmpeg
try:
    import MusicBot
except: pass
import os

from youtube_api import YouTubeDataAPI
from discord.utils import get
from discord.ext import commands



async def main_fplay(self,ctx, arg):
    global fplayGo, global_voice
    guild = ctx.guild

    self.voice = get(self.bot.voice_clients, guild = ctx.guild)
    global_voice = self.voice
    try:
        channel = ctx.author.voice.channel
    except:
        if await MusicBot.langueg(ctx) == "RUS":
            embed=discord.Embed(title=f"**{ctx.author.name} Вы не в голосовом канале**",color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed=discord.Embed(title=f"**{ctx.author.name} You are not in the voice channel**",color=0xff7606)
        await ctx.send(embed=embed)
        return

    if self.voice and self.voice.is_connected():
        await self.voice.move_to(channel)
    else:
        self.voice = await channel.connect()
    #Проверяю если есть https://www.youtube.com/watch?v= в arg
    #Если да то url = arg
    if 'https://www.youtube.com/watch?v=' in arg:
        url = arg
    #Если нет
    elif arg != None:
        global_video_id = await ffindyoutube(arg)
        url = f"https://www.youtube.com/watch?v={global_video_id[0]}"

    #Возврат
    if arg == None:
        return
    else:

        self.vol = 0.60
        music_chanel_id = ctx.channel.id
        try:
            video = pafy.new(url)
            best = video.getbest()
            self.playurl = best.url
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                await ctx.send("**Что то не так с этим видео, извините**\n**Попробуйте снова, но уже другое ролик**")
            elif await MusicBot.langueg(ctx) == "ENG":
                await ctx.send("**Something is wrong with this video, I'm sorry.**\n**Try again, but another video.**")
            return
        
       # try:
        self.voice.play(discord.FFmpegPCMAudio(self.playurl))

        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
        self.voice.source.volume = self.vol
       # except:#Если песня уже играет то мы добавим новую в список

            #path1 = f'{self.home}/servers/{ctx.guild.id}'
            #with open(f'{path1}/music_queue.txt','a',  encoding='Latin-1') as f:
            #    f.write(f'{url}\n')

            #video = pafy.new(url)
            #if await MusicBot.langueg(ctx) == "RUS":
            #    embed=discord.Embed(title=f"__{ctx.author.name}__ добавил __`{video.title}`__ в плейлист",color=0xff7606)
            #elif await MusicBot.langueg(ctx) == "ENG":
            #    embed=discord.Embed(title=f"__{ctx.author.name}__ add __`{video.title}`__ in playlist",color=0xff7606)
            #await ctx.send(embed=embed)
            #return

        path1 = f'{self.home}/servers/{guild.id}'
        # прочитаем файл построчно
        with open(f'{path1}/music_queue.txt', 'r') as f:
            lines = f.readlines()
        try:
            next_ = lines[0]
            next_video = pafy.new(next_) #получаем видео
            title_ = next_video.title
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                title_ = 'Больше нет песен'
            elif await MusicBot.langueg(ctx) == "ENG":
                title_ = 'No more songs'

        #title_ - исходный титл видео!!! @NikStor#5027 - не забудь!!

        #Вызываем плеер
        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title=f"**{video.title}**", url=url,
                description=f":white_small_square: **Лайков:  {video.likes} :thumbsup:**\n\n"
                f":white_small_square: **Дизлайков:  {video.dislikes} :thumbsdown:**\n\n"
                f":white_small_square: **Просмотров:  {video.viewcount} :eye: **\n\n"
                f":white_small_square: **Следушея песня:** *{title_}*\n\n", color=0xff7606)
            embed.set_author(name=f"❤ Рейтинг: {int(video.rating * 20)} ❤")
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
            embed.set_image(url=f'{video.bigthumb}')
            if (video.duration) == "00:00:00":
              embed.set_footer(text=f"•Прямой эфир\n•Автор: {video.author}")
            else:
              embed.set_footer(text=f"•Длительность видео: {video.duration}\n•Автор: {video.author}")
        elif await MusicBot.langueg(ctx) == "ENG":
            embed = discord.Embed(title=f"**{video.title}**", url=url,
                description=f":white_small_square: **Likes:  {video.likes} :thumbsup:**\n\n"
                f":white_small_square: **Dislikes:  {video.dislikes} :thumbsdown:**\n\n"
                f":white_small_square: **View count:  {video.viewcount} :eye:**\n\n"
                f":white_small_square: **Next song:** *{title_}*", color=0xff7606)
            embed.set_author(name=f"❤ Rating: {int(video.rating * 20)} ❤")
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
            embed.set_image(url=f'{video.bigthumb}')
            if (video.duration) == "00:00:00":
              embed.set_footer(text=f"•Live\n•Author: {video.author}")
            else:
              embed.set_footer(text=f"•Video duration: {video.duration}\n•Author: {video.author}")


        msg_play = await ctx.send(embed=embed)

        #Добовляем реакции
        self.msg_play = msg_play
        await self.msg_play.add_reaction(str("▶"))
        await self.msg_play.add_reaction(str("⏸"))
        await self.msg_play.add_reaction(str("🔊"))
        await self.msg_play.add_reaction(str("🔉"))
        await self.msg_play.add_reaction(str("⏹"))
        await self.msg_play.add_reaction(str("⏭️"))
        await self.msg_play.add_reaction(str("❤️"))

        fplayGo = True
        MusicBot.player = 1


async def main_play(self,ctx, arg):
    global playGo, global_voice
    guild = ctx.guild


    self.voice = get(self.bot.voice_clients, guild = ctx.guild)
    global_voice = self.voice
    try:
        channel = ctx.author.voice.channel
    except:
        if await MusicBot.langueg(ctx) == "RUS":
            embed=discord.Embed(title=f"**{ctx.author.name} Вы не в голосовом канале**",color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed=discord.Embed(title=f"**{ctx.author.name} You are not in the voice channel**",color=0xff7606)
        await ctx.send(embed=embed)
        return

    if self.voice and self.voice.is_connected():
        await self.voice.move_to(channel)
    else:
        self.voice = await channel.connect()

    #Проверяю если есть https://www.youtube.com/watch?v= в arg
    #Если да то url = arg
    if 'https://www.youtube.com/watch?v=' in arg:
        url = arg
    #Если нет
    elif arg != None:

        #embed для списка песен
        if await MusicBot.langueg(ctx) == "RUS":
            emb_list_music = discord.Embed(title="Выберите песню от 1 до 10\nИ нажмите на соответствующий смайл", color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG":
            emb_list_music = discord.Embed(title="Select a song from 1 to 10\nAnd click on the corresponding emoji", color=0xff7606)
        #Беру все id из findyoutube и перебераю их для того чтоб написать в embed
        i = 1
        global_video_id = await findyoutube(arg)
        for title in global_video_id[0]:
            emb_list_music.add_field(name=f"#{i}", value=f"{i} - **{title}**", inline=False)
            i += 1

        #Добавляю эмоции к сообщенитю смайлы
        msg_for_list = await ctx.send(embed=emb_list_music)
        await msg_for_list.add_reaction(str("1️⃣"))
        await msg_for_list.add_reaction(str("2️⃣"))
        await msg_for_list.add_reaction(str("3️⃣"))
        await msg_for_list.add_reaction(str("4️⃣"))
        await msg_for_list.add_reaction(str("5️⃣"))
        await msg_for_list.add_reaction(str("6️⃣"))
        await msg_for_list.add_reaction(str("7️⃣"))
        await msg_for_list.add_reaction(str("8️⃣"))
        await msg_for_list.add_reaction(str("9️⃣"))
        await msg_for_list.add_reaction(str("🔟"))

        #Проверяю на добовления эмоции
        try:
            r, u = await self.bot.wait_for('reaction_add', check=lambda r, u: r.message.id == msg_for_list.id and u.id == ctx.author.id, timeout=30)# Жду 30 сек
        except asyncio.TimeoutError as e:
            if await MusicBot.langueg(ctx) == "RUS":
                await ctx.send('**Вы выбираете так долго, придется заново ввести команду**')# если прошло 30 сек
            elif await MusicBot.langueg(ctx) == "ENG":
                await ctx.send('**You choose so long, you have to re-enter the command**')# если прошло 30 сек
            return
        #перебеарю все те айди которые там есть
        if str(r) == '1️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][0]}"
        elif str(r) == '2️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][1]}"
        elif str(r) == '3️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][2]}"
        elif str(r) == '4️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][3]}"
        elif str(r) == '5️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][4]}"
        elif str(r) == '6️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][5]}"
        elif str(r) == '7️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][6]}"
        elif str(r) == '8️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][7]}"
        elif str(r) == '9️⃣':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][8]}"
        elif str(r) == '🔟':
            url = f"https://www.youtube.com/watch?v={global_video_id[1][9]}"
        else:
            url = None

    #if url == NOen: pass
    if url == None:
        return
    #else
    else:
        self.vol = 0.60
        music_chanel_id = ctx.channel.id
        try:
            video = pafy.new(url)
            best = video.getbest()
            self.playurl = best.url
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                await ctx.send("**Что то не так с этим видео, извините**\n**Попробуйте снова, но уже другое ролик**")
            elif await MusicBot.langueg(ctx) == "ENG":
                await ctx.send("**Something is wrong with this video, I'm sorry.**\n**Try again, but another video.**")
            return

        try:
            self.voice.play(discord.FFmpegPCMAudio(self.playurl))

            self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
            self.voice.source.volume = self.vol
        except:#Если песня уже играет то мы добавим новую в список

            path1 = f'{self.home}/servers/{ctx.guild.id}'
            with open(f'{path1}/music_queue.txt','a',  encoding='Latin-1') as f:
                f.write(f'{url}\n')

            video = pafy.new(url)
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"__{ctx.author.name}__ добавил __`{video.title}`__ в плейлист",color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"__{ctx.author.name}__ add __`{video.title}`__ in playlist",color=0xff7606)
            await ctx.send(embed=embed)
            return

        path1 = f'{self.home}/servers/{guild.id}'

        # прочитаем файл построчно
        with open(f'{path1}/music_queue.txt', 'r') as f:
            lines = f.readlines()
        try:
            next_ = lines[0]
            next_video = pafy.new(next_) #получаем видео
            title_ = next_video.title
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                title_ = 'Больше нет песен'
            elif await MusicBot.langueg(ctx) == "ENG":
                title_ = 'No more songs'

        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title=f"**{video.title}**", url=url,
                description=f":white_small_square: **Лайков:  {video.likes} :thumbsup:**\n\n"
                f":white_small_square: **Дизлайков:  {video.dislikes} :thumbsdown:**\n\n"
                f":white_small_square: **Просмотров:  {video.viewcount} :eye: **\n\n"
                f":white_small_square: **Следушея песня:** *{title_}*\n\n", color=0xff7606)
            embed.set_author(name=f"❤ Рейтинг: {int(video.rating * 20)} ❤")
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
            embed.set_image(url=f'{video.bigthumb}')
            if (video.duration) == "00:00:00":
              embed.set_footer(text=f"•Прямой эфир\n•Автор: {video.author}")
            else:
              embed.set_footer(text=f"•Длительность видео: {video.duration}\n•Автор: {video.author}")
        elif await MusicBot.langueg(ctx) == "ENG":
            embed = discord.Embed(title=f"**{video.title}**", url=url,
                description=f":white_small_square: **Likes:  {video.likes} :thumbsup:**\n\n"
                f":white_small_square: **Dislikes:  {video.dislikes} :thumbsdown:**\n\n"
                f":white_small_square: **View count:  {video.viewcount} :eye:**\n\n"
                f":white_small_square: **Next song:** *{title_}*", color=0xff7606)
            embed.set_author(name=f"❤ Rating: {int(video.rating * 20)} ❤")
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
            embed.set_image(url=f'{video.bigthumb}')
            if (video.duration) == "00:00:00":
              embed.set_footer(text=f"•Live\n•Author: {video.author}")
            else:
              embed.set_footer(text=f"•Video duration: {video.duration}\n•Author: {video.author}")

        self.msg_play = await ctx.send(embed=embed)
        await self.msg_play.add_reaction(str("▶"))
        await self.msg_play.add_reaction(str("⏸"))
        await self.msg_play.add_reaction(str("🔊"))
        await self.msg_play.add_reaction(str("🔉"))
        await self.msg_play.add_reaction(str("⏹"))
        await self.msg_play.add_reaction(str("⏭️"))
        await self.msg_play.add_reaction(str("❤️"))


async def _id(num):
    return num["id"]["videoId"]


async def titel_func(num):
    return num["snippet"]["title"]



#Находим 10 выдео с ютуб
async def findyoutube(title):
    id_ = []
    titel_ = []

    yt = YouTubeDataAPI(next(MusicBot.YOUTUBE_API))

    video_id = yt.search(q=title,
            max_results=10,
            parser=None)
    for i in video_id:
        id_.append(await _id(i))
    for i in video_id:
        titel_.append(await titel_func(i))

    return titel_, id_


#Находим одно видео с ютуб
async def ffindyoutube(title):
    id_ = []

    yt = YouTubeDataAPI(next(MusicBot.YOUTUBE_API))

    video_id = yt.search(q=title,
            max_results=1,
            parser=None)
    for i in video_id:
        id_.append(i["id"]["videoId"])
    return id_

class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.home = os.getcwd()

    pafy.set_api_key(next(MusicBot.YOUTUBE_API))


    #----------------Пропустить песню-----------------#
    #Почему это сдесь???
    #Дело в том что мне надо сделать переменые для реакций, и сделать так что б без бд
    @commands.command(aliases = ["sk"])
    async def skip(self, ctx):


        path1 = f'{self.home}/servers/{ctx.guild.id}'

        # прочитаем файл построчно
        with open(f'{path1}/music_queue.txt', 'r') as f:
            lines = f.readlines()

        try:
            url = lines[0]
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                emb = discord.Embed(title=f"Плейлист сервера __{ctx.guild.name}__ пустой", color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                emb = discord.Embed(title=f"Playlist server __{ctx.guild.name}__ is empty", color=0xff7606)
            await ctx.send(embed=emb)
            return
        try:
            video = pafy.new(url)
            best = video.getbest()
            self.playurl = best.url
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                await ctx.send("**Что то не так с этим видео, извините**\n**Попробуйте снова, но уже другое ролик**")
            elif await MusicBot.langueg(ctx) == "ENG":
                await ctx.send("**Something is wrong with this video, I'm sorry.**\n**Try again, but another video.**")
            return

        #Запускаем поток
        self.voice.stop()
        self.voice.play(discord.FFmpegPCMAudio(self.playurl))

        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
        self.voice.source.volume = self.vol

        #Убираем первую строку из файла
        with open(f'{path1}/music_queue.txt', 'w') as f:
            f.writelines(lines[1:])

        # прочитаем файл построчно
        with open(f'{path1}/music_queue.txt', 'r') as f:
            lines = f.readlines()

        try:
            next_ = lines[0]
            next_video = pafy.new(next_) #получаем видео
            title_ = next_video.title
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                title_ = 'Больше нет песен'
            elif await MusicBot.langueg(ctx) == "ENG":
                title_ = 'No more songs'

        #Вызываем плеер
        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title=f"**{video.title}**", url=url,
                description=f":white_small_square: **Лайков:  {video.likes} :thumbsup:**\n\n"
                f":white_small_square: **Дизлайков:  {video.dislikes} :thumbsdown:**\n\n"
                f":white_small_square: **Просмотров:  {video.viewcount} :eye: **\n\n"
                f":white_small_square: **Следушея песня:** *{title_}*\n\n", color=0xff7606)
            embed.set_author(name=f"❤ Рейтинг: {int(video.rating * 20)} ❤")
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
            embed.set_image(url=f'{video.bigthumb}')
            if (video.duration) == "00:00:00":
              embed.set_footer(text=f"•Прямой эфир\n•Автор: {video.author}")
            else:
              embed.set_footer(text=f"•Длительность видео: {video.duration}\n•Автор: {video.author}")
        elif await MusicBot.langueg(ctx) == "ENG":
            embed = discord.Embed(title=f"**{video.title}**", url=url,
                description=f":white_small_square: **Likes:  {video.likes} :thumbsup:**\n\n"
                f":white_small_square: **Dislikes:  {video.dislikes} :thumbsdown:**\n\n"
                f":white_small_square: **View count:  {video.viewcount} :eye:**\n\n"
                f":white_small_square: **Next song:** *{title_}*", color=0xff7606)
            embed.set_author(name=f"❤ Rating: {int(video.rating * 20)} ❤")
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
            embed.set_image(url=f'{video.bigthumb}')
            if (video.duration) == "00:00:00":
              embed.set_footer(text=f"•Live\n•Author: {video.author}")
            else:
              embed.set_footer(text=f"•Video duration: {video.duration}\n•Author: {video.author}")

        msg = await ctx.send(embed=embed)
        await msg.add_reaction(str("▶"))
        await msg.add_reaction(str("⏸"))
        await msg.add_reaction(str("🔊"))
        await msg.add_reaction(str("🔉"))
        await msg.add_reaction(str("⏹"))
        await msg.add_reaction(str("⏭️"))
        await msg.add_reaction(str("❤️"))
        self.msg_play = msg

#----------------Плей первого попавшего видео---------#
    @commands.command(aliases = ["fp"])
    async def fplay(self,ctx, arg: str = None):
        if arg == None:
            return
        await main_fplay(self,ctx, arg)

#----------------Плей 10 песен--------------------#
    @commands.command(aliases = ["p"])
    async def play(self,ctx, arg: str = None):
        if arg == None:
            return
        await main_play(self,ctx, arg)


    @commands.command(aliases = ["vol"])
    async def volume(self, ctx, volume:float = 50):
        if volume > 100:
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"Максимум допустимое число это 100", color=0xf4680b)
                await ctx.send(embed=embed)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"The maximum allowed number is 100", color=0xf4680b)
                await ctx.send(embed=embed)
            return
        else:
            volume = volume / 100
            self.vol = volume
            self.voice.source.volume = self.vol
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"`Горомкость сейчас: {int(self.vol*100)}%`", color=0xf4680b)
                embed.set_author(name=f"Пользователь {ctx.author.name} изменил громкость", icon_url=f"{ctx.author.avatar_url}")
                mess = await ctx.send(embed=embed)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"`Volume now: {int(self.vol*100)}%`", color=0xf4680b)
                embed.set_author(name=f"User {ctx.author.name} changed the volume", icon_url=f"{ctx.author.avatar_url}")
                mess = await ctx.send(embed=embed)
            await asyncio.sleep(4)
            await mess.delete()




#----------------Рабочие кнопки-------------------#
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)

        message = await channel.fetch_message(payload.message_id)
        member = discord.utils.get(message.guild.members, id=payload.user_id)
        guild = message.guild
        emoji = str(payload.emoji)
        if emoji == "▶" and member.bot == False and member.voice:
            await message.remove_reaction(payload.emoji, member)
            self.voice.resume()

            if await MusicBot.langueg(message) == "RUS":
                embed=discord.Embed(title=f"▶`Возобновление`▶", color=0xff7606)
                embed.set_author(name=f"Пользователь {member.name} возобновил прослушивание", icon_url=f"{member.avatar_url}")
                mess = await channel.send(embed=embed)
            elif await MusicBot.langueg(message) == "ENG":
                embed=discord.Embed(title=f"▶`Resumption`▶", color=0xff7606)
                embed.set_author(name=f"User {member.name} resumption listening", icon_url=f"{member.avatar_url}")
                mess = await channel.send(embed=embed)
            await asyncio.sleep(4)
            await mess.delete()

        elif emoji == "⏸" and member.bot == False and member.voice :
            if self.voice and self.voice.is_playing() and message.id == self.msg_play.id:
                self.voice.pause()
                await message.remove_reaction(payload.emoji, member)
                if await MusicBot.langueg(message) == "RUS":
                    embed=discord.Embed(title=f"⏸`Пауза`⏸", color=0xff7606)
                    embed.set_author(name=f"Пользователь {member.name} поставил музыку на паузу", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                elif await MusicBot.langueg(message) == "ENG":
                    embed=discord.Embed(title=f"⏸`Pause`⏸", color=0xff7606)
                    embed.set_author(name=f"User {member.name} put the music on pause", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                await asyncio.sleep(4)
                await mess.delete()

        elif emoji == "⏹" and member.bot == False and member.voice:
            if self.voice and self.voice.is_playing() and message.id == self.msg_play.id:
                self.voice.stop()
                await message.remove_reaction(payload.emoji, member)
                if await MusicBot.langueg(message) == "RUS":
                    embed=discord.Embed(title=f"⏹`Остановка мызыки`⏹", color=0xff7606)
                    embed.set_author(name=f"Пользователь {member.name} остановил всё веселье", icon_url=f"{member.avatar_url}")
                    await channel.send(embed=embed)
                elif await MusicBot.langueg(message) == "ENG":
                    embed=discord.Embed(title=f"⏹`Stopped music`⏹", color=0xff7606)
                    embed.set_author(name=f"User {member.name} stopped music", icon_url=f"{member.avatar_url}")
                    await channel.send(embed=embed)


        elif emoji == "⏭️" and member.bot == False and member.voice:
            if message.id == self.msg_play.id:
                try:
                    self.voice.stop()
                except:
                    pass

                # прочитаем файл построчно
                with open(f'{path1}/music_queue.txt', 'r') as f:
                    lines = f.readlines()
                try:
                    url = lines[0]
                except: #Если файл пустой
                    if await MusicBot.langueg(message) == "RUS":
                        emb = discord.Embed(title=f"Плейлист сервера {message.guild.name} пустой", color=0xff7606)
                    elif await MusicBot.langueg(message) == "ENG":
                        emb = discord.Embed(title=f"Playlist server {message.guild.name} is empty", color=0xff7606)
                    await channel.send(embed=emb)
                    return

                if await MusicBot.langueg(message) == "ENG":
                    embed=discord.Embed(title=f"⏭️`Skip`⏭️", color=0xff7606)
                    embed.set_author(name=f"User {member.name} skip song", icon_url=f"{member.avatar_url}")
                    await channel.send(embed=embed)
                if await MusicBot.langueg(message) == "RUS":
                    embed=discord.Embed(title=f"⏭️`Переключил`⏭️", color=0xff7606)
                    embed.set_author(name=f"Пользователь {member.name} переключил песню", icon_url=f"{member.avatar_url}")
                    await channel.send(embed=embed)

                #Запускаем поток

                path1 = f'{self.home}/servers/{guild.id}'

                try:
                    video = pafy.new(url)
                    best = video.getbest()
                    self.playurl = best.url
                except:
                    if await MusicBot.langueg(message) == "RUS":
                        await channel.send("**Что то не так с этим видео, извините**\n**Попробуйте снова, но уже другое ролик**")
                    elif await MusicBot.langueg(message) == "ENG":
                        await channel.send("**Something is wrong with this video, I'm sorry.**\n**Try again, but another video.**")
                    return

                self.voice.play(discord.FFmpegPCMAudio(self.playurl))

                self.voice.source = discord.PCMVolumeTransformer(voice.source)
                self.voice.source.volume = self.vol

                #Убираем первую строку из файла
                with open(f'{path1}/music_queue.txt', 'w') as f:
                    f.writelines(lines[1:])

                # прочитаем файл построчно
                with open(f'{path1}/music_queue.txt', 'r') as f:
                    lines = f.readlines()

                try:
                    next_ = lines[0]
                    next_video = pafy.new(next_) #получаем видео
                    title_ = next_video.title
                except:
                    if await MusicBot.langueg(message) == "RUS":
                        title_ = 'Больше нет песен'
                    elif await MusicBot.langueg(message) == "ENG":
                        title_ = 'No more songs'

                #Вызываем плеер
                if await MusicBot.langueg(message) == "RUS":
                    embed = discord.Embed(title=f"**{video.title}**", url=url,
                        description=f":white_small_square: **Лайков:  {video.likes} :thumbsup:**\n\n"
                        f":white_small_square: **Дизлайков:  {video.dislikes} :thumbsdown:**\n\n"
                        f":white_small_square: **Просмотров:  {video.viewcount} :eye: \n\n"
                        f":white_small_square: **Следушея песня:** *{title_}*\n\n", color=0xff7606)
                    embed.set_author(name=f"❤ Рейтинг: {int(video.rating * 20)} ❤")
                    embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
                    embed.set_image(url=f'{video.bigthumb}')
                    if (video.duration) == "00:00:00":
                      embed.set_footer(text=f"•Прямой эфир\n•Автор: {video.author}")
                    else:
                      embed.set_footer(text=f"•Длительность видео: {video.duration}\n•Автор: {video.author}")
                elif await MusicBot.langueg(message) == "ENG":
                    embed = discord.Embed(title=f"**{video.title}**", url=url,
                        description=f":white_small_square: **Likes:  {video.likes} :thumbsup:**\n\n"
                        f":white_small_square: **Dislikes:  {video.dislikes} :thumbsdown:**\n\n"
                        f":white_small_square: **View count:  {video.viewcount} :eye:**\n\n"
                        f":white_small_square: **Next song:** _{title_}_", color=0xff7606)
                    embed.set_author(name=f"❤ Rating: {int(video.rating * 20)} ❤")
                    embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/232265/screenshots/832385/turntable.gif")
                    embed.set_image(url=f'{video.bigthumb}')
                    if (video.duration) == "00:00:00":
                      embed.set_footer(text=f"•Live\n•Author: {video.author}")
                    else:
                      embed.set_footer(text=f"•Video duration: {video.duration}\n•Author: {video.author}")

                self.msg_play = await channel.send(embed=embed)
                await self.msg_play.add_reaction(str("▶"))
                await self.msg_play.add_reaction(str("⏸"))
                await self.msg_play.add_reaction(str("🔊"))
                await self.msg_play.add_reaction(str("🔉"))
                await self.msg_play.add_reaction(str("⏹"))
                await self.msg_play.add_reaction(str("⏭️"))
                await self.msg_play.add_reaction(str("❤️"))


        elif emoji == "🔉" and member.bot == False and member.voice:
            if self.voice and self.voice.is_playing() and message.id == self.msg_play.id:
                await message.remove_reaction(payload.emoji, member)
                if self.vol <= 0:
                    self.vol = 0
                    return
                else:
                    self.vol -= 0.05
                self.voice.stop()
                self.voice.play(discord.FFmpegPCMAudio(self.playurl))
                self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
                self.voice.source.volume = self.vol
                if await MusicBot.langueg(message) == "RUS":
                    embed=discord.Embed(title=f"`Горомкость сейчас: {int(self.vol*100)}%`", color=0xff7606)
                    embed.set_author(name=f"Пользователь {member.name} понизил громкость", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                elif await MusicBot.langueg(message) == "ENG":
                    embed=discord.Embed(title=f"`Volume now: {int(self.vol*100)}%`", color=0xff7606)
                    embed.set_author(name=f"User {member.name} lower volume", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                await asyncio.sleep(4)
                await mess.delete()

        elif emoji == "🔊" and member.bot == False and member.voice:
            if self.voice and self.voice.is_playing() and message.id == self.msg_play.id:
                await message.remove_reaction(payload.emoji, member)
                if self.vol >= 1:
                    self.vol = 1
                    return
                else:
                    self.vol += 0.05

                self.voice.stop()
                self.voice.play(discord.FFmpegPCMAudio(self.playurl))
                self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
                self.voice.source.volume = self.vol
                if await MusicBot.langueg(message) == "RUS":
                    embed=discord.Embed(title=f"`Горомкость сейчас: {int(self.vol*100)}%`", color=0xf4680b)
                    embed.set_author(name=f"Пользователь {member.name} повысил громкость", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                elif await MusicBot.langueg(message) == "ENG":
                    embed=discord.Embed(title=f"`Volume now: {int(self.vol*100)}%`", color=0xf4680b)
                    embed.set_author(name=f"User {member.name} upper volume", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                await asyncio.sleep(4)
                await mess.delete()

        elif emoji == "🔊" or emoji == "🔉" or emoji == "⏹" or emoji == "⏸" or emoji == "▶" and not member.voice:
            if self.voice and self.voice.is_playing() and not member.bot and message.id == self.msg_play.id:
                await message.remove_reaction(payload.emoji, member)
                if await MusicBot.langueg(message) == "RUS":
                    embed=discord.Embed(title=f"❌`Ошибка`❌", color=0xff7606)
                    embed.set_author(name=f"{member.name} я не вижу вас в голосовом чате", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                elif await MusicBot.langueg(message) == "ENG":
                    embed=discord.Embed(title=f"❌`Error`❌", color=0xff7606)
                    embed.set_author(name=f"{member.name} I don't see you in voice channel", icon_url=f"{member.avatar_url}")
                    mess = await channel.send(embed=embed)
                await asyncio.sleep(4)
                await mess.delete()

        else:
            return

def setup(bot):
    bot.add_cog(play(bot))
