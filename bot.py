import discord
import socket
import asyncio
from discord.ext import commands, tasks

# Token del bot de Discord
TOKEN = 'TU_TOKEN_AQUI'

# Dirección IP y puerto de tu servidor de Minecraft
MINECRAFT_IP = '147.185.221.25'  # Cambia por la IP de tu servidor de Minecraft
MINECRAFT_PORT = 1258  # Por defecto es 25565

# Configura el bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Función para verificar si el servidor de Minecraft está activo
def check_minecraft_status():
    try:
        # Intentar conectar al servidor de Minecraft
        with socket.create_connection((MINECRAFT_IP, MINECRAFT_PORT), timeout=5):
            return True
    except (socket.timeout, socket.error):
        return False

# Tarea que se ejecuta periódicamente para comprobar el estado del servidor
@tasks.loop(minutes=5)
async def check_server_status():
    status = check_minecraft_status()
    channel = bot.get_channel(TU_CANAL_ID)  # Coloca el ID del canal donde quieres que se envíen los mensajes
    
    if status:
        await channel.send("¡El servidor de Minecraft está encendido!")
    else:
        await channel.send("El servidor de Minecraft está apagado.")

# Comando para iniciar el bot
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')
    check_server_status.start()  # Iniciar la tarea para verificar el estado del servidor

bot.run(TOKEN)
