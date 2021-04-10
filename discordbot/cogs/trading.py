import asyncio, discord, json,requests
from discord.ext import commands
from discord.utils import get
from rooturl import baseurl
import datetime

class Trading(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.trading())

    async def trading(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(30)
            trade_data=requests.get(f'{baseurl}trading/').json()
            for item in trade_data:
                #tradedata
                tradeid=item['id']
                subleagueid=item['team']['season']['subleague']['id']
                leagueid=item['team']['season']['subleague']['league']['id']
                teamname=item['team']['teamname']
                teamabbreviation=item['team']['teamabbreviation']
                logo=item['team']['logo']
                addedpokemon=item['added_pokemon']['name']
                sprite=item['added_pokemon']['sprite']
                droppedpokemon=item['dropped_pokemon']['name']
                weekeffective=item['weekeffective']
                #get channel data
                tradedata=requests.get(f'{baseurl}discord_settings/{subleagueid}/').json()
                server=tradedata['server']
                tradechannel=tradedata['tradechannel']
                #get guild
                goi=get(self.bot.guilds,id=server)
                channel=get(goi.channels,id=tradechannel)
                embed=discord.Embed(
                    title=f"In the latest blockbuster trade, the {teamname} ({teamabbreviation}) have picked up {addedpokemon} in exchange for their {droppedpokemon}.", 
                    url=f"https://pokemondraftleagueonline.herokuapp.com/league/{leagueid}/subleague/{subleagueid}/trading/", 
                    description=f"This will be effective Week {weekeffective}. Go to https://pokemondraftleagueonline.herokuapp.com/league/{leagueid}/subleague/{subleagueid}/trading/ for more information.")
                embed.set_thumbnail(url=logo)
                embed.set_image(url=sprite)
                #embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=embed)
                url=f'{baseurl}trading/{tradeid}/'
                data={'announced':True}
                update=requests.put(url,data = data)
                if update.status_code == 200:
                    print("updated")
                else:
                    print("error")

def setup(bot):
    bot.add_cog(Trading(bot))