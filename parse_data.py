import requests
from bs4 import BeautifulSoup
import json
import re
base_URL = "https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/?PAGEN_1="
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}
pr

def find_last_page(url):
    # Запрос к серверу для получения контента в HTML
    page = requests.get(f'{url}', headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Контейнер страниц
    pagination_container = soup.find(
        "div", {'class': "bx-pagination-container row"})

    # Поиск всех ссылок в контейнере для разбивки на страницы
    links = pagination_container.find_all('a')

    # Найти последнюю ссылку, прежде чем кнопка вернуться
    last_page = links[-2].text
    return int(last_page)


def data_to_json(data):
    # Загружаем старые данные из json файла
    try:
        with open('./data/smartphones.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)
    except:
        old_data = []

    # Добавляем новые данные к старым
    data_list = old_data + data

    # Записываем общий список данных в json файл
    with open('./data/smartphones.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)


def do_parse(URL, last_page):
    # Инициализируем пустой список для хранения данных товаров
    smartphones = []
    page = requests.get(f'{URL}', headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Находим все элементы с классом "bx_catalog_item"
    results = soup.find_all(
        'div', class_='bx_catalog_item_container gtm-impression-product')
    for result in results:
        data = json.loads(result.get("data-product"))
        smartphone = {
            'name': data['item_name'].replace('Смартфон', ''),
            'articul': data['item_id'],
            'price': data['price'],
            'memory_size': re.search(r'(\d+\s?[Gg][Bb])', data['item_name']).group(0).upper().replace("GB", 'Гб')
        }
        smartphones.append(smartphone)
    return smartphones


def main():
    last_page = find_last_page(base_URL)
    for number in range(1, last_page+1):
        url = base_URL + str(number)
        data = do_parse(url, last_page)
        data_to_json(data)
        print("Wait: " + str(last_page + 1 - number)+ "sec")
    print("Finish")

if __name__ == "__main__":
    main()
