import requests

# Проверь, доступен ли JSON
url = 'https://gist.githubusercontent.com/dmittriyyy/48730d6d78afd0bff86afff5f5c8be33/raw/metadata_1.json'

response = requests.get(url)
print(f"Статус: {response.status_code}")
print(f"Содержимое:\n{response.text}")
