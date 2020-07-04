from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password,check_password

class formView(forms.Form):
    # password = forms.CharField(
    #     max_length = 20,
    #     label = "Password",
    #     widget= forms.TextInput(attrs={'class':"input"})
    # )
    def __init__(self,*args,**kwargs):
        self.flag = kwargs.pop('flag', None)
        print(self.flag)
        #print('hello')
        super(formView,self).__init__(*args,**kwargs)
        self.fields['password'].widget = forms.TextInput(attrs={'class':"input"})
        #self.fields['password'].label = "New Email Label"

    password = forms.CharField()
    # def __init__(self, *args, **kwargs):
    #     flag = kwargs.pop('flag', None)
    #     print(flag)
    #     password = kwargs.pop('hel',None)
        
    
    # username = forms.CharField(
    #     max_length = 20,
    #     label = "First name",
    #     widget= forms.TextInput(attrs={'class':"input"})
    # )
    def clean_password(self):
        data = self.cleaned_data.get('password')
        if self.flag == 1:
            print("raiseed")
            raise forms.ValidationError('Password is invalid')

        #return data