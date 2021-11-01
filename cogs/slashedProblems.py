# cog.py
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext , manage_commands
import random
from db import pracc_contests, pracc_problems
from Codeforces import PROBLEMSET_TAGS

BASE_URL_CONTEST = "https://codeforces.com/contest/"
BASE_URL_PROBLEM = "https://codeforces.com/problemset/problem/"



class SlashedProblems(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="Problem" , description="Get a problem with a specified rating and tags." , options=[
    manage_commands.create_option(name="rating" , description="Problem Rating" , option_type=int , required=False),
    manage_commands.create_option(name="tags" , description="Problem Tags" , option_type=str , required=False),
    manage_commands.create_option(name="wild" , description="Use wild tags" , option_type=bool , required=False),
    manage_commands.create_option(name="help" , description="Problem command help" , option_type=bool , required=False )])
    async def problem(self, ctx: SlashContext , rating : int = 0, tags="" , help = "" , wild = False):
        em = Embed(color = 0xFFFFFF)
        if help : 
            em.title = "All Tags"
            em.add_field(name = "Usage(slash command) :" , value="/problem rating:1200 tags:-dp -math")
            em.add_field(name = "Regular Usage :" , value="!problem 1200 -dp -math")
            em.description = " * ".join(PROBLEMSET_TAGS)
            await ctx.send(embed = em)
            return

        if '-' not in tags : 
            tags = []
            
        if tags : 
            tags = tags.split("-")
            tags = list(map(lambda item : item.strip() , tags))
            try : 
                tags.remove('')
            except ValueError :
                pass 

            tags.sort()

        colors = [0xF0EF17 , 0x11A6F9 , 0xF80A0A]
        em = Embed(color = random.choice(colors))
        if not tags and not rating:
            rating = random.randint(8,40) * 100
            problems = list(pracc_problems.find({ "rating" : {"$gte" : rating-100, "$lte" : rating + 100} }))
        elif not tags :
            problems = list(pracc_problems.find({"rating" : rating}))
        elif not rating :
            if wild : 
                problems = list(pracc_problems.find({"rating" : { "$all" : tags } }))
            else :
                problems = list(pracc_problems.find({"tags" : tags}))
        else :
            if wild : 
                problems = list(pracc_problems.find({"tags" : { "$all" : tags } , "rating" : rating }))
            else : 
                problems = list(pracc_problems.find({"tags" :  tags , "rating" : rating }))

        if not problems :
            problems = list(pracc_problems.find({"tags" : { "$all" : tags } , "rating" : rating }))
        if not problems : 
            problems = list(pracc_problems.find({"tags" : { "$all" : tags } , "rating" : {"$gte" : rating , "$lte" : rating + 400 } }))

        if not problems : 
            em.description = "No Problem Found with provided arguments , Use '!problem tags' to get the full list of Tags.\n try changing the rating or vary the tags"
            await ctx.send(embed = em)
            return
        prob = random.choice(problems)
        em.title = prob["name"]
        em.add_field(name = "Link :" , value = f"{BASE_URL_PROBLEM}{prob['contestId']}/{prob['index']}/", inline=False)
        em.add_field(name = "Rating" , value = prob["rating"], inline=False)
        if not prob['tags'] : 
            em.add_field(name = "Tags" , value="Problem Has no tags.", inline=False)
        elif not tags:
            em.add_field(name = "Tags" , value="||" + "|| ||".join(prob["tags"]) + "||", inline=False)
        else : 
            em.add_field(name = "Tags" , value=" | ".join(prob["tags"]), inline=False)
        await ctx.send(embed = em)
    


def setup(bot: Bot):
    bot.add_cog(SlashedProblems(bot))