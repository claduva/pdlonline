import discord
from discord.ext import commands

class Poketwo(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    """
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id==716390085896962058:
            try:
                embed=message.embeds[0]
                if embed.title.find("A wild pokémon has appeared!")>-1:
                    data={
                        'title':embed.title,
                        'description':embed.description,
                        'fields':embed.fields,
                        'image':embed.image,
                    }
                    print(data)
                    await message.channel.send("p!c Lillipup")
            except:
                pass
    """

def setup(bot):
    bot.add_cog(Poketwo(bot))