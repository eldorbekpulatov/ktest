from django import forms
from django.contrib.auth.models import User
from ad.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password']

class PowerSupplyForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(PowerSupplyForm,self).__init__(*args,**kwargs)
        self.fields["powerSupply"] = forms.ModelChoiceField(queryset=Product.objects.all(), 
                                                            widget=forms.RadioSelect())

class ModelTypeForm(forms.Form): 
    def __init__(self, *args,**kwargs):
        super(ModelTypeForm,self).__init__(*tuple([args[0]]),**kwargs)
        self.fields["modelTypeSelected"] = forms.ModelChoiceField( queryset=args[1].model_set.all(), 
                                                                    widget=forms.RadioSelect())

