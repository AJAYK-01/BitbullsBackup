import requests
from fake_useragent import UserAgent
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
import argparse

nest_asyncio.apply()

parser = argparse.ArgumentParser(description="A spider to scrape and index TOR websites")
parser.add_argument('-d', '--depth', type=int, metavar='', default=1, help="Depth to which the spider should search for")
parser.add_argument('u', type=str, metavar='URL',  help="Base url from which to start scraping")
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def get_links(url):
    """
        Returns scraped links from given url.
    """
    ua = UserAgent()
    header = {'User-Agent': str(ua.firefox)}
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
        texts = soup.find_all(text=True)
        for link in tags:
            links.append(link['href'])
        
         #to get non href text links
        for text in texts:
            if re.match(r'(?:http|https)://\w*\.onion', text):
                links.append(text.split('.onion')[0]+'.onion')
            #to get links from just the random text part if present on site
            if len(text) == 56 or len(text) == 16:
                links.append('http://'+text+'.onion')
        return links
    except:
        print("site refused to connect")
        return None


async def get_contents(url):
    """
        Returns title of given url.
        Returns NOT FOUND otherwise.
    """
    ua = UserAgent()
    header = {'User-Agent': str(ua.firefox)}
    try:
        print("Current url is : ", url)
        proxies = 'socks5://127.0.0.1:9150'
        connector = ProxyConnector.from_url(proxies)
        async with aiohttp.ClientSession(headers=header, connector=connector) as session:
            async with session.get(url) as resp:
                data = await resp.text()
        soup = BeautifulSoup(data, 'html.parser')
        return dict({'url': url, 'title': soup.title.text, 'html': str(soup)})
    except Exception as e:
        print(e)
        return dict({'url': url, 'title': "NOT FOUND", 'html': ""})


def scrape(url):
    """
        the scrapper function
    """
    sites = []
    tasks = []
    links = get_links(url)
    if links:
        for link in links:
            if link != url:
                z = re.match(r'(?:http|https)://\w*\.onion', link)
                #to ignore the links containing '#'' which are just pointing to parts on same page
                y = re.search('#', link)    
                if not y and z :

                    tasks.append(get_contents(link))
        if tasks != []:    
            try:            
                #returns a tuple containing completed and pending futures
                done, pending = loop.run_until_complete( asyncio.wait(tasks)) 

                for future in done:
                    value = future.result()
                    sites.append(value)
                    
            except Exception as e:
                print(e)
            
        return sites


async def scrape_from_site(url, depth, threads):
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
        if depth > 1:
            subsite = {}
            tasks = []
            threads = []
            if sites:
                for subsite in sites:
                    url = subsite['url']
                    tasks.append(scrape_from_site(url, depth-1, threads))
                loop.run_until_complete(asyncio.wait(tasks))


    else:
        print("Not a suitable link")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.u, args.depth)
    loop.close()
