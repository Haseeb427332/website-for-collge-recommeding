from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from users.models import user_data23 as User
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    last_name = forms.CharField(max_length=20,required=True)
    Phone_no = forms.CharField(max_length=10,min_length=10,required=True)
    class Meta:
        model = User
        fields = ('username','last_name','email','Phone_no', 'password1', 'password2')