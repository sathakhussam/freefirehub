from django.db import models
from accounts.models import MyUser
from django.core.validators import RegexValidator
import os
from datetime import datetime



# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)

# class MyModel(models.Model):
#     upload = models.FileField(upload_to=user_directory_path)
# Create your models here.
def get_upload_path(instance, filename):
	if not os.path.exists(f'{instance.seller_user}/{instance.username}/{filename}'):
		os.makedirs(f'{instance.seller_user}/{instance.username}/{filename}')
	return f'{instance.seller_user}/{instance.username}/{filename}'
class Listing(models.Model):
	
	seller_user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
	freefire_id = models.BigIntegerField(unique=True, validators=[])
	level = models.PositiveIntegerField(validators=[])
	username = models.CharField(unique=True, max_length=264)
	description = models.TextField()
	estimated_price = models.PositiveIntegerField()
	price = models.PositiveIntegerField(blank=True, null=True)

	is_published = models.BooleanField(default=False)
	is_sold = models.BooleanField(default=False)
	signed_up_with = models.CharField(max_length=264, choices=[('Facebook','Facebook'), ('Gmail','Gmail'), ('VK','VK')])
	account_email = models.CharField(unique=True,max_length=264,)
	account_password = models.CharField(max_length=264,)


	photo_main = models.ImageField(upload_to=get_upload_path,)
	photo_1 = models.ImageField(upload_to=get_upload_path, blank=True)
	photo_2 = models.ImageField(upload_to=get_upload_path, blank=True)
	photo_3 = models.ImageField(upload_to=get_upload_path, blank=True)
	photo_4 = models.ImageField(upload_to=get_upload_path, blank=True)
	photo_5 = models.ImageField(upload_to=get_upload_path, blank=True)
	photo_6 = models.ImageField(upload_to=get_upload_path, blank=True)
	photo_7 = models.ImageField(upload_to=get_upload_path, blank=True)
	posted_date = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return f"{self.freefire_id} ({self.estimated_price})"

		

class Sale(models.Model):
	ListingAcc = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
	customer_user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
	purchased_date = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return f'{self.ListingAcc} ({self.customer_user})'
		