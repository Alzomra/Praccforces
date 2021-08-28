from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://alzomra:jLu6iSxlLSZXPj9C@discord-8kued.mongodb.net/test?retryWrites=true&w=majority")
db=cluster["Praccforces"]
pracc_servers = db["servers"]
pracc_users = db["users"] 
pracc_probs = db["problems"]
pracc_contests = db["contests"] 