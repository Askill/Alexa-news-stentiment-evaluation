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
    xPath["newsLinks"] = ""
    xPath["readHeadlineTitle"] = ""
    xPath["readHeadlineText"] = ""
    xPath["readArticleText"] = ""
    
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
        links = tree.xpath(self.xPath["newsLinks"])
        return articles, links

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
    Site.xPath["newsArticle"] = '//li//h2/text()'
    Site.xPath["newsLinks"] = '//header[@class="cluster-header"]//@href'
    Site.xPath["readHeadlineTitle"] = '//header/h1/span[@class="dh1 head5"]/text()'
    Site.xPath["readHeadlineText"] = '//header/p/text()'
    Site.xPath["readArticleText"] = '//div[@class="formatted"]/p/text()'

class Spiegel(Site):
    siteName = "spiegel"
    baseURL = "https://www.spiegel.de/"   
    searchURLString = "https://www.spiegel.de/suche/?suchbegriff="

    Site.xPath["searchArticle"] = '//span[@class="dh2 head2"]/text()'
    Site.xPath["searchLinks"] = '//ol[@class="list-articles"]/li/header//@href'
    Site.xPath["newsArticle"] = '//div[@class="column-wide pano_xxl"]//div[@class="teaser"]//h2[@class="article-title"]//span[@class="headline"]/text()'
    Site.xPath["newsLinks"] = '//div[@class="column-wide pano_xxl"]//div[@class="teaser"]//h2[@class="article-title"]//@href'
    Site.xPath["readHeadlineTitle"] = '//div[@class="column-both"]//span[@class="headline"]//text()'
    Site.xPath["readHeadlineText"] = '//div[@class="column-both"]/p/strong/text()'
    Site.xPath["readArticleText"] = '//div[@class="formatted"]/p/text()'
