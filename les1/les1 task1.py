#Михайловский Василий
#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.
import json
import requests
# user='mojombo'
user='wycats'
repos={}
page=1
n = 0

while True:
    url = f"https://api.github.com/users/{user}/repos?page={page}&per_page=100"
    data=requests.get(url)
    j_data=data.json()
    if len(j_data)==0:
        break
    for i in range(len(j_data)):
        repos[n+i+1]=j_data[i].get('name')
    n+=100
    page+=1
with open(f"{user}_repos.json",'w') as j_file:
    j_file.write(json.dumps(repos))
with open(f"{user}_repos.json",'r') as j_file:
    temp_data=json.loads(j_file.read())

print(repos)
print(temp_data)