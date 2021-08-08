import discord
from discord.ext import commands
# import secrets
# import smtplib
#
# SENDER = "xxxxxxxxxxx@gmail.com"
# PASSWORD = "xxxxxxxxxxxxxxxx"
# SUBJECT = "TROJAN CS SOCIETY AUTHORIZATION KEY"


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @ commands.command()
    # async def prompt(self, ctx):
    #     # get server
    #     for guild in self.client.guild:
    #         # get members in server
    #         for member in guild.members:
        #
    #             # prompt for email
    #             await member.send(f'Hello {member.name}! Please enter your USC email')
        #
    #             # function that checks whether the string ends in @usc.edu
    #             def isUSCEmail(msg):
    #                 if msg.content.endswith('@usc.edu') and len(msg.content) > 8 and '@' not in msg.content[0:-8]:
    #                     return True
    #                 return False
        #
    #             # get member email
    #             memberEmail = await self.client.wait_for('message', check=isUSCEmail)
        #
    #             # create unique keyphrase
    #             authKey = secrets.token_hex(3)
        #
    #             # email body
    #             body = "Case sensitive authorization key: " + authKey
    #             # email header
    #             message = f"""From: {SENDER}
        # 			To: {memberEmail}
        # 			Subject: {SUBJECT}\n
        # 			{body}
        # 			"""
        #
    #             # send email
    #             server = smtplib.SMTP("smtp.gmail.com", 587)
    #             server.starttls()
    #             try:
    #                 server.login(SENDER, PASSWORD)
    #                 server.sendmail(SENDER, memberEmail, message)
    #             except smtplib.SMTPAuthenticationError:
    #                 pass
        #
    #             # prompt for key
    #             await member.send(f'A unique key has been sent to the USC email inputted above. Please reply with this key')
        #
    #             # get auth key input
    #             memberInput = await self.client.wait_for('message')
        #
    #             # compare input and actual key
    #             if memberInput == authKey:
    #                 await member.send('Correct input')
    #             else:
    #                 await member.send('Incorrect input')
        #
    #             # find way to store email (database?)


def setup(client):
    client.add_cog(Commands(client))
