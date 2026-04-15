import os
import sys
import discord
from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "online"

Thread(target=lambda: app.run(host="0.0.0.0", port=8080), daemon=True).start()

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    print("ERROR: TOKEN no encontrado", flush=True)
    sys.exit(1)

print(f"Token OK, largo: {len(TOKEN)}", flush=True)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online: {client.user}", flush=True)

try:
    client.run(TOKEN)
except Exception as e:
    print(f"Error al conectar: {e}", flush=True)
    sys.exit(1)