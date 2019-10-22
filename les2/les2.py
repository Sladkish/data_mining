# Источник https://geekbrains.ru/posts
# Задача:
# Необходимо обойти все записи блога и получить следующую структуру информации:
#
# {
# "title": заголовок статьи,
# "image": Заглавное изображение статьи (ссылка),
# "text": Текст статьи,
# "pub_date": time_stamp даты публикации,
# "autor": {"name": Имя автора,
#                "url": ссылка на профиль автора,
#                },
# }
# по окончании сбора, полученые данные должны быть сохранены в json файл.
# В структуре должны присутсвовать все статьи на дату парсинга


import requests
from bs4 import BeautifulSoup
import json
import re
import datetime as DT
domain_url="https://geekbrains.ru"
blog_url="https://geekbrains.ru/posts"

def get_page_soup(url):
    page_data = requests.get(url)
    soup_data = BeautifulSoup(page_data.text, "lxml")
    return soup_data

def get_page_strict(soup):
    posts_list=[]
    posts_data = soup.find_all('div', class_='post-item')
    for post in posts_data:
        post_link = f"{domain_url}{post.find('a').attrs.get('href')}"
        one_post_data = requests.get(post_link)
        one_post_soup = BeautifulSoup(one_post_data.text, "lxml")
        post_time = one_post_soup.find('div', class_='blogpost-date-views').find("time").attrs.get('datetime')
        post_dict = {
            'post_url': post_link,
            'post_title': post.find(class_="post-item__title").text,
            'pud_date' : DT.datetime.fromisoformat(post_time).timestamp(),
            'post_text': one_post_soup.find('div', class_='blogpost-content').text,
            "autor": {'author_name': one_post_soup.find('div', class_='text-lg text-dark').text,
            'author_url' : f"{domain_url}{one_post_soup.find('a', attrs={'href': re.compile('^/user')}).get('href')}"}
        }
        posts_list.append(post_dict)
    return posts_list

def parser(url):
    posts_list = []
    while True:
        soup= get_page_soup(url)
        posts_list.extend(get_page_strict(soup))
        print(len(posts_list))
        try:
            url = soup.find('a', attrs={'rel': 'next'}, text='›').attrs.get('href')
        except AttributeError:
            break
        url = f"{domain_url}{url}"
    return posts_list

result_data=parser(blog_url)
print(len(result_data))
with open(f"result_data.json", 'w') as j_file:
    j_file.write(json.dumps(result_data))
with open(f"result_data.json", 'r') as j_file:
    temp_data = json.loads(j_file.read())
print(temp_data)



