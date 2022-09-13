import requests
import discord
import os

from discord.ext import commands

from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import embed as embedmaker

class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

@commands.command(name="nsfw", description="NSFW commands.", aliases=["nsfw"], usage="")
async def nsfw(self, ctx, selected_page: int = 1):
    cfg = config.Config()
    pages = cmdhelper.generate_help_pages(self.bot, "Img")

    if cfg.get("theme")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} nsfw commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    else:
            embed = embedmaker.Embed(title="Image Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)



def setup(bot):
    bot.add_cog(nsfw(bot))