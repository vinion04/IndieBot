# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER = os.getenv("DISCORD_SERVER")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#bot welcomees new members
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to our Discord server!')

#bot assigns strikes
@bot.command()
async def strike(ctx, member: discord.Member):
    print(f'Recieved member: {member}')
    role1 = discord.utils.get(ctx.guild.roles, name="1 STRIKE")
    role2 = discord.utils.get(ctx.guild.roles, name="2 STRIKES")
    role3 = discord.utils.get(ctx.guild.roles, name="3 STRIKES")

    #check if member has 1 strike
    if role1 in member.roles:
        if role2:
            await member.add_roles(role2)
            await member.remove_roles(role1)
            await ctx.send(f'{member.mention} has been assigned {role2}.')

    #check if member has 2 strikes
    elif role2 in member.roles:
        if role3:
            await member.add_roles(role3)
            await member.remove_roles(role2)
            await ctx.send(f'{member.mention} has been assigned {role3} and will no longer be able to work on the current game.')

    else:
        if role1:
            await member.add_roles(role1)
            await ctx.send(f'{member.mention} has been assigned {role1}.')

#bot responses
@bot.event
async def on_message(message):

    #"test"
    if message.content == "test":
        await message.channel.send('test complete ;)')

    #"what time is it"
    time_quotes = [
        'Hammer time!',
        'SUCK TIME',
        'Time for you to get a watch.'
    ]

    if message.content == "what time is it":
        response = random.choice(time_quotes)
        await message.channel.send(response)

    await bot.process_commands(message)

#start up
@bot.event
async def on_ready():
    for server in bot.guilds:
        if server.name == SERVER:
            break
    print(f'{bot.user} is connected to the following server: \n'
          f'{server.name} (id: {server.id})')

    members = '\n - '.join([member.name for member in server.members])
    print(f'Server Members:\n - {members}')


bot.run(TOKEN)