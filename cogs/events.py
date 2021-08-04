import discord
from discord.ext import commands

class Events(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	# When someone joins the server
	async def on_member_join(self, member):
		# prompt for email
		await member.send(f'Hello {member.name}! Please enter your USC email')
		# function that checks whether the string ends in @usc.edu
		def isUSCEmail(msg):
			if msg.content.endswith('@usc.edu') and len(msg.content) > 8 and '@' not in msg.content[0:-8]:
				return True
			return False
		# get message
		message = await self.client.wait_for('message', check=isUSCEmail)

		# send verification email
		# do we want to verify using a link or a randomly generated keyphrase?
	
	# When someone voluntarily DM's the bot
	async def on_message(message):
		# If a user DM's the bot
		if message.guild is None and not message.author.bot:
			user = await client.fetch_user(message.author.id)
			await user.send(f'Hello {member.name}! Please enter your USC email')
			# ...
			


def setup(client):
	client.add_cog(Events(client))
