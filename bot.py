import os
import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# =====================
# INICIO
# =====================

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Sistema de Sorteos"))

# =====================
# SORTEOS
# =====================

@bot.command(name="sorteo")
@commands.has_permissions(administrator=True)
async def sorteo(ctx, duracion: int, ganadores: int = 1, *, premio: str):
    embed = discord.Embed(
        title="SORTEO",
        description=f"Premio: {premio}\nGanadores: {ganadores}\nReacciona con la carita de fiesta para participar\nDuracion: {duracion} segundos",
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Organizado por {ctx.author.name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(duracion)
    msg = await ctx.channel.fetch_message(msg.id)
    usuarios = []
    for reaction in msg.reactions:
        if str(reaction.emoji) == "🎉":
            async for user in reaction.users():
                if not user.bot:
                    usuarios.append(user)
    if not usuarios:
        await ctx.send("No hubo participantes.")
        return
    ganadores_lista = random.sample(usuarios, min(ganadores, len(usuarios)))
    menciones = ", ".join([g.mention for g in ganadores_lista])
    embed2 = discord.Embed(
        title="Tenemos ganador",
        description=f"Felicidades {menciones}\nPremio: {premio}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed2)

@bot.command(name="reroll")
@commands.has_permissions(administrator=True)
async def reroll(ctx, message_id: int):
    try:
        msg = await ctx.channel.fetch_message(message_id)
    except:
        await ctx.send("No encontre ese mensaje.")
        return
    usuarios = []
    for reaction in msg.reactions:
        if str(reaction.emoji) == "🎉":
            async for user in reaction.users():
                if not user.bot:
                    usuarios.append(user)
    if not usuarios:
        await ctx.send("No hay participantes.")
        return
    ganador = random.choice(usuarios)
    await ctx.send(f"Nuevo ganador: {ganador.mention}")

@bot.command(name="participantes")
async def participantes(ctx, message_id: int):
    try:
        msg = await ctx.channel.fetch_message(message_id)
    except:
        await ctx.send("No encontre ese mensaje.")
        return
    usuarios = []
    for reaction in msg.reactions:
        if str(reaction.emoji) == "🎉":
            async for user in reaction.users():
                if not user.bot:
                    usuarios.append(user.name)
    if not usuarios:
        await ctx.send("No hay participantes aun.")
        return
    embed = discord.Embed(
        title=f"Participantes: {len(usuarios)}",
        description="\n".join(usuarios),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name="sorteorapido")
@commands.has_permissions(administrator=True)
async def sorteorapido(ctx, *, premio: str):
    await ctx.invoke(sorteo, duracion=30, ganadores=1, premio=premio)

# =====================
# MENSAJES POR ID
# =====================

@bot.command(name="dm")
@commands.has_permissions(administrator=True)
async def dm(ctx, user_id: int, *, mensaje: str):
    try:
        usuario = await bot.fetch_user(user_id)
        await usuario.send(mensaje)
        await ctx.send(f"Mensaje enviado a {usuario.name}")
    except discord.Forbidden:
        await ctx.send("Ese usuario tiene los mensajes privados cerrados.")
    except discord.NotFound:
        await ctx.send("No encontre a ese usuario con ese ID.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="dmanuncio")
@commands.has_permissions(administrator=True)
async def dmanuncio(ctx, user_id: int, *, mensaje: str):
    try:
        usuario = await bot.fetch_user(user_id)
        embed = discord.Embed(
            title="Anuncio importante",
            description=mensaje,
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Enviado por {ctx.author.name}")
        await usuario.send(embed=embed)
        await ctx.send(f"Anuncio enviado a {usuario.name}")
    except discord.Forbidden:
        await ctx.send("Ese usuario tiene los mensajes privados cerrados.")
    except:
        await ctx.send("No pude enviar el mensaje.")

@bot.command(name="dmganador")
@commands.has_permissions(administrator=True)
async def dmganador(ctx, user_id: int, *, premio: str):
    try:
        usuario = await bot.fetch_user(user_id)
        embed = discord.Embed(
            title="Ganaste un sorteo",
            description=f"Felicidades, ganaste: {premio}\nContacta a un administrador para reclamar tu premio.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Servidor: {ctx.guild.name}")
        await usuario.send(embed=embed)
        await ctx.send(f"Notificacion de ganador enviada a {usuario.name}")
    except discord.Forbidden:
        await ctx.send("Ese usuario tiene los mensajes privados cerrados.")
    except:
        await ctx.send("No pude enviar el mensaje.")

# =====================
# MODERACION
# =====================

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, razon="Sin razon especificada"):
    await member.kick(reason=razon)
    await ctx.send(f"{member.name} fue expulsado. Razon: {razon}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, razon="Sin razon especificada"):
    await member.ban(reason=razon)
    await ctx.send(f"{member.name} fue baneado. Razon: {razon}")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    try:
        usuario = await bot.fetch_user(user_id)
        await ctx.guild.unban(usuario)
        await ctx.send(f"{usuario.name} fue desbaneado.")
    except:
        await ctx.send("No encontre ese usuario.")

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, segundos: int = 60):
    await member.timeout(discord.utils.utcnow() + discord.timedelta(seconds=segundos))
    await ctx.send(f"{member.name} fue silenciado por {segundos} segundos.")

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, cantidad: int = 10):
    await ctx.channel.purge(limit=cantidad + 1)
    msg = await ctx.send(f"Se borraron {cantidad} mensajes.")
    await asyncio.sleep(3)
    await msg.delete()

# =====================
# INFORMACION
# =====================

@bot.command(name="info")
async def info(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Info de {member.name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Se unio", value=member.joined_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Cuenta creada", value=member.created_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Roles", value=len(member.roles) - 1)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="servidor")
async def servidor(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=discord.Color.purple())
    embed.add_field(name="Miembros", value=ctx.guild.member_count)
    embed.add_field(name="Canales", value=len(ctx.guild.channels))
    embed.add_field(name="Roles", value=len(ctx.guild.roles))
    embed.add_field(name="Creado", value=ctx.guild.created_at.strftime("%d/%m/%Y"))
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar de {member.name}", color=discord.Color.blue())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="id")
async def get_id(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"El ID de {member.name} es: {member.id}")

# =====================
# UTILIDADES
# =====================

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Latencia: {round(bot.latency * 1000)}ms")

@bot.command(name="dado")
async def dado(ctx, caras: int = 6):
    resultado = random.randint(1, caras)
    await ctx.send(f"Tiraste un dado de {caras} caras y salio: {resultado}")

@bot.command(name="moneda")
async def moneda(ctx):
    resultado = random.choice(["Cara", "Cruz"])
    await ctx.send(f"La moneda cayo en: {resultado}")

@bot.command(name="elegir")
async def elegir(ctx, *, opciones: str):
    lista = opciones.split(",")
    eleccion = random.choice(lista).strip()
    await ctx.send(f"Elegi: {eleccion}")

@bot.command(name="recordatorio")
async def recordatorio(ctx, segundos: int, *, mensaje: str):
    await ctx.send(f"Te recordare en {segundos} segundos.")
    await asyncio.sleep(segundos)
    await ctx.send(f"{ctx.author.mention} Recordatorio: {mensaje}")

@bot.command(name="anuncio")
@commands.has_permissions(administrator=True)
async def anuncio(ctx, *, mensaje: str):
    embed = discord.Embed(
        title="Anuncio",
        description=mensaje,
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Por {ctx.author.name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    await ctx.send(embed=embed)

@bot.command(name="encuesta")
async def encuesta(ctx, *, pregunta: str):
    embed = discord.Embed(title="Encuesta", description=pregunta, color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(name="ayuda")
async def ayuda(ctx):
    embed = discord.Embed(title="Comandos disponibles", color=discord.Color.gold())
    embed.add_field(name="Sorteos", value="!sorteo <segundos> <ganadores> <premio>\n!reroll <id>\n!participantes <id>\n!sorteorapido <premio>", inline=False)
    embed.add_field(name="Mensajes privados", value="!dm <id_usuario> <mensaje>\n!dmanuncio <id_usuario> <mensaje>\n!dmganador <id_usuario> <premio>", inline=False)
    embed.add_field(name="Moderacion", value="!kick @usuario\n!ban @usuario\n!unban <id>\n!mute @usuario <segundos>\n!clear <cantidad>", inline=False)
    embed.add_field(name="Informacion", value="!info @usuario\n!servidor\n!avatar @usuario\n!id @usuario", inline=False)
    embed.add_field(name="Utilidades", value="!ping\n!dado <caras>\n!moneda\n!elegir opcion1, opcion2\n!recordatorio <segundos> <mensaje>\n!anuncio <mensaje>\n!encuesta <pregunta>", inline=False)
    await ctx.send(embed=embed)

# =====================
# ERRORES
# =====================

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para usar ese comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltan argumentos. Usa !ayuda para ver como usarlo.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("No encontre ese usuario.")

import json
import os

# =====================
# ECONOMIA - BASE DE DATOS
# =====================

ECONOMIA_FILE = "economia.json"

def cargar_economia():
    if not os.path.exists(ECONOMIA_FILE):
        return {}
    with open(ECONOMIA_FILE, "r") as f:
        return json.load(f)

def guardar_economia(data):
    with open(ECONOMIA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_usuario(user_id: str):
    data = cargar_economia()
    if user_id not in data:
        data[user_id] = {"billetera": 0, "banco": 0, "ultimo_trabajo": 0, "ultimo_diario": 0, "ultimo_robo": 0}
        guardar_economia(data)
    return data[user_id]

def actualizar_usuario(user_id: str, nuevo_datos: dict):
    data = cargar_economia()
    data[user_id] = nuevo_datos
    guardar_economia(data)

# =====================
# ECONOMIA - COMANDOS
# =====================

@bot.command(name="balance")
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    usuario = get_usuario(str(member.id))
    embed = discord.Embed(title=f"Balance de {member.name}", color=discord.Color.green())
    embed.add_field(name="Billetera", value=f"{usuario['billetera']} monedas")
    embed.add_field(name="Banco", value=f"{usuario['banco']} monedas")
    embed.add_field(name="Total", value=f"{usuario['billetera'] + usuario['banco']} monedas")
    await ctx.send(embed=embed)

@bot.command(name="diario")
async def diario(ctx):
    import time
    usuario = get_usuario(str(ctx.author.id))
    ahora = time.time()
    if ahora - usuario["ultimo_diario"] < 86400:
        restante = int(86400 - (ahora - usuario["ultimo_diario"]))
        horas = restante // 3600
        minutos = (restante % 3600) // 60
        await ctx.send(f"Ya recogiste tu diario. Vuelve en {horas}h {minutos}m.")
        return
    ganancia = random.randint(100, 300)
    usuario["billetera"] += ganancia
    usuario["ultimo_diario"] = ahora
    actualizar_usuario(str(ctx.author.id), usuario)
    await ctx.send(f"Recogiste tu recompensa diaria de {ganancia} monedas.")

@bot.command(name="trabajar")
async def trabajar(ctx):
    import time
    trabajos = [
        ("programador", 200, 500),
        ("cocinero", 150, 350),
        ("conductor", 100, 300),
        ("medico", 300, 600),
        ("maestro", 150, 400),
        ("musico", 100, 250),
        ("artista", 120, 280),
    ]
    usuario = get_usuario(str(ctx.author.id))
    ahora = time.time()
    if ahora - usuario["ultimo_trabajo"] < 3600:
        restante = int(3600 - (ahora - usuario["ultimo_trabajo"]))
        minutos = restante // 60
        await ctx.send(f"Ya trabajaste. Descansa {minutos} minutos mas.")
        return
    trabajo = random.choice(trabajos)
    ganancia = random.randint(trabajo[1], trabajo[2])
    usuario["billetera"] += ganancia
    usuario["ultimo_trabajo"] = ahora
    actualizar_usuario(str(ctx.author.id), usuario)
    await ctx.send(f"Trabajaste como {trabajo[0]} y ganaste {ganancia} monedas.")

@bot.command(name="depositar")
async def depositar(ctx, cantidad: str):
    usuario = get_usuario(str(ctx.author.id))
    if cantidad.lower() == "todo":
        cantidad = usuario["billetera"]
    else:
        cantidad = int(cantidad)
    if cantidad <= 0 or cantidad > usuario["billetera"]:
        await ctx.send("No tienes suficiente dinero en la billetera.")
        return
    usuario["billetera"] -= cantidad
    usuario["banco"] += cantidad
    actualizar_usuario(str(ctx.author.id), usuario)
    await ctx.send(f"Depositaste {cantidad} monedas en el banco.")

@bot.command(name="retirar")
async def retirar(ctx, cantidad: str):
    usuario = get_usuario(str(ctx.author.id))
    if cantidad.lower() == "todo":
        cantidad = usuario["banco"]
    else:
        cantidad = int(cantidad)
    if cantidad <= 0 or cantidad > usuario["banco"]:
        await ctx.send("No tienes suficiente dinero en el banco.")
        return
    usuario["banco"] -= cantidad
    usuario["billetera"] += cantidad
    actualizar_usuario(str(ctx.author.id), usuario)
    await ctx.send(f"Retiraste {cantidad} monedas del banco.")

@bot.command(name="transferir")
async def transferir(ctx, member: discord.Member, cantidad: int):
    if cantidad <= 0:
        await ctx.send("La cantidad debe ser mayor a 0.")
        return
    if member.id == ctx.author.id:
        await ctx.send("No puedes transferirte dinero a ti mismo.")
        return
    emisor = get_usuario(str(ctx.author.id))
    receptor = get_usuario(str(member.id))
    if emisor["billetera"] < cantidad:
        await ctx.send("No tienes suficiente dinero en la billetera.")
        return
    emisor["billetera"] -= cantidad
    receptor["billetera"] += cantidad
    actualizar_usuario(str(ctx.author.id), emisor)
    actualizar_usuario(str(member.id), receptor)
    await ctx.send(f"Transferiste {cantidad} monedas a {member.name}.")

@bot.command(name="robar")
async def robar(ctx, member: discord.Member):
    import time
    if member.id == ctx.author.id:
        await ctx.send("No puedes robarte a ti mismo.")
        return
    usuario = get_usuario(str(ctx.author.id))
    victima = get_usuario(str(member.id))
    ahora = time.time()
    if ahora - usuario["ultimo_robo"] < 7200:
        restante = int(7200 - (ahora - usuario["ultimo_robo"]))
        minutos = restante // 60
        await ctx.send(f"Debes esperar {minutos} minutos para robar de nuevo.")
        return
    if victima["billetera"] <= 0:
        await ctx.send(f"{member.name} no tiene dinero en la billetera.")
        return
    usuario["ultimo_robo"] = ahora
    exito = random.randint(1, 100)
    if exito > 45:
        robado = random.randint(1, min(victima["billetera"], 200))
        victima["billetera"] -= robado
        usuario["billetera"] += robado
        actualizar_usuario(str(ctx.author.id), usuario)
        actualizar_usuario(str(member.id), victima)
        await ctx.send(f"Lograste robarle {robado} monedas a {member.name}.")
    else:
        multa = random.randint(50, 150)
        usuario["billetera"] = max(0, usuario["billetera"] - multa)
        actualizar_usuario(str(ctx.author.id), usuario)
        await ctx.send(f"Te atraparon robando y pagaste una multa de {multa} monedas.")

@bot.command(name="apostar")
async def apostar(ctx, cantidad: int):
    usuario = get_usuario(str(ctx.author.id))
    if cantidad <= 0 or cantidad > usuario["billetera"]:
        await ctx.send("No tienes suficiente dinero.")
        return
    resultado = random.randint(1, 100)
    if resultado > 50:
        usuario["billetera"] += cantidad
        actualizar_usuario(str(ctx.author.id), usuario)
        await ctx.send(f"Ganaste la apuesta y obtuviste {cantidad} monedas.")
    else:
        usuario["billetera"] -= cantidad
        actualizar_usuario(str(ctx.author.id), usuario)
        await ctx.send(f"Perdiste la apuesta y se fueron {cantidad} monedas.")

@bot.command(name="ranking")
async def ranking(ctx):
    data = cargar_economia()
    lista = []
    for uid, info in data.items():
        total = info["billetera"] + info["banco"]
        lista.append((uid, total))
    lista.sort(key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title="Ranking de riqueza", color=discord.Color.gold())
    for i, (uid, total) in enumerate(lista[:10], 1):
        try:
            usuario = await bot.fetch_user(int(uid))
            nombre = usuario.name
        except:
            nombre = f"Usuario {uid}"
        embed.add_field(name=f"{i}. {nombre}", value=f"{total} monedas", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="dardinero")
@commands.has_permissions(administrator=True)
async def dardinero(ctx, member: discord.Member, cantidad: int):
    usuario = get_usuario(str(member.id))
    usuario["billetera"] += cantidad
    actualizar_usuario(str(member.id), usuario)
    await ctx.send(f"Le diste {cantidad} monedas a {member.name}.")

@bot.command(name="quitardinero")
@commands.has_permissions(administrator=True)
async def quitardinero(ctx, member: discord.Member, cantidad: int):
    usuario = get_usuario(str(member.id))
    usuario["billetera"] = max(0, usuario["billetera"] - cantidad)
    actualizar_usuario(str(member.id), usuario)
    await ctx.send(f"Le quitaste {cantidad} monedas a {member.name}.")
bot.run(os.environ["TOKEN"])