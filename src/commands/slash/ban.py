import discord
from discord.ext import commands

# Comando /ban para banear usuarios

def setup(bot):
    @bot.slash_command(name="ban", description="Banea a un usuario del servidor.")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, usuario: discord.Member, razon: str = "No especificada"):
        if usuario == ctx.author:
            await ctx.respond("No puedes banearte a ti mismo.", ephemeral=True)
            return
        try:
            await usuario.ban(reason=razon)
            await ctx.respond(f"🔨 {usuario.mention} fue baneado. Razón: {razon}")
        except Exception as e:
            await ctx.respond(f"No se pudo banear a {usuario.mention}. Error: {e}", ephemeral=True)
