from django import forms
from accounts.models import MyUser
class registration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = MyUser
        fields = ['email', 'username', 'phone']
    def check_pass(self):
        if self.password!=self.password_confirm:
            raise forms.ValidationError('Both Passwords must match!')
        return self.password