import discord
from discord.ext import commands
import asyncio
import requests
import time
import random
from db import pracc_users

class Authentication(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def link(self,ctx,*args):
        if not args or args[0] == "help" : 
            em = discord.Embed(color = 0xF80A0A)
            em.title = "Account link help"
            #em.description = "To link your Codeforces account you need to write a blog entry \n with the title 'PraccForces Authentication' : case insensitive \n MAKE SURE THAT 'ALLOW TO VIEW HISTROY' OPTION IS CHECKED !"
            em.description = "Steps : "
            em.add_field(name = ":one:" , value = "Write a blog entry" , inline= False)
            em.add_field(name = ":two:" , value = "Title the post 'Praccforces authentication'" , inline= False)
            em.add_field(name = ":exclamation:" , value = "Make sure that  'ALLOW TO VIEW HISTROY' option is checked !" , inline= False)
            em.add_field(name = ":three:"  , value = "Run the link command with your handle" , inline= False)
            em.add_field(name = "The verification will expire when your post is more than 3 minutes old" , value =":exclamation:", inline= False)
            em.add_field(name = "Blog entry link" , value = "http://codeforces.com/blog/entry/new/" , inline= False)
            em.set_footer(text =f"Link command help for {ctx.author.name}" , icon_url=ctx.author.avatar_url)
            await ctx.send(embed = em)
        else :
            user = pracc_users.find_one({'user_id' : ctx.author.id})
            if user.get("auth_key",0) == 0 : 
                auth_key = random.randint(1000000, 9999999999)
                pracc_users.update_one({'user_id' : ctx.author.id} , {'$set' : {'auth_key' : auth_key}})
            else : 
                auth_key = user['auth_key']

            handle = " ".join(list(args))
            em = discord.Embed(color = 0xF80A0A)
            em.title = "Link verification"
            em.description = f"Are you sure that you want to link the following handle to your account ?"
            em.add_field(name = "Auth" , value = handle , inline= True)
            em.add_field(name = "Handle" , value = handle , inline= True)
            em.add_field(name = ":white_check_mark:" , value = "Confirm" , inline= True)
            em.add_field(name = ":x:" , value = "Abort" , inline= True)
            em.set_footer(text =f"Account link for {ctx.author.name}" , icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.author.send(f"""Your authentication Key is : `{auth_key}`
                                    Add your key as a comment to one of your recent public submissions to a problem then react  with :white_check_mark:""")
            msg = await ctx.author.send(embed = em)
            await msg.add_reaction("✅")  
            await msg.add_reaction("❌")


    @link.error
    async def link_error(self,ctx,error):
        em = discord.Embed(color = 0xF80A0A)
        em.title = "Link Error"
        em.add_field(name = "Missing Argument" , value = "Codeforces Handle" , inline= True)
        em.set_footer(text =f"Error in Link command for {ctx.author.name}" , icon_url=ctx.author.avatar_url)
        await ctx.send(embed = em)



    









def setup(client):
    client.add_cog(Authentication(client))