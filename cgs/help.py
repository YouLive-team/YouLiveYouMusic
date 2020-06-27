## -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import os
import json
import random
try:
    import MusicBot
except:pass
class help_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        self.name  = 20
        global page
        global p1,p2,p3,p4, p5
        home = os.getcwd()
        path1 = (f'{home}/servers/{ctx.guild.id}')
        with open(f'{path1}/config.json', 'r') as f:
            prefixes = json.load(f)#тут я прочитал то что там есть

        prefix = prefixes["Prefix"]
        if await MusicBot.langueg(ctx) == "RUS":
            p1 ="""
```
╔════════════╦══════════════════════════════════════════════╗
║  m.play    ║            Играет тебе музыку!               ║
║  (m.p)     ║  m.play [ютуб-url], m.play [название музыки] ║
╠════════════╬══════════════════════════════════════════════╣
║  m.fplay   ║  Для тех, кто не хочет ждать(я вас понимаю)  ║
║  (m.fp)    ║ m.fplay [ютуб-url], m.fplay [название музыки]║
╠════════════╬══════════════════════════════════════════════╣
║  m.youtube ║  Хотите посмотреть какое-то видео на ютуб?   ║
║  (m.yt)    ║        m.youtube [название видео]            ║
╠════════════╬══════════════════════════════════════════════╣
║  m.yaplay  ║      Проигрывать музыку из "Яндекс музыка"   ║
║  (m.yap)   ║                 m.yaplay                     ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
            p2 = """
```
╔════════════╦══════════════════════════════════════════════╗
║   m.add    ║       Добавляет музыку в ваш плейлист        ║
║            ║  m.add [ютуб-url], m.add [название музыки]   ║
╠════════════╬══════════════════════════════════════════════╣
║  m.purge   ║  Первая песня в вашем плейлисте удаляется    ║
║  (m.del)   ║                 m.purge                      ║
╠════════════╬══════════════════════════════════════════════╣
║  m.clear   ║             Очищает плейлист                 ║
║  (m.cls)   ║                 m.clear                      ║
╠════════════╬══════════════════════════════════════════════╣
║ m.playlist ║     Показывает весь плейлист на сервере      ║
║  (m.pl)    ║               m.playlist                     ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
            p3 = """
```
╔════════════╦══════════════════════════════════════════════╗
║  m.volume  ║      Установите громкость музыки вручную     ║
║  (m.vol)   ║         m.volume [значение в процентах]      ║
╠════════════╬══════════════════════════════════════════════╣
║   m.skip   ║     Пропустить трэк, которая сейчас играет   ║
║   (m.sk)   ║                 m.skip                       ║
╠════════════╬══════════════════════════════════════════════╣
║   m.join   ║      Бот присоединится к воис-каналу,        ║
║   (m.j)    ║           где находится заказчик             ║
╠════════════╬══════════════════════════════════════════════╣
║   m.leave  ║        Бот уйдет из воис-каналу              ║
║   (m.l)    ║                m.leave                       ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
            p4 = """
```
╔════════════╦══════════════════════════════════════════════╗
║ m.set_lang ║            Установите язык боту              ║
║  (m.lang)  ║           m.set_lang [RUS или ENG]           ║
╠════════════╬══════════════════════════════════════════════╣
║m.set_prefix║          Установить префикс боту             ║
║  (m.pre)   ║     m.set_prefix [максимум 2 символа]        ║
╠════════════╬══════════════════════════════════════════════╣
║  m.help    ║ Это команда, которую Вы вызвали,  как дизайн?║
║  (m.h)     ║               m.help                         ║
╠════════════╬══════════════════════════════════════════════╣
║  m.donate  ║  If you do not mind donating a few coins :3  ║
║   (m.d)    ║                m.donate                      ║
╚════════════╩══════════════════════════════════════════════╝
```
"""
            p5 = """
```
╔════════════╦══════════════════════════════════════════════╗
║m.info_creat║           Информация о создателях            ║
║(m.creators)║           и как с ними связаться             ║
╠════════════╬══════════════════════════════════════════════╣
║ m.info_bot ║              Информация о боте :3            ║
║  (m.bot)   ║                 m.info_bot                   ║
╠════════════╬══════════════════════════════════════════════╣
║  префикс   ║     Увидеть префикс, если вы забыли его      ║
║            ║                  префикс                     ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
        elif await MusicBot.langueg(ctx) == "ENG":
            p1 ="""
```
╔════════════╦══════════════════════════════════════════════╗
║  m.play    ║           Playing music to you!              ║
║  (m.p)     ║   m.play [youtube-url], m.play [music name]  ║
╠════════════╬══════════════════════════════════════════════╣
║  m.fplay   ║      For those who do not want to wait       ║
║  (m.fp)    ║   m.play [youtube-url], m.play [music name]  ║
╠════════════╬══════════════════════════════════════════════╣
║  m.youtube ║     Want to watch some video on YouTube?     ║
║  (m.yt)    ║           m.youtube [video title]            ║
╠════════════╬══════════════════════════════════════════════╣
║  m.yaplay  ║         Play music from Yandex Music         ║
║  (m.h)     ║                 m.yaplay                     ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
            p2 = """
```
╔════════════╦══════════════════════════════════════════════╗
║   m.add    ║         Adds music to your playlist          ║
║            ║   m.play [youtube-url], m.play [music name]  ║
╠════════════╬══════════════════════════════════════════════╣
║  m.purge   ║  The first song in your playlist is deleted  ║
║  (m.del)   ║                 m.purge                      ║
╠════════════╬══════════════════════════════════════════════╣
║  m.clear   ║             Clears a playlist                ║
║  (m.cls)   ║                 m.clear                      ║
╠════════════╬══════════════════════════════════════════════╣
║ m.playlist ║    Shows the entire playlist on the server   ║
║  (m.pl)    ║               m.playlist                     ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
            p3 = """
```
╔════════════╦══════════════════════════════════════════════╗
║  m.volume  ║           Set music volume manually          ║
║  (m.vol)   ║          m.volume [percentage value]         ║
╠════════════╬══════════════════════════════════════════════╣
║   m.skip   ║     Skip the track that is currently playing ║
║   (m.sk)   ║                 m.skip                       ║
╠════════════╬══════════════════════════════════════════════╣
║   m.join   ║     The bot will join the voice channel,     ║
║   (m.j)    ║           where is the customer              ║
╠════════════╬══════════════════════════════════════════════╣
║   m.leave  ║     The bot will leave the voice channel     ║
║   (m.l)    ║                m.leave                       ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
            p4 = """
```
╔════════════╦══════════════════════════════════════════════╗
║ m.set_lang ║              Set bot language                ║
║  (m.lang)  ║           m.set_lang [RUS or ENG]            ║
╠════════════╬══════════════════════════════════════════════╣
║m.set_prefix║               Set bot prefix                 ║
║  (m.pre)   ║      m.set_prefix [max. 2 characters]        ║
╠════════════╬══════════════════════════════════════════════╣
║  m.help    ║  Is this the command you call, how a design? ║
║  (m.h)     ║                 m.help                       ║
╠════════════╬══════════════════════════════════════════════╣
║  m.donate  ║  If you do not mind donating a few coins :3  ║
║   (m.d)    ║                m.donate                      ║
╚════════════╩══════════════════════════════════════════════╝
```
    """
            p5 = """
```
╔════════════╦══════════════════════════════════════════════╗
║m.info_creat║        Information about the creators        ║
║(m.creators)║           and how to contact them            ║
╠════════════╬══════════════════════════════════════════════╣
║ m.info_bot ║              Bot information :3              ║
║  (m.bot)   ║                 m.info_bot                   ║
╠════════════╬══════════════════════════════════════════════╣
║   prefix   ║         See the prefix if you forget it      ║
║            ║                  prefix                      ║
╚════════════╩══════════════════════════════════════════════╝
```
"""
        embed=discord.Embed(title=f"[1/5]", description=f"{p1}", color=0xff7606)
        if await MusicBot.langueg(ctx) == "RUS":
            embed.set_footer(text="ВНИМАНИЕ! если вы меняли префикс то вместо 'm.' надо использовать ваш префикс")
        elif await MusicBot.langueg(ctx) == "ENG":
            embed.set_footer(text="ATTENTION! if you changed the prefix then instead of 'm.' need to use your prefix")

        msg = await ctx.send(embed=embed)

        await msg.add_reaction(str('⬅️'))
        await msg.add_reaction(str('➡️'))
        page = 0

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            global page
            global p1,p2,p3,p4, p5
            channel = self.bot.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = discord.utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
            pages = [p1,p2,p3,p4,p5]
    
    
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            
            if emoji == "➡️" and member.bot == False:
                page += 1
                await message.remove_reaction(payload.emoji, member)
            elif emoji == "⬅️" and member.bot == False:
                page -= 1
    
                await message.remove_reaction(payload.emoji, member)
            else:
                return
            if page <= 0:
                page = 0
            elif page >= 5:
                page = 4
            embed=discord.Embed(title=f"[{page+1}/5]", description=f"{pages[page]}", color=0xff7606)
            if await MusicBot.langueg(message) == "RUS":
                embed.set_footer(text="ВНИМАНИЕ! если вы меняли префикс то вместо 'm.' надо использовать ваш префикс")
            elif await MusicBot.langueg(message) == "ENG":
                embed.set_footer(text="ATTENTION! if you changed the prefix then instead of 'm.' need to use your prefix")

            await message.edit(embed=embed)
        except: pass


def setup(bot):
    bot.add_cog(help_(bot))


