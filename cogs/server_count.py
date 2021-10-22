import topgg
import discord
from discord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, client):
        self.client = client
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc5NDkwMTE1Njg5MDY3MzE2MiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEwODAwNDAzfQ.-ug8IuwFzAPgAoOfsHHRi4jcEYFNN-uEFtEiU3bevhY' # set this to your DBL token
        self.dblpy = topgg.DBLClient(self.client, self.token, autopost=True , post_shard_count=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post(self):
        print("Server count posted successfully")
    

def setup(client):
    client.add_cog(TopGG(client))