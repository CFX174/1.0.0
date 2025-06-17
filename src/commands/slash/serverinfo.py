import discord
from discord.ext import commands

def setup(bot):
    @bot.slash_command(name="serverinfo", description="Muestra información del servidor")
    async def serverinfo(ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Información del servidor: {guild.name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Dueño", value=str(guild.owner))
        embed.add_field(name="Miembros", value=guild.member_count)
        await ctx.respond(embed=embed)