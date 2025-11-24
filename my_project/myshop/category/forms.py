from django import forms
from django.db import models
from django.forms import ModelForm, ValidationError
from django.utils import timezone
from .models import *
from django.core.exceptions import ValidationError
from datetime import date

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = [
            "category_name",
        ]
        