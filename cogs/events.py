import discord
from discord.ext import commands , tasks
import requests
from db import pracc_users , pracc_servers

class Events(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name = "!help"))
        # self.fetch_new_contests.start()
        # self.fetch_new_problems.start()
        print("Ready to serve API")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if not self.client.get_user(payload.user_id) or self.client.get_user(payload.user_id).bot : 
            return
        if str(payload.emoji) == '✅' :
            channel = await self.client.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if f"Account link for {self.client.get_user(payload.user_id).name}" == message.embeds[0].footer.text :
                    auth_key = pracc_users.find_one({'user_id' : payload.user_id})['auth_key']
                    handle = message.embeds[0].fields[0].value.strip()
                    request = requests.get(f"http://codeforces.com/api/user.status?handle={handle}&count=1")
                    submittion_id = request.json().get("result",[{"id": 0 }])[0]['id']
                    contest_id = request.json().get("result",[{"contestId": 0 }])[0]['contestId']
                    request = requests.get(f"http://codeforces.com/contest/{contest_id}/submission/{submittion_id}")
                    em = message.embeds[0]
                    if str(auth_key) in request.text : 
                        em.description= "Verification successful , Account linked :white_check_mark:"
                        pracc_users.update_one({"user_id" : payload.user_id} , {"$set" : {"handle" : handle}})
                    else :
                        em.description = """Cannot find the authentication key ! Account not linked :x:
                                            If the problem precists , try changing the problem or join the support server"""
                    await message.edit(embed = em , suppress = False)


    @tasks.loop(minutes=300)
    async def stat_refresh(self):
        pass
        """   users = pracc_users.find({})
        for user in users:
            if user["handle"] : 
                request = requests.get(f"https://codeforces.com/api/user.info?handles={user['handle']}")
                score = request.json().get("result",[{"rating" : 0}])[0]["rating"]
                pracc_users.update_one({"user_id" : user["user_id"]}, {"$set" : {"score" : score} }) 
        """
        

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id != 894591966501818428 :
           return
        guild = member.guild
        role_name = "CP enthusiast"
        role = discord.utils.get(guild.roles, name=role_name)
        print(role)
        if role :
            await member.add_roles(role,reason=None,atomic=True)
        

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        guild = pracc_servers.find_one({"server_id" : guild.id})
        if not guild :
            pracc_servers.insert({"server_id" : guild.id, 
                                "premium" : False,
                                "region" : guild.region,
                                "inactive" : True})
            return

        pracc_servers.update({"server_id" : guild.id}, 
                              {"$set" : {"incative" : False}})
        return


    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        guild = pracc_servers.find_one({"server_id" : guild.id})
        if guild : 
            pracc_servers.update({"server_id" : guild.id}, 
                                {"$set" : {"incative" : True}})
            return
        
        pracc_servers.insert({"server_id" : guild.id, 
                              "premium" : False,
                              "region" : guild.region,
                              "incative" : False})

        






def setup(client):
    client.add_cog(Events(client))