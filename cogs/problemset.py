import discord
from discord.embeds import Embed
from discord.ext import commands
import random
import requests
from db import pracc_users , pracc_servers
from checks import check_user , check_guild


def cleaned_args(args):
        diff = 0
        args = list(args)
        print(args)
        diffb = False
        new_args = []
        for arg in args : 
            try: 
                arg = int(arg)
            except:
                print("Not a number")
                new_args.append(arg)
            else : 
                if not diffb : 
                    print("found IT" , arg)
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
                    'expression parsing' ,'meet-in-the-middle' , '2-sat', 'chinese', 'remainder theorem','schedules' ,'']
    
    

    @commands.command()
    async def problem(self,ctx,*args):
        await check_guild(ctx)
        await check_user(ctx.author)
        args  , diff = cleaned_args(args)
        tag = ' '.join(args)
        if tag.lower() == "tags" : 
            em = discord.Embed(color = 0xFFFFFF)
            em.title = "All Tags"
            em.description = " * ".join(self.tags)
            await ctx.send(embed = em)
            return
        
        if tag not in self.tags : 
            raise commands.CommandError(message="Unvalid tag")
            return 
          
        colors = [0xF0EF17 , 0x11A6F9 , 0xF80A0A]
        
        problems = requests.get(f"https://codeforces.com/api/problemset.problems?tags={tag.replace(' ','')}")
        if diff : 
            probs = []
            ps= sorted(problems.json()["result"]["problems"] , key = lambda x : x["contestId"])
            for p in ps : 
                try : 
                    if abs(p["rating"] - diff) < 100 : 
                        probs.append(p)
                except :
                    pass
            if probs : 
                prob = random.choice(probs)

        if not diff or probs == [] :
            prob = random.choice(problems.json()["result"]["problems"])
        try  :
            rating = prob['rating']
        except :
            try : 
                rating = prob['points']
            except : 
                rating = "NULL"

        em = discord.Embed(color = random.choice(colors))
        em.title = prob["name"]
        em.add_field(name = "Link :" , value = f"https://codeforces.com/problemset/problem/{prob['contestId']}/{prob['index']}", inline=False)
        em.add_field(name = "Rating" , value = rating, inline=False)
        if tag == "" :
            em.add_field(name = "Tags" , value="||" + "|| ||".join(prob["tags"]) + "||", inline=False)
        else : 
            em.add_field(name = "Tags" , value=" | ".join(prob["tags"]), inline=False)
        await ctx.send(embed = em)
        pracc_users.update_one({"user_id":ctx.author.id},{"$inc" : {"problems_requested" : 1}})
    
    @problem.error
    async def problem_error(self,ctx,error):
        if error == "Unvalid Tag" : 
            await ctx.send("Unvalid TAG , Use '!problem tags' to get the full list of Tags.")   






def setup(client):
    client.add_cog(Problemset(client))