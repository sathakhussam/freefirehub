from django.shortcuts import render, redirect
from django.contrib.auth import login as login_dj, logout
from .models import MyUser,BaseUserManager
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from listings.models import Listing, Sale
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.



def login(requests):
	if requests.method == 'POST':
		email = requests.POST['email']
		password = requests.POST['password']
		user = authenticate(email=email, password=password)
		login_dj(requests,user=user)
		return redirect('dashboard')
	return render(requests, 'accounts/login.html')



def register(requests):
	print(requests.user)
	if requests.method == 'POST':
		email = requests.POST['email']
		number = requests.POST['phone-num']
		password1 = requests.POST['password-1']
		print(password1)
		password2 = requests.POST['password-2']
		listing = MyUser(email=email, phone=number)
		listing.set_password(raw_password=password1)
		listing.save()
	context = {}
	return render(requests, 'accounts/register.html')

@login_required	
def dashboard(requests):
	listings_userS = Listing.objects.filter(seller_user=requests.user)
	sales = Sale.objects.filter(customer_user=requests.user)
	context = {
		'listings': listings_userS,
		'sales':sales
	}
	return render(requests, 'accounts/dashboard.html', context)
@login_required
def Mylogout(requests):
	if user.is_authenticated():
		logout(requests)
	return redirect('home')
	
# I still have to make some changes to it and also add the logout view which redirects