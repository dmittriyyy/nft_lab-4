Главная
Аккаунт
Установить

почему минтятся пустые нфт без инфы
11 вложений
Почему создаются пустые NFT без информации

Я нашел несколько критических проблем в вашем коде, которые приводят к созданию пустых NFT:
Основная проблема 1: Неправильная передача URI метаданных в nft.py

В функции create_nft_mint() (файл nft.py):

python
metadata_url = f'https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/metadata_{1}.json'

Проблема: Вместо использования переменной index вы жёстко указали {1}, поэтому всегда используется metadata_1.json независимо от индекса NFT. Это создаёт некорректный URL.

Решение:

python
def create_nft_mint(index=7, owner_address='0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8'):
    collection = create_collection_mint()
    metadata_url = f'https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/metadata_{index}.json'  # index вместо 1
    body = collection.create_mint_body(
        item_index=index,
        new_owner_address=Address(owner_address),
        item_content_uri=metadata_url,
        amount=to_nano(0.02, 'ton')
    )
    return body

Основная проблема 2: Несоответствие между create_batch_nft_mint в nft.py и tsk4.py

В файле nft.py функция create_batch_nft_mint() создаёт hardcoded пути:

python
for i in range(1, 5):
    contents_and_owners.append((f'{i + 1}/meta.json', Address('kQATeRp5YOTP7UkhhVM_P9fE4xpro6gQCwb4ZjHuc2gR0bsu')))

Проблема:

    Используются относительные пути ('2/meta.json', '3/meta.json' и т.д.), которые подставляются как-есть

    На базовый URI (nft_item_content_base_uri) не указывает (это https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/)

    Окончательные URLs становятся невалидными: https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/2/meta.json

Основная проблема 3: Неправильные URI в базовой коллекции

В nft.py:

python
collection_content_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/meta.json',
nft_item_content_base_uri='https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/',

Проблема: Эти URLs указывают на чужую коллекцию GetGems, не на ваши метаданные на Gist.

Решение: Используйте Gist URLs как в tsk4.py:

python
collection_content_uri='https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/meta.json',
nft_item_content_base_uri='https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/',

Исправленный код для nft.py:

python
from tonsdk.contract.token.nft import NFTCollection, NFTItem
from tonsdk.contract import Address
from tonsdk.utils import to_nano
from wallet import wallet_address as my_wallet_address

GIST_BASE_URL = "https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw"

def create_collection_mint():
    royalty_base = 1000
    royalty_factor = 55
    owner = Address('0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8')
    
    collection = NFTCollection(
        royalty_base=royalty_base,
        royalty=royalty_factor,
        royalty_address=owner,
        owner_address=owner,
        collection_content_uri=f'{GIST_BASE_URL}/meta.json',
        nft_item_content_base_uri=f'{GIST_BASE_URL}/',
        nft_item_code_hex=NFTItem.code
    )
    return collection

def create_nft_mint(index=7, owner_address='0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8'):
    collection = create_collection_mint()
    metadata_url = f'{GIST_BASE_URL}/metadata_{index}.json'  # Правильная подстановка index
    body = collection.create_mint_body(
        item_index=index,
        new_owner_address=Address(owner_address),
        item_content_uri=metadata_url,
        amount=to_nano(0.02, 'ton')
    )
    return body

def create_batch_nft_mint(count=5, metadata_urls=None, owners=None, start_index=0):
    collection = create_collection_mint()
    contents_and_owners = []
    
    if metadata_urls is None:
        # Создаём список правильных URL для каждого NFT
        metadata_urls = [f'{GIST_BASE_URL}/metadata_{i}.json' for i in range(1, count + 1)]
    
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

Резюме проблем:
Проблема	Причина	Следствие
Hardcoded {1} в URL	Ошибка подстановки переменной	Все NFT используют одни метаданные или невалидный URL
Относительные пути в batch	'2/meta.json' вместо полного URL	Блокчейн не может разрешить URL
Неправильный базовый URI	Ссылка на чужую коллекцию GetGems	Метаданные не найдены
Недоступные Gist метаданные	Файлы на Gist могут быть недоступны	NFT остаются пустыми

Обновите коды так, чтобы все URL были полными и указывали на ваши реальные метаданные на Gist.

смотри мне надо только нфт мой с картинкой сделать чтобы был ну и кодом что я тебе скинул для этого другую коллекцию надо создавать?

Нет, не надо создавать новую коллекцию. Нужно просто:

    Загрузить картинку на Gist (у вас уже есть izobrazhenie.jpg)

    Создать JSON метаданных с ссылкой на картинку

    Использовать этот JSON при минтинге NFT

Вот минимальный план:
Шаг 1: Загрузить картинку на Gist

Создайте новый Gist на https://gist.github.com с файлом image.jpg и скопируйте raw ссылку:

text
https://gist.githubusercontent.com/dmittriyyy/XXXXXX/raw/image.jpg

Шаг 2: Создать JSON метаданных

Обновите meta.json:

json
{
  "name": "Мой NFT",
  "description": "Мой первый NFT с картинкой",
  "image": "https://gist.githubusercontent.com/dmittriyyy/XXXXXX/raw/image.jpg"
}

Шаг 3: Залить JSON на Gist

Также добавьте его на Gist с именем meta.json и возьмите raw ссылку:

text
https://gist.githubusercontent.com/dmittriyyy/XXXXXX/raw/meta.json

Шаг 4: Минтить NFT

Используйте код из deploy_internal.py:

python
import asyncio
from deploy_internal import deploy_one_item

asyncio.run(deploy_one_item())

Это всё! Коллекция уже есть и работает. Нужно только поправить URLs в коде, чтобы они указывали на ваши метаданные с картинкой на Gist.

Нужна помощь с загрузкой на Gist? Могу помочь с форматом или скриптом.

у меня гист оказывается был приватным я сделал паблик но 
нфт все равно без описания и картинок даже новые
nft_fixed.py
Сгенерированный файл

Теперь вот что нужно сделать:
Чек-лист:

    Откройте ваш Gist и убедитесь:

        Гист паблик ✓ (сделали)

        Есть файлы: meta.json, metadata_1.json, картинка

    Скопируйте свой GIST ID из URL:

text
https://gist.github.com/dmittriyyy/YOUR_ID_HERE

Замените в коде строку:

    python
    GIST_ID = "48730d6d78afd0bff86afff5f5c8be33"  # На вашу

    Замените nft.py на исправленный (код выше)

    Минтите заново - теперь NFT будут с метаданными

Почему новые NFT тоже пустые?

Потому что вы тот же create_collection_mint() используете, который указывает на GetGems URLs. Блокчейн "запомнил" эту базовую коллекцию и все новые NFT используют неправильные URLs.

Если хотите новую коллекцию - используйте create_collection_mint2() с новым версионированием.

Какой GIST_ID у вас? Помогу проверить структуру.


nft_fixed.py
from tonsdk.contract.token.nft import NFTCollection, NFTItem
from tonsdk.contract import Address
from tonsdk.utils import to_nano
from wallet import wallet_address as my_wallet_address

# === ИЗМЕНИТЕ ЗДЕСЬ НА ВАШИ GIST URLs ===
GIST_ID = "48730d6d78afd0bff86afff5f5c8be33"  # Замените на ваш ID
GIST_BASE_URL = f"https://gist.githubusercontent.com/dmittriyyy/{GIST_ID}/raw"

def create_collection_mint():
    """Создаёт коллекцию NFT с правильными URLs на метаданные"""
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

def create_collection_mint2(version=1):
    """Версионированная коллекция"""
    royalty_base = 1000
    royalty_factor = 55
    owner = Address('0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8')
    
    collection = NFTCollection(
        royalty_base=royalty_base,
        royalty=royalty_factor,
        royalty_address=owner,
        owner_address=owner,
        collection_content_uri=f'{GIST_BASE_URL}/meta_v{version}.json',
        nft_item_content_base_uri=f'{GIST_BASE_URL}/v{version}/',
        nft_item_code_hex=NFTItem.code
    )
    return collection

def create_nft_mint(index=7, owner_address='0QD5clkU5m7dkLIs70CmTeyHf8UM_cybz26KyryoLunXYym8'):
    """Создаёт одиночный NFT с метаданными"""
    collection = create_collection_mint()
    # Правильная ссылка на метаданные
    metadata_url = f'{GIST_BASE_URL}/metadata_{index}.json'
    
    body = collection.create_mint_body(
        item_index=index,
        new_owner_address=Address(owner_address),
        item_content_u
