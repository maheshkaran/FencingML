from unicodedata import name
from urllib.request import urlopen
import re

from bs4 import BeautifulSoup




def buildFencingNetwork(url):
    """ Given a url, create a url list of all the people they have fenced, from Fencing Tracker"""

    initial_url = "https://fencingtracker.com"
    page = urlopen(url)
    html= page.read().decode("utf-8")

    name_url_list = re.findall("href=\"/p.*?/history\"",html)
    url_list = [url]

    for urls in name_url_list:
        string = re.sub('history\"',"history",re.sub('href=\"',"",urls))
        url_list += [initial_url+string]
    return url_list

def buildRecursiveFencingNetwork(url,num_layers):
    """ Given an initial url and number of layers, return a full fencing network """

    network_urls = []

    if (num_layers == 1):
        network_urls = network_urls+buildFencingNetwork(url)
        return list(set(network_urls))
    else:
        mid = [buildRecursiveFencingNetwork(urls,num_layers-1) for urls in buildFencingNetwork(url)]
        flat_mid = [item for sublist in mid for item in sublist]
        network_urls = network_urls + flat_mid
        return list(set(network_urls))

def buildFencerJSON (url):
    return 0

if __name__ == "__main__":
    #network = buildRecursiveFencingNetwork("https://fencingtracker.com/p/100276575/Tarun-Mahesh/history",2)
    #print(len(network))


    html_doc = """<html><head><title>The Dormouse's story</title></head>
                <body>
                <p class="title"><b>The Dormouse's story</b></p>

                <p class="story">Once upon a time there were three little sisters; and their names were
                <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
                <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
                and they lived at the bottom of a well.</p>

                <p class="story">...</p>
                """
    soup = BeautifulSoup(html_doc, 'html.parser')
    (soup.prettify())
