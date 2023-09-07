from distutils.command.upload import upload
from unicodedata import category

from datetime import datetime

default_time = datetime.now()

from django.contrib.auth.models import AbstractUser
from django.db import models

now = datetime.now()
mod_now = now.strftime("%m/%d/%Y, %H:%M:%S")

class User(AbstractUser):
    pass

class Tag(models.Model):
    categories = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.categories}"

class Comment(models.Model):
    commenter = models.ForeignKey('User', on_delete=models.CASCADE, related_name="Commenter")
    user_comment = models.TextField()
    time = models.CharField(max_length = 200, default = mod_now)
    commented_listing = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="auction_commented_on", blank=True, null=True)

    def __str__(self):
        return f"{self.commenter} commented on {self.commented_listing}"

class Buyer(models.Model):
    latest_bidder = models.ForeignKey('User', on_delete=models.CASCADE, related_name="bidder_name")
    bid = models.IntegerField()
    bid_item = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="item_bidded_on", blank=True, null=True)

    def __str__(self):
        return f"${self.bid} by {self.latest_bidder}"

class Auction(models.Model):

    item = models.CharField(max_length=64)
    description = models.TextField()
    initial_bid = models.IntegerField()

    img = models.URLField(blank=True, null=True)
    
    time_of_creation = models.DateTimeField(default=default_time)

    category = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="related_categories", blank=True, null=True)
    latest_bid = models.ForeignKey('Buyer', on_delete=models.CASCADE, related_name="last_bidder", blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioner_name")
    comments = models.ManyToManyField(Comment, blank=True, related_name="Comments")
    
    closed = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.item} starting at {self.initial_bid}"

class Wishlist(models.Model):
    
    wishlist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_user")
    wishlist_items = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="items_in_wishlist", blank=True, null=True)

    def __str__(self):
        return f"Wishlist for {self.wishlist_user}"

class AuctionWinner(models.Model):

    closed_auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_that_has_finished", blank=True, null=True)
    auction_closer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_holder")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_winner")
    price = models.IntegerField()

    def __str__(self):
        return f"{self.winner} won {self.auction_closer}"