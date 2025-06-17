import discord
from discord.ext import commands
from mcstatus import JavaServer

# Comando /status para mostrar el estado del servidor de Minecraft

def setup(bot):
    @bot.slash_command(name="status", description="Muestra el estado del servidor de Minecraft.")
    async def status(ctx):
        ip_servidor = "bandicraft.ulaloud.com"
        logo_url = "https://i.imgur.com/g3F2unj.jpeg"  # Cambia esta URL por el logo real si tienes otro
        try:
            server = JavaServer.lookup(ip_servidor)
            status = server.status()
            jugadores = status.players.online
            max_jugadores = status.players.max
            version = "1.13x - 1.21x"  # Cambia esto si el rango de versiones es diferente
            embed = discord.Embed(
                title="🟢 Bandicraft Network - Servidor Online",
                description=f"**IP:** `{ip_servidor}`\n**Versión:** `{version}`\n**Jugadores conectados:** `{jugadores}/{max_jugadores}`",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=logo_url)
            embed.set_footer(text="¡Conéctate y juega ahora mismo!", icon_url=logo_url)
        except Exception:
            embed = discord.Embed(
                title="🔴 Bandicraft Network - Servidor Offline",
                description=f"No se pudo obtener el estado de `{ip_servidor}`.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=logo_url)
            embed.set_footer(text="Intenta más tarde o revisa la IP.", icon_url=logo_url)
        await ctx.respond(embed=embed)
