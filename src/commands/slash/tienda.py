import discord
from discord.ext import commands
from discord.ui import Button, View

class TiendaView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Ir a la Tienda", style=discord.ButtonStyle.link, url="https://tienda.bandicraft.net", emoji="🛒"))

def setup(bot):
    @bot.slash_command(name="tienda", description="Muestra la tienda oficial de Bandicraft Network.")
    async def tienda(ctx):
        url = "https://tienda.bandicraft.net"
        embed = discord.Embed(
            title="🛒 Tienda Oficial",
            description=f"Visita nuestra tienda: [tienda.bandicraft.net]({url})",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed, view=TiendaView())
