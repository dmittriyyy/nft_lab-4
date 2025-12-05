from tonsdk.contract.token.nft import NFTCollection, NFTItem
from tonsdk.contract import Address
from tonsdk.utils import to_nano
from wallet import wallet_address as my_wallet_address

GIST_BASE_URL = "https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw"
COLLECTION_ADDRESS = "kQATeRp5YOTP7UkhhVM_P9fE4xpro6gQCwb4ZjHuc2gR0bsu"

metadata_urls = [
    "https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/metadata_1.json",
    "https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/metadata_2.json",
]

def create_collection_mint():
    owner = Address('0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8')
    return NFTCollection(
        royalty_base=1000,
        royalty=55,
        royalty_address=owner,
        owner_address=owner,
        collection_content_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/meta.json',
        nft_item_content_base_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/',
        nft_item_code_hex=NFTItem.code
    )


def create_batch_nft_mint(
    count=5,
    metadata_urls=None,
    owners=None,
    start_index=9
):

    
    collection = create_collection_mint()
    contents_and_owners = []
    
    
    if metadata_urls is None:
        metadata_urls = [
            "https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/metadata_1.json"
        ] * count
    
    
    if owners is None:
        owners = [Address(my_wallet_address)] * count
    
   
    print(f"\n Создаю батч из {count} NFT:\n")
    
    for i in range(count):
        metadata_url = metadata_urls[i % len(metadata_urls)]
        owner = owners[i % len(owners)]
        
        contents_and_owners.append((metadata_url, owner))
        print(f"NFT #{start_index + i}")
        print(f"Метаданные: {metadata_url}")
        print(f"Владелец: {owner.to_string()}\n")
    

    body = collection.create_batch_mint_body(
        from_item_index=start_index,
        contents_and_owners=contents_and_owners,
        amount_per_one=to_nano(0.01, 'ton')
    )
    

    return body, contents_and_owners
