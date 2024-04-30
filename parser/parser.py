# import requests
# from bs4 import BeautifulSoup as bs
# import re
# import random
# import time
import datetime
def get_headers():
    link = f'https://www.useragents.me/#most-common-desktop-useragents-json-csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    response = requests.get(link, headers=headers)
    soup = bs(response.text, 'lxml')
    res = soup.find_all('div', class_='table-responsive')[0].find_all('textarea')
    pattern = r'<textarea[^>]*>(.*?)<\/textarea>'
    ans = []
    for i in res:
        i = str(i)
        try:
            matches = re.findall(pattern, i)[0]
            ans.append(matches)
        except:
            continue
    return {'User-Agent': random.choice(ans)}

movie_codes = open('movie_codes.txt', 'r', encoding='utf-8').read().splitlines()
print(len(movie_codes))

def parse_part(start = 0, end = 10):
    s = datetime.datetime.now()
    parsed_data = []
    for movie_code in movie_codes[start:end]:
        try:
            movie_url = 'https://www.imdb.com/title/' + movie_code
            movie_page = requests.get(movie_url, headers=get_headers())
            movie_soup = str(bs(movie_page.content, 'html.parser'))
            print(movie_soup)
            pattern = r'<script type="application/ld\+json">\s*(.*?)\s*</script>'
            info = re.findall(pattern, movie_soup)
            # print(movie_code, info)
            parsed_data.append(movie_code + ';' + info[0])
            with open("parsed_data.csv", 'a+', encoding='utf-8') as f:
                f.write(movie_code + ';' + info[0] + '\n')
                f.close()
        except:
            # print(movie_code, "NaN")
            parsed_data.append(movie_code + ';' + "NaN")
            # if len(parsed_data) in range(0, len(movie_codes), 1000):
            with open("parsed_data.csv", 'a', encoding='utf-8') as f:
                f.write(movie_code + ';' + "NaN" + '\n')
                f.close()
    e = datetime.datetime.now()
    # print(f'Время затрачено: {(e - s) / 60} минут')
    return parsed_data
    # with open("parsed_data.csv", 'w', encoding='utf-8') as f:
    #     f.write(parsed_data)
# parse_part(763400, 763401)
# import threading
s1 = set()
s2 = set(open("movie_codes.txt", "r").read().splitlines())
data = open("parsed_data.csv", "r").read().splitlines()
for d in data:
    d = d.split(';')[0]
    s1.add(d)
    print(d)
s = list(s2 - s1)
print(len(s))
with open("movie_codes.txt", 'w', encoding='utf-8') as f:
    f.write("\n".join(s))
# # Значения аргументов для каждого потока
# args_for_threads = [
#     (0, 135620),
#     (135620, 135620*2),
#     (135620*2, 135620*3),
#     (135620*3, 135620*4),
#     (135620*5, 135620*6),
#     (135620*6, len(movie_codes))
# ]
#
# # Создаем и запускаем четыре потока
# threads = []
# for i, args in enumerate(args_for_threads):
#     # args должен быть кортежем, который развернется в аргументы функции
#     thread = threading.Thread(target=parse_part, args=args)
#     threads.append(thread)
#     thread.start()
#
# # Ожидаем завершения всех потоков
# for thread in threads:
#     thread.join()
#
# print("All threads have finished executing.")

