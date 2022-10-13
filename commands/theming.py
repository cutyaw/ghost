import os
import sys
import discord

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import embed as embedmaker

class Theming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = cmdhelper.cog_desc("theming", "Theme commands.")
        self.cfg = config.Config()

    @commands.command(name="theming", description="Theme commands.", aliases=["design"], usage="")
    async def theming(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Theming")

        if cfg.get("theme")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} Theme commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = embedmaker.Embed(title="Theme Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.group(name="theme", description="Theme commands.", usage="")
    async def theme(self, ctx):
        cfg = config.Config()

        if ctx.invoked_subcommand is None:
            theme = cfg.get("theme")
            description = ""

            for key, value in theme.items():
                description += f"{key}: {value}\n"

            await ctx.send(str(codeblock.Codeblock(title="theme", description=description, style="yaml")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @theme.command(name="set", description="Set a theme value.", usage="[key] [value]")
    async def theme_set(self, ctx, key: str, value: str):
        cfg = config.Config()
        cfg.config["theme"][key] = value
        cfg.save()
        await ctx.send(f"Set theme {key} to {value}", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @theme.command(name="title", description="Set the title of the embed.", usage="[title]")
    async def theme_title(self, ctx, *, title: str):
        await self.theme_set(ctx, "title", title)
        
    @theme.command(name="colour", description="Set the colour of the embed.", usage="[colour]", aliases=["color"])
    async def theme_colour(self, ctx, colour: str):
        await self.theme_set(ctx, "colour", colour)

    @theme.command(name="footer", description="Set the footer of the embed.", usage="[footer]")
    async def theme_footer(self, ctx, *, footer: str):
        await self.theme_set(ctx, "footer", footer)

    @theme.command(name="image", description="Set the image of the embed.", usage="[image]")
    async def theme_image(self, ctx, image: str):
        await self.theme_set(ctx, "image", image)

    @theme.command(name="style", description="Set the style of the embed.", usage="[style]")
    async def theme_style(self, ctx, style: str):
        await self.theme_set(ctx, "style", style)

def setup(bot):
    bot.add_cog(Theming(bot))