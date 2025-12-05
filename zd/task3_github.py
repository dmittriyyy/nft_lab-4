import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_REPO = os.getenv("GITHUB_REPO", "dmittriyyy/nft_lab-4")
GITHUB_TOKEN = os.getenv("GIT_TOKEN")
JSON_FILENAME = "metadata_1.json"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{JSON_FILENAME}"


def create_local_json():
    """Создаём JSON файл локально"""
    metadata = {
        "name": "Мой Уникальный NFT",
        "description": "Описание для задания 3.",
        "image": "https://habrastorage.org/getpro/habr/upload_files/d46/574/35e/d4657435edff35e9c525aa25fc667393.png",
        "attributes": [
            {"trait_type": "Редкость", "value": "Легендарный"},
            {"trait_type": "Тип", "value": "Коллекционный"}
        ]
    }
    
    with open(JSON_FILENAME, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print("✓ Шаг 1: JSON создан локально")
    return metadata

# ============= ШАГ 2: ВЫВЕСТИ ИНФОРМАЦИЮ ИЗ ЛОКАЛЬНОГО JSON =============
def read_local_json():
    """Читаем и выводим локальный JSON"""
    print("\n" + "="*60)
    print("ШАГ 2: ИСХОДНЫЕ МЕТАДАННЫЕ (локально):")
    print("="*60)
    
    with open(JSON_FILENAME, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"✓ Название: {data['name']}")
    print(f"✓ Описание: {data['description']}")
    print(f"✓ Атрибуты: {data['attributes']}")
    
    return data

# ============= ШАГ 3: ЗАГРУЗИТЬ JSON НА GITHUB =============
def upload_to_github():
    """Загружаем JSON на GitHub"""
    print("\n" + "="*60)
    print("ШАГ 3: ЗАГРУЗКА JSON НА GITHUB")
    print("="*60)
    
    with open(JSON_FILENAME, "r", encoding="utf-8") as f:
        content = f.read()
    
    import base64
    encoded_content = base64.b64encode(content.encode()).decode()
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": "Add NFT metadata",
        "content": encoded_content,
        "branch": "main"
    }
    
    response = requests.put(GITHUB_API, json=data, headers=headers)
    
    if response.status_code in [201, 200]:
        print(f"✓ JSON загружен на GitHub!")
        print(f"  URL: https://github.com/{GITHUB_REPO}/blob/main/{JSON_FILENAME}")
        return True
    else:
        print(f"✗ Ошибка: {response.status_code}")
        print(f"  {response.json()}")
        return False

# ============= ШАГ 4: ПРОЧИТАТЬ JSON С GITHUB И ВЫВЕСТИ =============
def read_from_github():
    """Читаем JSON с GitHub и выводим"""
    print("\n" + "="*60)
    print("ШАГ 4: ЧТЕНИЕ JSON С GITHUB:")
    print("="*60)
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }
    
    response = requests.get(GITHUB_API, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ JSON прочитан с GitHub")
        print(f"✓ Название: {data['name']}")
        print(f"✓ Описание: {data['description']}")
        print(f"✓ Атрибуты: {data['attributes']}")
        return data
    else:
        print(f"✗ Ошибка чтения: {response.status_code}")
        return None

# ============= ШАГ 5: ОБНОВИТЬ JSON НА GITHUB =============
def update_on_github(new_description):
    """Обновляем описание JSON на GitHub"""
    print("\n" + "="*60)
    print("ШАГ 5: ОБНОВЛЕНИЕ JSON НА GITHUB")
    print("="*60)
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Сначала получаем текущий SHA
    response = requests.get(GITHUB_API, headers=headers)
    if response.status_code != 200:
        print(f"✗ Ошибка получения файла")
        return False
    
    current_sha = response.json()["sha"]
    
    # Читаем локальный JSON
    with open(JSON_FILENAME, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    # Обновляем описание
    metadata["description"] = new_description
    
    # Кодируем обновленный контент
    import base64
    updated_content = json.dumps(metadata, ensure_ascii=False, indent=2)
    encoded_content = base64.b64encode(updated_content.encode()).decode()
    
    # Отправляем на GitHub
    data = {
        "message": f"Update NFT metadata - change description",
        "content": encoded_content,
        "sha": current_sha,
        "branch": "main"
    }
    
    response = requests.put(GITHUB_API, json=data, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ JSON обновлен на GitHub!")
        print(f"✓ Новое описание: {new_description}")
        return True
    else:
        print(f"✗ Ошибка обновления: {response.status_code}")
        print(f"  {response.json()}")
        return False

# ============= ШАГ 6: ПРОЧИТАТЬ ОБНОВЛЕННЫЙ JSON С GITHUB =============
def read_updated_from_github():
    """Читаем обновленный JSON с GitHub"""
    print("\n" + "="*60)
    print("ШАГ 6: ОБНОВЛЕННЫЕ МЕТАДАННЫЕ С GITHUB:")
    print("="*60)
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }
    
    response = requests.get(GITHUB_API, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Обновленный JSON прочитан с GitHub")
        print(f"✓ Название: {data['name']}")
        print(f"✓ Описание: {data['description']}")
        print(f"✓ Атрибуты: {data['attributes']}")
        return data
    else:
        print(f"✗ Ошибка чтения: {response.status_code}")
        return None

# ============= ШАГ 7: МИНТИТЬ NFT =============
def mint_nft_final(metadata):
    """Минтим NFT с финальными метаданными"""
    print("\n" + "="*60)
    print("ШАГ 7: МИНТИНГ NFT:")
    print("="*60)
    print(f"✓ Минтим NFT:")
    print(f"  Название: {metadata['name']}")
    print(f"  Описание: {metadata['description']}")
    print(f"  Атрибуты: {metadata['attributes']}")
    print(f"\n✓ NFT готов к деплою на блокчейн!")
    # Здесь вставить логику минта из deploy_nft_task3.py

# ============= ГЛАВНАЯ ФУНКЦИЯ =============
def main():
    """Запуск всех шагов"""
    print("\n" + "#"*60)
    print("# ЗАДАНИЕ 3: JSON -> GITHUB -> ОБНОВЛЕНИЕ -> МИНТ")
    print("#"*60)
    
    # Шаг 1: Создать JSON
    create_local_json()
    
    # Шаг 2: Вывести локальный JSON
    read_local_json()
    
    # Шаг 3: Загрузить на GitHub
    if not upload_to_github():
        print("⚠️  Проверь GITHUB_TOKEN и убедись, что репо существует")
        return
    
    # Шаг 4: Прочитать с GitHub
    read_from_github()
    
    # Шаг 5: Обновить на GitHub
    update_on_github("ОБНОВЛЕННОЕ описание NFT - изменено на GitHub!")
    
    # Шаг 6: Прочитать обновленный с GitHub
    updated_metadata = read_updated_from_github()
    
    # Шаг 7: Минтить
    if updated_metadata:
        mint_nft_final(updated_metadata)
    
    print("\n" + "#"*60)
    print("# ✓ ВСЕ ШАГИ ЗАВЕРШЕНЫ!")
    print("#"*60)

if __name__ == "__main__":
    main()
