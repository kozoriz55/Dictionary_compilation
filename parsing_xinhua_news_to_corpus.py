# парсинг сайтів новин 新华 заголовки + посилання + новина, версія ChatGpt
import requests
import json
from bs4 import BeautifulSoup
import time
import csv
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.news.cn/",
    "X-Requested-With": "XMLHttpRequest"
}

def fetch_news_page(keyword, page=1):
    url = "https://so.news.cn/getNews"
    params = {
        "lang": "cn",
        "curPage": page,
        "searchFields": 1,
        "sortField": 0,
        "keyword": keyword
    }
    response = requests.get(url, headers=HEADERS, params=params)
    print(f"📡 Сторінка {page} — Статус: {response.status_code}")
    
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            print("❌ Не вдалося декодувати JSON.")
            print(response.text[:300])  # виводить частину відповіді
            return None

    else:
        print(f"❌ Помилка HTTP {response.status_code}")
        return None

def extract_article_text(url):
    try:
        r = requests.get(url, headers=HEADERS)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        candidates = [
            ("div", {"class": "article"}),
            ("div", {"class": "mainCon", "id": "content"}),
            ("div", {"id": "detail"}),
            ("div", {"class": "main"}),
            ("div", {"id": "content"}),
            ("div", {"class": "content"}),
            ("div", {"class": "zw"}),
            ("div", {"class": "con_txt"}),
        ]

        for tag, attrs in candidates:
            container = soup.find(tag, attrs=attrs)
            if container:
                paragraphs = container.find_all("p")
                return ''.join(p.get_text(strip=True) for p in paragraphs)

        return soup.get_text(strip=True)
    except Exception as e:
        print(f"❌ Не вдалося витягнути текст: {url} — {e}")
        return "не отримано"

def main():
    keyword = "乌克兰"
    first_page = fetch_news_page(keyword, 1)
    if not first_page:
        print("❌ Не вдалося отримати першу сторінку.")
        return

    total_pages = first_page.get("content", {}).get("pageCount", 1)
    seen_titles = set()

    with open("ukraine_news_xinhua.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Заголовок", "URL", "Текст"])

        for page in range(1, total_pages + 1):
            print(f"🔄 Обробка сторінки {page}/{total_pages}... ")
            data = fetch_news_page(keyword, page)
            if not data or "content" not in data or "results" not in data["content"]:
                print(f"⚠️ Пропущено сторінку {page}: некоректна відповідь.")
                continue

            for item in data.get("content", {}).get("results", []):
                try:
                    title = re.sub('<[^>]+>|&nbsp;', '', item.get("title", "")).strip()
                    url = item.get("url")
                    if title and url and title not in seen_titles:
                        text = extract_article_text(url)
                        writer.writerow([title, url, text])
                        seen_titles.add(title)
                        print(f"✅ {title}")
                        time.sleep(1)  # затримка між запитами
                except Exception as e:
                    print(f"⚠️ Помилка обробки новини: {e}")
                    continue

    print("✅ Завершено. Дані збережено у 'ukraine_news_xinhua.csv'")

if __name__ == "__main__":
    main()
