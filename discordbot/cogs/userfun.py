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
        await ctx.send(f"I've let Sleepy know he sucks for you. No thanks needed. It was my pleasure (Just a friendly reminder his username used to be SoggyWaffle, so he had it coming). {sleepy.mention}, in case you blocked me...You suck.")
    
    @commands.command(aliases=[])
    async def sleepycringe(self,ctx):
        await ctx.send(f"Ive learned a lot about myself as a player. Ive finished around the top of the standings most (every? idk) seasons; BUT having lots of help from teammates shows me that i totally have things that i miss in prep that they help make up for. Cb zong is a perfect example from last week. Sure I was 1-0 that week but that bit of advice was very important. There was that one season i forfeit 2 games that didn't matter which makes my record look bad but the games i played that meant something i did well lol. Record shows im a good player. But even still i miss things in prep. Still have room for improvement")

    @commands.command(aliases=["iaremoose"])
    async def moose(self,ctx):
        embed=discord.Embed(title="I came here to chew grass and fuck bitches. And I'm all out of grass.", colour=discord.Colour.red())
        embed.set_image(url="https://www.pbs.org/wnet/nature/files/2016/02/Moose16-c.gif")
        await ctx.send(embed=embed)

    @commands.command(aliases=["marryme"])
    async def marrymemoose(self,ctx):
        moose = await self.bot.fetch_user("259499391843303427")
        def check(reaction, user):
            return user == moose and reaction.emoji in ["🇾","🇳"]
        msg=await ctx.send(f"{moose.mention}... Will you marry me?")
        await msg.add_reaction("🇾")
        await msg.add_reaction("🇳")
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=3000.0, check=check)
            if reaction.emoji=="🇾":
                await ctx.send(f"This is the greatest day of my bot life.")
            else:
                await ctx.send(f"I'm heartbroken.")
        except:
            pass

def setup(bot):
    bot.add_cog(Userfun(bot))