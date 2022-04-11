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
                print("-----------------")
                try:
                    matchid=item['id']
                    week=item['week']
                    playoff_week=item['playoff_week']
                    wtu = f"Week {week}" if week else playoff_week
                    team1=item['team1']['teamname']
                    team1a=item['team1']['teamabbreviation']
                    team1score=item['team1score']
                    team2=item['team2']['teamname']
                    team2a=item['team2']['teamabbreviation']
                    team2score=item['team2score']
                    try:
                        winner=item['winner']['teamname']
                        winnera=item['winner']['teamabbreviation']
                    except:
                        winner=None
                        winnera="None"
                    replay=item['replay']
                    try:
                        subleagueid=item['team1']['season']['subleague']['id']
                        leagueid=item['team1']['season']['subleague']['league']['id']
                    except:
                        archive(matchid)
                    #get channel data
                    matchdata=requests.get(f'{baseurl}discord_settings/{subleagueid}/').json()
                    try:
                        if matchdata['server'] is None:
                            archive(matchid)
                    except:
                        pass
                    try:
                        if matchdata['detail'] == 'Not found.':
                            archive(matchid)
                    except:
                        pass
                    server=matchdata['server']
                    fachannel=matchdata['replaychannel']
                    #get guild
                    goi=get(self.bot.guilds,id=server)
                    channel=get(goi.channels,id=fachannel)
                    if replay.find("Forfeit")>-1:
                        embed=discord.Embed(
                            title=f"{wtu}: {team1} ({team1a}) vs. {team2} ({team2a})", 
                            description=f"Replay: {replay}")
                    else:
                        embed=discord.Embed(
                            title=f"{wtu}: {team1} ({team1a}) vs. {team2} ({team2a})", 
                            url=replay, 
                            description=f"Replay: {replay}")
                    embed.add_field(name="Winner", value=f"||{winnera}||", inline=True)
                    embed.add_field(name="Score", value=f"||{team1score}-{team2score}||", inline=True)
                    #embed.timestamp = datetime.datetime.utcnow()
                    await channel.send(embed=embed)
                    archive(matchid)
                except Exception as e:
                    print(e)

def setup(bot):
    bot.add_cog(Match(bot))

def archive(matchid):
    url=f'{baseurl}match/{matchid}/'
    data={'announced':True}
    update=requests.put(url,data = data)
    if update.status_code == 200:
        print("updated")
    else:
        print("error")