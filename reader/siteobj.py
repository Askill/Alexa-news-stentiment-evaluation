import urllib.request,urllib.parse,urllib.error
from lxml import html
import requests
import re


class Site:
    url = ""     
    header_values = {
            'Connection:' : 'Keep-alive',
            'name' : 'Michael Foord',
            'location' : 'Northampton',
            'language' : 'German',
            'User-Agent': 'Mozilla 4/0'}


    def __init__(self):

        return None

    def search_article(self, topic):
        return False
    def get_news(self):
        return False
    def read_article(self, url):
        return False
    def read_headlines(self, url):
        return False
    

class Golem(Site):
    url = "golem"   
    def search_article(self, topic):
        searchURL = "https://suche.golem.de/search.php?l=10&q=" + topic.replace(" ", "+")
        site = requests.get(searchURL)
        tree = html.fromstring(site.content)
        
        articles = tree.xpath('//span[@class="dh2 head2"]/text()')
        links = tree.xpath('//ol[@class="list-articles"]/li/header//@href')
        return articles, links
    
    def get_news(self):
        searchURL = "https://www.golem.de/"
        site = requests.get(searchURL)
        tree = html.fromstring(site.content)

        articles = tree.xpath('//h2[@class="head2"]/text()')
        return articles

    def read_headlines(self, url):
        site = requests.get(url)
        tree = html.fromstring(site.content)

        title = tree.xpath('//header/h1/span[@class="dh1 head5"]/text()')
        title += tree.xpath('//header/p/text()')
        return title

    def read_article(self, url):
        site = requests.get(url)
        tree = html.fromstring(site.content)

        title = self.read_headlines(url)
        title += tree.xpath('//div[@class="formatted"]/p/text()')
        return title
