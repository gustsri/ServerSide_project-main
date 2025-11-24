from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms

class updateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
        }
#เพราะว่าถ้าใช้ตัวปกติจะได้ เหมือนหน้า admin แล้วข้อมูลมันขาดไม่ได้