import sys
import os
import requests
import discord
import sched, time, asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
LAST_FETCH = "last_fetch.txt"
INTERVAL_TIME = 3600

def get_updates():
    url = "https://uconn.edu/public-notification/coronavirus/"
    print("Downloading from {}...".format(url))
    html = requests.get(url).text

    soup = BeautifulSoup(html, features="lxml")
    update_text = soup.body.find('div', attrs={'class':'fl-rich-text'}).text

    print(update_text)

    # Check if there was no update between this run and the last
    if os.path.exists(LAST_FETCH):
        with open(LAST_FETCH) as f:
            text = f.read()

        if update_text == text:
            print("No update needed.")
            return


    with open(LAST_FETCH, 'w+') as f:
        f.write(update_text)

    return update_text


print("Connecting to discord...")
client = discord.Client()

@client.event
async def on_ready():
    update_text = get_updates()
    if update_text is not None:
        guild = discord.utils.get(client.guilds, name=GUILD)
        channel = discord.utils.get(guild.channels, name="bot-test")
        print("Found channel: {}".format(channel))

        chunk_size = 2000
        for chunk in range(0, len(update_text), chunk_size):
            await channel.send(update_text[chunk:chunk+chunk_size])

    await asyncio.sleep(INTERVAL_TIME)
    await on_ready()


client.run(TOKEN)

