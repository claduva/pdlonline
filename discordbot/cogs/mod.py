import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amount:int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{amount} messages got deleted')
    
    @clear.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("You need to specify an amount!")
        if isinstance(error,commands.BadArgument):
            await ctx.send("Give an integer!")
        raise error

    @commands.command()
    @commands.is_owner()
    async def reload(self,ctx,cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"{cog} got reloaded!")
        except Exception as e:
            print(f"{cog} could not be loaded!")

def setup(bot):
    bot.add_cog(Mod(bot))