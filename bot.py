import discord
from discord.ext import commands, tasks
from mcstatus.server import JavaServer
import asyncio

# Configuración del bot
TOKEN = 'MTMyNjA0Njg0NTIxODE5MzUyMA.GNXqpN.ArC7jCqJv6hReNjeSrCqfnBr4HpCdG1uMFcQis'  # Reemplaza con el token de tu bot
GUILD_ID = '1312921447345160192'  # Reemplaza con el ID de tu servidor de Discord
CHANNEL_ID = '1312921447345160195'  # Reemplaza con el ID del canal donde quieres enviar mensajes
MINECRAFT_SERVER_HOST = 'HianeySMP.aternos.me'  # Cambia esto por el host de tu servidor
MINECRAFT_SERVER_PORT = 34892  # Cambia esto por el puerto de tu servidor

# URLs de las imágenes
SERVER_ON_IMAGE = "https://i.pinimg.com/736x/a6/20/c8/a620c8f7714e7aad2bed37d624953720.jpg"
SERVER_OFF_IMAGE = "https://i.pinimg.com/736x/85/5f/99/855f99168ed9f27920966c857adb812c.jpg"

# Crear intents y el bot
intents = discord.Intents.default()
intents.message_content = True  # Habilita la capacidad de leer el contenido de los mensajes

bot = commands.Bot(command_prefix='!', intents=intents)

# Función para verificar si el servidor de Minecraft está en línea
def is_minecraft_server_online():
    try:
        server = JavaServer.lookup(f"{MINECRAFT_SERVER_HOST}:{MINECRAFT_SERVER_PORT}")
        status = server.status()  # Intenta obtener el estado del servidor
        return True, status.players.online  # Devuelve True y la cantidad de jugadores en línea
    except Exception:
        return False, 0  # Devuelve False si el servidor no está disponible

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')
    check_server_status.start()  # Inicia la tarea periódica

# Comando para verificar el estado del servidor
@bot.command(name='status')
async def status(ctx):
    # Añadir un pequeño retraso al principio para asegurar que el bot esté listo
    await asyncio.sleep(5)

    is_online, players_online = is_minecraft_server_online()
    if is_online:
        embed = discord.Embed(
            title="┇         𝙈𝙄𝙉𝙀𝙎𝙀𝙍𝙑𝙀𝙍             ┇",
            description=(
                "——————✧◦♚◦✧——————⋆\n"
                "╰┈➤ **El Servidor actualmente se encuentra ENCENDIDO!**\n"
                f"╰┈➤ **Jugadores conectados:** `{players_online}`"
            ),
            color=discord.Color.green()
        )
        embed.set_image(url=SERVER_ON_IMAGE)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="┇         𝙈𝙄𝙉𝙀𝙎𝙀𝙍𝙑𝙀𝙍             ┇",
            description=(
                "——————✧◦♚◦✧——————⋆\n"
                "╰┈➤ **El Servidor actualmente se encuentra APAGADO.**"
            ),
            color=discord.Color.red()
        )
        embed.set_image(url=SERVER_OFF_IMAGE)
        await ctx.send(embed=embed)

# Tarea periódica para informar el estado del servidor cada 20 minutos
@tasks.loop(minutes=20)
async def check_server_status():
    # Obtiene el canal donde se enviarán los mensajes
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel is None:
        print(f"No se encontró el canal con ID {CHANNEL_ID}")
        return

    is_online, players_online = is_minecraft_server_online()
    if is_online:
        embed = discord.Embed(
            title="┇         𝙈𝙄𝙉𝙀𝙎𝙀𝙍𝙑𝙀𝙍             ┇",
            description=(
                "——————✧◦♚◦✧——————⋆\n"
                "╰┈➤ **El Servidor actualmente se encuentra ENCENDIDO!**\n"
                f"╰┈➤ **Jugadores conectados:** `{players_online}`"
            ),
            color=discord.Color.green()
        )
        embed.set_image(url=SERVER_ON_IMAGE)
    else:
        embed = discord.Embed(
            title="┇         𝙈𝙄𝙉𝙀𝙎𝙀𝙍𝙑𝙀𝙍             ┇",
            description=(
                "——————✧◦♚◦✧——————⋆\n"
                "╰┈➤ **El Servidor actualmente se encuentra APAGADO.**"
            ),
            color=discord.Color.red()
        )
        embed.set_image(url=SERVER_OFF_IMAGE)

    await channel.send(embed=embed)

# Manejo de errores al iniciar la tarea periódica
@check_server_status.before_loop
async def before_check_server_status():
    print("Esperando a que el bot esté listo...")
    await bot.wait_until_ready()

# Inicia el bot
bot.run(TOKEN)
