def setup(bot):
    @bot.command()
    async def hola(ctx):
        await ctx.send('¡Hola! Este comando fue cargado dinámicamente.')
