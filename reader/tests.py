import urllib.request,urllib.parse,urllib.error
from lxml import html
import requests
import re

url="https://www.golem.de/news/tchap-forscher-gelingt-anmeldung-im-regierungschat-frankreichs-1904-140799.html"
site = requests.get(url)
tree = html.fromstring(site.content)
title = tree.xpath('//div[@class="formatted"]/p/text()')
print(title)