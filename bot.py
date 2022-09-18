import os
import discord.utils, urllib.parse, urllib.request, re, discord, random, math, pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from discord.ext import commands

# tokens for bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# setting mongoDB database
cluster = MongoClient(
    "mongodb+srv://<user>:<password>@cluster0.4aslyra.mongodb.net/?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["karma"]

# setting up intents
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

######################################################## Events ###########################################################################

# check if connected
@bot.event
async def on_ready():
    print(f'{bot.user.name} bot has connect to Discord!')

# direct message new user when joining server
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the server!'
    )

# add role by reaction
@bot.event
async def on_raw_reaction_add(payload):

    if payload.emoji.name == 'upvote' or payload.emoji.name == 'downvote':
        channel = getChannelFromGuild(payload.guild_id, payload.channel_id)
        messages = [msg async for msg in channel.history(limit=200)]
        author = None
        for msg in messages:
            if msg.id == payload.message_id:
                author = msg.author.id
        if author:
            karmaAdd(author, payload.emoji, payload.member)

    message_id = payload.message_id
    if message_id == 1020826261758685214:  # change if need different message
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if payload.emoji.name == 'keycap':  # only if the role name is not the same name as emoji
            new_Role = discord.utils.get(guild.roles, name='keyboard')
        else:
            new_Role = discord.utils.get(guild.roles, name=payload.emoji.name)
        if new_Role:
            member = discord.utils.find(
                lambda m: m.id == payload.user_id, guild.members)
            if member:
                await member.add_roles(new_Role)
            else:
                print('member not found')
        else:
            print('role not found')

# remove role by reaction
@bot.event
async def on_raw_reaction_remove(payload):

    if payload.emoji.name == 'upvote' or payload.emoji.name == 'downvote':
        channel = getChannelFromGuild(payload.guild_id, payload.channel_id)
        messages = [msg async for msg in channel.history(limit=200)]
        author = None
        for msg in messages:
            if msg.id == payload.message_id:
                author = msg.author.id
        if author:
            karmaSub(author, payload.emoji, payload.user_id)

    message_id = payload.message_id
    if message_id == 1020826261758685214:  # change if need different message
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if payload.emoji.name == 'keycap':  # only if the role name is not the same name as emoji
            new_Role = discord.utils.get(guild.roles, name='keyboard')
        else:
            new_Role = discord.utils.get(guild.roles, name=payload.emoji.name)
        if new_Role:
            member = discord.utils.find(
                lambda m: m.id == payload.user_id, guild.members)
            if member:
                await member.remove_roles(new_Role)

######################################################## Commands ###########################################################################

# testing command
@bot.command(name='test')
async def test(ctx):
    await ctx.send("")

# flip coin
@bot.command(name='flip')
async def flip(ctx):
    coin = ['head', 'tail']
    randomVal = math.floor(random.random() * 2)
    await ctx.send(coin[randomVal])

# youtube search
@bot.command(name='youtube')
async def yt(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(
        r'/watch\?v=(.{11})', html_content.read().decode())
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

# return user score
@bot.command(name='karma')
async def getKarma(ctx):
    author = ctx.author.id
    if not collection.find_one(author):
        post = {"_id": author, "score": 0}
        collection.insert_one(post)
    user = collection.find_one(author)
    await ctx.send(ctx.author.name + " has " + str(user["score"]) + " karma")

# return keyboard websites
@bot.command(name='keyboard')
async def keeb(ctx):
    await ctx.send('Work in porgress')

######################################################## helper Functions ###########################################################################

# get the channel from guild
def getChannelFromGuild(guildId, channelId):
    guild = discord.utils.find(lambda g: g.id == guildId, bot.guilds)
    channel = discord.utils.find(lambda c: c.id == channelId, guild.channels)
    return channel

# update the karma of the author

def karmaAdd(author, emoji, reactor):
    if author == reactor.id:
        print("cant give self karma")
        return
    
    if not collection.find_one(author):
        post = {"_id": author, "score": 0}
        collection.insert_one(post)
    user = collection.find_one(author)
    if emoji.name == 'upvote':
        collection.update_one({"_id":user["_id"]}, {"$set": {"score": user["score"]+1}})
    else:
        collection.update_one({"_id": user["_id"]}, {"$set": {"score": user["score"]-1}})

def karmaSub(author, emoji, reactor):
    user = collection.find_one(author)
    if user["_id"] == reactor:
        return
    if emoji.name == 'upvote':
        collection.update_one({"_id":user["_id"]}, {"$set": {"score": user["score"]-1}})
    else:
        collection.update_one({"_id": user["_id"]}, {"$set": {"score": user["score"]+1}})

######################################################## end ###########################################################################
bot.run(TOKEN)