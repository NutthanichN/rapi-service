import bs4
import requests
r = requests.get('https://www.wongnai.com/regions/74-%E0%B8%98%E0%B8%99%E0%B8%9A%E0%B8%B8%E0%B8%A3%E0%B8%B5/businesses?domain=1')
html_page = bs4.BeautifulSoup(r.text, 'html.parser')
print(html_page.prettify())
# selector = 'span._2qDKIyMmA-jMRyfxACZWt6'
# price = html_page.select_one(selector)
# print(price.text)