#import dependencies
import asyncio, discord, itertools, os
from discord.ext import commands
from helperfunctions import getDiscordToken,loadCogs, change_pr

#set command prefix
#intents = discord.Intents().all()
#bot=commands.Bot(command_prefix="pdl.",intents=intents)
bot=commands.Bot(case_insensitive=True,command_prefix=["pdl.",'pdl!','Pdl.','Pdl!'])

#load cogs
loadCogs(bot)

#initialize bot
TOKEN=getDiscordToken()
bot.run(TOKEN)

#cycle bot status    
bot.loop.create_task(change_pr())