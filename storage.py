from pymongo import MongoClient

cluster = MongoClient('mongodb://localhost:27017')
collection = cluster.local.first
second = cluster.local.second

async def update_data(username,balance, wallet):

    user = {
        "username": username,
        "balance": balance,
        "wallet": wallet,
    }

    try:
        await collection.insert_one(user)
        return 0

    except:
        print('error')
        return 1


def update_withdraw(username,wallet,balance):
    query = {
        "username":username,
        "wallet":wallet,
        "balance": balance
    }

    try:
        second.insert_one(query)
        return 0

    except:
        print('error')
        return 1

def check_len(items):
    count = 0
    for item in items:
        count+=1

    return count



obj = collection.find({
        "username": {"$eq":746919662}
    })

collection.update_one({"username":21892},{"$set":{"balance":0.5}})
