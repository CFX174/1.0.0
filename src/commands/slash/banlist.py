import discord
from discord.ext import commands

# Comando /banlist para mostrar la lista de baneados

def setup(bot):
    @bot.slash_command(name="banlist", description="Muestra la lista de usuarios baneados del servidor.")
    @commands.has_permissions(ban_members=True)
    async def banlist(ctx):
        ban_entries = await ctx.guild.bans()
        if not ban_entries:
            await ctx.respond("No hay usuarios baneados en este servidor.", ephemeral=True)
            return
        lista = "\n".join([f"{entry.user} (ID: {entry.user.id})" for entry in ban_entries])
        embed = discord.Embed(title="Lista de baneados", description=lista, color=discord.Color.red())
        await ctx.respond(embed=embed)
