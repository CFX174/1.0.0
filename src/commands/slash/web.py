import discord
from discord.ext import commands
from discord.ui import Button, View

class WebView(View):
    def __init__(self, url):
        super().__init__(timeout=None)
        self.add_item(Button(label="Ir al sitio web", style=discord.ButtonStyle.link, url=url, emoji="🌐"))

def setup(bot):
    @bot.slash_command(name="web", description="Muestra el sitio web oficial de Bandicraft Network.")
    async def web(ctx):
        url = "https://bandicraft.net"
        embed = discord.Embed(
            title="🌐 Sitio Web Oficial",
            description=f"Visita nuestro sitio web: [bandicraft.net]({url})",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed, view=WebView(url))
