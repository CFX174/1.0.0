import discord
from discord.ext import commands
import os
import importlib.util

class CommandHandler:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.load_commands('src/commands/prefix')
        self.load_commands('src/commands/slash')

    def load_commands(self, folder_path):
        if not os.path.exists(folder_path):
            return
        for filename in os.listdir(folder_path):
            if filename.endswith('.py'):
                module_path = os.path.join(folder_path, filename)
                spec = importlib.util.spec_from_file_location(filename[:-3], module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'setup'):
                    module.setup(self.bot)

# Ejemplo de uso en bot.py:
# from src.handlers.command_handler import CommandHandler
# handler = CommandHandler(bot)
