"""
    This creates the discord bots servers then passes of most
    other responsibility to helper functions and classes.
"""

import os
import discord
from dotenv import load_dotenv
from MessageHandler import MessageHandler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
messageHandler = MessageHandler()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    response = messageHandler.handle_message(message, client)
    if response != "":
        await message.channel.send(response)


client.run(TOKEN)



