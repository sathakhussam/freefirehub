from django.shortcuts import render, redirect
from django.contrib.auth import login as login_dj, logout
from .models import MyUser,BaseUserManager
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from listings.models import Listing, Sale
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import registration,loginform
# Create your views here.



def login(requests):
	form = loginform()
	if requests.method == 'POST':
		form = loginform(requests.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			login_dj(requests, user=user)
			return redirect('dashboard')
	
	return render(requests, 'accounts/login.html', {'form':form})



def register(requests):
	form = registration()
	if requests.method == 'POST':
		form = registration(requests.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.set_username(user.username)
			user.save()
	context = {'form':form}
	return render(requests, 'accounts/register.html',context)

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
	if requests.user.is_authenticated():
		logout(requests)
	return redirect('home')
	
# I still have to make some changes to it and also add the logout view which redirects