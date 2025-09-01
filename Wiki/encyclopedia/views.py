from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms

from random import randrange
from markdown2 import markdown

from . import util

class NewPageCreation(forms.Form):
    page = forms.CharField(label="Title", widget=forms.TextInput(attrs={ 'placeholder': "Your title here..."}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'placeholder': "Your Markdown text here..."}))
    

def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
    
def title(request, title=None):
    
    if request.method == "GET":
        return render(request, "encyclopedia/title.html", {
            "content": markdown(util.get_entry(title)),
            "title": title
        })
        
    elif request.method == "POST":
        title = request.POST.get("q")
        content = util.get_entry(title)
        if not content:
            entries = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
            if entries:
                return render(request, "encyclopedia/index.html", {
                    "entries": entries
                })      
        return render(request, "encyclopedia/title.html", {
            "content": markdown(content),
            "title": title
        })


def create(request):
    
    if request.method == "POST":
        form = NewPageCreation(request.POST)
        if form.is_valid():
            page = form.cleaned_data["page"]
            if request.session.get("edit", None) == page.lower():
                util.save_entry(page, form.cleaned_data["content"])
                request.session.pop("edit")
                return redirect('title', title=page)
            elif page.lower() in [item.lower() for item in util.list_entries()]:
                messages.error(request, 'An encyclopedia entry with this title already exists! You might want to edit it instead.')
                return render(request, "encyclopedia/create.html", {'form': NewPageCreation()})
            else:    
                util.save_entry(page, form.cleaned_data["content"])
                return redirect('title', title=page)
            
    elif request.method == "GET":
        if page := request.GET.get("page"):
            request.session["edit"] = page.lower()
            return render(request, "encyclopedia/create.html", {'form': NewPageCreation(initial={'page': page, 'content': util.get_entry(page)})})
        else:
            return render(request, "encyclopedia/create.html", {'form': NewPageCreation()})


def random(request):
    
    entries = util.list_entries()
    page = randrange(0, len(entries))
    return render(request, "encyclopedia/title.html", {
        "content": markdown(util.get_entry(entries[page])),
        "title": entries[page]
    })