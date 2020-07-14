from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_dj, logout
from listings.models import Listing, Sale
from accounts.models import MyUser
from . import models
from . import forms
from django.http import HttpResponseRedirect, HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from PayTm import checksum
from random import randint
# email configurations
from django.core.mail import send_mail
from django.conf import settings
from pages.models import MailsToSend
# Create your views here.

# the list view for the app | | | | | | | | |
                          #  \/\/\/\/\/\/\/\/\/ 

MERCHANT_KEY = 'MvQ%sQ&NO05AgYWK'
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

    if requests.user == listing.seller_user:
        context = {
            'listing': listing,
            'owner':True
        }
        return render(requests, 'listings/listing_detail.html', context)
    elif listing.is_sold:
        obj = get_object_or_404(models.Sale, ListingAcc=listing)
        print(obj.customer_user)
        print(requests.user)
        if obj.customer_user == requests.user:
            context = {
                'listing': listing,
                'buyer': True
            }
            return render(requests, 'listings/listing_detail.html', context)
        return render(requests, 'listings/listing_detail.html')
    elif listing.is_published == True:
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
            allmails = MailsToSend.objects.all()
            recipient_list = []
            for mail in allmails:
                recipient_list.append(mail.email)
            subject = "There will be a new listing available sooner."
            message = f"Dear user, \n there will be a new listing available sooner for a price of {formm.price} and in level {formm.level}"
            email_from = settings.EMAIL_HOST_USER
            send_mail( subject, message, email_from, recipient_list )
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
        return render(requests, 'listings/listing_delete.html',{'list':obj})

        
@login_required
def listings_confirmdeleteview(requests, list_id):
    obj = get_object_or_404(Listing, id=list_id)
    if requests.user == obj.seller_user:
        obj.delete()   
        redirect(listings)
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
    # print(obj.price)
    order_id = randint(10000000000000000000000000000000000000000000000000,99999999999999999999999999999999999999999999999999)
    param_dict =  {
        'MID': 'icrDtJ34978828642501',
        'ORDER_ID': str(order_id),
        'TXN_AMOUNT': str(obj.price),
        'CUST_ID': requests.user.email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':f'http://127.0.0.1:8000/listings/handlerequests/{list_id}'
    }
    print(order_id)
    param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
    temp_storage = models.TempStorage(transaction_id=order_id,buyer=requests.user)
    temp_storage.save()
    return render(requests, 'listings/paytm.html', {'param_dict':param_dict})

# @login_required
@csrf_exempt
def handle_requests(requests,list_id):
        # paytm will send you post request here
    form = requests.POST
    # print(form)
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksums = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksums)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            temp_storage = get_object_or_404(models.TempStorage,transaction_id=form['ORDERID'])
            # print(temp_storage.buyer)
            login_dj(requests,temp_storage.buyer)
            obj = get_object_or_404(Listing, id=list_id)
            sale_process = Sale(transaction_id=form['ORDERID'],ListingAcc=obj,customer_user=temp_storage.buyer)
            sale_process.save()
            obj.is_sold=True
            obj.save()
            # to client 
            subject = 'Thanks For Buying In Our Website'
            message = f"Here's where you will find your newly bought account password and email.\n https://www.freefirehub.ga/listings/{obj.id} \n the account will be revisionised and secured for you"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [str(temp_storage.buyer.email),]
            send_mail( subject, message, email_from, recipient_list )
            # to buyer 
            subject = 'Your Account Has Been Sold Your Money Will Be Provided Soon'
            message = f"Your account has been bought just now and you will recieve your money as soon as your account is verified."
            email_from = settings.EMAIL_HOST_USER
            print(obj.seller_user.email)
            recipient_list = str(obj.seller_user.email)
            send_mail( subject, message, email_from, [str(obj.seller_user.email)] )
            # to me 
            subject = 'A new listings has been sold and you have recieved the payments'
            message = f"Secure the account and revision it for them \n ₹{obj.price} the price of this amount"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['sathakhussam@gmail.com',]
            send_mail( subject, message, email_from, recipient_list )
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(requests, 'listings/paymentstatus.html', {'response': response_dict})