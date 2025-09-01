from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models import Max
from django import forms

from .models import User, Listing, Bid, Comment

class NewListing(forms.Form):
    CHOICES = [('', "-"), ('Fashion', "Fashion"), ('Toy', "Toy"), ('Electronics', "Electronics"), ('Music', "Music"), ('Books', "Books"), ('Home', "Home"), ('Beauty', "Beauty"), ('Outdoors', "Outdoors"), ('Movies & TV', "Movies & TV")]
    CHOICES.sort()
    category = forms.ChoiceField(label="Category", choices=CHOICES, widget=forms.Select(attrs={'class': "select"}))
    name = forms.CharField(label="Title", max_length=150, widget=forms.TextInput(attrs={'placeholder': "Your title here...", 'class': "title"}))
    description = forms.CharField(label="Description", max_length=2500, widget=forms.Textarea(attrs={'placeholder': "Your description here...", 'class': "textarea"}))
    price = forms.DecimalField(validators=[MinValueValidator(0)], label="Starting price", max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': "0.00 €", 'class': "username"}))
    image = forms.ImageField(required=False, label="Image", widget=forms.ClearableFileInput(attrs={'class': "picture"}))
    
class NewBid(forms.Form):
    bid = forms.DecimalField(validators=[MinValueValidator(0)], label="Your bid", max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': "0.00 €", 'class': "title"}))

class NewComment(forms.Form):
    title = forms.CharField(label="Title", max_length=254, widget=forms.TextInput(attrs={'placeholder': "Your title here...", 'class': "title"}))
    comment = forms.CharField(label="Comment", max_length=1500, widget=forms.Textarea(attrs={'placeholder': "Your comment here...", 'class': "textarea"}))

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if username and email and password:
            if password != confirmation:
                messages.error(request, "Passwords must match.")
                return render(request, "auctions/register.html")

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                messages.error(request, "Passwords must match.")          
                return render(request, "auctions/register.html")
            
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Credentials missing.")
            return render(request, "auctions/register.html")
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        form = NewListing(request.POST, request.FILES)
        if form.is_valid():
            new_listing = Listing(image=form.cleaned_data["image"],
                                  price=form.cleaned_data["price"],
                                  name=form.cleaned_data["name"],
                                  description=form.cleaned_data["description"],
                                  category=form.cleaned_data["category"],
                                  user=request.user)
            new_listing.save()
            return redirect('index')
        else:
            messages.error(request, "Form not valid!")
            return redirect("create")
    else:    
        return render(request, "auctions/create.html", {'form': NewListing()})
    
    
def item(request, id):
    item = get_object_or_404(Listing, pk=id)
    highest_bid = Bid.objects.filter(item=item).order_by('-bid').first()
    watching = publishing = False
    if request.user.is_authenticated:
        if request.user.watching.filter(pk=id):
            watching = True
        if request.user.publishing.filter(pk=id):
            publishing = True
    return render(request, "auctions/item.html", {'item': item,
                                                'form_bid': NewBid(),
                                                'form_comment': NewComment(),
                                                'highest_bid': highest_bid,
                                                'watching': watching,
                                                'publishing': publishing,
                                                'comments': item.comments.all()})

@login_required
def watchlist(request, item_id=None):
    if item_id != None and request.method == "POST":
        listing = get_object_or_404(Listing, pk=item_id)
        listing.watchlist.add(request.user)
        messages.success(request, "Item successfully added to watchlist.")
        return redirect('item', item_id)
    else:
        return render(request, "auctions/watchlist.html", {'listings': request.user.watching.all()})


@login_required
def delete(request, item_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=item_id)
        listing.watchlist.remove(request.user)
        messages.success(request, "Item successfully removed from watchlist.")
        return redirect('watchlist')
    else:
        return render(request, "auctions/watchlist.html", {'listings': request.user.watching.all()})


@login_required
def bid(request, item_id):
    if request.method == "POST":
        form = NewBid(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            listing = get_object_or_404(Listing, pk=item_id, status=True)
            listing.watchlist.add(request.user)
            if highest_bid := listing.bids.aggregate(Max('bid'))['bid__max']:
                if bid <= highest_bid:
                    messages.error(request, "Bid must be higher than the current highest bid.")
                    return redirect('item', item_id)
            else:
                if bid < listing.price:
                    messages.error(request, "Bid must be equal or higher than the initial price.")
                    return redirect('item', item_id)
            new_bid = Bid(user = request.user,
                          item = listing,
                          bid = bid)
            new_bid.save()
            return redirect('item', item_id)
        else:
            messages.error(request, "Bid not valid")
            return redirect('item', item_id)
    else:
        return redirect('item', item_id)


def close(request, item_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=item_id, status=True)
        listing.status = False
        listing.save()
        messages.success(request, "Auction for this item closed successfully")
        return redirect('item', item_id)
    else:
        return redirect('item', item_id)
    

def comment(request, item_id):
    if request.method == "POST":
        form = NewComment(request.POST)
        if form.is_valid():
            listing = get_object_or_404(Listing, pk=item_id, status=True)
            new_comment = Comment(title = form.cleaned_data["title"],
                                     comment = form.cleaned_data["comment"],
                                     user = request.user,
                                     item = listing)
            new_comment.save()
        return redirect('item', item_id)
    else:
        return redirect('item', item_id)
    
    
def list_categories(request):
    form = NewListing()
    return render(request, "auctions/list_categories.html", {'categories': form.fields["category"].choices[1:]})


def categories(request, category):
    categories = NewListing().fields["category"].choices
    if category not in [category[0] for category in categories]:
        raise Http404("Category not found")
    return render(request, "auctions/categories.html", {"items": Listing.objects.filter(category=category, status=True),
                                                        "category": category})