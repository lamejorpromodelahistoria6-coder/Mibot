import os
import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online: {client.user}")

client.run(os.environ["TOKEN"])