from django import forms
from django.db import models
from django.forms import ModelForm, ValidationError
from django.utils import timezone
from .models import *
from django.core.exceptions import ValidationError
from datetime import date

class ProductInfo(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = [
            "name",
            "price_at_sale",
            "unit",
            "description"
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple
        }
        
        