from db import pracc_users , pracc_servers

async def check_guild(ctx):
        guild = pracc_servers.find_one({"server_id":ctx.guild.id})
        if not guild : 
            pracc_servers.insert_one({"server_id":ctx.guild.id , "premium" : False , "region" : str(ctx.guild.region) })
    
async def check_user(member):
        user = pracc_users.find_one({"user_id":member.id})
        if not user : 
            pracc_users.insert_one({"user_id":member.id,"problems_requested" : 0 , "problems_solved" : 0 ,"contests_requested" : 0,"user_name" : str(member) ,"handle" : None ,"score" : 0})
