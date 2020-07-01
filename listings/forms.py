from django import forms
from listings.models import Listing
class create_listing(forms.ModelForm):
    class Meta():
        model = Listing
        fields = ['freefire_id','username','level', 'description', 'estimated_price','signed_up_with', 'account_email','account_password','photo_main','photo_1','photo_2','photo_3','photo_4','photo_5','photo_6','photo_7']