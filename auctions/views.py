from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import datetime
from auctions.models import *

class BidForm(forms.Form):
    bid = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'name': 'bid'}))

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

class CreateForm(forms.Form):
    title = forms.CharField(max_length=32)
    description = forms.CharField(max_length=600)
    starting_price = forms.FloatField(min_value=0)
    category = forms.CharField(max_length=16,required=False)
    image_url = forms.URLField(required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "auctions":  AuctionListing.objects.all(),
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, id):
    return render(request, "auctions/listing.html", {
        "auction":  AuctionListing.objects.filter(pk=id).get,
        "bid_form": BidForm,
        "comment_form": CommentForm,
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            listing= AuctionListing( 
                title = form.cleaned_data["title"],
                seller = request.user,
                description = form.cleaned_data["description"],
                starting_price = form.cleaned_data["starting_price"],
                is_active = True,
                category = form.cleaned_data["category"],
                image_url = form.cleaned_data["image_url"],
                date_time = datetime.datetime.now(),
            )
            listing.save()
            return HttpResponseRedirect("/listing/"+ str(listing.pk))

    else:
        return render(request, "auctions/create.html", {
        "create_form": CreateForm
    })

def category(request):
    if request.method == "POST":
        pass
    else:
        all = AuctionListing.objects.all()
        categories = []
        for i in all:
            categories.append(i.category)
        
        return render(request, "auctions/category.html", {
        "categories":  list(set(categories))
        })

def entry(request, entry):
    return render(request, "auctions/categorylisting.html", {
        "auctions":  AuctionListing.objects.all(),
        "category": entry
    })

def bidding(request, id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid() and form.cleaned_data["bid"] > AuctionListing.objects.filter(pk=id).all()[0].bids.last().price :
            Bid(price=form.cleaned_data["bid"], bidder=request.user, listing=AuctionListing.objects.filter(pk=id).all()[0]).save()
            return HttpResponseRedirect("/listing/"+ str(id))
        else:
            return render(request, "auctions/listing.html", {
                "auction":  AuctionListing.objects.filter(pk=id).get,
                "bid_form": BidForm,
                "comment_form": CommentForm,
                "error": True
            })

def commenting(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            AuctionComment(comment=form.cleaned_data["comment"], user=request.user, auction_listing=AuctionListing.objects.filter(pk=id).all()[0]).save()
        return HttpResponseRedirect("/listing/"+ str(id))

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "auctions":  AuctionListing.objects.all(),
    })

def add_watchlist(request, id):
    if request.method == "POST":
        auction_listing=AuctionListing.objects.filter(pk=id).all()[0]
        if request.user in auction_listing.watchers.all():
            auction_listing.watchers.remove(request.user)
        else:
            auction_listing.watchers.add(request.user)
        auction_listing.save()
        return HttpResponseRedirect("/listing/"+ str(id))

def close_listing(request, id):
    if request.method == "POST":
        auction_listing=AuctionListing.objects.filter(pk=id).all()[0]
        auction_listing.is_active = False
        auction_listing.save()
        return HttpResponseRedirect("/listing/"+ str(id))
