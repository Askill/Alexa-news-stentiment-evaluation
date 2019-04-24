import urllib.request,urllib.parse,urllib.error
from lxml import html
import requests
import re

searchURL = "https://suche.golem.de/search.php?l=10&q=gaming" 
site = requests.get(searchURL)
tree = html.fromstring(site.content)

articles = tree.xpath('//span[@class="dh2 head2"]/text()')
links = tree.xpath('//ol[@class="list-articles"]/li/header//@href')
print(len(articles), len(links))