import discord
from discord.ext import commands
from discord.ui import Button, View

class IPView(View):
    def __init__(self, ip):
        super().__init__(timeout=None)
        self.ip = ip

    @discord.ui.button(label="Copiar IP", style=discord.ButtonStyle.primary, emoji="📋")
    async def copiar_ip(self, button: Button, interaction: discord.Interaction):
        await interaction.response.send_message(f"IP copiada: `{self.ip}`", ephemeral=True)

# Comando /ip para mostrar la IP del servidor

def setup(bot):
    @bot.slash_command(name="ip", description="Muestra la IP y versión del servidor de Minecraft.")
    async def ip(ctx):
        ip_servidor = "bandicraft.ulaloud.com"
        version = "1.13x - 1.21x"
        embed = discord.Embed(
            title="🌐 IP del Servidor",
            description=f"La IP de Bandicraft Network es: **{ip_servidor}**\nVersión: **{version}**",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed, view=IPView(ip_servidor))
