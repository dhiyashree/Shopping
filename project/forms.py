from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password'] 
 
class createorderform(ModelForm):
    class Meta:
        model=Order
        fields="_all_"
        exclude=['status']
 
class createproductform(ModelForm):
    class Meta:
        model=Product
        fields='_all_'
 
class createcustomerform(ModelForm):
    class Meta:
        model=Customer
        fields='_all_'
        exclude=['user']