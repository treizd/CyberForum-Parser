from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

START_URL = "https://www.cyberforum.ru/python-tasks/"
BASE_URL = "https://www.cyberforum.ru/python-tasks-page"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'} # Не менять, иначе парсер не может получить доступ к сайту.


def get_page_count():
    response = requests.get(START_URL, headers=HEADERS)
    response.raise_for_status()
    html_parser = BeautifulSoup(response.text, "html.parser")
    page_count_text = [item.text for item in html_parser.find_all("td", {"class": "vbmenu_control"}) if "из" in item.text][0]
    return int(page_count_text.split(" из ")[1])


def fetch():
    page_count = get_page_count()
    unanswered_tasks = []
    start_time = datetime.now()

    for page_number in range(1, page_count + 1):
        url = START_URL if page_number == 1 else f"{BASE_URL}{page_number}.html"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        html_parser = BeautifulSoup(response.text, "html.parser")
        rows = html_parser.find_all('tr', attrs={'id': re.compile("^vbpostrow_")})

        for row in rows:
            answers_count_element = row.find("td", {"class": "alt1", "align": "center"})
            link_element = row.find('a', href=True, attrs={'id': re.compile("^thread_title")})

            if answers_count_element.text.isdigit() and int(answers_count_element.text) == 0:
                link = link_element["href"]
                full_link = link if page_number == 1 else f"https://www.cyberforum.ru/{link}"
                unanswered_tasks.append({"link": full_link, "page": page_number})

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Парсинг завершен за {duration.seconds}.{duration.microseconds} сек.")
    return unanswered_tasks # Дальше сами выбирайте, что делать с полученными темами - сохранять / выводить и т.д.


if __name__ == "__main__":
    print(fetch())
