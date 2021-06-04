import discord
from discord.ext import commands

class Copypasta(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(aliases=[])
    async def arctozolt(self,ctx):
        await ctx.send("Arctozolt is the most broken mon in draft. What is your switch in bolt beak plus icicle crash. If your opponent think they are big brain and run bright powder, you run gravity and win. Arctozolt has no switch ins and should be going for 18 points or banned. Please spread.")
    
    @commands.command(aliases=[])
    async def fletchinder(self,ctx):
        await ctx.send("Fletchinder is the most broken mon in draft format. Priority acrobatics means it only needs one attack so in can run no speed. Comes in before rocks on the ground types that it is immune to. Deceptively good bulk without even needing eviolite. Fletchinder always has a good matchup. And all this for T5 unlike overrated Talonflame.")

    @commands.command(aliases=["megaabsol"])
    async def absol(self,ctx):
        await ctx.send("Absol is the worst mega in the game because it gives you hope that it might be good. It’s a relatively fast, relatively strong dark type that can reflect sr will o wisp etc with magic bounce, has knock sucker pursuit which are all super good moves, sd to sweep or break, and many coverage options. Mega Absol is good enough on paper where you might expect it to actually do something during the game. This is the main problem. The disparity between what you think the mon can do vs what it actually does is so massive that it’s a liability to your team. For example, you’d think bringing mega Absol would help vs an opposing mega latios right? Well they just stay in, live literally any hit, and ohko back. Surely mega Absol must be good against a mon like reuniclus right? Well I’ve seen Absol do exactly 34% to a reuni and die to focus blast. Absol is a good pursuit trapper for victini right? First of all, it doesn’t even kill if they switch, and if they stay in, you just die. When you have a mega banette/audino, you don’t expect much from it, and you don’t spend many points on it, so overall it’s not too bad. You get what you paid for. But Absol? No. You get far far less than you paid for, as Absol usually hovers around 2-2.5x the price of those lowest tier megas. This is why mega Absol is easily the worst mega in the draft league format.")

    @commands.command(aliases=[])
    async def forretress(self,ctx):
        await ctx.send("Forretress...just...sucks. Idk man.")

def setup(bot):
    bot.add_cog(Copypasta(bot))