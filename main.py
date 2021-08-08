import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
	print('Bot is ready')


# @client.command()
# async def loadCog(ctx, extension):
# 	client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run('ODcyMzcyMTI4ODAzMDgyMjkx.YQo52w.QIiwYJO2XPMkx9m2HL5L7qFeRv0')