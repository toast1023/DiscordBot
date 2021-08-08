import discord
from discord.ext import commands
import secrets
import smtplib

# global constants
SENDER = "usc.email.verify@gmail.com"
PASSWORD = "UscemailbotPW"
SUBJECT = "TROJAN CS SOCIETY AUTHORIZATION KEY"


class Events(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_message(self, message):

		user = None

		# if a user DM's the bot
		if message.guild is None and not message.author.bot:
			# fetch the user
			user = await self.client.fetch_user(message.author.id)

		# edge case user DNE
		if not user:
			return False
		
		# check if the message is to validate USC email
		if message.content.lower() != 'verify email':
			return False

		# prompt user for USC email
		await user.send(f'Hello {user.name}! Please enter your USC email')

		# function to verify whether input was a formatted as a valid USC email
		def isUSCEmail(msg):
			if msg.content.endswith('@usc.edu') and len(msg.content) > 8 and '@' not in msg.content[0:-8]:
				return True
			return False

		# wait for a valid USC email to be inputted
		memberEmail = None
		try:
			memberEmail = await self.client.wait_for(event='message', check=isUSCEmail, timeout=300)
		except:
			await user.send('Session has timed out, please message the bot again with "verify email" to restart the email verification process')
			return False

		# edge case email DNE
		if not memberEmail:
			return False

		# create unique keyphrase
		authKey = secrets.token_hex(3)

		# email body
		body = 'Case sensitive authorization key: ' + authKey
		message = f'Subject: {SUBJECT}\n\n{body}'

		# create smtp instance
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()

		# try to log in to email and send email
		try:
			server.login(SENDER, PASSWORD)
			server.sendmail(SENDER, memberEmail.content, message)
		except smtplib.SMTPAuthenticationError:
			return False
		
		# prompt for key
		await user.send(f'A unique key has been sent to the USC email inputted above. Please reply with this key in the next 5 minutes')

		# get auth key input
		try: 
			await self.client.wait_for(event='message', check=lambda x: x.content == authKey, timeout=300)
		except:
			await user.send('Session has timed out, please message the bot again with "verify email" to restart the email verification process')
			return False

		await user.send('Your USC email has been validated!')
		return True


def setup(client):
    client.add_cog(Events(client))
