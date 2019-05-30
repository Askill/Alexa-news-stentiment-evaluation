import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import yaml
from nltk.corpus import treebank
from textblob_de import TextBlobDE as TextBlob
import siteobj as site2
import util

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

###           ###
#    Helper     #
###           ###

def get_site_obj(site):
    if site == "golem":
        obj = site2.Golem()
    elif site.lower() == "spiegel":
        obj = site2.Spiegel()
    else:
        obj = None
    return obj

###              ###
#    CONTROLLER    #
###              ###

@ask.intent('searchon', mapping={'site': 'Site'}, default={'site': 'golem'})
def search_on(site):
    session.attributes["siteName"] = site

    if not util.session_value_is(session.attributes, "searchTerm", None) and util.session_value_is(session.attributes, "lastCall", "searchfor"):
        searchTerm = session.attributes["searchTerm"]
        return search_for(searchTerm)

    if util.session_value_is(session.attributes, "lastCall", "news"):
        return news(site)

    session.attributes["lastCall"] = "searchon"
    return question("Wonach?")

@ask.intent('searchfor', mapping={'searchTerm':'Topic'}, default={'searchTerm':''})
def search_for(searchTerm):
    site = util.get_session_value(session.attributes, "siteName")

    if site is not None:
        obj = get_site_obj(site) 
    else:
        session.attributes["searchTerm"] = searchTerm
        session.attributes["lastCall"] = "searchfor"
        return question("Auf welcher Seite wollen Sie hiernach Suchen?")

    if obj is None: # should never be called
        return question("Error. Auf welcher Seite wollen Sie hiernach suchen?")

    articles, links = obj.search_article(searchTerm)

    session.attributes["lastSearch"] = links
    session.attributes["lastCall"] = "searchfor"

    response = "Für welchen der folgenden Artikel interessieren Sie sich?"
    if len(articles) > 0:
        for i in range(0, min(5, len(articles))):
            response += articles[i] 
    else:
        return question("Dazu konnte nichts gefunden werden. Möchten Sie nach etwas anderem Suchen?")


    return question(response + "noch etwas?")

@ask.intent('News', mapping={'site': 'Site'}, default={'site': ''})
def news(site):
    site = util.get_session_value(session.attributes, "siteName")

    if site is not None:
        obj = get_site_obj(site) 
    else:
        session.attributes["lastCall"] = "news"
        return question("Auf welcher Seite wollen Sie hiernach Suchen?")

    if obj is None:
        return statement("error")

    news, links = obj.get_news()

    session.attributes["lastSearch"] = links
    session.attributes["lastCall"] = "news"
    
    response = ""
    for i in range(0, min(5, len(news))):
        response += news[i] + ". "

    return question(response)

@ask.intent('SearchTwo', mapping={'number': 'Nummer'}, default={'number': 1})
def search_answer(number):
    site = util.get_session_value(session.attributes, "siteName")

    if site is not None:
        obj = get_site_obj(site) 
    else:
        session.attributes["lastCall"] = "search_answer"
        return question("Wonach wollen Sie suchen?")

    if obj is None: # should never be called
        return question("Error. Wonach wollen Sie suchen?")


    links = util.get_session_value(session.attributes, "lastSearch")
    
    # if the site uses relative links, make absolute ones
    if str(links).count("http") < len(links):
        newLinks = []
        for link in links:
            if "http" not in link:
                newLinks.append(obj.baseURL + link)
            else:
                newLinks.append( link)
        links = newLinks
    if int(number) > len(links):
        return question("Dieser Artikel existiert leider nicht, versuchen Sie eine andere Nummer.")
    art = obj.read_headlines(links[int(number)-1])
    response = ""
    for element in art:
        response +=  element 

    session.attributes["lastCall"] = "search2"
    return question(response)


@ask.intent('Senti', mapping={'number': 'Nummer'}, default={'number': 1})
def get_sentiment(number):
    site = util.get_session_value(session.attributes, "siteName")

    if site is not None:
        obj = get_site_obj(site) 
    else:
        session.attributes["lastCall"] = "senti"
        return question("Wonach wollen Sie suchen?")

    if obj is None: # should never be called
        return question("Error. Wonach wollen Sie suchen?")


    links = util.get_session_value(session.attributes, "lastSearch")
    # if the site uses relative links, make absolute ones
    if str(links).count("http") < len(links):
        newLinks = []
        for link in links:
            if "http" not in link:
                newLinks.append(obj.baseURL + link)
            else:
                newLinks.append( link)
        links = newLinks
        
    if int(number) > len(links):
        return question("Dieser Artikel existiert leider nicht, versuchen Sie eine andere Nummer.")

    url = links[int(number)-1]
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

    return question(good)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Dieser Skill erlaubt es Ihnen einige Nachrichten Websites zu nutzen'
    return statement(speech_text)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    return statement("ein fehler ist aufgetreten")

@ask.launch
def launch():
    return question("Was möchten Sie tun?")

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    
    app.run(host='127.0.0.1',port=5000)
