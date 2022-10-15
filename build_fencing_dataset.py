from unicodedata import name
from urllib.request import urlopen
import re
from venv import create
import pandas as pd
from bs4 import BeautifulSoup
import json

def openPage(url):
    page = urlopen(url)
    html= page.read().decode("utf-8")
    return html

def buildFencingNetwork(url):
    """ Given a url, create a url list of all the people they have fenced, from Fencing Tracker"""

    initial_url = "https://fencingtracker.com"
    html = openPage(url)

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
    html= openPage(url)
    soup = BeautifulSoup(html, 'html.parser')
    fencer_name = soup.find("h1")
    rating = soup.find("h6").text
    rating = re.search('Rating (.*?),',rating).group(1)

    data = []
    table = soup.find_all('table',limit=3)
    
    for tables in table:
        table_body = tables.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    data = [row[-1] for row in data]

    for i in range(len(data)):
        if data[i] == '-':
            data[i] = '0'

    all_time_data = [float(x.replace('%','e-2')) for x in data]

    if len(all_time_data) != 0 or sum(all_time_data)>0:
        
        fencer_json = {
            "name": fencer_name.text,
            "current_rating": rating,
            "Victories": all_time_data[0],
            "Losses": all_time_data[1],
            "Win Ratio": all_time_data[2], 
            "Pool Victories": all_time_data[3], 
            "Pool Losses": all_time_data[4], 
            "Pool Win Ratio": all_time_data[5],
            "DE Victories": all_time_data[6], 
            "DE Losses": all_time_data[7], 
            "DE Win Ratio": all_time_data[8]}
        return json.dumps(fencer_json)
    else:
        return 0

def createFencerDataSet(initial_fencer_url, num_layers, output_file):

    network = buildRecursiveFencingNetwork(initial_fencer_url,num_layers)

    outfile = open(output_file,"w")
    for url in network:
        fencer_json = buildFencerJSON(url)
        if fencer_json != 0:
            outfile.write(fencer_json)
            outfile.write("\n")

def buildBoutJSON(fencer1_url, fencer2_url):
    fencer1 = buildFencerJSON(fencer1_url)
    html = openPage(fencer1_url)
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    table = soup.find_all('table')

    for tables in table[4:-1]:
        table_body = tables.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    fencer2 = buildFencerJSON(fencer2_url)
    bout_json = {
            "fencer1_name":fencer1["name"],
            "fencer1_rating": fencer1["rating"],
            "fencer1_statistics":[fencer1["Victories"], fencer1["Losses"], fencer1["Win Ratio"], fencer1["Pool Victories"], fencer1["Pool Losses"], fencer1["Pool Win Ratio"], fencer1["DE Victories"], fencer1["DE Losses"], fencer1["DE Win Ratio"]],
            "fencer2_name":fencer2["name"],
            "fencer2_rating": fencer2["rating"],
            "fencer2_statistics":[fencer2["Victories"], fencer2["Losses"], fencer2["Win Ratio"], fencer2["Pool Victories"], fencer2["Pool Losses"], fencer2["Pool Win Ratio"], fencer2["DE Victories"], fencer2["DE Losses"], fencer2["DE Win Ratio"]],
            }


    return data



if __name__ == "__main__":
    #createFencerDataSet("https://fencingtracker.com/p/100276575/Tarun-Mahesh/history",1,"FencerDataSet.json")

    print(buildBoutJSON("https://fencingtracker.com/p/100276575/Tarun-Mahesh/history"))



    