import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import random
import yaml
import siteobj as site2

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.intent('searchon', mapping={'site': 'Site'}, default={'site': 'golem'})
def search_on(site):
    try:
        session.attributes["siteName"] = site
    except: 
        print("error")

    if "searchTerm" in session.attributes and session.attributes["searchTerm"] is not None and "lastCall" in session.attributes and session.attributes["lastCall"] == "searchfor":
        searchTerm = session.attributes["searchTerm"]
        session.attributes["searchTerm"] = None
        return search_for(searchTerm)
    if "lastCall" in session.attributes and session.attributes["lastCall"] == "news":
        return news(site)
    session.attributes["lastCall"] = "searchon"
    return question("Wonach?")

@ask.intent('searchfor', mapping={'searchTerm':'Topic'}, default={'searchTerm':''})
def search_for(searchTerm):
    try:
        site = session.attributes["siteName"]
    except:
        site = None

    if site == "golem":
        obj = site2.Golem()
    elif site is None:
        session.attributes["searchTerm"] = searchTerm
        session.attributes["lastCall"] = "searchfor"
        return question("Auf welcher Seite wollen Sie hiernach Suchen?")
    else:
        return statement("error")

    articles, links = obj.search_article(searchTerm)
    session.attributes["lastSearch"] = links
    response = "Für welchen der folgenden Artikel interessieren Sie sich?"

    if len(articles) > 0:
        for i in range(0, max(5, len(articles))):
            response += articles[i] 
    else:
        return question("Dazu konnte nichts gefunden werden. Möchten Sie nach etwas anderem Suchen?")

    session.attributes["lastCall"] = "searchfor"

    return question(response + "noch etwas?")

@ask.intent('News', mapping={'site': 'Site'}, default={'site': ''})
def news(site):

    if site == "golem":
        obj = site2.Golem()
    elif site == '':
        session.attributes["lastCall"] = "news"
        return question("Auf welcher Seite wollen Sie hiernach Suchen?")
    else:
        return statement("error")

    news = obj.get_news()

    response = ""
    for i in range(0, 5):
        response += news[i] + ". "

    session.attributes["lastCall"] = "news"
    return statement(response)

@ask.intent('SearchTwo', mapping={'number': 'Nummer'}, default={'number': 1})
def search_answer(number):
    print(number)
    obj = site2.Golem()

    art = obj.read_headlines(session.attributes["lastSearch"][int(number)-1])
    response = ""
    for element in art:
        response +=  element + "   "

    session.attributes["lastCall"] = "search2"
    return statement(response)

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
    app.run()
