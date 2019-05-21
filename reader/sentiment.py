# http://www.ulliwaltinger.de/sentiment/
# https://github.com/solariz/german_stopwords
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import copy
import encodings
import csv
from siteobj import *
from nltk.corpus import treebank

negatives = dict()
positives = dict()
neutrals = dict()

with open("./reader/GermanPolarityClues-2012/GermanPolarityClues-Negative.tsv", "r", encoding="utf-8") as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
        
        if "-" not in row[4].split("/"):
                negatives[row[0]] = [float(row[4].split("/")[0]), float(row[4].split("/")[1]), float(row[4].split("/")[2])]

with open("./reader/GermanPolarityClues-2012/GermanPolarityClues-Neutral.tsv", "r", encoding="utf-8") as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row  in reader:
        if "-" not in row[4].split("/"):
                neutrals[row[0]] = [float(row[4].split("/")[0]), float(row[4].split("/")[1]), float(row[4].split("/")[2])]

with open("./reader/GermanPolarityClues-2012/GermanPolarityClues-Positive.tsv", "r", encoding="utf-8") as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row  in reader:
        if "-" not in row[4].split("/"):
                positives[row[0]] = [float(row[4].split("/")[0]), float(row[4].split("/")[1]), float(row[4].split("/")[2])]

# get stopwords
stopwords = []
with  open("./reader/stopwords.txt", 'r', encoding='utf-8') as f:
        for line in f:
                stopwords.append(line)

extraSW = [".", ",", "´´", "``", "'", '"', ]
stopwords += extraSW

obj = Spiegel()

NewsText = obj.read_article("https://www.spiegel.de/netzwelt/games/labo-vr-set-von-nintendo-im-test-erst-basteln-dann-staunen-a-1265633.html")

newText = ""
for text in NewsText:
        newText += text

tokens = nltk.word_tokenize(newText)

toDelete = []
for token in tokens:
        if token in stopwords:
                toDelete.append(token)

for token in toDelete:
        while token in tokens:
                tokens.remove(token)

p = 0
ne = 0
nu = 0
for token in tokens:
        if token in negatives:
                p += negatives[token][0]
                ne += negatives[token][1]
                nu += negatives[token][2]
        elif token in positives:
                p += positives[token][0]
                ne += positives[token][1]
                nu += positives[token][2]
        elif token in neutrals:
                p += neutrals[token][0]
                ne += neutrals[token][1]
                nu += neutrals[token][2]
                

total = p + ne + nu

p /= total
nu /= total
ne /= total

print(p, nu, ne)
