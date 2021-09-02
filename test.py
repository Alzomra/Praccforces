from CodeforcesAPI import Codeforces 

cf = Codeforces(api_key="2da07181f68098c7fb54b7e482a661e8ad4cb199" , secret="6259c639ad87989ff1bd0791d90a04ab4aea9541")

print(cf.contest().list())