# An Alexa Skill for reading news sites

Supports: Spiegel.de, Golem.de
### How to expand the supported Sites:

1. in siteobj.py create a new class for your Site
2. Follow the examples for Golem or Spiegel
3. fill the xPath Dict with the needed xPath Expression
4. update the get_site_obj() in main.py
5. exapnd the "Site" type in den Amazon developer console


### Interaction Flow:
![Interaction Flow](./images/flow.png)