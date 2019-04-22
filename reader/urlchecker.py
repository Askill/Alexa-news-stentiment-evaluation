import urllib.request,urllib.parse,urllib.error
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urljoin
import requests
import re

import networkx as nx
import matplotlib.pyplot as plt

class url:

    url = ""                # the url of the website to be checked
    sites = dict()          # dic. with all sites and urls on those sites
    does_work = []          # array with all prev. positiv tested urls
    does_not_work = dict()  # dic. with all not working urls and the site that linked there
    header_values = {
                'Connection:' : 'Keep-alive',
                'name' : 'Michael Foord',
                'location' : 'Northampton',
                'language' : 'English',
                'User-Agent': 'Mozilla 4/0'}

    def __init__(self, url):
        self.url = urllib.request.urlopen(url).geturl()
            

    def make_url(self, link, start):
        ret_link = urljoin(start, link)
       
        return ret_link

    def test_url(self, link, root):

        if link in self.sites or link in self.does_work:
            return True
        elif link in self.does_not_work:
            return False
        else:
            try:
            
                header = urllib.parse.urlencode(self.header_values)
                header=header.encode('ascii')
                request = urllib.request.Request(link, header)
                response = urllib.request.urlopen(request)
                self.does_work.append(link)
                print(" works " + link)
                return True

            except (urllib.error.HTTPError, urllib.error.URLError, ValueError): 
                self.does_not_work[link]=root
                print(" doesn't work " + link)
                return False

    def get_actual_urls(self, links, root):
        temp_links = []
        for each_link in links:

            if each_link.startswith("http") | each_link.startswith("//"):
                temp_links.append(each_link)
            else:
                temp_links.append(urljoin(root, each_link)) 
            
        for each_temp_link in temp_links:
            self.test_url(each_temp_link, root)

        return temp_links    

    def run_check(self, root=None):      # root is the url of the current Site
        
        if root == None:
            root = self.url
        else:
            pass
        
        if root in self.sites or self.url.rsplit('/', 1)[0] not in root or not self.test_url(root, root):
            return  

        header = urllib.parse.urlencode(self.header_values)
        header=header.encode('ascii')
        
        request = urllib.request.Request(root, header)
        http_response = urllib.request.urlopen(request)
        root = http_response.geturl()
        response_data= http_response.read()
      
        
        links = re.findall(r'href="(.*?)"' , str(response_data))
        
        links = self.get_actual_urls(links, root)   
        
       
        self.sites[root]=links
        for each_link in links:         
            self.run_check(each_link)
      

    def graph(self):
        
        G = nx.Graph(self.sites)

        label_dict = {}
        for key, value in self.sites.items():               #that's not how it works... todo: later
            label_dict[key]=self.remove_root(value)
          
        nx.draw(G, with_labels=True, font_size=8 , node_size=1000, node_color="skyblue", edge_color='#A0FFA2', pos=nx.spring_layout(G))

        plt.show()  

    def remove_root(self, links):
        ret_links = []
        for link in links: 
            ret_links.append(link.rsplit('.', 1)[0])

        return ret_links

    def clean(self):
        self.sites.clear()
        self.does_not_work.clear()
        self.does_work.clear()














            