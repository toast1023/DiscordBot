import discord
from discord.ext import commands
import secrets
import smtplib

# global constants
SENDER = "xxxxxxxxxxx@gmail.com"
PASSWORD = "xxxxxxxxxxxxxxxx"
SUBJECT = "TROJAN CS SOCIETY AUTHORIZATION KEY"


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(message):
        # If a user DM's the bot
        if message.guild is None and not message.author.bot:
            # fetch the user
            user = await client.fetch_user(message.author.id)
            # edge case user DNE
            if not user:
                return False
            # prompt user for USC email
            await user.send(f'Hello {member.name}! Please enter your USC email')

            # function to verify whether input was a formatted as a valid USC email
            def isUSCEmail(msg):
                if msg.content.endswith('@usc.edu') and len(msg.content) > 8 and '@' not in msg.content[0:-8]:
                    return True
                return False

            # wait for a valid USC email to be inputted
            memberEmail = await self.client.wait_for('message', check=isUSCEmail)
            # create unique keyphrase
            authKey = secrets.token_hex(3)

            # email body
            body = "Case sensitive authorization key: " + authKey
            # email header
            message = f"""From: {SENDER}
			To: {memberEmail}
			Subject: {SUBJECT}\n
			{body}
			"""

            # create smtp instance
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            # try to log in to email and send email
            try:
                server.login(SENDER, PASSWORD)
                server.sendmail(SENDER, memberEmail, message)
            except smtplib.SMTPAuthenticationError:
                pass
            # prompt for key
            await member.send(f'A unique key has been sent to the USC email inputted above. Please reply with this key')
            # get auth key input
            memberInput = await self.client.wait_for('message', lambda x: x == authKey)

            return True


def setup(client):
    client.add_cog(Events(client))
