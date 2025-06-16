import undetected_chromedriver
import random
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from JsonHtmlFuncs import json_to_html, save_channels_to_json
from pathlib import Path
from ParseFuncs import parse_channel



if __name__ ==  "__main__":
    try:

        driver = undetected_chromedriver.Chrome()
        driver.get("https://tgstat.ru/ratings/channels")
        cookie = [
            {"name": "_ym_uid", "value": "1702479296231132795", "path": "/"},
            {"name": "_ym_d", "value": "1743477278", "path": "/"},
            {"name": "tgstat_settings",
             "value": "f7e26f5d1be638583c1848175d4df050697604776eda4645b37467ebd1d79f6ca%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22tgstat_settings%22%3Bi%3A1%3Bs%3A19%3A%22%7B%22fp%22%3A%22VGAt5zhwmM%22%7D%22%3B%7D",
             "path": "/"},
            {"name": "_ym_isad", "value": "1", "path": "/"},
            {"name": "_gid", "value": "GA1.2.1457856778.1749897055", "path": "/"},
            {"name": "_ga", "value": "GA1.1.1897481012.1743477278", "path": "/"},
            {"name": "cf_clearance",
             "value": "hjkVGXEhBlcrnT09HkAlNvOPrP04SUPMrB9IwAmQiHc-1749910808-1.2.1.1-dlFkbAvfTQkd7rowFlsuanf6uCwYxY87asE41TqilJAzxjJZtt8GFSILTH36vFkw8FMmJvQqWz4pXOcPH1Vu40OKjlv5vfDYDNf7Dl0wl4KyEjik1RMZpg2AeP5fyA4bYIDNamA1ukgAqGhZINL1Zr2RJjjmCDJnnS_sdurpHrWtUE_JbEwhCKK.MKkLN2gMwsKdAKX9nw4IgqBTxTqlHHNfsjjP514OGyyNbq9GWc_4.R8Z8LhtqWGWwa2wQpilXH8YXaHtyiUUuQM58Gsnf3RKGoJpLqhGns7iZWp11qBfKBAX6DdZSK01pYJIqGbp48FrikTK.OP7J11f9XFsngc394PNfDpHW158bt5zG5A",
             "path": "/"},
            {"name": "tgstat_idrk",
             "value": "fc5083620d6ae75048e17cbad7199fda07185689735c3db33cc6e7e1b44c5481a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22tgstat_idrk%22%3Bi%3A1%3Bs%3A53%3A%22%5B11540621%2C%22O96_OkV-zSHY0iv-9dvMRhiko3XgZZGV%22%2C2592000%5D%22%3B%7D",
             "path": "/"},
            {"name": "tgstat_sirk", "value": "imbbp0m0lbpcefs4bpedp6o6nq", "path": "/"},
            {"name": "_tgstat_csrk",
             "value": "6bc090a67d2b7162abe79264daf1a05412604b15332c10f377a50609fc6e3b18a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22_tgstat_csrk%22%3Bi%3A1%3Bs%3A32%3A%225AsumaMqYkfX7z4wbrUr5TkUuojmpTv-%22%3B%7D",
             "path": "/"},
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
        for name, url in categories:
            json_path = Path("jsons") / (name + ".json")
            if json_path.exists():
                continue
            driver.get("https://tgstat.ru" + url)
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
            all_channels = []
            counter = 0
            for ch in all_urls:
                counter += 1
                c = parse_channel(driver, ch)
                all_channels.append(c)
                print(c)
                time.sleep(random.uniform(2, 5))
                if counter > 10:
                    time.sleep(20)
                    counter = 0
            save_channels_to_json(all_channels, name)
            json_to_html(name + ".json", name + " Отчёт.html")
            time.sleep(60)

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
