import discord
from discord.ext import commands
from discord.ui import Button, View

class WikiView(View):
    def __init__(self, url):
        super().__init__(timeout=None)
        self.add_item(Button(label="Ir a la Wiki", style=discord.ButtonStyle.link, url=url, emoji="📖"))

def setup(bot):
    @bot.slash_command(name="wiki", description="Muestra la wiki oficial de Bandicraft Network.")
    async def wiki(ctx):
        url = "https://wiki.bandicraft.net"
        embed = discord.Embed(
            title="📖 Wiki Oficial",
            description=f"Consulta la wiki de Bandicraft Network: [wiki.bandicraft.net]({url})",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed, view=WikiView(url))
