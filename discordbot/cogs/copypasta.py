import discord
from discord.ext import commands

class Copypasta(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(aliases=["Arctozolt"])
    async def arctozolt(self,ctx):
        await ctx.send("Arctozolt is the most broken mon in draft. What is your switch in bolt beak plus icicle crash. If your opponent think they are big brain and run bright powder, you run gravity and win. Arctozolt has no switch ins and should be going for 18 points or banned. Please spread.")
    
    @commands.command(aliases=["Fletchinder"])
    async def fletchinder(self,ctx):
        await ctx.send("Fletchinder is the most broken mon in draft format. Priority acrobatics means it only needs one attack so in can run no speed. Comes in before rocks on the ground types that it is immune to. Deceptively good bulk without even needing eviolite. Fletchinder always has a good matchup. And all this for T5 unlike overrated Talonflame.")

    @commands.command(aliases=["Forretress"])
    async def forretress(self,ctx):
        await ctx.send("Forretress...just...sucks. Idk man.")

def setup(bot):
    bot.add_cog(Copypasta(bot))