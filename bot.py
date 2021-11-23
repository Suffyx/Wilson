import discord
from core import Wilson

bot = Wilson()

def main():
    """Builds and runs Wilson."""
    for item in bot.config.EXTENSIONS:
        bot.load_extension(item)
    
    bot.run(bot.config.TOKEN)
    
