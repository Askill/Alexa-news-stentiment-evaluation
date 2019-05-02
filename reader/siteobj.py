import urllib.request,urllib.parse,urllib.error
from lxml import html
import requests
import re


class Site:
    siteName = ""     
    baseURL = ""
    searchURLString = ""
    xPath = dict()
    xPath["searchArticle"] = ""
    xPath["searchLinks"] = ""
    xPath["newsArticle"] = ""
    xPath["readHeadlineTitle"] = ""
    xPath["readHeadlineText"] = ""
    xPath["readArticleText"] = ""

    header_values = {
            'Connection:' : 'Keep-alive',
            'name' : 'Michael Foord',
            'location' : 'Northampton',
            'language' : 'German',
            'User-Agent': 'Mozilla 4/0'}
    

    def __init__(self):
        return None

    def search_article(self, topic):
        searchURL = self.searchURLString + topic.replace(" ", "+")
        site = requests.get(searchURL)
        tree = html.fromstring(site.content)
        
        articles = tree.xpath(self.xPath["searchArticle"])
        links = tree.xpath(self.xPath["searchLinks"])
        return articles, links
    
    def get_news(self):
        searchURL = self.baseURL
        site = requests.get(searchURL)
        tree = html.fromstring(site.content)

        articles = tree.xpath(self.xPath["newsArticle"])
        return articles

    def read_headlines(self, url):
        site = requests.get(url)
        tree = html.fromstring(site.content)

        title = tree.xpath(self.xPath["readHeadlineTitle"] )
        title += tree.xpath(self.xPath["readHeadlineText"])
        return title

    def read_article(self, url):
        site = requests.get(url)
        tree = html.fromstring(site.content)

        title = self.read_headlines(url)
        title += tree.xpath(self.xPath["readArticleText"])
        return title
    

class Golem(Site):
    siteName = "golem"
    baseURL = "https://www.golem.de/"   
    searchURLString = "https://suche.golem.de/search.php?l=10&q="
    Site.xPath["searchArticle"] = '//span[@class="dh2 head2"]/text()'
    Site.xPath["searchLinks"] = '//ol[@class="list-articles"]/li/header//@href'
    Site.xPath["newsArticle"] = '//h2[@class="head2"]/text()'
    Site.xPath["readHeadlineTitle"] = '//header/h1/span[@class="dh1 head5"]/text()'
    Site.xPath["readHeadlineText"] = '//header/p/text()'
    Site.xPath["readArticleText"] = '//div[@class="formatted"]/p/text()'

