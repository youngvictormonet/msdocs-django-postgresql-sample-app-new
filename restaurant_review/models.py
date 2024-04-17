from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField('review date')

    def __str__(self):
        return f"{self.restaurant.name} ({self.review_date:%x})"

class Users(models.Model):
    twitter = models.CharField(max_length=250)
    email = models.EmailField()
    ordinals_address = models.CharField(max_length=250)
    points = models.IntegerField()
    ref_status = models.BooleanField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    tweet_link = models.CharField(max_length=250)
    wl = models.BooleanField()
    fcfs = models.BooleanField()