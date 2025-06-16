from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


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

def check_capcha(soup: BeautifulSoup) -> str:
    a_tag = soup.find("a", class_="active")

    if a_tag:
        # Берём текст без иконки и лишних пробелов
        text = a_tag.get_text(strip=True)
        return text
    else:
        return ""
def parse_channel(driver, url: str) -> dict:
    driver.get(url)

    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-group-item"))
            )
        except:
            print(f"[!] Не удалось дождаться загрузки h1: {url}")
            time.sleep(15)
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        check = check_capcha(soup)

        if check:
            break
        else:
            print(f"[!] Имя не найдено, возможно капча. Ждём решения капчи... ({url})")
            time.sleep(5)

    data = {
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

    return data
