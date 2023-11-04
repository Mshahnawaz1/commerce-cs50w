from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import Listing_form

def index(request):
    return render(request, "auctions/index.html",{
        "items" : Listing.objects.all()
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

@login_required(login_url="/login")
def create_listing(request):
    if request.method == 'POST':
        form = Listing_form(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse(index))
    else:
        form = Listing_form()
        return render(request, "auctions/create_listing.html", {'form': form})


def listing(request, item_id):
    item= Listing.objects.get(id = item_id) #use .filter when multiple items are in

    # checks if item is in watchlist
    try:
        item_in_watchlist = Watchlist.objects.filter(user=request.user, item=item).exists()
    except TypeError:
        item_in_watchlist = False

    # get the bidding info
    bid_item = Bid.objects.filter(item=item_id)
    current_bid = bid_item.aggregate(largest_bid=models.Max("bid_amount"))["largest_bid"]
    if current_bid is None:
        current_bid = item.starting_bid

    # get comments 
    comments = Comment.objects.filter(item=item_id)
    # check if winner
    winner = Winner.objects.filter(item=item)
    if winner is None:
        winner = False

    return render(request, "auctions/listing.html",{
        "item" : item,
        "item_in_watchlist" : item_in_watchlist,
        "current_bid" : current_bid,
        "comments" : comments,
        "winner" : winner
    })

@login_required(login_url="/login")
def watchlist(request):
    items =  Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html",{
        "items" : items
    })

@login_required(login_url="login/")
def add_watchlist(request, item_id):
    watchlist = Watchlist.objects.all()
    item= Listing.objects.get(id = item_id)

    try:
        newitem= Watchlist.objects.create(user=request.user, item=item)
        newitem.save()
    except IntegrityError:
        remo = Watchlist.objects.get(user=request.user, item=item)
        remo.delete()

    url = reverse('listing', args=[item_id])
    return HttpResponseRedirect(url)

@login_required(login_url="login/")
def bid(request):
    bid_amount = float(request.POST.get("bid_amount"))
    item= Listing.objects.get(id = request.GET.get("item_id"))
    bid_item = Bid.objects.filter(item=item) 

    # get the largest bid amount
    largest = bid_item.aggregate(largest_bid=models.Max('bid_amount'))["largest_bid"]
    try:
        largest = float(largest)
    except TypeError:
        largest = 0

    # validate if bid amount is greater than the previous bids 
    if ((bid_amount >= item.starting_bid and bid_amount > largest)):
        newbid = Bid.objects.create(user=request.user, item=item, bid_amount=bid_amount)
        newbid.save()
    else:
        return render(request, "auctions/error.html",{
            "error_message" : "Bid should be higher than previous bid"
        })
    url = reverse('listing', args=[request.GET.get("item_id")])
    return HttpResponseRedirect(url)

@login_required(login_url="login/")
def close_auction(request):
    item_id  = request.GET.get("item_id")
    item = Listing.objects.get(id=item_id)
    current_bid = request.GET.get("lar")
    winner = True
    if request.user == item.user:
        # add winner info to winner
        try:
            winner = Bid.objects.get(bid_amount=current_bid, item=item)
            winner = Winner.objects.create(user=winner.user, item=winner.item, last_bid=winner.bid_amount)
            winner.save()
        except:
            winner = Winner.objects.create(user=item.user, item=item, last_bid=item.starting_bid)
        item.sold = True
        item.save()

    context_data= {
        'item' : item,
        'current_bid' : current_bid,
        'winner' : winner
    }
    url = reverse('listing', args=[request.GET.get("item_id")])
    return HttpResponseRedirect(url,context_data)

def comment(request):
    comment = request.POST.get("comment")
    item= Listing.objects.get(id = request.GET.get("item_id"))

    newcomment = Comment.objects.create(user=request.user, comment=comment, item=item)
    newcomment.save()
    context_data= {
        'item' : item,
        # 'current_bid' : current_bid,
    }
    url = reverse('listing', args=[request.GET.get("item_id")])
    return HttpResponseRedirect(url,context_data)
    
def categories(request):
    items = Listing.objects.all()
    categories = []
    for item in items:
        if item.category.capitalize() not in categories:
            categories.append(item.category.capitalize())
    print(categories)

    return render(request, "auctions/category.html",{
        "categories" : categories,
    })

def category_items(request):
    category = request.GET.get("category").lower()
    print(category)
    items = Listing.objects.filter(category=category)
    print(items)
    return render(request, "auctions/category.html",{
        "items" : items
    })


def sold_items(request):
    items= Listing.objects.all()
    return render(request , "auctions/sold-items.html",{
        "items" : items
    })
    
# python manage.py runserver
# python manage.py runserver --verbosity 3 

    # categories = Listing.Category


    # sample ={}

    # for category, category_u in categories:
    #     for item in items:
    #         print(category, item.category)
    #         if (category == item.category) and (item.sold == False):
    #             if category in sample:
    #                 sample[category].append(item.id)
    #             else:
    #                 sample[category] = item.id
    # print(sample)