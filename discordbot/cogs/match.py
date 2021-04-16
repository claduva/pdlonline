import asyncio, discord, json,requests
from discord.ext import commands
from discord.utils import get
from rooturl import baseurl
import datetime

class Match(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.match())

    async def match(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(30)
            match_data=requests.get(f'{baseurl}match/').json()
            for item in match_data:
                try:
                    #fadata
                    faid=item['id']
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
                    matchdata=requests.get(f'{baseurl}discord_settings/{subleagueid}/').json()
                    server=matchdata['server']
                    fachannel=matchdata['replaychannel']
                    #get guild
                    goi=get(self.bot.guilds,id=server)
                    channel=get(goi.channels,id=fachannel)
                    embed=discord.Embed(
                        title=f"The {teamname} ({teamabbreviation}) have picked up {addedpokemon} in free agency. To make room on the roster, they have released {droppedpokemon}.", 
                        url=f"https://pokemondraftleagueonline.herokuapp.com/league/{leagueid}/subleague/{subleagueid}/free_agency/", 
                        description=f"This will be effective Week {weekeffective}. Go to https://pokemondraftleagueonline.herokuapp.com/league/{leagueid}/subleague/{subleagueid}/free_agency/ for more information.")
                    embed.set_thumbnail(url=logo)
                    embed.set_image(url=sprite)
                    #embed.timestamp = datetime.datetime.utcnow()
                    await channel.send(embed=embed)
                    url=f'{baseurl}free_agency/{faid}/'
                    data={'announced':True}
                    update=requests.put(url,data = data)
                    if update.status_code == 200:
                        print("updated")
                    else:
                        print("error")
                except Exception as e:
                    print(e)

def setup(bot):
    bot.add_cog(Match(bot))