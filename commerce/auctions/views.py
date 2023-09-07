from multiprocessing import context
from queue import Empty
from sre_parse import CATEGORIES
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms
from .models import User, Auction, Comment, Buyer, Tag, Wishlist, AuctionWinner



def index(request):

    auctions = Auction.objects.all()

    for auction in auctions:
        
        try:
            Buyer.objects.filter(bid_item = auction).latest('bid')
        except:
            pass
        else:    
            bidder = Buyer.objects.filter(bid_item = auction).latest('bid')
            auction.latest_bid = bidder
            auction.save(update_fields=['latest_bid'])


    return render(request, "auctions/index.html",{
        "auctions":Auction.objects.all(),
        "buyer": Buyer.objects.all()
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


class CreateAuction(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['item','description','initial_bid','img','category']
        
        widgets =   {
                    'item' : forms.TextInput(),
                    'description': forms.TextInput(),
                    'initial_bid': forms.NumberInput(),
                    'category': forms.Select(choices=Tag.objects.all()),
                    'img': forms.URLInput()
                    }


def create(request):
    logged_user = request.user.username

    if logged_user:
        if request.method == 'POST':
            create_auction = CreateAuction(request.POST)
            
            if create_auction.is_valid():
                item = create_auction.cleaned_data['item']
                description = create_auction.cleaned_data['description']
                initial_bid = create_auction.cleaned_data['initial_bid']
                category = create_auction.cleaned_data['category']

                img = create_auction.cleaned_data['img']
                seller = request.user

                if not img:
                    no_img = "https://haes.ca/wp-content/plugins/everest-timeline/images/no-image-available.png"
                    Auction.objects.create(item=item, description=description, initial_bid=initial_bid, img=no_img, seller=seller, category=category)
                    
                    return render(request,"auctions/index.html",{
                    "auctions":Auction.objects.all(),
                    "buyer": Buyer.objects.all()
                    })

                Auction.objects.create(item=item, description=description, initial_bid=initial_bid, img=img, seller=seller, category=category)
                

                return render(request,"auctions/index.html",{
                    "auctions":Auction.objects.all(),
                    "buyer": Buyer.objects.all()
                    })

    else:
        return render(request,"auctions/login.html")
        
    return render(request,"auctions/create.html",{
        'form': CreateAuction()
    })


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_comment']
        widgets =   {'user_comment': forms.TextInput()}




def listing(request, id):
    
    logged_user_check = request.user.username

    if logged_user_check:

        auction = Auction.objects.get(pk=id)
        comments = Comment.objects.filter(commented_listing = auction)
        logged_user = request.user
        add_str = "Add to Wishlist"
        remove_str = "Remove from Wishlist"



        if auction.closed == True:
            
            last_bid = Buyer.objects.filter(bid_item = auction).latest('bid')
            latest_bid = last_bid.bid
        
            auction_closer = auction.seller
            winner = last_bid.latest_bidder
            price = latest_bid

            context={
            'auction':auction,
            'price':price,
            'auction_closer':auction_closer,
            'winner':winner,
            }
            return render(request,"auctions/winner.html", context)


        try:    
                Wishlist.objects.filter(wishlist_user = logged_user)
        except:
                button_str = add_str
        else:
                w1 = Wishlist.objects.filter(wishlist_user = logged_user)    
                try: 
                    w1.get(wishlist_items = auction)
                except:
                    button_str = add_str
                else:
                    button_str = remove_str



            
        try:
            Buyer.objects.filter(bid_item = auction).latest('bid')
        except:  
            latest_bid =auction.initial_bid
            context={
                'auction' : auction,
                'latest_bid' : latest_bid,
                'message' : "",
                'comments': comments,
                'form': CreateComment(),
                'button_str': button_str,
                'logged_user':logged_user
            }
        else:
            last_bid = Buyer.objects.filter(bid_item = auction).latest('bid')
            latest_bid = last_bid.bid
            comments = Comment.objects.filter(commented_listing = auction)

            context={
                'auction' : auction,
                'latest_bid' : latest_bid,
                'message' : "",
                'comments': comments,
                'form': CreateComment(),
                'button_str': button_str,
                'logged_user':logged_user
            }
        


        if request.method == 'POST' and 'button_submit1' in request.POST:
            create_comment = CreateComment(request.POST)
                
            if create_comment.is_valid():
                user_comment = create_comment.cleaned_data['user_comment']
                commenter = logged_user
                commented_listing = auction

                Comment.objects.create(user_comment=user_comment, commenter=commenter, commented_listing=commented_listing)
                comments2 = Comment.objects.filter(commented_listing = auction)
                

                context={
                    'auction' : auction,
                    'latest_bid' : latest_bid,
                    'message' : "",
                    'comments': comments2,
                    'form': CreateComment(),
                    'button_str': button_str,
                    'logged_user':logged_user
                    }
                return render(request,"auctions/listing.html", context)


        if request.method == 'POST' and 'button_submit2' in request.POST:
                
            str_check = add_str 
                
            if button_str == str_check :
                Wishlist.objects.create(wishlist_user = logged_user, wishlist_items = auction)

            else:       
                w1 = Wishlist.objects.filter(wishlist_user = logged_user)
                w2 = w1.get(wishlist_items = auction)
                w2.delete()

            context={
                'wishlists' : Wishlist.objects.filter(wishlist_user = logged_user)
            }
            return render(request,"auctions/wishlist.html", context)



        
        return render(request,"auctions/listing.html", context)
    
    else:
        return render(request,"auctions/login.html")



    
    

class Bidding(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['bid']

        widgets =   {'bid': forms.NumberInput()}


def bid(request,id):
    
    logged_user = request.user
    auction = Auction.objects.get(pk=id)
    add_str = "Add to Wishlist"
    remove_str = "Remove from Wishlist"


    try:    
        Wishlist.objects.filter(wishlist_user = logged_user)
    except:
        button_str = add_str
    else:
        w1 = Wishlist.objects.filter(wishlist_user = logged_user)    
        try: 
            w1.get(wishlist_items = auction)
        except:
            button_str = add_str
        else:
            button_str = remove_str



    
    
    try:
        last_bid = Buyer.objects.filter(bid_item = auction).latest('bid')
    except:
        latest_bid = auction.initial_bid
    else:
        last_bid = Buyer.objects.filter(bid_item = auction).latest('bid')
        latest_bid = last_bid.bid


    item = auction.item
    
    
    if request.method == 'POST':
        bidding = Bidding(request.POST)

        if bidding.is_valid():
            bid = bidding.cleaned_data['bid']

            if bid < latest_bid:
                message2 = "Error! Your bid was not greater than the latest bid ! Please try again."
                
                return render(request,"auctions/listing.html",{
                    'auction' : auction,
                    'message' : message2,
                    'form': CreateComment(),
                    'button_str': button_str
                })
            
            else:
                latest_bidder = logged_user
                bid_item = auction
                latest_bid2 = bid
                Buyer.objects.create(latest_bidder=latest_bidder, bid_item=bid_item, bid=bid)
                message = ""

                return render(request,"auctions/listing.html",{
                    'auction' : auction,
                    'latest_bid':latest_bid2,
                    'message' : message,
                    'form': CreateComment(),
                    'button_str': button_str
                })
   
            

    return render(request,"auctions/bid.html",{
        'form': Bidding(),
        'auction' : Auction.objects.get(pk=id),
        'item': item,
        'latest_bid': latest_bid,
    })


def wishlist(request):
    logged_user_check = request.user.username

    if logged_user_check:

        logged_user = request.user
        w1 = Wishlist.objects.all()
        wishlists = w1.filter(wishlist_user=logged_user)
        context={
            'wishlists':wishlists
        }
        return render(request,"auctions/wishlist.html", context)

    else:
        return render(request,"auctions/login.html")    


def winner(request,id):

    auction = Auction.objects.get(pk=id)

    closed_auction = auction
    auction_closer = request.user
    
    try:
        last_bid = Buyer.objects.filter(bid_item = auction).latest('bid')
    except:
        auction.closed = False
        auction.save(update_fields=['closed'])
    else:
        auction.closed = True
        auction.save(update_fields=['closed'])
        last_bid = Buyer.objects.filter(bid_item = auction).latest('bid')
        latest_bid = last_bid.bid
    
        auction_closer = auction.seller
        winner = last_bid.latest_bidder
        price = latest_bid

        context={
            'auction':auction,
            'price':price,
            'auction_closer':auction_closer,
            'winner':winner,
        }

        return render(request,"auctions/winner.html", context)

    return render(request,"auctions/error.html")


class SearchTag(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['category']
        
        widgets =   {
                    'category': forms.Select(choices=Tag.objects.all()),
                    }

def category(request):
    
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        form = SearchTag(request.POST)
        if form.is_valid():

            chosen_category = form.cleaned_data['category']
            auctions = Auction.objects.filter(category = chosen_category)
            
            context = {
                'auctions' : auctions
            }

            return render(request,"auctions/index.html", context)



    return render(request,"auctions/category.html", {
        'tags':tags,
        'auctions': Auction.objects.all(),
        'form':SearchTag()
    })
