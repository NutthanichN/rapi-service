import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dirs import ROOT_DIR
from time import sleep
from datetime import datetime


DOMAIN_URL = 'https://www.wongnai.com/'
THIS_DIR = ROOT_DIR / 'web_scraping/'


def get_soup_using_selenium(url: str, driver: webdriver, timeout) -> BeautifulSoup:
    driver.get(url)
    WebDriverWait(driver, timeout)
    return BeautifulSoup(driver.page_source, 'html.parser')


def write_to_file(text: str, output_file: str):
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(text)


def get_region_links_and_name(soup: BeautifulSoup) -> list:
    region_links = []
    region_url = DOMAIN_URL + 'regions/'
    a_regions = soup.find('div', class_='regions f').find_all('a', class_='name', href=True)
    for a in a_regions:
        link = region_url + a['href'] + '/businesses'
        region_links.append((a.string, link))
    print(f'Get {len(region_links)} region links...')
    return region_links


def write_regions_link_to_file(region_links: list, file: str):
    f = open(file, 'a', encoding='utf8')
    for name, link in region_links:
        f.write(f"{name},{link}\n")
    f.close()


def read_regions_links(file: str) -> dict:
    with open(file, 'r', encoding='utf8') as f:
        pass


def _get_restaurants_links(soup: BeautifulSoup) -> dict:
    r_links = []
    big_div = soup.find('div', class_='sc-195dyzv-0 fkmkTf')
    a_tags = big_div.find_all('a', class_='sc-19mqvkt-0 fYjaTu', href=True)
    for a in a_tags:
        r_links.append(DOMAIN_URL + a['href'])
    print(f'Get {len(r_links)} restaurants...')

    next_page = ''
    a_nexts = soup.find('div', class_='aefy6t-0 jAQpRS').find_all('a', class_='k0pvs2-0 gciMDQ', href=True)
    # print(a_nexts)
    for a in a_nexts:
        button = a.find('button')
        if button.string == 'ถัดไป >':
            next_page = a['href']

    return {
        'next_url': DOMAIN_URL + next_page,
        'links': r_links
    }


def get_restaurant_links_from_all_pages(driver: webdriver, start_url: str, district_name: str):
    print(f"Start at {datetime.now().strftime('%H:%M:%S')}: {district_name}")
    r_links = []
    url = start_url
    page_num = 1
    while url != '':
        soup = get_soup_using_selenium(url, driver, 15)
        try:
            restaurants = _get_restaurants_links(soup)
            r_links += restaurants['links']
            url = restaurants['next_url']
            print(f"Finished page {page_num}")
            page_num += 1
            write_restaurant_link_to_file(r_links, f"{THIS_DIR}/restaurant_links_{district_name}.txt")
            if page_num >= 80:
                sleep(20)
            elif page_num >= 40:
                sleep(15)
            else:
                sleep(8)
        except AttributeError:
            print(r_links)
            print(f"Stopped at {datetime.now().strftime('%H:%M:%S')}")
            raise Exception(f"Is suspected to be a robot at page {page_num}. Try again.")
    print(f"Finished at {datetime.now().strftime('%H:%M:%S')}")
    return r_links


def write_restaurant_link_to_file(restaurant_links: list, file: str):
    print(f"Writing to {file} ...")
    f = open(file, 'a', encoding='utf8')
    for link in restaurant_links:
        f.write(link + '\n')
    f.close()
    print("Finished writing.")


BANGKOK_URL = DOMAIN_URL + 'regions/bangkok/districts-neighborhoods'

driver = webdriver.Chrome(f"{THIS_DIR}/chromedriver.exe")
# soup = get_soup_using_selenium(BANGKOK_URL, driver, 15)
# region_links = get_region_links_and_name(soup)
# write_regions_link_to_file(region_links, f"{THIS_DIR}/region_links.txt")

DISTRICT_URL = 'https://www.wongnai.com/regions/178-%E0%B8%A7%E0%B8%B1%E0%B8%92%E0%B8%99%E0%B8%B2/businesses'

# page 118
# district = 'วัฒนา'
# start_url = 'https://www.wongnai.com/businesses?regions=178&rerank=false&page.number=118'

# page 46
# district = 'ปทุมวัน'
# start_url = 'https://www.wongnai.com/businesses?regions=42&rerank=false&page.number=46'

# page 58
# district = 'บางกะปิ'
# start_url = 'https://www.wongnai.com/businesses?regions=39&rerank=false&page.number=58'

# page 52
# district = 'ประเวศ'
# start_url = 'https://www.wongnai.com/businesses?regions=151&rerank=false&page.number=52'

district = 'ห้วยขวาง'
start_url = 'https://www.wongnai.com/regions/85-%E0%B8%AB%E0%B9%89%E0%B8%A7%E0%B8%A2%E0%B8%82%E0%B8%A7%E0%B8%B2%E0%B8%87/businesses'
restaurant_links = get_restaurant_links_from_all_pages(driver, start_url, district)
print(restaurant_links)
# driver.close()
