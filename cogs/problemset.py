import discord
from discord.ext import commands
import random
import requests
from db import pracc_users , pracc_servers
from checks import check_user , check_guild
import emoji


class Problemset(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.tags ="""implementation ,math ,greedy ,dp ,data ,structures ,brute ,force ,constructive 
                    algorithms ,graphs ,sortings ,binary ,search ,dfs and similar ,trees ,strings ,number theory,combinatorics ,*special ,geometry ,bitmasks ,two pointers ,dsu shortest paths 
                    probabilities ,divide and conquer ,hashing ,games ,flows ,interactive matrices 
                    string suffix ,structures ,fft ,graph matchings ,ternary search expression 
                    parsing ,meet-in-the-middle ,2-sat chinese remainder theorem,schedules"""
    
    
    @commands.command()
    async def problem(self,ctx,*args):
        await check_guild(ctx)
        await check_user(ctx.author)
        args = list(args)
        ok = True 
        for arg in args : 
            if arg in emoji.UNICODE_EMOJI :
                ok = False
                break
        if ok :
            if len(args) == 0 : 
                tag = ''
                diff = 0
            if len(args) == 1: 
                try : 
                    args[0] = int(args[0])
                except ValueError :
                    tag = args[0]
                    diff = 0 
                else :
                    diff = args[0]
                    tag = ''
            if len(args) >= 2 :
                try : 
                    args[0] = int(args[0])
                except ValueError :
                    tag = args[0]
                    diff = int(args[1]) 
                else :
                    diff = args[0]
                    tag = args[1]

            print(tag,diff)
            if f"{tag}" not in self.tags.replace(",","") and tag != "" : 
                await ctx.send(f"Available tags :\n{self.tags}")   
                ok = False

        if ok :

            colors = [0xF0EF17 , 0x11A6F9 , 0xF80A0A]
            problems = requests.get(f"https://codeforces.com/api/problemset.problems?tags={tag.replace('*','')}")
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
                x = random.randint(1,1000)
                for i,problem in enumerate(problems.json()["result"]["problems"]) :
                    if x == i :
                        break 
                    prob = problem

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
        await ctx.send("Please check command arguments!")   






def setup(client):
    client.add_cog(Problemset(client))