from tonsdk.contract.token.nft import NFTCollection, NFTItem
from tonsdk.contract import Address
from tonsdk.utils import to_nano


from wallet import wallet_address as my_wallet_address

GIST_ID = "48730d6d78afd0bff86afff5f5c8be33"
GIST_BASE_URL = f"https://gist.githubusercontent.com/dmittriyyy/{GIST_ID}/raw"


def create_collection_mint():
    royalty_base = 1000 
    royalty_factor = 55 
    
    collection = NFTCollection(royalty_base=royalty_base,
                               royalty=royalty_factor)
    
    owner = Address('0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8')

    collection = NFTCollection(
        royalty_base=royalty_base, 
        royalty=royalty_factor, 
        royalty_address=owner,  # Роялти идут мне
        owner_address=owner,    # Владелец - я
        collection_content_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/meta.json',
        nft_item_content_base_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/',
        nft_item_code_hex=NFTItem.code
        # код смарт‑контракта одного NFT‑айтема, который коллекция будет использовать при минте новых токенов
    )
 
    return collection

def create_collection_mint2(version=1):
    royalty_base = 1000 
    royalty_factor = 55 
    
    owner = Address('0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8')

    collection = NFTCollection(
        royalty_base=royalty_base, 
        royalty=royalty_factor, 
        royalty_address=owner,
        owner_address=owner,
        # Метаданные коллекции
        collection_content_uri=f'{GIST_BASE_URL}/meta.json',
        # Базовый URL для NFT айтемов
        nft_item_content_base_uri=f'{GIST_BASE_URL}/',
        nft_item_code_hex=NFTItem.code
    )
 
    return collection



def create_nft_mint(index=9, owner_address='0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8'):
    collection = create_collection_mint()
    
    metadata_url = f'https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/metadata_{1}.json'
    
    body = collection.create_mint_body(
        item_index=index,
        new_owner_address=Address(owner_address),
        item_content_uri=metadata_url,  
        amount=to_nano(0.02, 'ton')
    )
    return body


def create_batch_nft_mint(index=0, address='kQATeRp5YOTP7UkhhVM_P9fE4xpro6gQCwb4ZjHuc2gR0bsu'):

    collection = create_collection_mint()

    contents_and_owners = []

    for i in range(1, 5):
        contents_and_owners.append((f'{i + 1}/meta.json', Address('kQATeRp5YOTP7UkhhVM_P9fE4xpro6gQCwb4ZjHuc2gR0bsu')))

    body = collection.create_batch_mint_body(from_item_index=1,
                                      contents_and_owners=contents_and_owners,
                                      amount_per_one=to_nano(0.01, 'ton'))
    return body