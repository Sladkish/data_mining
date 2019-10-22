#Михайловский Василий
#Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.
import json
import requests

url = "https://api.weather.yandex.ru/v1/forecast?"
response = requests.get(url,
    params={'lat': '54.989342', 'lon': '73.368212'},
    headers={'X-Yandex-API-Key': '6163bb65-0837-4c82-a58d-dbeb4a48ddbf'}
)
json_response = response.json()
city=json_response.get('info').get('tzinfo').get('name').split('/')[1]

with open(f"{city}_weather.json",'w') as j_file:
      j_file.write(json.dumps(json_response.get('fact')))
with open(f"{city}_weather.json",'r') as j_file:
     temp_data=json.loads(j_file.read())

print(temp_data)