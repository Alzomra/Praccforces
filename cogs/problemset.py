import discord
from discord.ext import commands
import random
import os
from db import pracc_users,  pracc_problems
from checks import check_user, check_guild
from Codeforces import Codeforces


BASE_URL_PROBLEM = "https://codeforces.com/problemset/problem/"


def cleaned_args(args):
    if (args == ''):
        return [''], 0, False
    args = args.split('-')
    diff = 0
    wild = False
    diffb = False
    new_args = []
    for arg in args:
        try:
            arg = int(arg)
        except:
            if arg.strip() == "*":
                wild = True
            else:
                new_args.append(arg.lower().strip())
        else:
            if not diffb:
                diff = arg
                diffb = True
    return new_args, diff, wild


class Problemset(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tags = Codeforces().problemset_tags

    @commands.command()
    async def problem(self, ctx, *, args=""):
        await check_guild(ctx)
        await check_user(ctx.author)
        args, diff, wild = cleaned_args(args)
        tags = args
        if not args:
            tags = ['']

        if tags[0].lower() == "tags":
            em = discord.Embed(color=0xFFFFFF)
            em.title = "All Tags"
            em.description = " * ".join(self.tags)
            em.add_field(name="Usage(slash command) :",
                         value="/problem rating:1200 tags:-dp -math")
            em.add_field(name="Regular Usage :",
                         value="!problem 1200 -dp -math")
            await ctx.send(embed=em)
            return

        for tag in tags:
            if tag not in self.tags:
                raise commands.CommandError(message="Unvalid Tag")
                return

        colors = [0xF0EF17, 0x11A6F9, 0xF80A0A]
        em = discord.Embed(color=random.choice(colors))
        tags.remove('')
        tags.sort()
        tags = list(set(tags))
        if not tags and not diff:
            diff = random.randint(8, 40) * 100
            problems = list(pracc_problems.find(
                {"rating": {"$gte": diff-100, "$lte": diff + 100}}))
        elif not tags:
            problems = list(pracc_problems.find({"rating": diff}))
        elif not diff:
            if wild:
                problems = list(pracc_problems.find(
                    {"rating": {"$all": tags}}))
            else:
                problems = list(pracc_problems.find({"tags": tags}))
        else:
            if wild:
                problems = list(pracc_problems.find(
                    {"tags": {"$all": tags}, "rating": diff}))
            else:
                problems = list(pracc_problems.find(
                    {"tags":  tags, "rating": diff}))

        if not problems:
            problems = list(pracc_problems.find(
                {"tags": {"$all": tags}, "rating": diff}))
        if not problems:
            problems = list(pracc_problems.find(
                {"tags": {"$all": tags}, "rating": {"$gte": diff, "$lte": diff + 400}}))

        if not problems:
            em.description = "No Problem Found with provided arguments , Use '!problem tags' to get the full list of Tags.\n try changing the rating or vary the tags"
            await ctx.send(embed=em)
            return
        prob = random.choice(problems)
        em.title = prob["name"]
        em.add_field(
            name="Link :", value=f"{BASE_URL_PROBLEM}{prob['contestId']}/{prob['index']}/", inline=False)
        em.add_field(name="Rating", value=prob["rating"], inline=False)
        if tag == "":
            em.add_field(name="Tags", value="||" +
                         "|| ||".join(prob["tags"]) + "||", inline=False)
        else:
            em.add_field(name="Tags", value=" | ".join(
                prob["tags"]), inline=False)
        await ctx.send(embed=em)
        pracc_users.update_one({"user_id": ctx.author.id}, {
                               "$inc": {"problems_requested": 1}})

    @problem.error
    async def problem_error(self, ctx, error):
        em = discord.Embed(color=0XFF0000)
        em.title = "Problem Error !"
        if str(error) == "Unvalid Tag":
            em.description = "Unvalid TAG , Use '!problem tags' to get the full list of Tags."
        elif str(error) == "No Problem Found":
            em.description = "No Problem Found with provided arguments , Use '!problem tags' to get the full list of Tags.\n try changing the rating or vary the tags"
        else:
            em.title = "Problem Invalid Syntax!"
            em.description = """ Problem tags must be preceded with dashes (-)
                               **Try the following syntax : !problem -[tag]**
                                Example : **!problem -math -dp**"""

        await ctx.send(embed=em)

    @commands.command()
    async def solution(self, ctx, arg):
        if not arg:
            return
        arg = arg.replace('.', '').replace('/', '').replace('\\', '').replace('"',
                                                                              '').replace("'", '').replace('*', '').replace('$', '')
        arg = arg.upper()
        if (not os.path.exists(f"D:\ACM\Codeforces Problemset\ProblemSet\{arg}.cpp")):
            return
        with open(f"D:\ACM\Codeforces Problemset\ProblemSet\{arg}.cpp") as f:
            await ctx.send(f'```cpp\n{f.read()}```')


def setup(client):
    client.add_cog(Problemset(client))
