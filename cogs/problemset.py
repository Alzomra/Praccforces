import discord
from discord import embeds
from discord.embeds import Embed
from discord.ext import commands
import random
import os
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandError
import requests
from db import pracc_users , pracc_servers , pracc_problems
from checks import check_user , check_guild


def cleaned_args(args):
        diff = 0
        args = list(args)
        diffb = False
        new_args = []
        for arg in args : 
            try: 
                arg = int(arg)
            except:
                new_args.append(arg.lower())
            else : 
                if not diffb : 
                    diff = arg
                    diffb = True
        return new_args , diff

class Problemset(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.tags =['implementation','math' ,'greedy' ,'dp' ,'data structures' ,'brute force' ,'constructive algorithms'
                    ,'graphs' ,'sortings' ,'binary search' ,'dfs and similar','trees' ,'strings' ,'number theory','combinatorics' 
                    ,'*special' ,'geometry' ,'bit masks' ,'two pointers','dsu', 'shortest paths', 
                    'probabilities','divide and conquer','hashing' ,'games' ,'flows' ,'interactive','matrices' 
                    ,'string suffix structures' ,'fft' ,'graph matchings' ,'ternary search', 
                    'expression parsing' ,'meet-in-the-middle' , '2-sat', 'chinese remainder theorem','schedules' ,'']
    
    

    @commands.command()
    async def problem(self,ctx,*args):
        await check_guild(ctx)
        await check_user(ctx.author)
        args  , diff = cleaned_args(args)
        tags = args
        if not args : 
            tags = ''

        if tags[0].lower() == "tags" : 
            em = discord.Embed(color = 0xFFFFFF)
            em.title = "All Tags"
            em.description = " * ".join(self.tags)
            await ctx.send(embed = em)
            return

        for tag in tags :
            print(tag , tag in self.tags)
            if tag not in self.tags : 
                raise commands.CommandError(message="Unvalid Tag")
                return 
          
        colors = [0xF0EF17 , 0x11A6F9 , 0xF80A0A]
        tags.sort()

        problems = list(pracc_problems.find({"tags" : tags , "rating" : diff or {'$gt' : diff} }))

        if not problems:
            problems = list(pracc_problems.find({"tags" : {"$all" : tags} , "rating" : diff or {'$gt' : diff} }))
            if not problems : 
                raise commands.CommandError(message="No Problem Found")
                return

        prob = random.choice(problems)
        em = discord.Embed(color = random.choice(colors))
        em.title = prob["name"]
        em.add_field(name = "Link :" , value = prob["link"], inline=False)
        em.add_field(name = "Rating" , value = prob["rating"], inline=False)
        if tag == "" :
            em.add_field(name = "Tags" , value="||" + "|| ||".join(prob["tags"]) + "||", inline=False)
        else : 
            em.add_field(name = "Tags" , value=" | ".join(prob["tags"]), inline=False)
        await ctx.send(embed = em)
        pracc_users.update_one({"user_id":ctx.author.id},{"$inc" : {"problems_requested" : 1}})
    
    @problem.error
    async def problem_error(self,ctx,error):
        em = discord.Embed(color = 0XFF0000)
        em.title = "Problem Error !"
        if str(error) == "Unvalid Tag" : 
            em.description = "Unvalid TAG , Use '!problem tags' to get the full list of Tags."
        if str(error) == "No Problem Found" : 
            em.description = "No Problem Found with provided arguments , Use '!problem tags' to get the full list of Tags.\n try changing the rating or vary the tags"
        await ctx.send(embed = em) 
    

    @commands.command()
    async def solution(self,ctx,arg):
        if not arg : 
            return 
        arg = arg.replace('.','').replace('/','').replace('\\','').replace('"','').replace("'",'').replace('*','').replace('$','')
        arg = arg.upper()
        if (not os.path.exists(f"D:\ACM\Codeforces Problemset\ProblemSet\{arg}.cpp")) : 
            return
        with open(f"D:\ACM\Codeforces Problemset\ProblemSet\{arg}.cpp") as f : 
                    await ctx.send(f'```cpp\n{f.read()}```')

def setup(client):
    client.add_cog(Problemset(client))