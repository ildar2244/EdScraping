# базовые операции с библиотекой BeautifulSoup

import re
from bs4 import BeautifulSoup

# чтение из локального файла
with open("blank/index2.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")


# получаем заголовок(title) страницы
def get_title():
    title = soup.title
    print(title)
    print(title.text)
    print(title.string)


# операции с .find() .find_all()
def get_h1():
    page_h1 = soup.find("h1")
    print(page_h1)

    page_h1_all = soup.find_all("h1")
    print(page_h1_all)

    for item in page_h1_all:
        print(item.text)


# поиск по имени класса и доп атрибуту
def get_by_class():
    user_name = soup.find("div", class_="user__name")
    print(user_name.text.strip())  # strip() убираем пробелы

    user_name = soup.find(class_="user__name").find("span").text
    print(user_name)

    user_name = soup \
        .find("div", {"class": "user__name", "id": "aaa"}) \
        .find("span").text
    print(user_name)


# поиск по атрибуту span
def get_spans():
    find_all_spans_in_user_info = soup \
        .find(class_="user__info") \
        .find_all("span")
    print(find_all_spans_in_user_info)

    for item in find_all_spans_in_user_info:
        print(item.text)

    print(find_all_spans_in_user_info[0])
    print(find_all_spans_in_user_info[2].text)


# значение из списков ('ul')
def get_list():
    social_links = soup \
        .find(class_="social__networks") \
        .find("ul") \
        .find_all("a")
    print(social_links)


# значение по атрибуту элемента
def get_by_attribute():
    all_a = soup.find_all("a")
    print(all_a)
    for item in all_a:
        item_text = item.text
        item_url = item.get("href")
        print(f"{item_text}: {item_url}")


# .find_parent() .find_parents()
def get_parent():
    post_div = soup.find(class_="post__text").find_parent()
    print(post_div)

    post_div = soup.find(class_="post__text") \
        .find_parent("div", "user__post")
    print(post_div)

    post_divs = soup.find(class_="post__text") \
        .find_parents("div", "user__post")
    print(post_divs)


# .next_element .previous_element
def get_next_or_preview():
    next_el = soup.find(class_="post__title").next_element.next_element.text
    print(next_el)

    next_el = soup.find(class_="post__title").find_next().text
    print(next_el)


# .find_next_sibling() .find_previous_sibling()
def get_sibling():
    next_sib = soup.find(class_="post__title").find_next_sibling()
    print(next_sib)

    prev_sib = soup.find(class_="post__date").find_previous_sibling()
    print(prev_sib)

    post_title = soup.find(class_="post__date") \
        .find_previous_sibling() \
        .find_next().text
    print(post_title)


def get_links():
    links = soup.find(class_="some__links").find_all("a")
    print(links)

    for link in links:
        link_href_attr = link.get("href")
        link_href_attr1 = link["href"]

        link_data_attr = link.get("data-attr")
        link_data_attr1 = link["data-attr"]

        print(link_href_attr1)
        print(link_data_attr1)


# поиск по тексту (раньше вместо параметра 'string' использовался 'text')
def search_by_text():
    find_a_by_text = soup.find("a", string="Одежда")
    print(find_a_by_text)

    find_a_by_text = soup.find("a", string="Одежда для взрослых")
    print(find_a_by_text)


# поиск по тексту с помощью регулярного выражения
def search_text_with_regular():
    find_a_by_text = soup.find("a", string=re.compile("Одежда"))
    print(find_a_by_text)

    find_all_clothes = soup.find_all(string=re.compile("([Оо])дежда"))
    print(find_all_clothes)


if __name__ == '__main__':
    # get_title()
    # get_h1()
    # get_by_class()
    # get_spans()
    # get_list()
    # get_by_attribute()
    # get_parent()
    # get_next_or_preview()
    # get_sibling()
    # get_links()
    # search_by_text()
    search_text_with_regular()
