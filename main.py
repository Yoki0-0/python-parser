import undetected_chromedriver
import random
import json
from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import List

@dataclass
class Channel:
    name: str
    link: str
    category: str
    subs: int
    avg_views_post: int
    err: float
    migr_sub7d: int
    migr_sub30d: int
    lifetime: str



def json_to_html(json_file: str, html_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        channels = json.load(f)

    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Отчёт по каналам</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background-color: #f0f0f0; cursor: pointer; position: relative; }
    th.sorted-asc::after { content: " ↑"; position: absolute; right: 8px; }
    th.sorted-desc::after { content: " ↓"; position: absolute; right: 8px; }
    tbody td.active-col { background-color: #f9f9f9; }
    h1 { text-align: center; }
  </style>
</head>
<body>
  <h1>Отчёт по каналам</h1>
  <table id="channelsTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">Название</th>
        <th onclick="sortTable(1)">Ссылка</th>
        <th onclick="sortTable(2)">Категория</th>
        <th onclick="sortTable(3)">Подписчики</th>
        <th onclick="sortTable(4)">Средний просмотр</th>
        <th onclick="sortTable(5)">ERR (%)</th>
        <th onclick="sortTable(6)">Миграция 7д</th>
        <th onclick="sortTable(7)">Миграция 30д</th>
        <th onclick="sortTable(8)">Возраст</th>
      </tr>
    </thead>
    <tbody>
"""

    for ch in channels:
        html += f"""
      <tr>
        <td>{ch.get("name", "")}</td>
        <td><a href="{ch.get("link", "")}">{ch.get("link", "")}</a></td>
        <td>{ch.get("category", "")}</td>
        <td>{ch.get("subs", "")}</td>
        <td>{ch.get("avg_views_post", "")}</td>
        <td>{ch.get("err", "")}</td>
        <td>{ch.get("migr_sub7d", "")}</td>
        <td>{ch.get("migr_sub30d", "")}</td>
        <td>{ch.get("lifetime", "")}</td>
      </tr>
"""

    html += """
    </tbody>
  </table>

  <script>
  function sortTable(n) {
    var table = document.getElementById("channelsTable");
    var rows = Array.from(table.rows).slice(1);
    var asc = table.getAttribute("data-sort-col") != n || table.getAttribute("data-sort-order") == "desc";

    rows.sort(function(rowA, rowB) {
      var a = rowA.cells[n].innerText.replace(/\\s+/g, '').replace(',', '.');
      var b = rowB.cells[n].innerText.replace(/\\s+/g, '').replace(',', '.');
      var numA = parseFloat(a);
      var numB = parseFloat(b);
      if (!isNaN(numA) && !isNaN(numB)) {
        return asc ? numA - numB : numB - numA;
      } else {
        return asc ? a.localeCompare(b) : b.localeCompare(a);
      }
    });

    for (var row of rows) table.tBodies[0].appendChild(row);

    // Снять старую подсветку
    var ths = table.tHead.rows[0].cells;
    for (var i = 0; i < ths.length; i++) {
      ths[i].classList.remove("sorted-asc", "sorted-desc");
    }

    // Добавить новую стрелку
    ths[n].classList.add(asc ? "sorted-asc" : "sorted-desc");

    // Подсветить колонку
    for (var r of rows) {
      for (var i = 0; i < r.cells.length; i++) {
        r.cells[i].classList.toggle("active-col", i == n);
      }
    }

    table.setAttribute("data-sort-col", n);
    table.setAttribute("data-sort-order", asc ? "asc" : "desc");
  }
  </script>

</body>
</html>
"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML-отчёт с визуальной сортировкой сохранён в {html_file}")

def save_channels_to_json(channels: List[Channel], filename: str):
    filename += ".json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)

def extract_sub7(soup : BeautifulSoup) -> int:
    rows = soup.select('table.mt-1 tbody tr')

    for row in rows:
        desc_td = row.find_all('td')[1]
        if desc_td and 'за неделю' in desc_td.get_text(strip=True):
            # Первая ячейка с числом
            number_td = row.find_all('td')[0]
            if number_td:
                value = number_td.find('b')
                if value:
                    return int(value.get_text(strip=True).replace(' ', '').replace("+",""))
def extract_sub30(soup : BeautifulSoup) -> int:
    rows = soup.select('table.mt-1 tbody tr')

    for row in rows:
        desc_td = row.find_all('td')[1]
        if desc_td and 'за месяц' in desc_td.get_text(strip=True):
            number_td = row.find_all('td')[0]
            if number_td:
                value = number_td.find('b')
                if value:
                    return int(value.get_text(strip=True).replace(' ', '').replace("+",""))
def extract_subs(soup : BeautifulSoup) -> int:
    blocks = soup.select(".card.card-body.pt-1.pb-2.position-relative.border.min-height-155px")
    for block in blocks:
        label = block.select_one(".position-absolute.text-uppercase.text-dark.font-12")
        if label and label.get_text(strip=True) == "подписчики":
            h2 = block.find("h2")
            if h2:
                num_str = h2.get_text(strip=True).replace(" ", "")
                return int(num_str)

def extract_avg_views(soup : BeautifulSoup) -> int:
    blocks = soup.select(".card.card-body.pt-1.pb-2.position-relative.border.min-height-155px")
    for block in blocks:
        label = block.select_one(".position-absolute.text-uppercase.text-dark.font-12").select_one(".text-right")
        if label and label.get_text(strip=True) == "средний охват":
            h2 = block.find("h2")
            if h2:
                num_str = h2.get_text(strip=True).replace(" ", "")
                return int(num_str)
def extract_lifetime(soup: BeautifulSoup) -> str:
    age_label_div = soup.find('div', string=lambda text: text and 'возраст канала' in text.lower())
    if not age_label_div:
        return None

    container = age_label_div.find_parent('div', class_='card')
    if not container:
        return None


    h2_tag = container.find('h2', class_='text-dark text-truncate')
    if h2_tag:
        return h2_tag.get_text(strip=True)

def extract_err(soup : BeautifulSoup) -> float:
    cards = soup.find_all('div', class_='card card-body pt-1 pb-2 position-relative border min-height-155px')

    for card in cards:
        if "вовлеченность подписчиков (ERR)" in card.get_text():
            h2 = card.find('h2', class_='text-dark')
            if h2:
                return float(h2.text.strip().replace("%", ""))

def extract_name(soup : BeautifulSoup) -> str:
    h1_tag = soup.find("h1")
    return h1_tag.get_text(strip=True) if h1_tag else "N/A"

def extract_link(soup: BeautifulSoup) -> str:
    link_tag = soup.select_one(".text-center.text-sm-left a")
    if link_tag and link_tag.has_attr("href"):
        return link_tag["href"]

def extract_category(soup : BeautifulSoup) -> str | None:
    blocks = soup.find_all("div", class_="text-left text-sm-right")
    for block in blocks:
        category = block.find("div", class_="mt-2").find("a").get_text(strip=True)
    return category

def parse_channel(driver, url: str) -> dict:
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
    except:
        print(f"[!] Не удалось дождаться загрузки: {url}")
        return {}

    soup = BeautifulSoup(driver.page_source, "html.parser")

    return {
        "name": extract_name(soup),
        "link": extract_link(soup),
        "category": extract_category(soup),
        "subs": extract_subs(soup),
        "avg_views_post": extract_avg_views(soup),
        "err": extract_err(soup),
        "migr_sub7d": extract_sub7(soup),
        "migr_sub30d": extract_sub30(soup),
        "lifetime": extract_lifetime(soup),
    }

    
try:

    driver = undetected_chromedriver.Chrome()
    # print(parse_channel(driver, "https://tgstat.ru/channel/@leoday/stat"))
    driver.get("https://tgstat.ru/ratings/channels")
    cookie = [
    {"name": "_ym_uid", "value": "1702479296231132795", "path": "/"},
    {"name": "_ym_d", "value": "1743477278", "path": "/"},
    {"name": "tgstat_settings", "value": "f7e26f5d1be638583c1848175d4df050697604776eda4645b37467ebd1d79f6ca%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22tgstat_settings%22%3Bi%3A1%3Bs%3A19%3A%22%7B%22fp%22%3A%22VGAt5zhwmM%22%7D%22%3B%7D", "path": "/"},
    {"name": "_ym_isad", "value": "1", "path": "/"},
    {"name": "_gid", "value": "GA1.2.1457856778.1749897055", "path": "/"},
    {"name": "_ga", "value": "GA1.1.1897481012.1743477278", "path": "/"},
    {"name": "cf_clearance", "value": "hjkVGXEhBlcrnT09HkAlNvOPrP04SUPMrB9IwAmQiHc-1749910808-1.2.1.1-dlFkbAvfTQkd7rowFlsuanf6uCwYxY87asE41TqilJAzxjJZtt8GFSILTH36vFkw8FMmJvQqWz4pXOcPH1Vu40OKjlv5vfDYDNf7Dl0wl4KyEjik1RMZpg2AeP5fyA4bYIDNamA1ukgAqGhZINL1Zr2RJjjmCDJnnS_sdurpHrWtUE_JbEwhCKK.MKkLN2gMwsKdAKX9nw4IgqBTxTqlHHNfsjjP514OGyyNbq9GWc_4.R8Z8LhtqWGWwa2wQpilXH8YXaHtyiUUuQM58Gsnf3RKGoJpLqhGns7iZWp11qBfKBAX6DdZSK01pYJIqGbp48FrikTK.OP7J11f9XFsngc394PNfDpHW158bt5zG5A", "path": "/"},
    {"name": "tgstat_idrk", "value": "fc5083620d6ae75048e17cbad7199fda07185689735c3db33cc6e7e1b44c5481a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22tgstat_idrk%22%3Bi%3A1%3Bs%3A53%3A%22%5B11540621%2C%22O96_OkV-zSHY0iv-9dvMRhiko3XgZZGV%22%2C2592000%5D%22%3B%7D", "path": "/"},
    {"name": "tgstat_sirk", "value": "imbbp0m0lbpcefs4bpedp6o6nq", "path": "/"},
    {"name": "_tgstat_csrk", "value": "6bc090a67d2b7162abe79264daf1a05412604b15332c10f377a50609fc6e3b18a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22_tgstat_csrk%22%3Bi%3A1%3Bs%3A32%3A%225AsumaMqYkfX7z4wbrUr5TkUuojmpTv-%22%3B%7D", "path": "/"},
    {"name": "_ga_ZEKJ7V8PH3", "value": "GS2.1.s1749910806$o14$g1$t1749910898$j35$l0$h0", "path": "/"}
]
    for cook in cookie:
        driver.add_cookie(cook)

    driver.get("https://tgstat.ru/ratings/channels")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    blocks = soup.select('.col.col-12.col-sm-5.col-md-5.col-lg-4')
    all_urls = []
    for card in blocks:
        link = card.find('a')
        if link and link.has_attr('href'):
            all_urls.append(link['href'])

    categories = []

    container = soup.find("div", class_="list-group")

    links = container.find_all("a", href=True)

    for link in links:
        name = link.get_text(strip=True)
        href = link["href"]
        categories.append((name, href))

    all_channels = []
    counter = 0
    for ch in all_urls:
        counter += 1
        c = parse_channel(driver, ch)
        all_channels.append(c)
        print(c)
        time.sleep(random.uniform(1, 3))
        if counter > 10:
            time.sleep(15)
            counter = 0
    save_channels_to_json(all_channels, "TgChannels")
    json_to_html("TgChannels.json", "channels_report.html")

except Exception as ex:
    print(ex)
finally:
    driver.quit()