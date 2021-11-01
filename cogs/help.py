import discord
from discord.ext import commands
from db import pracc_users , pracc_servers

class Help(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def help(self,ctx):
        em = discord.Embed(color = 0xF80A0A)
        em.title = "PraccForces Help"
        em.add_field(name = "Commands list :question:" , value = "[PraccForces.Top.gg](https://top.gg/bot/794901156890673162)" , inline= True)
        em.set_footer(text =f"Help for {ctx.author.name}" , icon_url=ctx.author.avatar_url)
        await ctx.send(embed = em)

    
    @commands.command()
    async def database(self,ctx,x):
        em = discord.Embed(color = 0xFFFF00)
        em.set_thumbnail(url = "https://cdn.discordapp.com/avatars/794901156890673162/8de21d514c9f90fb9ed09de7d2f2be1c.png")
        em.title = "Slash Commands are here & More !"
        em.description = "You can now interact with PraccForces with slash commands!"
        em.add_field(name ="**!example : **" , value = "/problem rating:1800", inline=False)
        em.add_field(name ='**Result : **' , value = "A problem with the provided tags and rating.", inline=False)
        em.add_field(name ='**Wild Tags !**' , value = "!problem -dp -* -2000", inline=False)
        em.add_field(name ='**Result : **' , value = "The provided problem will have the 'dp' tag and more random tags.", inline=False)
        em.add_field(name ='**TOP.GG**' , value = "[top.gg/Praccforces](https://top.gg/bot/794901156890673162)", inline=False)
        for guild in self.client.guilds :
                for channel in guild.text_channels :
                        try : 
                                await channel.send(embed = em)
                        except : 
                                pass
                        else : 
                                break


def setup(client):
    client.add_cog(Help(client))