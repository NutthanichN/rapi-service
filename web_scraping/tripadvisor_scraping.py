from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dirs import ROOT_DIR
from time import sleep
from datetime import datetime
from web_scraping.wongnai_scraping import write_restaurant_link_to_file


DOMAIN_URL = 'https://www.tripadvisor.com'
THIS_DIR = ROOT_DIR / 'web_scraping/'


def get_soup_using_selenium(url: str, driver: webdriver, timeout) -> BeautifulSoup:
    driver.get(url)
    WebDriverWait(driver, timeout)
    return BeautifulSoup(driver.page_source, 'html.parser')


def write_to_file(text: str, output_file: str):
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(text)


def get_restaurant_links_from_a_page(soup: BeautifulSoup) -> list:
    divs = soup.find('div', attrs={'data-test-target': 'restaurants-list'})
    a_tags = divs.find_all('a', class_='_2uEVo25r _3tdrXOp7', target='_blank', href=True)

    r_links = []
    for a in a_tags:
        link = DOMAIN_URL + a['href']
        r_links.append(link)
    return r_links


def get_restaurant_links_from_all_pages(driver: webdriver, start_url: str):
    print(f"Start at {datetime.now().strftime('%H:%M:%S')}")
    r_links = []
    url = start_url
    page_num = 1
    while page_num <= 408:
        soup = get_soup_using_selenium(url, driver, 15)
        try:
            r_links = get_restaurant_links_from_a_page(soup)
            write_restaurant_link_to_file(r_links, THIS_DIR / 'data/tripadvisor/restaurant_links_t.txt')
            print(f"Finished page {page_num}")
            page_num += 1
            url = driver.find_element_by_link_text('Next').get_attribute('href')
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
    print(f"Finished at {datetime.now().strftime('%H:%M:%S')} (page {page_num})")
    return r_links


if __name__ == '__main__':
    driver = webdriver.Chrome(f"{THIS_DIR}/chromedriver.exe")
    get_restaurant_links_from_all_pages(driver, "https://www.tripadvisor.com/Restaurants-g293916-Bangkok.html")

    # soup = get_soup_using_selenium("https://www.tripadvisor.com/Restaurants-g293916-Bangkok.html",
    #                                driver, 15)
    #
    # divs = soup.find('div', attrs={'data-test-target': 'restaurants-list'})
    # a_tags = divs.find_all('a', class_='_2uEVo25r _3tdrXOp7', target='_blank', href=True)
    #
    # restaurant_list = []
    # for a in a_tags:
    #     link = DOMAIN_URL + a['href']
    #     restaurant_list.append(link)
    # write_restaurant_link_to_file(restaurant_list, THIS_DIR / 'data/tripadvisor/restaurant_links_t_2.txt')
    # a_next = driver.find_element_by_link_text('Next').get_attribute('href')
    # print(a_next.get_attribute('href'))

    # driver.close()
