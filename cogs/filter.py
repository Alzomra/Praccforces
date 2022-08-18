import discord
from discord.ext import commands
import re


class Filter(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.client.add_listener(self.on_message)

    def filter_zb(self, word):
        r = re.search(r".*[z,s]+[aei]+[b,p]+y*.*", word)
        return bool(r)

    def filter_ny(self, word):
        r = re.search(r".*n+[a,é,e]*[i,y]+[e,a,u]*[k,q]+.*", word)
        return bool(r)

    def filter_as(self, word):
        r = re.search(r".*[3a]+[s]+[b]+[a]*.*", word)
        return bool(r)

    def all(self, word):
        zb = self.filter_zb(word)
        ny = self.filter_ny(word)
        aas = self.filter_as(word)
        if zb or ny or aas:
            return True
        else:
            return False

    async def on_message(self, message):
        if 'private' in message.channel.type:
            return
        elif not message.author.bot and message.guild.id == 648553103955591178:
            res = False
            for word in message.content.split(" "):
                if self.all(word.lower().strip()):
                    res = True
                    break
            if res:
                await message.channel.send("Naughty BOI !")


def setup(client):
    client.add_cog(Filter(client))
