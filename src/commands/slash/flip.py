import discord
from discord.ext import commands
from discord.ui import Button, View
import logging

# Diccionario para llevar el marcador de los duelos
scoreboard = {}


class CaraSelloView(View):
    def __init__(self, ctx, jugadores, key):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.jugadores = jugadores
        self.key = key
        self.elecciones = {}
        self.resultado = None

    @discord.ui.button(label="Cara", style=discord.ButtonStyle.success, emoji="🙂")
    async def cara(self, button: Button, interaction: discord.Interaction):
        logging.info(f"{interaction.user} presionó Cara")
        await self.elegir(interaction, "Cara")

    @discord.ui.button(label="Sello", style=discord.ButtonStyle.primary, emoji="🦅")
    async def sello(self, button: Button, interaction: discord.Interaction):
        logging.info(f"{interaction.user} presionó Sello")
        await self.elegir(interaction, "Sello")

    async def elegir(self, interaction, eleccion):
        logging.info(f"{interaction.user} eligió {eleccion}")
        if interaction.user not in self.jugadores:
            await interaction.response.send_message("Solo los jugadores pueden elegir.", ephemeral=True)
            return
        # Deshabilitar el botón elegido para el otro jugador
        self.elecciones[interaction.user.id] = eleccion
        for child in self.children:
            if isinstance(child, Button):
                if child.label == eleccion:
                    child.disabled = True
        # Si ya eligieron ambos, mostrar resultado
        if len(self.elecciones) == 2:
            import random
            resultado = random.choice(["Cara", "Sello"])
            self.resultado = resultado
            ganador = None
            for jugador in self.jugadores:
                if self.elecciones[jugador.id] == resultado:
                    ganador = jugador
            if ganador:
                scoreboard[self.key][ganador.id] += 1
            # Crear embed estético
            embed = discord.Embed(
                title="🪙 ¡Resultado del Duelo de Moneda! 🪙",
                description=f"**{self.jugadores[0].mention}** eligió `{self.elecciones[self.jugadores[0].id]}`\n"
                            f"**{self.jugadores[1].mention}** eligió `{self.elecciones[self.jugadores[1].id]}`\n\n"
                            f"**Resultado:** `{resultado}`",
                color=discord.Color.purple()
            )
            if ganador:
                embed.add_field(name="Ganador", value=f"🏆 {ganador.mention}", inline=False)
            else:
                embed.add_field(name="Ganador", value="Empate", inline=False)
            embed.add_field(
                name="Marcador",
                value=f"{self.jugadores[0].mention}: {scoreboard[self.key][self.jugadores[0].id]}  -  {self.jugadores[1].mention}: {scoreboard[self.key][self.jugadores[1].id]}",
                inline=False
            )
            embed.set_footer(text="¡Pulsa el botón para jugar otra vez!")
            # Botón para jugar otra vez
            class PlayAgainView(View):
                def __init__(self, ctx, jugadores, key):
                    super().__init__(timeout=60)
                    self.ctx = ctx
                    self.jugadores = jugadores
                    self.key = key
                @discord.ui.button(label="Jugar otra vez", style=discord.ButtonStyle.success, emoji="🔁")
                async def play_again(self, button: Button, interaction: discord.Interaction):
                    if interaction.user not in self.jugadores:
                        await interaction.response.send_message("Solo los jugadores pueden usar este botón.", ephemeral=True)
                        return
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="Elige Cara o Sello",
                            description=f"{self.jugadores[0].mention} vs {self.jugadores[1].mention}\nPulsa un botón para elegir.",
                            color=discord.Color.blurple()
                        ),
                        view=CaraSelloView(self.ctx, self.jugadores, self.key),
                        ephemeral=False
                    )
            await interaction.response.edit_message(embed=embed, view=PlayAgainView(self.ctx, self.jugadores, self.key))
        else:
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(f"Has elegido `{eleccion}`. Esperando al otro jugador...", ephemeral=True)

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = True
        # Deshabilitar botones al expirar el tiempo
        if self.message:
            await self.message.edit(view=self)

def setup(bot):
    @bot.slash_command(name="flip", description="Reta a otro usuario a un duelo de moneda")
    async def flip(ctx, oponente: discord.Member = None):
        if oponente is None or oponente == ctx.author:
            await ctx.respond("Debes mencionar a otro usuario para el duelo.", ephemeral=True)
            return
        jugadores = [ctx.author, oponente]
        key = tuple(sorted([jugadores[0].id, jugadores[1].id]))
        if key not in scoreboard:
            scoreboard[key] = {jugadores[0].id: 0, jugadores[1].id: 0}
        embed = discord.Embed(
            title="Elige Cara o Sello",
            description=f"{jugadores[0].mention} vs {jugadores[1].mention}\nPulsa un botón para elegir.",
            color=discord.Color.blurple()
        )
        await ctx.respond(embed=embed, view=CaraSelloView(ctx, jugadores, key))