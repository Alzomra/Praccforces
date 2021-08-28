import discord
from discord.ext import commands , tasks
import requests
from db import pracc_users

class Events(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name = "Codeforces"))
        self.stat_refresh.start()
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
        users = pracc_users.find({})
        for user in users:
            if user["handle"] : 
                request = requests.get(f"https://codeforces.com/api/user.info?handles={user['handle']}")
                score = request.json().get("result",[{"rating" : 0}])[0]["rating"]
                pracc_users.update_one({"user_id" : user["user_id"]}, {"$set" : {"score" : score} })
        


        







def setup(client):
    client.add_cog(Events(client))