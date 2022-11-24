from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auctions.models import User, AuctionListing, Bid, AuctionComment

admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(AuctionComment)
# Register your models here.
