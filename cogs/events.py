import discord
from discord.ext import commands
from database import cursor, connection
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
            print('awaiting email input')
            memberEmail = await self.client.wait_for(event='message', check=isUSCEmail, timeout=30)
        except:
            await user.send('Session has timed out, please message the bot again with "verify email" to restart the email verification process')
            return False

        print('done getting member email')

        # edge case email DNE
        if not memberEmail:
            return False

        print(memberEmail)

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
            print('ISSUE')
            return False

        # prompt for key
        await user.send(f'A unique key has been sent to the USC email inputted above. Please reply with this key in the next 5 minutes')

        # get auth key input
        try:
            await self.client.wait_for(event='message', check=lambda x: x.content == authKey, timeout=300)
        except:
            await user.send('Session has timed out, please message the bot again with "verify email" to restart the email verification process')
            return False

        # query database for existing user
        cursor.execute("SELECT * FROM users WHERE email=:email",
                       {'email': memberEmail.content})
        existingUser = cursor.fetchone()

        # if no user with inputted email exists, add to database
        if not existingUser:
            cursor.execute("INSERT INTO users VALUES (:email, :id, :num_reg)",
                           {'email': memberEmail.content, 'id': user.id, 'num_reg': 0})
            try:
                connection.commit()
            except:
                connection.rollback()
                await user.send('An error has occured associating your email. Please contact a Trojan CS Society moderator')
        # if the email is already associated with a user
        else:
            # if the usernames match, no need for change
            if user.id == existingUser[1]:
                await user.send('This USC email has already been validated and is associated with your current discord account')
                return True
            # if trying to reassociate email to a different account
            else:
                # if user has reassociated less than 3 times
                if existingUser[2] < 3:
                    # prompt user if they would like to reassociate
                    await user.send(
                        f'''This USC email is currently associated with a different discord account. Would you like to associate it with this one instead?
                        changes remaining: {3-existingUser[2]}
                        enter y/n'''
                    )

                    # wait for user input yes or no
                    reassociate = None
                    try:
                        reassociate = await self.client.wait_for(event='message', check=lambda x: x.content == 'y' or x.content == 'n', timeout=300)
                    except:
                        await user.send('Session has timed out, please message the bot again with "verify email" to restart the email verification process')
                        return False

                    # if yes, update user in database
                    if reassociate.content == 'y':
                        cursor.execute("UPDATE users SET num_reg=:num_reg, id=:id WHERE email=:email",
                                       {'num_reg': existingUser[2] + 1, 'id': user.id, 'email': memberEmail.content})
                        try:
                            connection.commit()
                        except:
                            connection.rollback()
                            await user.send('An error has occured associating your email. Please contact a Trojan CS Society moderator')
                    # if no
                    else:
                        await user.send('Your USC email will remain associated with your current discord account')
                        return True

        await user.send('Your USC email has been validated!')
        return True


def setup(client):
    client.add_cog(Events(client))
