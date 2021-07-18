#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Category checker
"""

import json
import csv
import difflib
import sys

csv.field_size_limit(sys.maxsize)

# def read_csv(csv_file):
    # data = []
    # for row in csv_file:
        # data.append(dict({'html': row[0], 'title': row[1], 'url': row[2]}))
    
    # return data

def categorize(title, url, html, categories):
    
    for word in title.split(' '):
        for key, values in categories.items():
            for term in values['terms']:
                if word.casefold() == term.casefold():
                    k = 1
                    for link in values['links']:
                        if url == link['url']:
                            k = 0
                            break
                    if k:
                        # print("url : {url}\n html : {html}".format(url=url, html=html))
                        categories[key]['links'].append(dict({'url': url, 'title': title, 'html': html}))    

# def categorise_json():
#     list = open("categories.json", "w")
#     cat = dict()
#     for key, values in categories_terms.items():
#         cat.update({key: dict({'terms': values, 'url': []})})

#     json.dump(cat, list, indent=6)

def main():

    cat_json = open('categories.json', "r")
    categories = json.load(cat_json)
    cat_json.close()

    # with open(sys.argv[-1], encoding='utf-8') as csvf: 
    #     csvReader = csv.reader(csvf)
    #     # onion = read_csv(csvReader)
    with open(sys.argv[-1]) as js:
        onion = json.load(js)
        for entries in onion:
            for entry in entries:
                title = entry['title']
                url = entry['url']
                html = entry['html']
                if title != 'NOT FOUND':
                    categorize(title, url, html, categories)
        js.close()
    # csvf.close()
    
    with open('categories.json', "w") as js_cat:
        json.dump(categories, js_cat, indent=6)
        js_cat.close()
    
    print(categories)

if __name__ == "__main__":
    main()
