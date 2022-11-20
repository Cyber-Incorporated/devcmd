import datetime

import ciberedev
import discord
from discord.ext import commands

from ..utils import filter_text


@commands.is_owner()
class BaseSection(commands.Cog):
    cdev: ciberedev.Client
    bot: commands.Bot

    async def send_error(self, messageable, message: str) -> discord.Message:
        em = discord.Embed(
            title="Error",
            description=message,
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        return await self.send_message(messageable, em)

    async def send_success(self, messageable, message: str) -> discord.Message:
        em = discord.Embed(
            title="Success",
            description=message,
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow(),
        )
        return await self.send_message(messageable, em)

    async def send_info(self, messageable, title: str, message: str) -> discord.Message:
        em = discord.Embed(
            title=title,
            description=message,
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow(),
        )
        return await self.send_message(messageable, em)

    async def send_message(self, messageable, embed: discord.Embed) -> discord.Message:
        if embed.description:
            embed.description = filter_text(embed.description)
        if embed.title:
            embed.title = filter_text(embed.title)

        try:
            msg = await messageable.send(embed=embed)
        except discord.HTTPException:
            paste = await self.cdev.create_paste(str(embed.description))
            em = embed
            em.description = (
                f"(Message was too long to send, so I sent it here)[{str(paste)}]"
            )
            msg = await messageable.send(embed=em)

        return msg


def command(*, name: str, description: str, aliases: list[str] = []):
    def inner(func):
        func.cmd_info = {"name": name, "desc": description, "aliases": aliases}
        return func

    return inner
