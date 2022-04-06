import asyncio, discord, json,requests
from discord.ext import commands
from discord.utils import get
from rooturl import baseurl
import datetime

class Draft(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.draft())

    async def draft(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(30)
            #run on outbids
            outbid_data=requests.get(f'{baseurl}outbid/').json()
            for bid in outbid_data:
                try:
                    #pickdata
                    bidid=bid['id']
                    userid=bid['user']
                    text=bid['text']
                    discorduser = await self.bot.fetch_user(userid)
                    channel = await discorduser.create_dm()
                    await channel.send(f"You have been outbid for {text}. If you would like to bid again, please visit the draftsite before the timer expires.")
                    url=f'{baseurl}outbid/{bidid}/'
                    data={'announced':True}
                    update=requests.put(url,data = data)
                    if update.status_code == 200:
                       print("updated")
                    else:
                        print("error")
                except Exception as e:
                    print(e)
            # run on draft
            """
            draft_data=requests.get(f'{baseurl}draft/').json()
            for pick in draft_data:
                try:
                    #pickdata
                    draftid=pick['id']
                    subleagueid=pick['team']['season']['subleague']['id']
                    leagueid=pick['team']['season']['subleague']['league']['id']
                    picknumber=pick['picknumber']
                    teamname=pick['team']['teamname']
                    teamabbreviation=pick['team']['teamabbreviation']
                    logo=pick['team']['logo']
                    pokemon=pick['pokemon']['name']
                    sprite=pick['pokemon']['sprite']
                    points=pick['points']
                    #get channel data
                    draft_data=requests.get(f'{baseurl}discord_settings/{subleagueid}/').json()
                    server=draft_data['server']
                    draftchannel=draft_data['draftchannel']
                    #get guild
                    goi=get(self.bot.guilds,id=server)
                    channel=get(goi.channels,id=draftchannel)
                    upnextuser=None
                    try:
                        nextpick=requests.get(f'{baseurl}draft/nextpick/{subleagueid}/{picknumber}/').json()
                        upnextuser=await self.bot.fetch_user(nextpick['userid'])
                        desc=f"The {nextpick['teamname']} ({nextpick['teamabbreviation']}), coached by {nextpick['username']}, are now on the clock. Please go to https://pokemondraftleagueonline.herokuapp.com/league/{leagueid}/subleague/{subleagueid}/draft/ to input your pick."
                    except:
                        desc=f"The draft has completed. Please go to https://pokemondraftleagueonline.herokuapp.com/league/{leagueid}/subleague/{subleagueid}/draft/ to see the complete draft."
                    embed=discord.Embed(
                        title=f"With pick number {picknumber} of the draft, the {teamname} ({teamabbreviation}) have selected {pokemon} for {points} points.", 
                        url=f"https://pokemondraftleagueonline.herokuapp.com/league/{leagueid}/subleague/{subleagueid}/draft/", 
                        description=desc)
                    embed.set_thumbnail(url=logo)
                    embed.set_image(url=sprite)
                    #embed.timestamp = datetime.datetime.utcnow()
                    await channel.send(embed=embed)
                    if upnextuser:
                        await channel.send(upnextuser.mention)
                    url=f'{baseurl}draft/{draftid}/'
                    data={'announced':True}
                    update=requests.put(url,data = data)
                    if update.status_code == 200:
                        print("updated")
                    else:
                        print("error")
                except Exception as e:
                    print(e)
        """

def setup(bot):
    bot.add_cog(Draft(bot))