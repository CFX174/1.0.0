import discord
from discord.ext import commands
from discord.ui import Button, View

class RedesView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Instagram", style=discord.ButtonStyle.link, url="https://www.instagram.com/bandicraft_net", emoji="📸"))
        self.add_item(Button(label="Twitter", style=discord.ButtonStyle.link, url="https://twitter.com/BandiCraft_Net", emoji="🐦"))
        self.add_item(Button(label="YouTube", style=discord.ButtonStyle.link, url="https://youtube.com/@bandicraftnetwork", emoji="▶️"))

def setup(bot):
    @bot.slash_command(name="redes", description="Muestra las redes sociales oficiales de Bandicraft Network.")
    async def redes(ctx):
        embed = discord.Embed(
            title="🌐 Redes Sociales",
            description="¡Síguenos en nuestras redes sociales oficiales!",
            color=discord.Color.purple()
        )
        embed.add_field(name="Instagram", value="[bandicraftnetwork](https://www.instagram.com/bandicraft_net)", inline=True)
        embed.add_field(name="Twitter", value="[bandicraftnet](https://twitter.com/BandiCraft_Net)", inline=True)
        embed.add_field(name="YouTube", value="[@bandicraftnetwork](https://youtube.com/@bandicraftnetwork)", inline=True)
        await ctx.respond(embed=embed, view=RedesView())
