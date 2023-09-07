from django.shortcuts import render
from django.shortcuts import HttpResponse
from django import forms
from django.shortcuts import redirect
from django.urls import reverse

import random

from . import util
from markdown2 import Markdown
import markdownify

md = Markdown()




class SearchForm(forms.Form):
    searchbar = forms.CharField(label="Search Encyclopedia")

def index(request):

    entries = util.list_entries()
    random_entry = random.choice(entries)


    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            searchbar = form.cleaned_data["searchbar"]

            if searchbar in entries:
                raw_entry1 = util.get_entry(searchbar)
                entry1 = md.convert(raw_entry1)
                values = {
                'entry': entry1,
                'title': searchbar
                }
                return render(request, "encyclopedia/entry_template.html", values) 

            else:
                substring = searchbar.lower()
                new_entries=[]
                for x in entries:
                    if x.lower().find(substring) != -1:
                        new_entries.insert(1, x)

                values={
                    'entries': new_entries   
                }
                  
                return render(request, "encyclopedia/related_search.html", values)

        else:
            return render(request, "encyclopedia/index.html"),{
                "form": SearchForm(),
                "entries": util.list_entries(),
                "random_entry": random_entry 
            }

    return render(request, "encyclopedia/index.html", {
        "form": SearchForm(),
        "entries": util.list_entries(),
        "random_entry": random_entry
    })





def wiki_search(request, search):
    entry_titles = util.list_entries() 
    if search in entry_titles:
        raw_entry = util.get_entry(search)
        entry = md.convert(raw_entry)
        values = {
        'entry': entry,
        'title': search
        }
        return render(request, "encyclopedia/entry_template.html", values)
    else:
        values = {
        'search': search
        }
        return render(request, "encyclopedia/error_template.html", values)



class CreateEntry(forms.Form):
    titlebar = forms.CharField(widget = forms.Textarea(attrs={'title': 'New Entry Title', 'style': 'height:2em'}))
    textbar = forms.CharField(widget = forms.Textarea(attrs={'size':10, 'title': 'Text', 'style': 'height:40%'}))

def create_entry(request):

    if request.method == "POST":
        create_form = CreateEntry(request.POST)
        entries = util.list_entries()
        test_entries = util.list_entries()
        
        if create_form.is_valid():
            titlebar = create_form.cleaned_data["titlebar"]
            textbar = create_form.cleaned_data["textbar"]

            for i in range(len(test_entries)):
                test_entries[i] = entries[i].lower()

            if titlebar.lower() in test_entries:
                values={
                    'search': titlebar.capitalize()
                }
                return render(request, "encyclopedia/error_template2.html", values)

            elif (not titlebar) or (not textbar):
                return render(request,"encyclopedia/error_template2.html")
            
            else:
                util.save_entry(titlebar.capitalize(), textbar)

                raw_entry = util.get_entry(titlebar.capitalize())
                entry = md.convert(raw_entry)
                values = {
                    'title': titlebar.capitalize(),
                    'entry': entry
                }
                return render(request,"encyclopedia/entry_template.html",values)
    return render(request,"encyclopedia/create_entry.html", {
        "form": CreateEntry()
    })


class EditEntry(forms.Form):
    edittext = forms.CharField(widget = forms.Textarea(attrs={'size':10, 'style': 'height:60%'}))

def edit_entry(request, title):

    if request.method == "POST":
        create_form = CreateEntry(request.POST)
        editted_entry = EditEntry(request.POST)

        if editted_entry.is_valid():
            edittext = editted_entry.cleaned_data["edittext"]

            util.save_entry(title, edittext)

            values={
                'title':title,
                'entry':edittext
            }
            return render(request,"encyclopedia/entry_template.html", values)


    initial_text = util.get_entry(title)
    initial_text_md = md.convert(initial_text)

    edit_form = EditEntry()
    edit_form.fields["edittext"].initial = initial_text_md

    values={
        'title':title,
        'form':edit_form,
        'text':initial_text_md
    }
    return render(request,"encyclopedia/edit_entry.html", values)