import bs4
import requests

restaurant = requests.get('https://www.wongnai.com/restaurants/471014bo-verti-q-verti-q')
html_page = bs4.BeautifulSoup(restaurant.text, 'html.parser')

# restaurant name
selector = 'h1.sc-AxirZ.sc-1gupvet-4.juuudx'
name = html_page.select_one(selector)
print(name.text)

# rating
selector = 'abbr.sc-1iz478n-2.kypXeq'
rating = html_page.select_one(selector)
print(rating.text)

# review
review = html_page.select("h2.aefy6t-0-h2.fwdDgt")[3].text
print(review)

# cuisine
selector = 'span.sc-AxirZ.juZDil'
cuisine = html_page.select_one(selector).text
print(cuisine)

# address
selector = 'div.nsh7fl-0.jgUGTS'
address = html_page.select_one(selector).string
print(address)

# google map

# opening
opening = html_page.select("table.sc-1kh6w3g-7.eIdclj")[0].text
print(opening)
