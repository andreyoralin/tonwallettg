import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from heplers import check_owner  # Убедитесь, что у вас есть этот модуль

# Подключение к базе данных MongoDB
cluster = AsyncIOMotorClient('mongodb://localhost:27017')
collection = cluster.local.first


async def collect():
    while True:
        async for document in collection.find():
            adress = document["wallet"]
            balance = document["balance"]
            try:
                a = check_owner(adress)["nft_items"]
                for i in a:
                    rarity = i['metadata']["attributes"][0]["value"]
                    if rarity == "Diamond":
                        balance += 1
                    elif rarity == "Platinum":
                        balance += 0.4
                    elif rarity == "Golden":
                        balance += 0.2
                    elif rarity == "Basic":
                        balance += 0.05
                    else:
                        print('none')

                await collection.update_one({"wallet": adress}, {'$set': {'balance': balance}})
            except Exception as err:
                print('Ошибка:\n', err)

        await asyncio.sleep(86400)

async def main():
    await collect()



if __name__ == "__main__":
    asyncio.run(main())

