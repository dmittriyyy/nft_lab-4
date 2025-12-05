import json

metadata = {
    "name": "Мой Уникальный NFT",
    "description": "Описание для задания 3.",
    "image": "https://habrastorage.org/getpro/habr/upload_files/d46/574/35e/d4657435edff35e9c525aa25fc667393.png",
    "attributes": [
        {"trait_type": "Редкость", "value": "Легендарный"},
        {"trait_type": "Тип", "value": "Коллекционный"}
    ]
}


with open("metadata_1.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

with open("metadata_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(f"✓ Название: {data['name']}")
    print(f"✓ Описание: {data['description']}")
    print(f"✓ Атрибуты: {data['attributes']}")


metadata["description"] = "ОБНОВЛЕННОЕ описание NFT!"
with open("metadata_1.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)
print("======================================")
with open("metadata_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(f"✓ Название: {data['name']}")
    print(f"✓ Описание: {data['description']}")
    print(f"✓ Атрибуты: {data['attributes']}")
print("Описание обновлено и сохранено!")
