from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

cluster = MongoClient(os.environ.get("DATABASE_URI"))
db = cluster["Praccforces"]
pracc_servers = db["servers"]
pracc_users = db["users"]
pracc_probs = db["problems"]
pracc_contests = db["contests"]
pracc_problems = db["problems"]
