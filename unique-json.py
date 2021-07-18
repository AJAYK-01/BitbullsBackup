import json
import os

list1 = []
for filename in os.listdir(os.getcwd()+'/scraped/'):
    filename = 'scraped/'+filename

    if filename.split('.')[-1] == "json":
        print(filename)
        with open(filename) as name:
            list1.append(json.load(name))
unique_list = []
for x in list1:
    if x not in unique_list:
        unique_list.append(x)
with open('../sorted.json', 'w') as res:
    json.dump(unique_list, res, indent=6)
