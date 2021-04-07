import asyncio, discord, json,requests
from discord.ext import commands
from discord.utils import get

class BotMessages(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.send_bot_messages())

    async def send_bot_messages(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            bot_messages=requests.get(f'http://localhost:8000/api/bot_message/').json()
            for message in bot_messages:
                try:
                    recipient = await self.bot.fetch_user(message['recipient']['discordid'])
                    sender = await self.bot.fetch_user(message['sender']['discordid'])
                    content=f"{sender.mention} ({message['sender']['username']}) has sent you a message via pokemondraftleague.online!\n\n{message['message']}"
                    channel = await recipient.create_dm()
                    await channel.send(content)
                except:
                    print("Message failed")
                x = requests.delete(f"http://localhost:8000/api/bot_message/{message['id']}")
                print(x.status_code)
            await asyncio.sleep(30)

def setup(bot):
    bot.add_cog(BotMessages(bot))