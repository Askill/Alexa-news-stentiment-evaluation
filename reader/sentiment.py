# http://www.ulliwaltinger.de/sentiment/
# https://github.com/solariz/german_stopwords
#!/usr/bin/env python
# https://github.com/markuskiller/textblob-de
# -*- coding: utf-8 -*-
import nltk
import copy
import encodings
import csv
from siteobj import *
from nltk.corpus import treebank
from textblob_de import TextBlobDE as TextBlob


def get_sentiment(url):
        NewsText = obj.read_article(url)

        newText = ""
        for text in NewsText:
                newText += text

        newText = TextBlob(newText)

        sent = newText.sentiment[0] 
        if sent < 0:
                good = "shit"
        else:
                good = "nice" 
        print(good, newText.sentiment,"\n", link.split("/")[-1], "\n")
        return good

obj = Golem()
news, links = obj.get_news()

for link in links:
        get_sentiment(link)
