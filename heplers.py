import requests


def check_owner(address: str) -> str:
    url = (f'https://tonapi.io/v2/accounts/{address}/nfts?collection=EQBtku7tDsgeI3M-qe3HDLGEQdefcJ-yOSBv5W-4seG7vwQl&limit=1000&offset=0&indirect_ownership=false')

    try:

        response = requests.get(url).json()
    except:
        print("Something went wrong...")
        return 'something went wrong'

    return response

adress = 'EQA54DqIcVxSKsNh0KYZIfqMjEPb4uw4UxRoJFdm8v0tYgcB'




def check_items(adress: str):
    a = check_owner(adress)["nft_items"]
    for i in a:
        rarity = i['metadata']["attributes"][0]["value"]
        print(rarity)

