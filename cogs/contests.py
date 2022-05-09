import discord
from discord.ext import commands
import time
import datetime
import requests
import random
from db import pracc_users, pracc_problems, pracc_contests
from checks import check_user, check_guild

BASE_URL_CONTEST = "https://codeforces.com/contest/"
BASE_URL_PROBLEM = "https://codeforces.com/problemset/problem/"


class Contests(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def contests(self, ctx, all=""):
        em = discord.Embed(color=0x00FF00)
        if not all:
            contests = pracc_contests.find(
                {"phase": "BEFORE", "name": {"$regex": "Div"}})
            em.title = "Upcoming Codeforces Contests (Rounds)"
        else:
            contests = pracc_contests.find({"phase": "BEFORE"})
            em.title = "All Upcoming Codeforces Contests"

        contests = list(contests)
        contests.reverse()

        for contest in contests:
            em.add_field(
                name=contest["name"], value=f"{str(datetime.timedelta(seconds = contest['startTime'] - time.time()))[:-7]}Left for registration. **ID : {contest['id']}**", inline=False)

        await ctx.send(embed=em)

    @commands.command()
    async def contest(self, ctx, div=""):
        await check_guild(ctx)
        await check_user(ctx.author)
        colors = [0xF0EF17, 0x11A6F9, 0xF80A0A]
        try:
            div = int(div)
        except:
            em = discord.Embed(color=0xFF0000)
            em.title = "Contest divisions can only be 1 , 2 , 3 , 4"
            await ctx.send(embed=em)
            return

        if not (int(div) <= 4 and int(div) > 0):
            em = discord.Embed(color=0xFF0000)
            em.title = "Contest divisions can only be 1 , 2 , 3 , 4"
            await ctx.send(embed=em)
            return

        contests = pracc_contests.find({"div": str(div), "phase": "FINISHED"})
        contest = random.choice(list(contests))
        problems = pracc_problems.find({"contestId": contest['id']})

        em = discord.Embed(color=random.choice(colors))
        em.title = f"{contest['name']} ProblemSet"
        em.add_field(name="Contest link : ",
                     value=f"{BASE_URL_CONTEST}{contest['id']}", inline=False)
        for problem in problems:
            em.add_field(
                name=f"{problem['name']}", value=f"[Problem Link]({BASE_URL_PROBLEM}{problem['contestId']}/{problem['index']})", inline=True)
        await ctx.send(embed=em)

        #pracc_users.update_one({"user_id":ctx.author.id},{"$inc" : {"contests_requested" : 1}})


def setup(client):
    client.add_cog(Contests(client))
