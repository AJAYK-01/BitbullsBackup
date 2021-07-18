# Bitbulls moniTOR spider :spider:

## Features
![screenshot_1](https://github.com/HacKP-CyberDome/bitbull-monitor-web/blob/master/imgs/Screenshot_1.png)

Users can put two types of inputs:
* Search term
* Onion link to scrap 

The Django server automatically understands the type of query specified and acts accordingly.
If a search string is specified, it acts as a search engine and gives out information already in the database.


If a .onion link is specified, the Django server initiates the scraping and plays a loading animations until the 
process is complete and then displays the result. 

![screenshot_2](https://github.com/HacKP-CyberDome/bitbull-monitor-web/blob/master/imgs/Screenshot_2.png)


## Installation 

```bash
git clone https://github.com/HacKP-CyberDome/bitbull-monitor-web
cd bitbull-monitor-web
python -m pip install -r requirements.txt --user
```
Additionaly, some other programs are required which should be installed from the OS package manager.

```bash
sudo apt update
sudo apt install tor 
```

## Running

Edit the torrc file situated in /etc/tor/torrc and change the port to 9150.

```bash
sudo su
nano /etc/tor/torrc
```
Uncomment line `SocksPort localhost:9050` and 
change it to `SocksPort localhost:9150`

Initiate the `tor` service.
```sudo service tor start```

## Script
The standalone scrapping script used for scraping is called bitbulls.py located at the root of the directory.

```
usage: bitbulls.py [-h] [-d] URL

A spider to scrape and index TOR websites

positional arguments:
  URL            Base url from which to start scraping

optional arguments:
  -h, --help     show this help message and exit
  -d , --depth   Depth to which the spider should search for
```
It scraps urls asynchronously and implements the use of threading. 

## Django Server

Start Django server

```bash
python manage.py runserver
```

## Data Flow

Given below is a simplified flowchart on how the spider/search engine works.
![flowchart](https://github.com/HacKP-CyberDome/bitbull-monitor-web/blob/master/flowchart.jpg)

