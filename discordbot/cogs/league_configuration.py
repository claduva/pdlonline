import discord, requests
from discord.ext import commands
from discord.utils import get
#baseurl="http://localhost:8000/api/"
baseurl="https://pokemondraftleagueonline.herokuapp.com/api/"

class LeagueConfiguration(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(aliases=["cl"])
    async def configure_league(self,ctx):
        #initialize variables
        emojis=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        def check_react(reaction, user):
            return user == ctx.author and reaction.emoji in emojis
        await ctx.send("What is the name of the league you are configuring? Pick the corresponding emoji.")
        url=f'{baseurl}user/{ctx.author.id}/'
        user_data = requests.get(url).json()
        emojidict = await configureLeagueOptions(ctx,self.bot,emojis,user_data['leagues'])
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
            leagueid=emojidict[reaction.emoji]
        except:
            await ctx.send('Timed Out') 
            return
        invite = await ctx.channel.create_invite()
        url=f'{baseurl}leagues/{leagueid}/'
        update=requests.put(url,data = {'discordurl':f'https://discord.com/invite/{invite.code}/'},)
        if update.status_code == 200:
            await ctx.send('Great thank you!')
        else:
            await ctx.send('There was an error. Please contact claduva#3705') 
            return
        url=f'{baseurl}leagues/{leagueid}/'
        league_data = requests.get(url).json()
        if len(league_data['subleagues'])>0:
            await ctx.send("Now let's move on to configuring the subleagues.")
        for subleague in league_data['subleagues']:
            await ctx.send(f"Configuring {subleague[1]}")
            await ctx.send("Select the category containing your subleague's channels by reacting with the associated emoji.")
            filteredchannels=filter(lambda x: x.category == None, ctx.guild.channels)
            emojidict = await configureOptions(ctx,self.bot,emojis,filteredchannels)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
                subleaguecat=emojidict[reaction.emoji]
            except:
                await ctx.send('Timed Out') 
                return
            subleaguecategory=get(ctx.guild.channels,id=subleaguecat)
            filteredchannels=filter(lambda x: x.category == subleaguecategory, ctx.guild.channels)
            await ctx.send('Select you draft channel by reacting with the associated emoji.')
            emojidict = await configureOptions(ctx,self.bot,emojis,filteredchannels)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
                draftchannel=emojidict[reaction.emoji]
            except:
                await ctx.send('Timed Out') 
                return
            await ctx.send('Select you replays channel by reacting with the associated emoji.')
            filteredchannels=filter(lambda x: x.category == subleaguecategory, ctx.guild.channels)
            emojidict = await configureOptions(ctx,self.bot,emojis,filteredchannels)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
                replaychannel=emojidict[reaction.emoji]
            except:
                await ctx.send('Timed Out') 
                return
            await ctx.send('Select you free agency channel by reacting with the associated emoji.')
            filteredchannels=filter(lambda x: x.category == subleaguecategory, ctx.guild.channels)
            emojidict = await configureOptions(ctx,self.bot,emojis,filteredchannels)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
                fachannel=emojidict[reaction.emoji]
            except:
                await ctx.send('Timed Out') 
                return
            await ctx.send('Select you trading channel by reacting with the associated emoji.')
            filteredchannels=filter(lambda x: x.category == subleaguecategory, ctx.guild.channels)
            emojidict = await configureOptions(ctx,self.bot,emojis,filteredchannels)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
                tradechannel=emojidict[reaction.emoji]
            except:
                await ctx.send('Timed Out') 
                return
            data={
                'draftchannel':draftchannel,
                'replaychannel':replaychannel,
                'fachannel':fachannel,
                'tradechannel':tradechannel,
            }
            url=f'{baseurl}discord_settings/{subleague[0]}/'
            update=requests.put(url,data = data)
            if update.status_code == 200:
                await ctx.send(f"Great thank you! {subleague[1]}'s settings were updated.")
            else:
                await ctx.send('There was an error. Please contact claduva#3705') 

def setup(bot):
    bot.add_cog(LeagueConfiguration(bot))

async def configureLeagueOptions(ctx,bot,emojis,leagues):
    newline="\n"
    options=[]
    i=0
    emojidict={}
    reactemojis=[]
    for league in leagues:
        if i<10:
            options.append(f'{emojis[i]}{league[1]}')
            emojidict[emojis[i]]=league[0]
            reactemojis.append(emojis[i])
            i+=1
    options_join=newline.join(options)
    msg = await ctx.send(options_join)
    for emoji in reactemojis:
        await msg.add_reaction(emoji)
    return emojidict

async def configureOptions(ctx,bot,emojis,filteredchannels):
    newline="\n"
    options=[]
    i=0
    emojidict={}
    reactemojis=[]
    for channel in filteredchannels:
        if i<10:
            options.append(f'{emojis[i]}{channel.name}')
            emojidict[emojis[i]]=channel.id
            reactemojis.append(emojis[i])
            i+=1
    options_join=newline.join(options)
    msg = await ctx.send(options_join)
    for emoji in reactemojis:
        await msg.add_reaction(emoji)
    return emojidict