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


@ask.intent('GolemSearch',
    mapping={'site': 'Site',  'searchTerm':'Topic'},
    default={'site': 'golem', 'searchTerm':''})
def search(site, searchTerm):
    print(site, searchTerm)

    obj = site2.Golem()

    articles, links = obj.search_article(searchTerm)

    session.attributes["lastSearch"] = links
    response = "Für welchen der folgenden Artikel interessieren Sie sich?"
    for i in range(0, 5):
        response += articles[i] 

    return question(response)

@ask.intent('News',
    mapping={'site': 'Site'},
    default={'site': 'golem'})
def news(site):
    print(site)
    obj = site2.Golem()
    news = obj.get_news()
    response = ""
    for i in range(0, 5):
        response += news[i] 
    return statement(response)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Dieser Skill erlaubt es Ihnen einige Nachrichten Websites zu nutzen'
    return statement(speech_text)

@ask.launch
def launch():
    return search("golem", "gaming")

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run()
