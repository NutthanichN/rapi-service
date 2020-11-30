# import bs4
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dirs import ROOT_DIR


# r = requests.get('https://www.wongnai.com/regions/74-%E0%B8%98%E0%B8%99%E0%B8%9A%E0%B8%B8%E0%B8%A3%E0%B8%B5/businesses?domain=1')
# soup = bs4.BeautifulSoup(r.text, 'html.parser')
# print(soup.prettify())

# selector = 'span._2qDKIyMmA-jMRyfxACZWt6'
# price = html_page.select_one(selector)
# print(price.text)


def get_region_links_and_name(soup: BeautifulSoup) -> list:
    region_links = []
    domain_url = 'https://www.wongnai.com/regions/'
    a_regions = soup.find('div', class_='regions f').find_all('a', class_='name', href=True)
    for a in a_regions:
        link = domain_url + a['href'] + '/businesses'
        region_links.append((a.string, link))
    print(f'Get {len(region_links)} region links...')
    return region_links


def write_regions_link_to_file(region_links: list, file: str):
    f = open(file, 'a', encoding='utf8')
    for name, link in region_links:
        f.write(f"{name},{link}\n")
    f.close()


def get_soup_using_selenium(url: str, driver: webdriver, timeout) -> BeautifulSoup:
    driver.get(url)
    WebDriverWait(driver, timeout)
    return BeautifulSoup(driver.page_source, 'html.parser')


def write_to_file(text: str, output_file: str):
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(text)


BASE_URL = 'https://www.wongnai.com/regions/bangkok/districts-neighborhoods'
THIS_DIR = ROOT_DIR / 'web_scraping/'

driver = webdriver.Chrome(f"{THIS_DIR}/chromedriver.exe")
soup = get_soup_using_selenium(BASE_URL, driver, 15)
region_links = get_region_links_and_name(soup)
write_regions_link_to_file(region_links, f"{THIS_DIR}/region_links.txt")
driver.close()
