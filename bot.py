import discord
import os
from flask import Flask
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO)

app = Flask("")

@app.route("/")
def home():
    return "Bot online"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_flask, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Online: {client.user}")

token = os.environ.get("TOKEN")
if not token:
    print("❌ ERROR: No se encontró el TOKEN")
else:
    print("🔑 Token encontrado, conectando...")
    client.run(token)