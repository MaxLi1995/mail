from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

import random
import markdown2

from encyclopedia import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    details = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    details = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    content = util.get_entry(title)

    if content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "stuff": markdown2.markdown(content),
            "title": title
        })

def search(request):
    query = request.POST.get('q')
    content = util.get_entry(query)

    if content == None:
        filtered = list(filter(lambda x: query.lower() in x.lower(), util.list_entries()))

        if len(filtered) != 0:
            return render(request, "encyclopedia/search.html", {
                "stuff": filtered
            })
        else:
            return render(request, "encyclopedia/error.html")
    else:
        return HttpResponseRedirect("/wiki/" + query)

def create(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid() and util.get_entry(form.cleaned_data["title"]) is None:
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["details"])
            return HttpResponseRedirect("/wiki/" + form.cleaned_data["title"])
        else:
            messages.info(request, 'ERROR: page with same title already exists!')
            return HttpResponseRedirect("/create/")
        
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewTaskForm()
        })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data["details"])
            return HttpResponseRedirect("/wiki/" + title)
        else:
            messages.info(request, 'ERROR!')
            return HttpResponseRedirect("/wiki/" + title + "/edit")
        
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": EditForm({'details': util.get_entry(title)}),
            "title": title
        })

def lucky(request):
    list = util.list_entries()
    return HttpResponseRedirect("/wiki/" + random.choice(list))
