from django.contrib.auth.models import AbstractUser
from django.db import models

# python manage.py makemigrations
class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"
   
class Listing(models.Model):
    # list of categories which are key and value pair
    Category = [
    ('electronics', 'Electronics'),
    ('clothing', 'Clothing'),
    ('books', 'Books'),
    ('furniture', 'Furniture'),
    ('bathroom', 'Bathroom'),
    ('utensils', 'Utensils'),
    ('gadgets', 'Gadgets'),
    ('others', 'Others'),

    # ... add more categories as needed
]
# make item to be unique 

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    item = models.CharField(max_length=64)
    description = models.TextField()
    image_url    = models.URLField(blank=True,max_length= 1000, default='https://i.ibb.co/4pG5hBD/noimage.png')
    category = models.CharField(max_length=64, default="others", choices=Category)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} : {self.item} , bid price is {self.bid_amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    comment= models.TextField()
    comment_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} commented on {self.item} : {self.comment} "

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.item}: {self.user}"

class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")
    item = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="winner")
    last_bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} bought {self.item} at {self.last_bid}"