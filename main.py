import discord
import os

from service import Service
from repository import Repository

from dotenv import load_dotenv
from discord.ext import tasks



load_dotenv()

repository = Repository()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    checkAllBans.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('d!hello'):
        await message.channel.send('Hello!')

    elif message.content.startswith('d!add'):
        steam_url = message.content.split()[1]
        # check for valid steam account
        flag, steam_id = Service.isValidAccount(steam_url)
        if flag:
            response = repository.saveOne(steam_id)
            await message.channel.send(response)

        else:
            response = "Account does not exist"
            await message.channel.send(response)

    elif message.content.startswith('d!remove'):
        steam_url = message.content.split()[1]
        # check for valid steam account
        flag, steam_id = Service.isValidAccount(steam_url)
        if flag:
            response = repository.removeOne(steam_id)
            await message.channel.send(response)
        else:
                response = "Account does not exist"
                await message.channel.send(response)

    elif message.content.startswith('d!check'):
        steam_url = message.content.split()[1]
        # check for valid steam account
        flag, steam_id = Service.isValidAccount(steam_url)
        if flag:
            ban_flag, response = Service.checkBan(steam_id)
            await message.channel.send(response)

        else:
            response = "Account does not exist"
            await message.channel.send(response)
    
    elif message.content.startswith('d!troll'):
        await message.channel.send("aaj jeetnge, kl jeetnge, parso jeetnge. Roz harte hai!!")

@tasks.loop(hours=24)
async def checkAllBans():
    channel_id = os.getenv("VAC_WATCH_CHANNEL_ID")
    
    channel = await client.fetch_channel(channel_id)
    response = Service.checkAllBans(repository)

    if response != "":
        await channel.send(response)

client.run(os.getenv('BOT_TOKEN'))

