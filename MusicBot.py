import discord
import os,random,asyncio
from discord.ext import commands, tasks
import json
from itertools import cycle


async def custom_prefix(bot, message):
    home = os.getcwd()

    path1 = (f'{home}/servers/{message.guild.id}')
    with open(f'{path1}/config.json', 'r') as f:
        prefixes = json.load(f)#тут я прочитал то что там есть
    return prefixes["Prefix"] #Тут я возвращаю то значение которое есть в prefix

bot = commands.Bot(command_prefix=custom_prefix)


#Here you should put youtubeapi
YOUTUBE_API = cycle([str(os.environ.get("YT_API1")),
               str(os.environ.get("YT_API2")),
               str(os.environ.get("YT_API3")),
               str(os.environ.get("YT_API4")),
               str(os.environ.get("YT_API5"))
                    ])
#Here you should put in first nikname from yandex music, second password from yandex music
YANDEX_API = [str(os.environ.get("NIKNAME")), str(os.environ.get("PASSWORD"))]

#Удаление команд
bot.remove_command('help')


async def langueg(ctx):
    home = os.getcwd()
    try:
        path1 = (f'{home}/servers/{ctx.guild.id}')
        os.mkdir(path1)
        os.chdir(path1)
    except OSError:
        os.chdir(path1)
    with open(f'config.json', 'r') as f:
        lang = json.load(f)#тут я прочитал то что там есть
    os.chdir(home)
    return lang["Language"] #Тут я возвращаю то значение которое есть в prefix

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

#Загружаю коги
@bot.command()
async def load(ctx, extensions):
    bot.load_extensions(f'cogs.{extensions}')#Загрузка дополнений
    await ctx.send('loaded')

#Разгрузка
@bot.command()
async def reload(ctx, extensions):
    bot.unload_extension(f'cogs.{extensions}')#Розгрузка дополнений
    await ctx.send('unloaded')

@bot.command()
async def unload(ctx, extensions):
    bot.unload_extension(f'cogs.{extensions}')#Розгрузка дополнений
    bot.load_extensions(f'cogs.{extensions}')#Загрузка дополнений
    await bot.send('unload')





for filename in os.listdir('./cgs'): # Цикл перебирающий файлы в cogs
    if filename.endswith('.py'): # если файл кончается на .py, то это наш ког
        bot.load_extension(f'cgs.{filename[:-3]}')# загрузка дополнений



bot.run(str(os.environ.get("BOT_TOKEN")))
