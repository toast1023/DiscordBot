import discord
from discord.ext import commands
import youtube_dl


class Commands(commands.Cog):

	def __init__(self, client):
		self.client = client

	# @ commands.command()
	# async def clean(self, ctx, amount=5):
	# 	await ctx.channel.purge(limit=amount+1)

def setup(client):
	client.add_cog(Commands(client))