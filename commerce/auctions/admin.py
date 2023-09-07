from django.contrib import admin

from .models import User, Tag, Auction, Buyer, Comment, Wishlist
# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("seller", "item", "initial_bid", "latest_bid", "time_of_creation")

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Buyer)
admin.site.register(Comment)
admin.site.register(Wishlist)
