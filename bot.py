import discord
from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "Bot online"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Online: {client.user}")

client.run("TU_TOKEN_AQUI")