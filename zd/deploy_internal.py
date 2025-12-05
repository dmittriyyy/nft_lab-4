import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

from wallet import wallet, wallet_address
from nft import *

import requests
from pathlib import Path

from tsk4 import create_batch_nft_mint, create_collection_mint, COLLECTION_ADDRESS, metadata_urls

async def get_client():
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=0, config=config, keystore=keystore_dir, tonlib_timeout=120)

    await client.init()

    return client


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


async def deploy_collection():

    collection = create_collection_mint2()
    state_init = collection.create_state_init()['state_init']

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=collection.address.to_string(),
                                   amount=to_nano(0.05, 'ton'), seqno=seqno, state_init=state_init)

    await client.raw_send_message(query['message'].to_boc(False))


async def deploy_one_item():
    body = create_nft_mint()
    collection = create_collection_mint2()

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=collection.address.to_string(),
                                   amount=to_nano(0.04, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))


async def deploy_batch_items():
    body = create_batch_nft_mint()
    collection = create_collection_mint()

    client = await get_client()

    seqno = await get_seqno(client, wallet_address)

    query = wallet.create_transfer_message(to_addr=collection.address.to_string(),
                                   amount=to_nano(0.2, 'ton'), seqno=seqno, payload=body)

    await client.raw_send_message(query['message'].to_boc(False))

async def find_next_index():
    collection = create_collection_mint()
    address = collection.address.to_string()
    print(f"Проверяем коллекцию: {address}")
    client = await get_client()
    try:
        data = await client.raw_run_method(method='get_collection_data', stack_data=[], address=address)
        next_index = int(data['stack'][0][1], 16)  
        print(f"------------------------------------------------")
        print(f"СЛЕДУЮЩИЙ СВОБОДНЫЙ ИНДЕКС: {next_index}")
        print(f"------------------------------------------------")
        return next_index
    except Exception as e:
        print(f"Ошибка получения данных {e}")
        return 0

async def deploy_batch_items2():

    try:
        count = int(input("Сколько NFT минтить: "))
        if count <= 0:
            print(" Количество должно быть больше 0!")
            return
    except ValueError:
        print(" Введи корректное число!")
        return
    
    
    try:

        body, nft_info = create_batch_nft_mint(
            count=count,
            metadata_urls=metadata_urls,
            start_index=9
        )
        
        collection = create_collection_mint()
        client = await get_client()
        seqno = await get_seqno(client, wallet_address)
        
        total_amount = count * 0.01 + 0.05
        
        print(f" Отправляю {total_amount} TON...")
        
        query = wallet.create_transfer_message(
            to_addr=COLLECTION_ADDRESS,
            amount=to_nano(total_amount, 'ton'),
            seqno=seqno,
            payload=body
        )
        
        await client.raw_send_message(query['message'].to_boc(False))
        
        print("\n" + "=" * 70)
        print("УСПЕШНО ОТПРАВЛЕНО!")
        print("=" * 70)
        print(f"Заминчено NFT: {count}")
        
    except Exception as e:
        print(f" ОШИБКА: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(deploy_one_item())