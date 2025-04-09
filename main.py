import sys
import logging
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import time
from io import BytesIO
import qrcode
import sys
from tonconnect import connector
import asyncio
from tonconnect.connector import AsyncConnector
from tonconnect.connector import Connector
from pytonconnect import TonConnect
from tonconnect.connector import AsyncConnector
from pytoniq_core import Address
import aiohttp
import asyncio
from pytonconnect import TonConnect
import config
import phrase
from phrase import phrases
from storage import update_data,check_len,collection,update_withdraw
from heplers import check_owner
from balance import collect

wallets_list = TonConnect.get_wallets()
print(wallets_list)
dp = Dispatcher()
bot = Bot(config.TOKEN)

@dp.message(CommandStart())
async def start(message: Message):
    username = message.from_user.id

    obj = collection.find({
        "username": {"$eq": username}
    })

    if check_len(tuple(obj)) == 0:
        update_data(username,0,'Null')

    await message.answer(text=phrase.phrases.get_greet(message.from_user.first_name))
    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text = 'Profitability and investment process', callback_data = 'process')
    inline_kb.button(text='My personal account', callback_data='account')
    inline_kb.button(text='Contact support',callback_data='support')
    inline_kb.adjust(1)
    await message.answer(text='What do you want to know?',reply_markup=inline_kb.as_markup())

@dp.callback_query(F.data == 'start')
async def start(call: CallbackQuery):
    await call.answer()
    username = call.message.chat.id

    obj = collection.find({
        "username": {"$eq": username}
    })

    if check_len(tuple(obj)) == 0:
        update_data(username,0,'Null')

    await call.message.answer(text=phrase.phrases.get_greet(call.from_user.first_name))
    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text='Profitability and investment process', callback_data = 'process')
    inline_kb.button(text='My personal account', callback_data='account')
    inline_kb.button(text='Contact support',callback_data='support')
    inline_kb.adjust(1)
    await call.message.answer(text='What do you want to know?',reply_markup=inline_kb.as_markup())

@dp.callback_query(F.data == "process")
async def process(call:CallbackQuery):
    await call.answer()
    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text="Back", callback_data='start')
    inline_kb.adjust(1)
    await call.message.answer(text=open("chance").read(), reply_markup=inline_kb.as_markup())

@dp.callback_query(F.data == "account")
async def account(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='Welcome to your personal account! 👋')
    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text="Connect wallet",callback_data="connect")
    inline_kb.button(text="Balance", callback_data="balance")
    inline_kb.button(text="Withdraw", callback_data="withdraw")
    inline_kb.button(text="Back",callback_data='start')
    inline_kb.adjust(1)
    await callback.message.answer(text="Here you can",reply_markup=inline_kb.as_markup())




@dp.callback_query(F.data == "connect")
async def connect(callback: CallbackQuery):
    await callback.answer()
    username = callback.message.chat.id
    print(username)
    obj = collection.find({
        "username": {"$eq": username}
    })
    obj = dict(tuple(obj)[0])

    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json',
        # api_tokens={'tonapi': 'key'},
    )

    generated_url = await connector.connect(wallets_list[0])

    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text='Connect',url=generated_url)
    await callback.message.answer(text='You have 3 minutes to connect',reply_markup=inline_kb.as_markup())

    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                inline_kb = InlineKeyboardBuilder()
                inline_kb.button(text='Back',callback_data="account")
                if obj['balance'] > 0:
                    await callback.message.answer(f'You are connected with address {wallet_address}',reply_markup=inline_kb.as_markup())
                else:
                    await callback.message.answer(f'You are connected with address {wallet_address}\n\n+0.5 TON for first connect\nYour balance - 0.5 TON',
                                                  reply_markup=inline_kb.as_markup())
                    obj['balance'] = obj['balance'] + 0.5
                    collection.update_one({"username":username},{'$set':{'balance' : 0.5,'wallet':wallet_address}})
                break

@dp.callback_query(F.data == "balance")
async def balance(call: CallbackQuery):
    await call.answer()
    username = call.message.chat.id
    obj = collection.find({
        "username": {"$eq": username}
    })
    obj = dict(tuple(obj)[0])
    balance = obj['balance']

    i_kb = InlineKeyboardBuilder()
    i_kb.button(text="Back",callback_data="account")
    await call.message.answer(text=f'Your balance - {balance} TON',reply_markup=i_kb.as_markup())

@dp.callback_query(F.data == "card")
async def card(call: CallbackQuery):
    await call.answer()
    username = call.message.chat.id
    obj = collection.find({
        "username": {"$eq": username}
    })
    obj = dict(tuple(obj)[0])
    wallet = obj["wallet"]
    list_item = check_owner(wallet)["nft_items"]
    if len(list_item) == 0:
        i_kb = InlineKeyboardBuilder()
        i_kb.button(text="Back", callback_data="account")
        await call.message.answer(text ='You have 0 TRADERS CARD items(', reply_markup=i_kb.as_markup())
    else:
        i_kb = InlineKeyboardBuilder()
        i_kb.button(text="Back", callback_data="account")
        collection.update_one({"username": username}, {'$set': {'balance': 2.5}})
        await call.message.answer(text=f'+2 TON for your items \n\n Your balance - 2.5 TON', reply_markup=i_kb.as_markup())



@dp.callback_query(F.data == "withdraw")
async def withdraw(call:CallbackQuery):
    await call.answer()
    username = call.message.chat.id
    obj = collection.find({
        "username": {"$eq": username}
    })
    obj = dict(tuple(obj)[0])
    balance = obj["balance"]
    i_kb = InlineKeyboardBuilder()
    i_kb.button(text="Back", callback_data="account")
    i_kb.button(text="Withdraw", callback_data="query")
    i_kb.adjust(1)
    await call.message.answer(text=f'Your balance - {balance} TON,click here to withdraw', reply_markup=i_kb.as_markup())

@dp.callback_query(F.data == "query")
async def query(call:CallbackQuery):
    await call.answer()
    username = call.message.chat.id
    obj = collection.find({
        "username": {"$eq": username}
    })
    obj = dict(tuple(obj)[0])


    i_kb = InlineKeyboardBuilder()
    i_kb.button(text="Back", callback_data="account")
    await call.message.answer(text=f'Request was successfully created\n\nyour balance - 0 TON',
                              reply_markup=i_kb.as_markup())
    collection.update_one({"username": username}, {'$set': {'balance': 0.0,}})
    update_withdraw(username,obj['wallet'],obj["balance"])


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # skip_updates = True
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(collect())
















"""async def main():
    session = aiohttp.ClientSession()
    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json',
        # api_tokens={'tonapi': 'key'},
    )
    is_connected = await connector.restore_connection()
    print('is_connected:', is_connected)

    generated_url = await connector.connect(wallets_list[0])
    print('generated_url:', generated_url)


    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                print(wallet_address)
                break
    await session.close()
"""

