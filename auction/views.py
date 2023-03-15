from os import lseek
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import Listing_Form, Bid_Form, Comment_Form
from .models import User, Listing, Bid, Comment
from datetime import datetime


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return HttpResponseRedirect(reverse("auctionindex"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctionindex"))


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
        return HttpResponseRedirect(reverse("auctionindex"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "POST":
        form = Listing_Form(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            image = form.cleaned_data.get("image")
            category = form.cleaned_data.get("category")
            price = form.cleaned_data.get("price")
            lister = form.cleaned_data.get("lister")
            obj = Listing.objects.create(
                title = title,
                description = description,
                image = image,
                category = category,
                price = price,
                lister = lister
            )
            obj.save()
            return HttpResponseRedirect(reverse("auctionindex"))
    else:
        form = Listing_Form()

    return render(request, "auctions/create.html", {
        "form": form
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def mine(request):
    return render(request, "auctions/mine.html", {
        "listings": Listing.objects.all()
    })


def watching(request):
    return render(request, "auctions/watching.html", {
        "listings": Listing.objects.all()
    })


def watch(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)
        item = Listing.objects.get(pk=int(request.POST["listing"]))
        item.watchers.add(user)
        return HttpResponseRedirect(reverse("watching"))


def unwatch(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)
        item = Listing.objects.get(pk=int(request.POST["listing"]))
        item.watchers.remove(user)
        return HttpResponseRedirect(reverse("watching"))


def bid(request):
    if request.method == "GET":
        form = Bid_Form()
        try:
            listing = Listing.objects.get(pk=int(request.GET["listing"]))
            return render(request, "auctions/bid.html", {
                "listing": listing,
                "form": form
            })
        except:
            return render(request, "auctions/bid.html", {
                "none": "Listing does not exist"
            })
    else:
        form = Bid_Form(request.POST)
        listing = Listing.objects.get(pk=int(request.POST["item"]))
        if form.is_valid():
            amount = form.cleaned_data.get("amount")
            bidder = form.cleaned_data.get("bidder")
            item = form.cleaned_data.get("item")
            if amount > listing.price:
                obj = Bid.objects.create(
                    amount = amount,
                    bidder = bidder,
                    item = item,
                )
                obj.save()
                listing.price = amount
                listing.save(update_fields=['price'])
                return render(request, "auctions/listing.html", {
                    "listing": listing
                })
            else:
                form = Bid_Form()
                listing = Listing.objects.get(pk=int(request.POST["item"]))
                return render(request, "auctions/bid.html", {
                    "listing": listing,
                    "form": form,
                    "message": "Bid must be higher than current price"
                })
        else:
            form = Bid_Form()
            listing = Listing.objects.get(pk=int(request.POST["item"]))
            return render(request, "auctions/bid.html", {
                "listing": listing,
                "form": form
            })


def comment(request):
    if request.method == "GET":
        form = Comment_Form()
        try:
            listing = Listing.objects.get(pk=int(request.GET["listing"]))
            return render(request, "auctions/comment.html", {
                "listing": listing,
                "form": form
            })
        except:
            return render(request, "auctions/comment.html", {
                "none": "Listing does not exist"
            })
    else:
        form = Comment_Form(request.POST)
        listing = Listing.objects.get(pk=int(request.POST["item"]))
        if form.is_valid():
            comment = form.cleaned_data.get("comment")
            commenter = form.cleaned_data.get("commenter")
            item = form.cleaned_data.get("item")

            obj = Comment.objects.create(
                comment = comment,
                commenter = commenter,
                item = item
            )
            return render(request, "auctions/listing.html", {
                "listing": listing
            })
        else:
            comment = Comment_Form()
            listing = Listing.objects.get(pk=int(request.POST["item"]))
            return render(request, "auctions/comment.html", {
                "listing": listing,
                "form": form
            })


def close(request):
    if request.method == "POST":
        item = Listing.objects.get(pk=int(request.POST["listing"]))
        item.active = False
        item.save(update_fields=['active'])
        return render(request, "auctions/close.html", {
            "listings": Listing.objects.all()
        })
    else:
        return render(request, "auctions/close.html", {
            "listings": Listing.objects.all()
        })


def category(request):
    if request.method == "POST":
        items = Listing.objects.all()
        category = request.POST["category"]
        matching = []
        for item in items:
            if item.category == category:
                matching.append(item)
        return render(request, "auctions/category.html", {
            "listings": matching,
            "category": category
        })