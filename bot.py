import discord
from discord.ext import commands
from config import Config
from dotenv import load_dotenv
import os
from src.handlers.command_handler import CommandHandler

# Cargar variables de entorno
load_dotenv()

# Inicializar el bot con el prefijo de comando y los intents
intents = discord.Intents.default()
intents.message_content = True  # Habilitar el intent de contenido de mensaje
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

# Cargar el token de las variables de entorno
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("El token de Discord no está configurado en las variables de entorno.")
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name} (ID: {bot.user.id})')
    print('------')

handler = CommandHandler(bot)

bot.run(TOKEN)