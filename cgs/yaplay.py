import discord
from discord.ext import commands
import asyncio
from discord.utils import get
from yandex_music.client import Client
import logging
import os
import ffmpeg

try:
    import MusicBot
except: pass



class yaplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.home = os.getcwd()
    @commands.command(aliases = ["yap"])
    async def yaplay(self, ctx, arg: str = None):
        path1 = f'{self.home}/servers/{ctx.guild.id}'
        if arg == None:
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"Вы должны указать название трэка",color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"You must indicate the name of the track.",color=0xff7606)
            await ctx.send(embed=embed)
            return
        vol = 50
        self.vol = vol
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        try:
            channel = ctx.author.voice.channel
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"**{ctx.author.name} Вы не в голосовом канале**",color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"**{ctx.author.name} You are not in the voice channel**",color=0xff7606)
            await ctx.send(embed=embed)
            return

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        try:
            #Логирование (отключение)
            logger = logging.getLogger()
            logger.setLevel(logging.CRITICAL)

            #Подключенеи к акку
            client = Client.from_credentials(MusicBot.YANDEX_API[0], MusicBot.YANDEX_API[1]) #<--- Top password:3

            #Делаем поисковой запрос
            search = client.search(arg)

            #Получаем треки
            tracks = search.tracks

            #Сортируем треки в list
            results = tracks.results

            #Получаем первый трек
            track = results[0]

            #Получаем всю инфу по загрузке
            info = track.get_download_info(get_direct_links=True)
            #get_direct_links=True - обязательно надо, а то х*йня получается!!!!!!!!!
        except:
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"**{ctx.author.name} На данный момент песня уже играет**",color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"**{ctx.author.name} At the moment the song is already playing**",color=0xff7606)
            await ctx.send(embed=embed)
            return
        
        #Получаем полный путь к музыкальному файлу (поток)
        self.playurl = info[0].direct_link
        self.voice = voice

        self.voice.play(discord.FFmpegPCMAudio(self.playurl))

        self.voice.source = discord.PCMVolumeTransformer(voice.source)
        self.voice.source.volume = self.vol

        #Вызываем плеер

        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title=f"**{track.title}**",
                description=f":white_small_square: **ID:  {track.id} :game_die:**\n\n"
                f":white_small_square: **Регион: {track.regions[0]} :globe_with_meridians:**\n\n"
                f":white_small_square: **[Поделится](https://music.yandex.ru/track/{track.id}) :trumpet:\n\n", color=0xf2a20d)
            # ~ embed.set_thumbnail(url=f"{cover_uri}")
            # ~ embed.set_image(url=f'{track.og_image}')
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/851627/screenshots/2270820/record-player.gif")

            embed.set_footer(text=f"•Длительность трека: {int((track.duration_ms)/1000/60)} минут\n•Исполнитель: {track.artists[0].name}")
        elif await MusicBot.langueg(ctx) == "ENG":
            embed = discord.Embed(title=f"**{track.title}**",
                description=f":white_small_square: **ID:  {track.id} :game_die:**\n\n"
                f":white_small_square: **Region: {track.regions[0]} :globe_with_meridians:**\n\n"
                f":white_small_square: **[Share](https://music.yandex.ru/track/{track.id}) :trumpet:\n\n", color=0xf2a20d)
            # ~ embed.set_thumbnail(url=f"{cover_uri}")
            # ~ embed.set_image(url=f'{track.og_image}')
            embed.set_thumbnail(url=f"https://cdn.dribbble.com/users/851627/screenshots/2270820/record-player.gif")


        msg = await ctx.send(embed=embed)

        await msg.add_reaction(str("▶"))
        await msg.add_reaction(str("⏸"))
        await msg.add_reaction(str("🔊"))
        await msg.add_reaction(str("🔉"))
        await msg.add_reaction(str("⏹"))
        await msg.add_reaction(str("❤️"))
        self.msg_play = msg

#----------------Рабочие кнопки-------------------#
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)

        message = await channel.fetch_message(payload.message_id)
        member = discord.utils.get(message.guild.members, id=payload.user_id)
        guild = message.guild
        path1 = f'{self.home}/servers/{message.guild.id}'
        emoji = str(payload.emoji)
        try:
            if emoji == "▶" and member.bot == False and member.voice:
                if self.voice and self.voice.is_playing() and message.id == self.msg_play.id:
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
        except:
            return


def setup(bot):
    bot.add_cog(yaplay(bot))


