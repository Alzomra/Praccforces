from pymongo import mongo_client
import requests 
from db import * 
import random

BASE_URL = "https://codeforces.com/problemset/problem/"

# problems = requests.get("https://codeforces.com/api/problemset.problems?tags=").json()
# print(problems["status"])

# with open("./probs.txt",'w', encoding="utf-8") as probs : 
#     for problem in problems["result"]["problems"] : 
#         if (not problem.get("rating" , None)) : 
#             if(not problem.get("points" , None)) : 
#                 pracc_problems.insert_one({"name" : problem['name'] , "tags" : problem['tags'] , "link" : f"{BASE_URL}{problem['contestId']}/{problem['index']}" })
#             else : 
#                 pracc_problems.insert_one({"name" : problem['name'] , "rating" : problem['points'] , "tags" : problem['tags'] , "link" : f"{BASE_URL}{problem['contestId']}/{problem['index']}" })
#         else : 
#             pracc_problems.insert_one({"name" : problem['name'] , "rating" : problem['rating'] , "tags" : problem['tags'] , "link" : f"{BASE_URL}{problem['contestId']}/{problem['index']}" })




tags = ['dp']
problem = list(pracc_problems.find({"tags" : tags , "rating" : {"$gt" : 1200 } }))

print(random.choice(problem))