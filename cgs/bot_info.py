import discord
from discord.ext import commands
from discord.utils import get
try:
    import MusicBot
except:pass

class about_bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["creators"])
    async def info_creat(self, ctx):
        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title="Создатели", color=0xff7606)
            embed.add_field(name="Cоздатели:", value="<@!398538710993600523>, <@!501089151089770517>", inline=False)
            embed.add_field(name="Где можно связаться с создателями:", value="[#ТыЖПрограммист](https://discord.gg/UFYE9wR) - здесь вы можете связатся с <@!398538710993600523>"
                "\n[AmlTego RU](https://discord.gg/s56geYQ) - здесь вы можете связатся с <@!501089151089770517>")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/705754869163753486/724921157954043914/unknown.png")
            await ctx.author.send(embed=embed)
        elif await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title="Creators", color=0xff7606)
            embed.add_field(name="Creators:", value="<@!398538710993600523>, <@!501089151089770517>", inline=False)
            embed.add_field(name="Where can I contact the creators:", value="[#YouAreAProgrammer](https://discord.gg/UFYE9wR) - here you can contact <@!398538710993600523>"
                "\n[AmlTego RU](https://discord.gg/s56geYQ) - here you can contact <@!501089151089770517>")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/705754869163753486/724921157954043914/unknown.png")
            await ctx.author.send(embed=embed)

    @commands.command(aliases = ["d"])
    async def donate(self, ctx):
        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title="Пожертвование", 
                description=
                "Вы действительно решили нам задонатить:3 ?\n"
                "Мы будем рады каждой копейке, "
                "ведь благодаря вашим пожертвований, "
                "мы можем продвигать нашего бота вперед.\n"
                "Все деньги идут на поддержку нашего бота!!!\n"
                "С уважением <@!501089151089770517> и <@!398538710993600523>",
                color=0xff7606, url="https://www.donationalerts.com/r/youliveyoumusic")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/705754869163753486/724921157954043914/unknown.png")
            await ctx.author.send(embed=embed)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed = discord.Embed(title="Donation", 
                description=
                "You really decided to donate to us:3 ?\n"
                "We will be happy for every coin, "
                "because thanks to your donations, "
                "we can push our bot forward.\n"
                "All the money goes to support our bot!!!\n"
                "Respectfully <@!501089151089770517> и <@!398538710993600523>",
                color=0xff7606, url="https://www.donationalerts.com/r/youliveyoumusic")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/705754869163753486/724921157954043914/unknown.png")
            await ctx.author.send(embed=embed)

    @commands.command(aliases = ["bot"])
    async def info_bot(self, ctx):
        all_person = 0
        for i in self.bot.guilds:
            if i.bot:
                return
            all_person += i.member_count

        if await MusicBot.langueg(ctx) == "RUS":
            embed = discord.Embed(title="Биография бота", color=0xff7606)

            embed.add_field(name="Сервера", value=f"Я нахожусь на {len(self.bot.guilds)} серверах", inline=False)
            embed.add_field(name="Пользователи", value=f"Мною пользуются {all_person} пользователей", inline=False)

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/705754869163753486/724921157954043914/unknown.png")
            await ctx.send(embed=embed)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed = discord.Embed(title="Bot Biography", color=0xff7606)

            embed.add_field(name="Servers", value=f"I am on {len(self.bot.guilds)} servers", inline=False)
            embed.add_field(name="Users", value=f"Use me {all_person} of users", inline=False)

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/705754869163753486/724921157954043914/unknown.png")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(about_bot(bot))