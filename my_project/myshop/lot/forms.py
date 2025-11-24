from django import forms
from django.db import models
from django.forms import ModelForm, ValidationError
from django.utils import timezone
from .models import *
from django.core.exceptions import ValidationError
from datetime import date

class Lotform(forms.ModelForm):
    
    class Meta:
        model = Lot
        fields = [
            "product","import_date","expiry_date",
            "quantity","purchase_price",
        ]
        widgets = {
            'import_date': forms.DateInput(attrs={"type": "date", "format": "%Y-%m-%d"}),
            'expiry_date': forms.DateInput(attrs={"type": "date", "format": "%Y-%m-%d"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        import_date = cleaned_data.get("import_date")
        expiry_date = cleaned_data.get("expiry_date")

        if expiry_date and expiry_date <= date.today():
            raise ValidationError("Expiry date must be later than today.")
        
        if import_date and expiry_date and expiry_date <= import_date:
            raise ValidationError("Expiry date must be later than import date.")

        return cleaned_data