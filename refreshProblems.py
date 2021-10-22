import requests
from db import * 
import random

BASE_URL = "https://codeforces.com/contest/"

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




""" tags = ['dp']
problem = list(pracc_problems.find({"tags" : tags , "rating" : {"$gt" : 1200 } }))
"""

#contests = requests.get("https://codeforces.com/api/contest.list?gym=false").json()

# for contest in contests["result"] :
#     if "Div. " in contest['name'] : 
#         pracc_contests.insert_one({"id" : contest['id'] , "name" : contest['name'] , "phase" : contest['phase'] , "startTime" :contest['startTimeSeconds'] , "link" : f"{BASE_URL}{contest['id']}" , "div" : contest['name'][contest['name'].find("Div. ")+5] })
#     else : 
#         pracc_contests.insert_one({"id" : contest['id'] , "name" : contest['name'] , "phase" : contest['phase'] , "startTime" :contest['startTimeSeconds'] , "link" : f"{BASE_URL}{contest['id']}"})
        


# contest = pracc_contests.find_one({"div" : "2" , "phase" : "FINISHED"})
# problems = pracc_problems.find({"link" : {"$regex" : str(contest['id'])}})


# for problem in problems: 
#     print(problem)

#### NOT RAN WITH GT

# with open("newprobs.txt" , "w") as file :
#     contests = pracc_contests.find({"id" : {"$lt" : 128 , "$gt" : 0}})
#     for contest in contests :
#         try  :
#             problems = requests.get(f"https://codeforces.com/api/contest.standings?contestId={contest['id']}").json()["result"]["problems"]
#         except : 
#             print(contest['id'] , "isfucked")
#         else : 
#             print("scanning" , contest['id'])
#             for problem in problems : 
#                 exists = pracc_problems.find_one({"contestId" : contest['id'] , "index" : problem['index']})
#                 if not exists : 
#                     try : 
#                         file.write(f"{problem['name']} , {problem['index']}")
#                     except : 
#                         file.write(f"{problem['index']}")
#                     if (not problem.get("rating" , None)) : 
#                         if(not problem.get("points" , None)) : 
#                             pracc_problems.insert_one({"name" : problem['name'] , "tags" : problem['tags'] , "contestId" : problem["contestId"], "index" : problem['index']})
#                         else : 
#                             pracc_problems.insert_one({"name" : problem['name'] , "rating" : problem['points'] , "tags" : problem['tags'] , "contestId" : problem["contestId"], "index" : problem['index']})
#                     else : 
#                         pracc_problems.insert_one({"name" : problem['name'] , "rating" : problem['rating'] , "tags" : problem['tags'] , "contestId" : problem["contestId"], "index" : problem['index'] })

problems = pracc_problems.find({})
removed = 0
for problem in problems :
    remo = True
    while remo :
        pracc_problems.delete_one({"contestId" : problem['contestId'] , "index" : problem['index']})
        removed +=1
        prob = pracc_problems.find_one({"contestId" : problem['contestId'] , "index" : problem['index']})
        if not prob :
            removed-=1
            prob = pracc_problems.insert_one(problem)
            remo = False
        
print(removed)

exit()

contests = requests.get("https://codeforces.com/api/contest.list?gym=false").json()['result']

for contest in contests :
    check = pracc_contests.find_one({"id" : contest['id']})
    if not check : 
        pracc_contests.insert_one({"id" : contest['id'] , "name" : contest['name'] , "phase" : contest['phase'] , "startTime" :contest['startTimeSeconds'] , "link" : f"{BASE_URL}{contest['id']}"})
    else :
        if check['phase'] != contest['phase'] : 
            pracc_contests.update({"id" : contest["id"]} , {"$set" : {"phase" : contest['phase']}}) 
        else : 
            break

        
exit()




contests = pracc_contests.find({"phase" : "FINISHED" , "fetched" : {"$exists" : False}})

for contest in contests :
    problem = pracc_problems.find_one({"link" : {"$regex" : str(contest['id'])}}) 
    if not problem :
        try : 
            problems = requests.get(f"https://codeforces.com/api/contest.standings?contestId={contest['id']}").json()["result"]["problems"]
        except : 
            print(contest)
        for problem in problems : 
            if (not problem.get("rating" , None)) : 
                if(not problem.get("points" , None)) : 
                 pracc_problems.insert_one({"name" : problem['name'] , "tags" : problem['tags'] , "contestId" : problem["contestId"], "index" : problem['index']})
                else : 
                 pracc_problems.insert_one({"name" : problem['name'] , "rating" : problem['points'] , "tags" : problem['tags'] , "contestId" : problem["contestId"], "index" : problem['index']})
            else : 
             pracc_problems.insert_one({"name" : problem['name'] , "rating" : problem['rating'] , "tags" : problem['tags'] , "contestId" : problem["contestId"], "index" : problem['index'] })
    pracc_contests.update_one({"id" : int(contest["id"]) } , {"$set" : {"fetched" : True}})


