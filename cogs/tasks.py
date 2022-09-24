import discord
from discord.ext import commands, tasks
import requests
from db import pracc_contests, pracc_problems


BASE_URL_CONTEST = "https://codeforces.com/contest/"


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fetch_new_contests.start()
        self.fetch_new_problems.start()

    @tasks.loop(seconds=3600)
    async def fetch_new_contests(self):
        print("UPDATING CONTESTS")
        contests = requests.get(
            "https://codeforces.com/api/contest.list?gym=false").json()['result']
        for contest in contests:
            check = pracc_contests.find_one({"id": contest['id']})
            if not check:
                pracc_contests.insert_one({"id": contest['id'], "name": contest['name'], "phase": contest['phase'],
                                          "startTime": contest['startTimeSeconds'], "link": f"{BASE_URL_CONTEST}{contest['id']}"})
            else:
                if contest['relativeTimeSeconds'] > 0:
                    pracc_contests.update_one({"id": contest["id"]}, {
                                              "$set": {"phase": "FINISHED"}})
                if check['phase'] == contest['phase'] and check['phase'] == "FINISHED":
                    break

    @tasks.loop(seconds=3780)
    async def fetch_new_problems(self):
        print("UPDATING PROBLEMS")
        contests = pracc_contests.find(
            {"phase": "FINISHED", "fetched": {"$exists": False}})
        for contest in contests:
            problem = pracc_problems.find_one(
                {"link": {"$regex": str(contest['id'])}})
            if not problem:
                try:
                    problems = requests.get(
                        f"https://codeforces.com/api/contest.standings?contestId={contest['id']}").json()["result"]["problems"]
                except:
                    pass
                else:
                    for problem in problems:
                        if (not problem.get("rating", None)):
                            if (not problem.get("points", None)):
                                pracc_problems.insert_one(
                                    {"name": problem['name'], "tags": problem['tags'], "contestId": problem["contestId"], "index": problem['index']})
                            else:
                                pracc_problems.insert_one(
                                    {"name": problem['name'], "rating": problem['points'], "tags": problem['tags'], "contestId": problem["contestId"], "index": problem['index']})
                        else:
                            pracc_problems.insert_one(
                                {"name": problem['name'], "rating": problem['rating'], "tags": problem['tags'], "contestId": problem["contestId"], "index": problem['index']})
                    pracc_contests.update_one({"id": int(contest["id"])}, {
                                              "$set": {"fetched": True}})


def setup(client):
    client.add_cog(Tasks(client))
