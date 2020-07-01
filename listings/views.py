from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_dj, logout
from listings.models import Listing, Sale
from accounts.models import MyUser
from . import models
from . import forms
from django.http import HttpResponseRedirect
import stripe

# Create your views here.

# the list view for the app | | | | | | | | |
                          #  \/\/\/\/\/\/\/\/\/ 


def listings_listview(requests):
    listings_filtered = models.Listing.objects.filter(is_published=True, is_sold=False)
    context = {
        'listings': listings_filtered,
    }
    return render(requests, 'listings/listing_list.html', context)

# the detail view for the app | | | | | | | | |
                          #  \/\/\/\/\/\/\/\/\/ 

def listings_detailview(requests, list_id):
    listing = get_object_or_404(models.Listing, id=list_id)
    if listing.is_published == True:
        context = {
            'listing': listing,
        }
        return render(requests, 'listings/listing_detail.html', context)
    else:
        return render(requests, 'listings/listing_detail.html')
# the create view for the app | | | | | | | | |
                          #  \/\/\/\/\/\/\/\/\/ 

@login_required
def listings_createview(requests):
    if requests.method== 'POST':
        form = forms.create_listing(requests.POST, requests.FILES)
        form.seller_user=requests.user
        if form.is_valid():
            formm = form.save(commit=False)
            formm.seller_user=requests.user
            formm.save()
    else:
        form = forms.create_listing()
    return render(requests, 'listings/listing_create.html',{'form':form})


# the update view for the app | | | | | | | | |
                          #  \/\/\/\/\/\/\/\/\/ 
                        
@login_required
def listings_updateview(requests,list_id):
    obj = get_object_or_404(Listing, id=list_id)
    if requests.user==obj.seller_user:
        form = forms.create_listing(requests.POST or None, instance=obj)
        if form.is_valid(): 
            form.save() 
        context = {
            'forms':form
        }
        return render(requests, 'listings/listing_update.html',context)
    else:
        return render(requests, 'listings/listing_update.html')
@login_required
def listings_deleteview(requests, list_id):
    obj = get_object_or_404(Listing, id=list_id)
    if requests.user == obj.seller_user:
        if requests.method == 'POST':
            decision = requests.POST['decision']
            obj.delete()
            return HttpResponseRedirect("/listings")
        return render(requests, 'listings/listing_delete.html')
@login_required
def listings_buy(requests, list_id):
    # stripe payments
    # stripe private key 
    obj = get_object_or_404(Listing, id=list_id)
    print(requests.user.username)
    if obj.seller_user != requests.user:
        context = {'listing':obj}
        return render(requests, 'listings/listing_buy.html',context)
    elif obj.seller_user == requests.user:
        return render(requests, 'listings/listing_buy.html')
@login_required
def confirm_buy(requests, list_id):
    obj = get_object_or_404(Listing, id=list_id)
    
    stripe.api_key = "sk_test_51H05nvDAVogauJQRhh2BxE3LcdBv8Xwjs3HGUgX7s7CPDIuZ4Dptxg5NZfdVROJ10vT4WvLuO7Vc4AsUPdCN0ClR001dvdIa9f"
    if requests.method == 'POST':

            customer = stripe.Customer.create(
            email=requests.user.email,
            phone=requests.user.phone,
            source=requests.POST['stripeToken']
        )
            charge = stripe.Charge.create(customer=customer, amount=int(obj.price)*100, currency='inr', description=obj,)
    sales = Sale()
    sales.ListingAcc = obj
    sales.customer_user = requests.user
    sales.save()
    if sales:
        obj.is_sold = True
        obj.save()
    return redirect('dashboard')
