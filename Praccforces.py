import discord
import os 
import time
from discord.ext import commands
import requests 
import hashlib
from db import pracc_users

intents = discord.Intents.default()
intents.members = True 
intents.presences = True

client = commands.Bot(command_prefix = "!" , intents = intents , case_insensitive = True)
client.remove_command('help')










    

### old contests contests ###

@client.command()
async def list_servers(ctx):
    await ctx.send(f"Number of servers Praccforces is serving : {client.guilds}") 



@client.event
async def on_command_error(ctx,error):
        print(error)
        if isinstance(error, commands.CommandNotFound):
            pass
        else : 
            print(error)
            await ctx.send('please check command arguments!')




# automatic server count

@client.command()
async def reload(ctx,extension) : 
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")


    

@client.command()
async def leaderboard(ctx): 
    #pracc_users.update_many({} , {"$set" : {"score" : 0}})
    users = pracc_users.find({}).sort("score",-1).limit(10)
    em = discord.Embed(color = 0xFF0000)
    em.title = "PraccForces Leaderboards"
    description = """Make sure to link your CodeForces account with !link cf_handle"""
    for i,user in enumerate(users) : 
        description=description + "\n" +f"#{i+1} - {user['user_name'][:-5]} `{user['score']}`"
    em.description = description
    em.set_footer(text="Praccforces Leaderboard" , icon_url=ctx.author.avatar_url)
    await ctx.send(embed = em)



def hachapi(mtd):
    hached = hashlib.sha512(("praccc/"+mtd).encode()).hexdigest()
    print(hached)
    return hached



@client.command()
async def submit(ctx):
    apikey = "2da07181f68098c7fb54b7e482a661e8ad4cb199"
    secret = "6259c639ad87989ff1bd0791d90a04ab4aea9541"
    handle = "oussema_loukil"
    contestId = "1256"
    apiSig = hachapi(f"contest.status?contestId={contestId}&handle={handle}&apikey={apikey}&count=1&time={time.time()}#{secret}")
    request = requests.get(f"https://codeforces.com/api/contest.status?contestId={contestId}&apikey={apikey}&count=1&handle={handle}&time={time.time()}&apiSig=praccc{apiSig}")
    print(request.json())


for filename in os.listdir('./cogs'): 
    if filename.endswith('.py') :  
        client.load_extension(f'cogs.{filename[:-3]}')


#client.run("Nzk0OTAxMTU2ODkwNjczMTYy.X_BjZA.FZqLqB01WyZz5-c1elt0_vWNczg")
client.run("NzE2ODkzODU3MjMyNDUzNjgy.XtSZeQ.U97RD_izy2G60kcGUr1COdnB878")



