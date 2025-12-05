import asyncio
from tonsdk.contract.token.nft import NFTCollection, NFTItem
from tonsdk.contract import Address
from tonsdk.utils import to_nano
from pytonlib import TonlibClient
import requests
from pathlib import Path
from wallet import wallet, wallet_address

# ... (остальные функции см. в deploy_nft_simple.py)

async def deploy_one_item():
    # 📌 ВСТАВЬ СЮДА GITHUB GIST ССЫЛКУ:
    METADATA_URL = "https://gist.githubusercontent.com/твоё_имя/.../raw/metadata.json"
    
    body = create_nft_mint(METADATA_URL)
    collection = create_collection_mint()
    client = await get_client()
    seqno = await get_seqno(client, wallet_address)
    
    query = wallet.create_transfer_message(
        to_addr=collection.address.to_string(),
        amount=to_nano(0.04, 'ton'),
        seqno=seqno,
        payload=body
    )
    
    await client.raw_send_message(query['message'].to_boc(False))
    
    print("✓ NFT отправлен на блокчейн!")
    print(f"✓ Адрес коллекции: {collection.address.to_string()}")

asyncio.run(deploy_one_item())
