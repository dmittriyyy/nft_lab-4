import asyncio
import requests
from tonsdk.contract.token.nft import NFTCollection
from tonsdk.contract import Address
from nft import create_collection_mint2 

BASE_URL = "https://testnet.tonapi.io/v2"



async def get_collection_info_and_nfts(collection_address_str):
    print("--- Информация о коллекции ---")
    collection_obj = create_collection_mint2() # Получаем объект коллекции из вашего кода
    # Используем getattr для безопасного получения атрибутов, если их нет в объекте
    owner_addr = getattr(collection_obj, 'owner_address', None)
    collection_owner_str = owner_addr.to_string() if owner_addr and hasattr(owner_addr, 'to_string') else 'Не указан при создании (наш объект не хранит его явно)'

    content_uri = getattr(collection_obj, 'collection_content_uri', 'Не указан')
    base_uri = getattr(collection_obj, 'nft_item_content_base_uri', 'Не указан')
    royalty_base = getattr(collection_obj, 'royalty_base', 'N/A')
    royalty_factor = getattr(collection_obj, 'royalty_factor', 'N/A')
    royalty_addr = getattr(collection_obj, 'royalty_address', None)
    royalty_addr_str = royalty_addr.to_string() if royalty_addr and hasattr(royalty_addr, 'to_string') else 'N/A'

    print(f"Адрес коллекции: {collection_obj.address.to_string()}")
    print(f"Адрес владельца коллекции: {collection_owner_str}")
    print(f"URI контента коллекции: {content_uri}")
    print(f"Базовый URI контента NFT: {base_uri}")
    print(f"Параметры роялти (base/factor): {royalty_base} / {royalty_factor}")
    print(f"Адрес роялти: {royalty_addr_str}")


    print("\n--- Список NFT в коллекции (получение через API) ---")
    headers = {
        'Accept': 'application/json',
    }

    try:
        # Запрос к API для получения NFT в коллекции
        url = f"{BASE_URL}/nfts/collections/{collection_address_str}/items"
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Проверка на ошибки HTTP
        data = response.json()

        nft_list = data.get('nft_items', [])
        if not nft_list:
            print("Коллекция пуста или NFT не найдены через API.")
            return

        print(f"Найдено {len(nft_list)} NFT в коллекции.")

        for i, nft_item in enumerate(nft_list):
            print(f"\n--- NFT #{i+1} ---")
            nft_address = nft_item.get('address', 'N/A')
            # Правильная обработка поля owner
            owner_info = nft_item.get('owner')
            nft_owner_address = 'N/A (No Owner Yet)' # Значение по умолчанию, если owner пустой
            if owner_info:
                # API tonapi возвращает owner как словарь с полем address
                nft_owner_address = owner_info.get('address', 'N/A (Owner Info Malformed)')
            # Если owner_info == None, nft_owner_address останется 'N/A (No Owner Yet)'

            # Используем get для content и затем get для uri
            content_info = nft_item.get('content', {})
            nft_content_uri = content_info.get('uri', 'N/A')

            print(f"  Адрес NFT: {nft_address}")
            print(f"  Адрес владельца: {nft_owner_address}")
            print(f"  URI контента: {nft_content_uri}")

            # --- Получение и отображения метаданных ---
            if nft_content_uri and nft_content_uri != 'N/A':
                print("  Метаданные (получение с URI):")
                try:
                    # Обработка URI: если он относительный (например, '1/meta.json'), добавляем базовый URI
                    full_uri = nft_content_uri
                    # Проверим, является ли URI относительным и попробуем восстановить полный,
                    # используя base_uri из коллекции, если API вернул относительный путь.
                    collection_obj = create_collection_mint2()
                    base_uri = getattr(collection_obj, 'nft_item_content_base_uri', '')
                    if base_uri and not nft_content_uri.startswith('http'):
                         full_uri = base_uri.rstrip('/') + '/' + nft_content_uri.lstrip('/')
                         print(f"    (Конструируется полный URI из base: {full_uri})")

                    metadata_response = requests.get(full_uri)
                    metadata_response.raise_for_status()
                    metadata_json = metadata_response.json()
                    print(f"    {metadata_json}")
                except requests.exceptions.RequestException as e:
                    print(f"    Ошибка при получении метаданных с {full_uri}: {e}")
                except ValueError: # json.decoder.JSONDecodeError является подклассом ValueError
                    print(f"    Ошибка: Полученный контент с {full_uri} не является валидным JSON.")
            else:
                print("  Метаданные: URI контента отсутствует или недоступен.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API для получения NFT коллекции: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


async def main():
    # Используем адрес коллекции, созданный внутри функции
    collection_obj = create_collection_mint2()
    collection_address_str = collection_obj.address.to_string()

    print(f"Получение информации для коллекции: {collection_address_str}\n")
    await get_collection_info_and_nfts(collection_address_str)


if __name__ == "__main__":
    asyncio.run(main())