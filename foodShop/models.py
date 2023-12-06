from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import User,auth
from django.utils import timezone


# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    logo_image=models.ImageField(upload_to="home/images", default="",null=True, blank=True)
    resturant_name=models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=254,null=True, blank=True)
    number_of_table=models.CharField(max_length=255, null=True, blank=True)
    food_list = models.JSONField(default=list)
    def __str__(self):
        return "%s" % (self.user)

class Food(models.Model):
    index=models.CharField(max_length=255, null=True, blank=True)
    food_title=models.CharField(max_length=255, null=True, blank=True)
    food_price=models.CharField(max_length=255, null=True, blank=True)
    category=models.CharField(max_length=255, null=True, blank=True)
    description=models.CharField(max_length=255, null=True, blank=True)
    food_image=models.ImageField(upload_to="home/images", default="",null=True, blank=True)
    def as_dict(self):
        return {
            'index':self.index,
            'food_title': self.food_title,
            'food_price': self.food_price,
            'category': self.category,
            'description': self.description,
            'food_image': self.food_image.url
        }







class Order(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    food_list=models.JSONField(default=list)
    table_no=models.CharField(max_length=255, null=True, blank=True)
    status=models.CharField(max_length=255, null=True, blank=True)
    customer_phone_number=models.CharField(max_length=255, null=True, blank=False)
    total=models.CharField(max_length=255, null=True, blank=False)
    created_at=models.DateTimeField(null=True) 

        