import requests
from fake_useragent import UserAgent
import sys
import re
from bs4 import BeautifulSoup
import json
import os.path
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
from os import path
from threading import Thread
import nest_asyncio
nest_asyncio.apply()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def get_links(url):
    """
        Returns scraped links from given url.
    """
    ua = UserAgent()
    header = {'User-Agent':str(ua.firefox)}
    links = []
    proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }
    try:
        data = requests.get(url, proxies=proxies, headers=header).text 
        soup = BeautifulSoup(data, 'html.parser')
        print(soup.title.text)
        tags = soup.find_all('a')
        for link in tags:
            links.append(link['href'])
        return links
    except:
        print("site refused to connect")
        return None
     

async def get_title(url):
    """
        Returns title of given url.
        Returns NOT FOUND otherwise.
    """
    ua = UserAgent()
    header = {'User-Agent':str(ua.firefox)}
    try:
        print("Current url is : ", url)
        proxies = 'socks5://127.0.0.1:9150'
        connector = ProxyConnector.from_url(proxies)
        
        async with aiohttp.ClientSession(headers=header, connector=connector) as session:
            async with session.get(url) as resp:
                data = await resp.text()
        soup = BeautifulSoup(data, 'html.parser')
            
        return dict({'url': url, 'title': soup.title.text})
    except Exception as e:
        print(e)
        return dict({'url': url, 'title': "NOT FOUND"})

def scrape(url):
    """
        the scrapper function
    """
    sites = []
    tasks = []
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    links = get_links(url)
    if links:
        for link in links:
            if link != url:
                z = re.match(r'(?:http|https)://\w*\.onion', link)
                y = re.search('#', link)    #to ignore the links containing # which are just pointing to parts on same page
                if not y and z :
                    tasks.append(get_title(link))
        if tasks != []:    
            try:            
                done, pending = loop.run_until_complete( asyncio.wait(tasks)) #returns a tuple containing completed and pending futures
                for future in done:
                    value = future.result()
                    sites.append(value)
                    
            except Exception as e:
                print(e)
            
        # loop.close()
        return sites

async def scrape_from_site(url,depth,threads):
    """
        Extracts each link from previous run and reruns main() with those links
    """
    t = Thread(target=main,args=(url,depth))
    threads.append(t)
    t.start()
    # Thread(target=main(url, depth))

def main(url, depth):
    sites = []
    x = re.match(r'(?:http|https)://\w*\.onion', url)
    if 1:
        file_dir = (url.split('://')[1] + ".json").replace('/', '')
        if path.exists(file_dir):

            print("This link is already scrapped")
        else:
            print("scrapping ", x.string)
            sites = scrape(x.string)
            if sites != [] and sites:
                out_file = open(file_dir, "w")
                json.dump(sites, out_file, indent=6)
                out_file.close()
        if depth > 1 :
            subsite = {}
            tasks = []
            threads = []
            if sites:
                for subsite in sites:
                    url = subsite['url']
                    if subsite['title'] != "NOT FOUND":
                        tasks.append(scrape_from_site(url, depth-1, threads))
                loop.run_until_complete( asyncio.wait(tasks))

    else:
        print("Not a suitable link")


if __name__ == "__main__":
    (main(sys.argv[1], int(sys.argv[2])))
    loop.close()
