import requests
import urllib.request
from bs4 import BeautifulSoup as bs

response= requests.get('https://s.1688.com/selloffer/offer_search.htm?keywords=&n=y&netType=1%2C11&encode=utf-8&spm=a260k.dacugeneral.search.0')
out =bs(response.content,"lxml")
price = out.find('span',attrs={'class':'sm-offer-priceNum sw-dpl-offer-priceNum'})
print(price.text)

