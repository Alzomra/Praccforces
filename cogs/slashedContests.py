# cog.py
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext , manage_commands
import random
from db import pracc_contests, pracc_problems
import datetime , time

BASE_URL_CONTEST = "https://codeforces.com/contest/"
BASE_URL_PROBLEM = "https://codeforces.com/problemset/problem/"

class SlashedContests(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="Contest" , description="Get a Contest with a specified division." , options=[
    manage_commands.create_option(name="division" , description="Contest division" , option_type=int , required=True , choices=[1,2,3])])
    async def contest(self, ctx: SlashContext , division):
        colors = [0xF0EF17 , 0x11A6F9 , 0xF80A0A]

        contests = pracc_contests.find({"div" : str(division) , "phase" : "FINISHED"})
        contest = random.choice(list(contests))
        problems = pracc_problems.find({"contestId" : contest['id']})

        em = Embed(color = random.choice(colors))
        em.title = f"{contest['name']} ProblemSet"
        em.add_field(name= "Contest link : " , value = f"{BASE_URL_CONTEST}{contest['id']}",inline=False)
        for problem in problems : 
            em.add_field(name = f"{problem['name']}" , value = f"[Problem Link]({BASE_URL_PROBLEM}{problem['contestId']}/{problem['index']})", inline=True)
        await ctx.send(embed = em) 

    @cog_ext.cog_slash(name="Contests" , description="Get upcoming codeforces contests" , options=[
        manage_commands.create_option(name="all" ,description="Fetch all contests or codeforces rounds only." , required=False, option_type=bool)
    ])
    async def contests(self,ctx,all=False):
        em = Embed(color = 0x00FF00)    
        if not all :
            contests = pracc_contests.find({"phase" : "BEFORE" , "name" : {"$regex" : "Div"}})
            em.title = "Upcoming Codeforces Contests (Rounds)"
        else : 
            contests = pracc_contests.find({"phase" : "BEFORE"})
            em.title = "All Upcoming Codeforces Contests"

        contests = list(contests)
        contests.reverse()

        for contest in contests :
            em.add_field(name = contest["name"] , value = f"{str(datetime.timedelta(seconds = contest['startTime'] - time.time()))[:-7]}Left for registration. **ID : {contest['id']}**" , inline=False)

        await ctx.send(embed = em)


def setup(bot: Bot):
    bot.add_cog(SlashedContests(bot))