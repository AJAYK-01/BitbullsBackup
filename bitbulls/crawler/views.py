from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import searchForm
import os, json, glob
from .scrapper import main
import subprocess
from .parser import outputter
import re
from .search import search_call

def jsonreading(search_Term):
   #scriptdir = os.path.dirname(__file__)
   #jsondir = os.path.join(scriptdir, '../../categories.json')

    dictionary = search_call(search_Term)
    list2 = []
    k = 0
    for element in dictionary:
        for x in list2:
            if element['title'] == x['title']:
                k = 1
                break
        if k == 0:
            list2.append(element)
    #with open(jsondir, 'r') as f:
    #    dictionary.append(json.load(f))
    return list2

def index(request):
    """
        Renders home page
    """
    form = searchForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            Term = form.cleaned_data['search_Term']
            link_Term = "" 
            x = re.match(r'(?:http|https)://\w*\.onion', Term)
            if x:
                link_Term = Term
                print("going to data")
                subprocess.call(["python3", "crawler/scrapper.py", Term, '-d', '1'])
                print("data finished")
                try:
                    with open(Term.split('://')[1].replace('/','')+".json",'r') as f:
                        Json = json.load(f)
                        list2 = []
                        k = 0
                        for element in Json:
                            for x in list2:
                                if element['title'] == x['title']:
                                    k = 1
                                    break
                            if k == 0:
                                list2.append(element)
                    return render(request, 'crawler/resbase.html', {'search_Term': Term, 'dictionary': list2})
                except FileNotFoundError:
                    return render(request, 'crawler/index.html', {'form': form})

                # os.system('python crawler/scrapper.py http://wikikijoy3lk2anu.onion 1')
                # return render(request, 'crawler/resbase.html', {'link_Term': link_Term})
            else:
                search_Term = Term
                dictionary = jsonreading(search_Term)
                return render(request, 'crawler/resbase.html', {'search_Term': search_Term, 'dictionary': dictionary}) 
                
    else:
        return render(request, 'crawler/index.html', {'form': form})
