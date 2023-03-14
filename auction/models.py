from time import time
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices
from mail.models import User


User


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='images')
    categories = Choices("Clothing/Footwear","Books","Electronics","Cosmetics","Toys","Home/Garden","Sport/Leisure", "Other")
    category = models.CharField(choices=categories, max_length=32)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="selling")
    active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watching")
    time = models.DateTimeField("Time listed", auto_now_add=True)

    def __str__(self):
        return f"{self.title} in {self.category}"


class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField("Bid time", auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid {self.amount}"


class Comment(models.Model):
    comment = models.TextField(blank=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_comments")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField("Comment time", auto_now_add=True)

    def __str__(self):
        return f'{self.commenter}: "{self.comment}"'
