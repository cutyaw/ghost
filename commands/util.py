import os
import sys

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="util", description="Utility commands.", aliases=["utilities", "utility", "utils"], usage="")
    async def util(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Util")

        msg = codeblock.Codeblock(
            f"{cfg.get('theme')['emoji']} util commands",
            description=pages[selected_page - 1],
            extra_title=f"Page {selected_page}/{len(pages)}"
        )

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.group(name="config", description="Configure ghost.", usage="")
    async def config(self, ctx):
        cfg = config.Config()

        if ctx.invoked_subcommand is None:
            description = ""
            for key, value in self.cfg.config.items():
                if key == "token":
                    continue
                # check if the key is a dict
                if isinstance(value, dict):
                    sub_msg = f"{key}:\n"
                    for sub_key, sub_value in value.items():
                        sub_msg += f"\t{sub_key}: {sub_value}\n"
                    description += sub_msg
                else:
                    description += f"{key}: {value}\n"

            await ctx.send(str(codeblock.Codeblock(title="config", description=description, style="yaml")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @config.command(name="set", description="Set a config value.", usage="[key] [value]")
    async def set(self, ctx, key, *, value):
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False

        if key.lower() == "message_settings.auto_delete_delay":
            try:
                value = int(value)
            except ValueError:
                await ctx.send(str(codeblock.Codeblock(title="error", extra_title="the value isnt an integer")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return

        if "." in key:
            key2 = key.split(".")
            if key2[0] not in self.cfg.config or key2[1] not in self.cfg.config[key2[0]]:
                await ctx.send(str(codeblock.Codeblock(title="error", extra_title="invalid key")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return
        
        else:
            if key not in self.cfg.config:
                await ctx.send(str(codeblock.Codeblock(title="error", extra_title="invalid key")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return

        if key == "prefix":
            self.bot.command_prefix = value

        if "." in key:
            key2 = key.split(".")
            self.cfg.config[key2[0]][key2[1]] = value

        else:
            self.cfg.config[key] = value

        self.cfg.save()
        await ctx.send(str(codeblock.Codeblock(title="config", extra_title="key updated", description=f"{key} :: {value}")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="restart", description="Restart the bot.", usage="", aliases=["reboot", "reload"])
    async def restart(self, ctx):
        cfg = config.Config()
        
        await ctx.send(f"```ini\n[ ghost ] restarting...\n```", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
        
        os.execl(sys.executable, sys.executable, *sys.argv)

    @commands.command(name="settings", description="View ghost's settings.", usage="")
    async def settings(self, ctx):
        cfg = config.Config()
        command_amount = len(self.bot.commands)

        await ctx.send(str(codeblock.Codeblock(title="settings", description=f"""prefix         :: {self.bot.command_prefix}
version        :: {config.VERSION}
command amount :: {command_amount}""")), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Util(bot))