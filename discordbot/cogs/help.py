import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(aliases=["site"])
    async def website(self,ctx):
        embed=discord.Embed(title="Pokemon Draft League Online",description="Site for Pokemon Draft Leagues", colour=discord.Colour.red(),url="http://pokemondraftleague.online/")
        embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=ctx.author.name,icon_url=ctx.author.avatar_url)
        embed.set_image(url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))