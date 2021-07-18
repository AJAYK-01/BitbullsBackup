from django import forms

class searchForm(forms.Form):
    search_Term = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'search', 'placeholder':'Enter search term or link to crawl'}))
