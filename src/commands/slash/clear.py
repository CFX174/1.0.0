import discord
from discord.ext import commands

# Comando /clear para borrar mensajes

def setup(bot):
    @bot.slash_command(name="clear", description="Borra una cantidad de mensajes del canal actual.")
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, cantidad: int):
        if cantidad < 1 or cantidad > 100:
            await ctx.respond("Debes indicar un número entre 1 y 100.", ephemeral=True)
            return
        await ctx.channel.purge(limit=cantidad)
        await ctx.respond(f"🧹 Se han borrado {cantidad} mensajes.", ephemeral=True)
