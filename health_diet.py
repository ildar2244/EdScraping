# 1.парсим; headers берём из бразуера консоли разработчика (Network->Request)
# 2.сохраняем локально в файл
# 3.работаем с локальными данными

import json
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import random
import local_properties as lp

url = lp.HEALTH_DIET_URL

headers = {
    "accept": "*/*",
    "user-agent": lp.HEADER_USER_AGENT
}

local_page_file_name = "health_diet.html"
file_categories = "all_categories_dict.json"


# общие методы
def open_file(name: str):
    with open(name) as file:
        return file.read()


def open_file_utf8(name: str):
    with open(name, encoding="utf-8") as file:
        return file.read()


def write_to_file(name: str, data: str):
    with open(name, "w") as file:
        file.write(data)


def write_to_file_utf8(name: str, data: str):
    with open(name, "w", encoding="utf-8") as file:
        file.write(data)


def open_json(name: str):
    with open(name) as file:
        return json.load(file)


def write_to_json(file_name: str, data: dict):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# парсим веб-страницу
def scrap_page():
    req = requests.get(url, headers)
    src = req.text
    return src


# сохраняем локально данные парсинга
def save_page_to_local(src: str):
    write_to_file(local_page_file_name, src)


# данные из локального файла веб-страницы
def get_local_page():
    return open_file(local_page_file_name)


# ссылки на все категории
def get_all_products_href(src: str):
    soup = BeautifulSoup(src, "lxml")
    all_products_href = soup.find_all(class_="mzr-tc-group-item-href")
    # print(all_products_href)
    return all_products_href


# словарь категорий и ссылки на них
def get_all_categories(src: str):
    all_categories_dict = {}
    hrefs = get_all_products_href(src)

    for item in hrefs:
        item_text = item.text
        item_href = "https://health-diet.ru" + item.get("href")

        all_categories_dict[item_text] = item_href

    return all_categories_dict


def get_product_data():
    all_categories = open_json(file_categories)
    iteration_count = int(len(all_categories)) - 1
    count = 0
    print(f"Всего итераций: {iteration_count}")

    for category_name, category_href in all_categories.items():
        rep = [",", " ", "-", "'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")

        req = requests.get(url=category_href, headers=headers)
        src = req.text

        result_file_name = f"data/{count}_{category_name}"

        write_to_file_utf8(f"{result_file_name}.html", src)
        src = open_file_utf8(f"{result_file_name}.html")

        soup = BeautifulSoup(src, "lxml")
        # проверка страницы на наличие таблицы с продуктами
        alert_block = soup.find(class_="uk-alert-danger")
        if alert_block is not None:
            continue

        # собираем заголовки таблицы
        table_head = soup \
            .find(class_="mzr-tc-group-table") \
            .find("tr") \
            .find_all("th")
        product = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text

        with open(f"{result_file_name}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

        # собираем данные продуктов
        products_data = soup \
            .find(class_="mzr-tc-group-table") \
            .find("tbody") \
            .find_all("tr")

        product_info = []
        for item in products_data:
            product_tds = item.find_all("td")

            title = product_tds[0].find("a").text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text

            product_info.append(
                {
                    "Title": title,
                    "Calories": calories,
                    "Proteins": proteins,
                    "Fats": fats,
                    "Carbohydrates": carbohydrates
                }
            )

            with open(f"{result_file_name}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )

            with open(f"{result_file_name}.json", "a", encoding="utf-8") as file:
                json.dump(product_info, file, indent=4, ensure_ascii=False)

            count += 1
            print(f"# Итерация {count}. {category_name} записан...")
            iteration_count = iteration_count + 1

            if iteration_count == 0:
                print("Работа завершена")
                break

            print(f"Осталось итераций: {iteration_count}")
            sleep(random.randrange(2, 4))


if __name__ == '__main__':
    # 1 step
    # src1 = scrap_page()
    # save_page_to_local(src1)
    # 2 step
    # src2 = get_local_page()
    # get_all_products_href(src2)
    # 3 step
    # src3 = get_local_page()
    # categories = get_all_categories(src3)
    # write_to_json(file_categories, categories)
    # 4 step
    get_product_data()
