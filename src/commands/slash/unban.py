import discord
from discord.ext import commands

# Comando /unban para desbanear usuarios

def setup(bot):
    @bot.slash_command(name="unban", description="Desbanea a un usuario del servidor.")
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, usuario: str):
        # usuario debe ser en formato nombre#discriminador o ID
        guild = ctx.guild
        try:
            # Buscar por ID
            user = await bot.fetch_user(int(usuario))
        except:
            # Buscar por nombre#discriminador
            user = None
            banlist = await guild.bans()
            for ban_entry in banlist:
                if f"{ban_entry.user.name}#{ban_entry.user.discriminator}" == usuario:
                    user = ban_entry.user
                    break
        if not user:
            await ctx.respond("Usuario no encontrado en la lista de baneados.", ephemeral=True)
            return
        try:
            await guild.unban(user)
            await ctx.respond(f"✅ {user.mention} ha sido desbaneado.")
        except Exception as e:
            await ctx.respond(f"No se pudo desbanear a {usuario}. Error: {e}", ephemeral=True)
