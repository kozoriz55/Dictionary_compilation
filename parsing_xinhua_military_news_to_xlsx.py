#парсинг сайтів Військових новин 新华 заголовки + новина + текст + переклад, версія Military json + ChatGpt
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import json
import time
import math
from openpyxl import Workbook

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Mobile Safari/537.36',
    'accept': '*/*'
}

BASE_API = "http://qc.wa.news.cn/nodeart/list"
CNT_PER_PAGE = 200
#http://www.xinhuanet.com/mil/shijie.htm
#http://www.xinhuanet.com/mil/zhongguo.htm
#http://www.xinhuanet.com/mil/hangtianfangwu.htm
#http://www.xinhuanet.com/mil/yuejunqing.htm
# ID розділів і назви для Excel-аркушів
CATEGORIES = {
    "11139634": "Військова аналітика",
    "11139635": "Китай",
    "11139636": "Світ",
    "11139637": "Точка зору",
    "11139641": "Космос та оборона"
}

def get_total_pages(nid, cnt_per_page=20):
    params = {
        "nid": nid,
        "pgnum": 1,
        "cnt": cnt_per_page,
        "tp": 1,
        "orderby": 1,
        "_": int(time.time() * 1000)
    }
    try:
        res = requests.get(BASE_API, headers=HEADERS, params=params, timeout=10)
        res.encoding = 'utf-8'
        json_data = res.text
        json_str = json_data[json_data.find('{'):json_data.rfind('}') + 1]
        data = json.loads(json_str)
        total = int(data['totalnum'])
        pages = math.ceil(total / cnt_per_page)
        print(f"✅ {total} новин у розділі (nid={nid}).MAX_PAGES = {pages}")
        return pages
    except Exception as e:
        print(f"[!] Не вдалося отримати кількість сторінок: {e}")

def get_article_links(nid):
    max_pages = get_total_pages(nid, CNT_PER_PAGE)
    links = []
    for page in range(1, max_pages+1):
        params = {
            "nid": nid,
            "pgnum": page,
            "cnt": CNT_PER_PAGE,
            "tp": 1,
            "orderby": 1,
            "_": int(time.time() * 1000)
        }
        try:
            res = requests.get(BASE_API, headers=HEADERS, params=params, timeout=10)
            res.encoding = 'utf-8'
            json_data = res.text
            json_str = json_data[json_data.find('{'):json_data.rfind('}') + 1]
            data = json.loads(json_str)
            news_list = data['data']['list']

            for item in news_list:
                link = item.get('LinkUrl')
                title = item.get('Title')
                if link and title:
                    links.append((title.strip(), link.strip()))
        except Exception as e:
            print(f"[!] Помилка на сторінці {page} (nid={nid}): {e}")
        time.sleep(1)
    return links

def get_article_text(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        selectors = ['#detail', '#p-detail', '.article', '.main-content', '.content']

        for sel in selectors:
            block = soup.select_one(sel)
            if block:
                paragraphs = block.find_all(['p', 'div'])
                text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                if text:
                    return text
        return ""
    except Exception as e:
        print(f"[!] Помилка завантаження тексту: {e}")
        return ""

def translate_text(text):
    try:
        translator = GoogleTranslator(source='zh-CN', target='uk')
        return translator.translate(text)
    except Exception as e:
        print(f"[!] Помилка перекладу: {e}")
        return "[не вдалося перекласти]"

def collect_news_for_category(nid, sheet_name):
    print(f"\n=== 🗂️ Розділ: {sheet_name} ===")
    links = get_article_links(nid)
    results = []

    for i, (title, url) in enumerate(links, 1):
        print(f"[{i}/{len(links)}] ⬇️ {title[:40]}...")
        zh_text = get_article_text(url)
        uk_text = translate_text(zh_text) if zh_text else "[текст не знайдено]"
        results.append({
            "title_zh": title,
            "url": url,
            "text_zh": zh_text,
            "text_uk": uk_text
        })
        time.sleep(1)
    return sheet_name, results

def save_all_to_excel(all_data, filename):
    wb = Workbook()
    wb.remove(wb.active)# видаляємо дефолтний аркуш

    for sheet_name, records in all_data:
        ws = wb.create_sheet(title=sheet_name)
        ws.append(["Назва (ZH)", "URL", "Текст (ZH)", "Переклад (UK)"])
        for record in records:
            ws.append([record["title_zh"], record["url"], record["text_zh"], record["text_uk"]])
    wb.save(filename)
    print(f"\n✅ Excel-файл збережено: {filename}")

def main():
    all_data = []
    for nid, name in CATEGORIES.items():
        sheet_data = collect_news_for_category(nid, name)
        all_data.append(sheet_data)

    save_all_to_excel(all_data, "C:\\Users\\davin\\Desktop\\xinhuanet_all_news.xlsx")

if __name__ == "__main__":
    main()
