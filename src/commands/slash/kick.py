import discord
from discord.ext import commands

# Comando /kick para expulsar usuarios

def setup(bot):
    @bot.slash_command(name="kick", description="Expulsa a un usuario del servidor.")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, usuario: discord.Member, razon: str = "No especificada"):
        if usuario == ctx.author:
            await ctx.respond("No puedes expulsarte a ti mismo.", ephemeral=True)
            return
        try:
            await usuario.kick(reason=razon)
            await ctx.respond(f"👢 {usuario.mention} fue expulsado. Razón: {razon}")
        except Exception as e:
            await ctx.respond(f"No se pudo expulsar a {usuario.mention}. Error: {e}", ephemeral=True)
