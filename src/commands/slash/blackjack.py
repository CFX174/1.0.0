import discord
from discord.ext import commands
from discord.ui import Button, View
import random

# Diccionario para llevar el marcador de los duelos
scoreboard_blackjack = {}

class BlackjackView(View):
    def __init__(self, ctx, jugadores, key):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.jugadores = jugadores
        self.key = key
        self.manos = {jugadores[0]: [], jugadores[1]: []}
        self.mazo = [str(i) for i in range(1, 11)] * 4
        random.shuffle(self.mazo)
        self.turno = jugadores[0]
        self.terminado = False
        self.resultado = None
        self.iniciar_partida()

    def iniciar_partida(self):
        for jugador in self.jugadores:
            self.manos[jugador] = [self.mazo.pop(), self.mazo.pop()]

    def valor_mano(self, mano):
        return sum(int(carta) for carta in mano)

    def mostrar_mano(self, mano):
        emoji_map = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '10': '🔟'}
        return ' '.join(emoji_map[c] for c in mano)

    def siguiente_turno(self):
        idx = self.jugadores.index(self.turno)
        self.turno = self.jugadores[(idx + 1) % 2]

    def actualizar_botones(self):
        # Los botones siempre estarán habilitados, el control es solo en el callback
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = False

    @discord.ui.button(label="Pedir carta", style=discord.ButtonStyle.success, emoji="🃏")
    async def pedir(self, button: Button, interaction: discord.Interaction):
        if self.terminado:
            await interaction.response.send_message("La partida ya terminó.", ephemeral=True)
            return
        if interaction.user != self.turno:
            await interaction.response.send_message("No es tu turno.", ephemeral=True)
            return
        self.manos[self.turno].append(self.mazo.pop())
        valor = self.valor_mano(self.manos[self.turno])
        if valor == 21:
            self.terminado = True
            self.resultado = f"{self.turno.mention} hizo 21 y gana automáticamente! 🥳"
            scoreboard_blackjack[self.key][self.turno.id] += 1
            await interaction.response.edit_message(embed=self.resultado_embed(), view=PlayAgainView(self.ctx, self.jugadores, self.key))
        elif valor > 21:
            self.terminado = True
            perdedor = self.turno
            ganador = self.jugadores[0] if self.turno == self.jugadores[1] else self.jugadores[1]
            self.resultado = f"{perdedor.mention} se pasó de 21. {ganador.mention} gana! 😎"
            scoreboard_blackjack[self.key][ganador.id] += 1
            await interaction.response.edit_message(embed=self.resultado_embed(), view=PlayAgainView(self.ctx, self.jugadores, self.key))
        else:
            self.siguiente_turno()
            self.actualizar_botones()
            await interaction.response.edit_message(embed=self.estado_embed(), view=self)

    @discord.ui.button(label="Plantarse", style=discord.ButtonStyle.primary, emoji="✋")
    async def plantarse(self, button: Button, interaction: discord.Interaction):
        if self.terminado:
            await interaction.response.send_message("La partida ya terminó.", ephemeral=True)
            return
        if interaction.user != self.turno:
            await interaction.response.send_message("No es tu turno.", ephemeral=True)
            return
        self.siguiente_turno()
        # Si ambos se plantan, comparar manos
        if all(len(self.manos[j]) >= 2 and self.valor_mano(self.manos[j]) >= 17 for j in self.jugadores):
            self.terminado = True
            v0 = self.valor_mano(self.manos[self.jugadores[0]])
            v1 = self.valor_mano(self.manos[self.jugadores[1]])
            if v0 > v1:
                ganador = self.jugadores[0]
            elif v1 > v0:
                ganador = self.jugadores[1]
            else:
                ganador = None
            if ganador:
                self.resultado = f"{ganador.mention} gana con {self.valor_mano(self.manos[ganador])}! 🏆"
                scoreboard_blackjack[self.key][ganador.id] += 1
            else:
                self.resultado = "¡Empate! 🤝"
            await interaction.response.edit_message(embed=self.resultado_embed(), view=PlayAgainView(self.ctx, self.jugadores, self.key))
        else:
            self.actualizar_botones()
            await interaction.response.edit_message(embed=self.estado_embed(), view=self)

    def estado_embed(self):
        embed = discord.Embed(
            title="Blackjack Duelos 🃏",
            description=f"{self.jugadores[0].mention}: **{self.valor_mano(self.manos[self.jugadores[0]])}**\n{self.jugadores[1].mention}: **{self.valor_mano(self.manos[self.jugadores[1]])}**",
            color=discord.Color.green()
        )
        embed.add_field(
            name=f"🔔 TURNO ACTUAL",
            value=f"➡️ **{self.turno.mention}**",
            inline=False
        )
        embed.set_footer(text="Llega a 21 para ganar automáticamente. Si te pasas, pierdes.")
        return embed

    def resultado_embed(self):
        embed = discord.Embed(
            title="Resultado del Blackjack 🏆",
            description=f"{self.jugadores[0].mention}: {self.mostrar_mano(self.manos[self.jugadores[0]])} (Total: {self.valor_mano(self.manos[self.jugadores[0]])})\n{self.jugadores[1].mention}: {self.mostrar_mano(self.manos[self.jugadores[1]])} (Total: {self.valor_mano(self.manos[self.jugadores[1]])})\n\n{self.resultado}",
            color=discord.Color.gold()
        )
        embed.add_field(name="Marcador", value=f"{self.jugadores[0].mention}: {scoreboard_blackjack[self.key][self.jugadores[0].id]}  -  {self.jugadores[1].mention}: {scoreboard_blackjack[self.key][self.jugadores[1].id]}", inline=False)
        return embed

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = True
        if hasattr(self, 'message') and self.message:
            await self.message.edit(view=self)

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
        view = BlackjackView(self.ctx, self.jugadores, self.key)
        embed = view.estado_embed()
        msg = await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
        view.message = await msg.original_response()

def setup(bot):
    @bot.slash_command(name="blackjack", description="Reta a otro usuario a un duelo de Blackjack.")
    async def blackjack(ctx, oponente: discord.Member = None):
        if oponente is None or oponente == ctx.author:
            await ctx.respond("Debes mencionar a otro usuario para el duelo.", ephemeral=True)
            return
        jugadores = [ctx.author, oponente]
        key = tuple(sorted([jugadores[0].id, jugadores[1].id]))
        if key not in scoreboard_blackjack:
            scoreboard_blackjack[key] = {jugadores[0].id: 0, jugadores[1].id: 0}
        view = BlackjackView(ctx, jugadores, key)
        embed = view.estado_embed()
        msg = await ctx.respond(embed=embed, view=view)
        view.message = await msg.original_response()
