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
from discord.ext import commands

from core import Wilson

from subprocess import call
from os import chdir


class Login(commands.Cog):
    """Initialize Login Cog

    Parameters:
       bot: Wilson - The bot on which the cog is loaded. Passed by setup function in plugins/core/__init__.py
    """

    def __init__(self, bot: Wilson):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready():
        """Run script 'initializedWilson.sh' so that startup messages continue output even if Wilson is silenced or made a background process."""
        chdir("../../../scripts/")
        call("./initializedWilson.sh", shell=True)
        chdir("../plugins/core/startup/")
