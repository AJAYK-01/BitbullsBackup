import sys
import json

def search(keyword, data):
    # result_row = {}
    results = []
    keyword = keyword.lower()

    for key, values in data.items():
        key = key.lower()
        #if search term in category name
        if key == keyword or keyword in key.split(' ') or key in keyword.split(' '):
            for value in values['links']:
                if value['url'] != "":
                    results.append(value)
            return results
        
        else:
            terms = values['terms']
            links = values['links']
            #if search term in 'terms' of any category
            if keyword in terms:
                for link in links:
                    if link['url'] != "":
                        results.append(link)
            #if search term in 'title' of any link within a category
            else:
                for link in links:
                    for word in link['title'].split(' '):
                        if word.lower() == keyword:
                            results.append(link)
    return results

def main(keyword):
    with open('data3.json', 'r') as data_json:
        data = json.load(data_json)

    results = search(keyword, data)
    print(results)

if __name__ == "__main__":
    main(sys.argv[-1])