from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.TextField(max_length=32)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="selling")
    description = models.TextField()
    starting_price = models.FloatField()
    is_active = models.BooleanField()
    category = models.CharField(max_length=16, blank=True)
    image_url = models.URLField(blank=True)
    date_time= models.DateTimeField(default=datetime.datetime(year=2022,month=1,day=1,hour=00,minute=00,second=0))
    watchers = models.ManyToManyField(User, blank=True,related_name="watch_list")
    
class Bid(models.Model):
    price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")

class AuctionComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    