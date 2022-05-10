import discord
import os
import time
from discord.ext import commands
import requests
import hashlib
from db import pracc_users
from dotenv import load_dotenv
from discord_slash import SlashCommand
load_dotenv()


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents,
                      case_insensitive=True)
slash = SlashCommand(client, sync_commands=True)

client.remove_command('help')


@client.command()
async def list_servers(ctx):
    await ctx.send(f"Number of servers Praccforces is serving : {client.guilds}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


@client.command()
async def leaderboard(ctx):
    users = pracc_users.find({}).sort("score", -1).limit(10)
    em = discord.Embed(color=0xFF0000)
    em.title = "PraccForces Leaderboards"
    description = """Make sure to link your CodeForces account with !link cf_handle"""
    for i, user in enumerate(users):
        description = description + "\n" + \
            f"#{i+1} - {user['user_name'][:-5]} `{user['score']}`"
    em.description = description
    em.set_footer(text="Praccforces Leaderboard",
                  icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print("loaded", filename)

client.run(os.environ.get('PRACC_TOKEN'))
