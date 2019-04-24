import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import random
import yaml
import site as s

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.intent('Search',
    mapping={'site': 'Site',  'searchTerm':'SearchTerm'},
    default={'site': 'golem', 'searchTerm':''})
def search(site, searchTerm):
    print(site, searchTerm)

    if site == "golem":
        obj = s.Golem()
    elif site == "zeit":
        obj = s.Zeit()
    elif site == "welt":
        obj = s.Welt()
    else:
        return statement("Es gab einen Fehler")
    session.attributes["site"] = obj.url

    articles, links = obj.search_article(searchTerm)
    session.attributes["lastSearch"] = links
    antwort = "Für welchen der folgenden Artikel interessieren Sie sich?"
    for i in range(0, len(articles)):
        antwort += articles[i] + "..."

    return question(antwort)

@ask.intent('Read',
    mapping={'site': 'Site',  'activity':'Activity'},
    default={'site': 'golem', 'activity':'read_headlines'})
def read(site, activity):
    print(site, activity)

    response = ""
    return statement(response)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Dieser Skill erlaubt es Ihnen einige Nachrichten Websites zu nutzen'
    return statement(speech_text)

@ask.launch
def launch():
    return read("golem", "read_headlines")

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run()
