from django.db import models
from accounts.models import MyUser
from django.core.validators import RegexValidator
from datetime import datetime
# Create your models here.
class Listing(models.Model):
	seller_user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
	freefire_id = models.BigIntegerField(unique=True, validators=[RegexValidator(r'({1000000000,9999999999})')])
	level = models.PositiveIntegerField(validators=[RegexValidator(r'({0,81})')])
	username = models.CharField(unique=True, max_length=264)
	description = models.TextField()
	estimated_price = models.PositiveIntegerField()
	price = models.PositiveIntegerField(blank=True, null=True)
	
	is_published = models.BooleanField(default=False)
	is_sold = models.BooleanField(default=False)

	signed_up_with = models.CharField(max_length=264, choices=[('Facebook','Facebook'), ('Gmail','Gmail'), ('VK','VK')])
	account_email = models.CharField(unique=True,max_length=264,)
	account_password = models.CharField(max_length=264,)


	photo_main = models.ImageField(upload_to=f'images/{seller_user}/{username}/',)
	photo_1 = models.ImageField(upload_to=f'images/{seller_user}/{username}/', blank=True)
	photo_2 = models.ImageField(upload_to=f'images/{seller_user}/{username}/', blank=True)
	photo_3 = models.ImageField(upload_to=f'images/{seller_user}/{username}/', blank=True)
	photo_4 = models.ImageField(upload_to=f'images/{seller_user}/{username}/', blank=True)
	photo_5 = models.ImageField(upload_to=f'images/{seller_user}/{username}/', blank=True)
	photo_6 = models.ImageField(upload_to=f'images/{seller_user}/{username}/', blank=True)
	photo_7 = models.ImageField(upload_to=f'images/{seller_user}/{username}/', blank=True)
	posted_date = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return f"{self.freefire_id} ({self.estimated_price})"

class Sale(models.Model):
	ListingAcc = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
	customer_user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
	purchased_date = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return f'{self.ListingAcc} ({self.customer_user})'
		