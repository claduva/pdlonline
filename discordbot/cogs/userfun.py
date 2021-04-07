import discord
from discord.ext import commands

class Userfun(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(aliases=["donnygif"])
    async def donny(self,ctx):
        embed=discord.Embed(title="Donny Sends His Regards", colour=discord.Colour.red())
        embed.set_image(url="https://cdn.discordapp.com/attachments/748662034802933943/748929003078811808/donnygif.gif")
        await ctx.send(embed=embed)

    @commands.command(aliases=["chezz"])
    async def chez(self,ctx):
        embed=discord.Embed(title="It's over. Chez has stolen your girl.", colour=discord.Colour.red())
        embed.set_image(url="https://media.discordapp.net/attachments/472241866427990036/775822586494976040/unknown.png")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["sleepysheepy"])
    async def sleepy(self,ctx):
        sleepy = await self.bot.fetch_user("248633879529783296")
        channel = await sleepy.create_dm()
        await channel.send(f"{ctx.author.mention} wants you to know that you suck.")
        await ctx.send(f"I've let Sleepy know he sucks for you. No thanks needed. It was my pleasure. {sleepy.mention}, in case you blocked me...You suck.")
    
    @commands.command(aliases=["iaremoose"])
    async def moose(self,ctx):
        embed=discord.Embed(title="I came here to chew grass and fuck bitches. And I'm all out of grass.", colour=discord.Colour.red())
        embed.set_image(url="https://www.pbs.org/wnet/nature/files/2016/02/Moose16-c.gif")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Userfun(bot))