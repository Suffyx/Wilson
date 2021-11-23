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

import discord
from discord.commands import message_command, slash_command, Option
from discord.ext import commands

class Menus(commands.Cog):
    """Initialize Menus Cog
    Parameters:
       bot: Wilson - The bot on which the cog is loaded. Passed by setup function in plugins/reaction_roles/__init__.py
    """

    def __init__(self, bot: Wilson):
        self.bot = bot
        
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.message_id) in db:
            guild = self.bot.get_guild(payload.guild_id)
            user = await guild.fetch_member(payload.user_id)
            role = discord.utils.get(guild.roles, name=self.bot.db[str(payload.message_id)][payload.emoji.name])
            await user.add_roles(role)
    

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if str(payload.message_id) in db:
            guild = self.bot.get_guild(payload.guild_id)
            user = await guild.fetch_member(payload.user_id)
            role = discord.utils.get(guild.roles, name=self.bot.db[str(payload.message_id)][payload.emoji.name])
            await user.remove_roles(role)
        
    @message_command(name="Create Role Menu")
    async def _create_role_menu(ctx, message: discord.Message):
        items = message.content.split("\n\n")

        _message = await ctx.channel.send(
            "** **"
        )

        self.bot.db[str(_message.id)] = {}

        description_string = ""
        for item in items[2].split("\n"):
            if " | " in item:
                if not discord.utils.get(ctx.guild.roles, name=item.split(" | ")[1]):
                    await ctx.guild.create_role(name=item.split(" | ")[1])
                description_string += "\n {0} | {1}".format(item.split(" | ")[0].strip(), item.split(" | ")[1].strip())
                emojis.append(item.split(" | ")[0].strip())
                emoji = item.split(" | ")[0].strip()
                try:
                    emoji = self.bot.get_emoji(int(emoji.replace("<:", "").split(":")[0].replace(">", ""))).name
                except:
                    emoji = emoji
                self.bot.db[str(_message.id)][emoji] = item.split(" | ")[1].strip()
            else:
                description_string+="\n{}".format(item)

        embed=discord.Embed(
            title=items[0],
            description=items[1]+"\n"+description_string,
            color=random.choice(colours)
        )

        await _message.edit(embed=embed)


        for emoji in emojis:
            await message.add_reaction(emoji)
            
    @slash_command()
    async def edit_role_menu(
      ctx,
      message_id: Option(str, "Message ID for the new reaction role base."),
      menu: Option(str, "The original reaction role menu.")
    ):
        items = message.content.split("\n\n")

        _message = ctx.fetch_message(menu)

        self.bot.db[str(_message.id)] = {}

        description_string = ""
        for item in items[2].split("\n"):
            if " | " in item:
                if not discord.utils.get(ctx.guild.roles, name=item.split(" | ")[1]):
                    await ctx.guild.create_role(name=item.split(" | ")[1])
                description_string += "\n {0} | {1}".format(item.split(" | ")[0].strip(), item.split(" | ")[1].strip())
                emojis.append(item.split(" | ")[0].strip())
                emoji = item.split(" | ")[0].strip()
                try:
                    emoji = self.bot.get_emoji(int(emoji.replace("<:", "").split(":")[0].replace(">", ""))).name
                except:
                    emoji = emoji
                self.bot.db[str(_message.id)][emoji] = item.split(" | ")[1].strip()
            else:
                description_string+="\n{}".format(item)

        embed=discord.Embed(
            title=items[0],
            description=items[1]+"\n"+description_string,
            color=random.choice(colours)
        )

        await _message.edit(embed=embed)


        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
            except:
                continue
                
    @message_command(name="Set Role Colours")
    async def _set_role_colors(ctx, message: discord.Message):
        items = message.content.split("\n")
        for item in items:
            data = item.split(" | ")
            role = discord.utils.get(ctx.guild.roles, name=data[1])
            await role.edit(color=int(data[2].replace("#", "0x"), base=16))

        await ctx.respond("Role colours edited.")
