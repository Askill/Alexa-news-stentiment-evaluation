import urllib.request,urllib.parse,urllib.error
from lxml import html
import requests

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

    # not used, who wants to listen to alexa for 10 minutes?
    def read_article(self, url):
        site = requests.get(url)
        tree = html.fromstring(site.content)

        # may need to be reworked
        title = self.read_headlines(url)
        title += tree.xpath(self.xPath["readArticleText"])
        return title
    

class Golem(Site):
    siteName = "golem"
    baseURL = "https://www.golem.de/"   
    searchURLString = "https://suche.golem.de/search.php?l=10&q="
    xPath = dict()
    xPath["searchArticle"] = '//span[@class="dh2 head2"]/text()'
    xPath["searchLinks"] = '//ol[@class="list-articles"]/li/header//@href'
    xPath["newsArticle"] = '//li//h2/text()'
    xPath["newsLinks"] = '//div[@class="g g4"]//header//@href'
    xPath["readHeadlineTitle"] = '//header/h1/span[@class="dh1 head5"]/text()'
    xPath["readHeadlineText"] = '//header/p/text()'
    xPath["readArticleText"] = '//div[@class="formatted"]/p/text()'

class Spiegel(Site):
    siteName = "spiegel"
    baseURL = "https://www.spiegel.de/"   
    searchURLString = "https://www.spiegel.de/suche/?suchbegriff="
    xPath = dict()
    xPath["searchArticle"] = '//div[@class="search-teaser"]/p/text()'
    xPath["searchLinks"] = '//div[@class="search-teaser"]/p//@href'
    xPath["newsArticle"] = '//*[@class="teaser"]/div/h2/a/span[2]/text()'
    xPath["newsLinks"] = '//*[@class="teaser"]/div/h2//@href'
    xPath["readHeadlineTitle"] = '//div[@class="column-both"]//span[@class="headline"]//text()'
    xPath["readHeadlineText"] = '//div[@class="column-both"]/p/strong/text()'
    xPath["readArticleText"] = '//*[@id="js-article-column"]/div/p[1]/text()'
