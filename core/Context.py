"""
MIT License

Copyright (c) 2021 Suffyx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

import discord.abc

if TYPE_CHECKING:
    import discord
    from discord import Bot
    from discord.state import ConnectionState

    from discord.ext.commands import ApplicationCommand, Option
    from discord.cog import Cog

from discord.guild import Guild
from discord.interactions import Interaction, InteractionResponse
from discord.member import Member
from discord.message import Message
from discord.user import User
from discord.utils import cached_property

__all__ = (
    "ApplicationContext",
    "AutocompleteContext"
)

class ApplicationContext(discord.abc.Messageable):
    """Represents a Discord application command interaction context.

    This class is not created manually and is instead passed to application
    commands as the first parameter.

    .. versionadded:: 2.0

    Attributes
    -----------
    bot: :class:`.Bot`
        The bot that the command belongs to.
    interaction: :class:`.Interaction`
        The interaction object that invoked the command.
    command: :class:`.ApplicationCommand`
        The command that this context belongs to.
    """

    def __init__(self, bot: Bot, interaction: Interaction):
        self.bot = bot
        self.interaction = interaction
        self.command: ApplicationCommand = None  # type: ignore
        self._state: ConnectionState = self.interaction._state

    async def _get_channel(self) -> discord.abc.Messageable:
        return self.channel

    @cached_property
    def channel(self):
        return self.interaction.channel

    @cached_property
    def channel_id(self) -> Optional[int]:
        return self.interaction.channel_id

    @cached_property
    def guild(self) -> Optional[Guild]:
        return self.interaction.guild

    @cached_property
    def guild_id(self) -> Optional[int]:
        return self.interaction.guild_id

    @cached_property
    def me(self) -> Union[Member, User]:
        return self.guild.me if self.guild is not None else self.bot.user

    @cached_property
    def message(self) -> Optional[Message]:
        return self.interaction.message

    @cached_property
    def user(self) -> Optional[Union[Member, User]]:
        return self.interaction.user

    @cached_property
    def author(self) -> Optional[Union[Member, User]]:
        return self.user

    @property
    def voice_client(self):
        return self.guild.voice_client

    @cached_property
    def response(self) -> InteractionResponse:
        return self.interaction.response

    @property
    def respond(self):
        return self.followup.send if self.response.is_done() else self.interaction.response.send_message

    @property
    def defer(self):
        return self.interaction.response.defer

    @property
    def followup(self):
        return self.interaction.followup

    async def delete(self):
        """Calls :attr:`~discord.commands.ApplicationContext.respond`.
        If the response is done, then calls :attr:`~discord.commands.ApplicationContext.respond` first."""
        if not self.response.is_done():
            await self.defer()

        return await self.interaction.delete_original_message()

    @property
    def edit(self):
        return self.interaction.edit_original_message

    @property
    def cog(self) -> Optional[Cog]:
        """Optional[:class:`.Cog`]: Returns the cog associated with this context's command. ``None`` if it does not exist."""
        if self.command is None:
            return None
       
        return self.command.cog
    
    async def error(self, content: str) -> Message:
        """Display's an Wilson exception.

        Parameters:
           content: str - The content of the error itself
        """
        return await ctx.respond(
            embed=discord.Embed(
                title="Command Error",
                description=f"```{content}```",
                color=discord.Colour.red(),
            )
        )
