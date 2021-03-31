import asyncio, discord, itertools, os

def getDiscordToken():
    try:
        from configuration import BOTTOKEN
        TOKEN=BOTTOKEN
    except:
        TOKEN=os.environ.get('BOTTOKEN')
    return TOKEN

def loadCogs(bot):
    for cog in os.listdir("discordbot/cogs"):
        if cog.endswith(".py") and not cog.startswith("_"):
            try:
                cog=f"cogs.{cog.replace('.py','')}"
                bot.load_extension(cog)
                print(f"{cog} was loaded!")
            except Exception as e:
                print(f"{cog} could not be loaded!")
                raise e

async def change_pr():
    await bot.wait_until_ready()
    statuslist=["pdl.help","http://pokemondraftleague.online/"]
    statuslist=itertools.cycle(statuslist)
    while not bot.is_closed():
        status=next(statuslist)
        await bot.change_presence(activity=discord.Game(status))
        await asyncio.sleep(5)