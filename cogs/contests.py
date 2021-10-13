import discord
from discord.ext import commands
import time
import datetime
import requests
import random
from db import pracc_users
from checks import check_user , check_guild


class Contests(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def contests(self,ctx):
        await check_guild(ctx)
        await check_user(ctx.author)
        contests = requests.get(f"https://codeforces.com/api/contest.list?gym=false&apikey=2da07181f68098c7fb54b7e482a661e8ad4cb199&time={time.time()}&apiSig=zabbebe9f37bb129543a1e51cfdc346e06dfbdd0561f0123ecb121b44912d08636b8a227572200507125a19cbf8cd8a38c08147b2acb72a57f1f4862a3fdec08176a95")
        available = []
        for contest in contests.json()["result"] : 
            if contest["startTimeSeconds"] > time.time() and "Div." in contest["name"] : 
                available.append(contest)
                
        available.reverse()
        em = discord.Embed(color = 0x00FF00)
        em.title = "Upcoming Codeforces Contests"
        for contest in available : 
            em.add_field(name = contest["name"] , value = f"{str(datetime.timedelta(seconds = contest['startTimeSeconds'] - time.time()))[:-7]} Left for registration" , inline=False)

        await ctx.send(embed = em)
    
    @commands.command()
    async def contest(self,ctx,div=4): 
        await check_guild(ctx)
        await check_user(ctx.author)
        colors = [0xF0EF17 , 0x11A6F9 , 0xF80A0A]
        em = discord.Embed(color = random.choice(colors))
        if int(div) < 4 and int(div) > 0 : 
            contests = requests.get(f"https://codeforces.com/api/contest.list?gym=false&apikey=2da07181f68098c7fb54b7e482a661e8ad4cb199&time={time.time()}&apiSig=zabbebe9f37bb129543a1e51cfdc346e06dfbdd0561f0123ecb121b44912d08636b8a227572200507125a19cbf8cd8a38c08147b2acb72a57f1f4862a3fdec08176a95")
            diff = "Div. "+ str(div)
            valid = []
            for contest in contests.json()["result"]: 
                if diff in contest["name"] : 
                    valid.append(contest)

            contest = random.choice(valid)

            colors = [0xF0EF17 , 0x11A6F9 , 0xF80A0A]

            em = discord.Embed(color = random.choice(colors))

            em.title = f"{contest['name']} ProblemSet"

            problems = requests.get(f"https://codeforces.com/api/contest.standings?contestId={contest['id']}&apikey=2da07181f68098c7fb54b7e482a661e8ad4cb199&time={time.time()}&apiSig=zabbebe9f37bb129543a1e51cfdc346e06dfbdd0561f0123ecb121b44912d08636b8a227572200507125a19cbf8cd8a38c08147b2acb72a57f1f4862a3fdec08176a95")
            problems = problems.json()["result"]["problems"]
            for problem in problems : 
                em.add_field(name = f"Problem {problem['index']}" , value = f"https://codeforces.com/contest/{contest['id']}/problem/{problem['index']}", inline=False )

            await ctx.send(embed = em)
        else : 
            em.title = "Contest divisions can only be 1 , 2 , 3"
            await ctx.send(embed = em)
        pracc_users.update_one({"user_id":ctx.author.id},{"$inc" : {"contests_requested" : 1}})






def setup(client):
    client.add_cog(Contests(client))