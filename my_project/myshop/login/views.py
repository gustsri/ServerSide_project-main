from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout, login,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from login.forms import updateUserForm

class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = updateUserForm(instance=request.user) 
        #print(request.user)
        return render(request, 'profile.html', {
            "user_form": user_form,
        })

    def post(self, request):
        user_form = updateUserForm(request.POST, instance=request.user) 
        if user_form.is_valid():
            user_form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  
        
        #messages.error(request, 'Please correct the error below.')
        return render(request, 'profile.html', {
            "user_form": user_form,
        })

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        password_form = PasswordChangeForm(request.user) 
        
        return render(request, 'changepass.html', {
            "password_form": password_form,
        })

    def post(self, request):
        password_form = PasswordChangeForm(request.user, request.POST)  
        if password_form.is_valid():
            user = password_form.save()
            
            update_session_auth_hash(request, user)  # ป้องกันไม่ให้ล็อกเอาท์ เก็บเป็นsession 
            messages.success(request, 'Password updated successfully!')
            return redirect('change_password') 
        
        return render(request, 'changepass.html', {
            "password_form": password_form,
        })

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #print("Registration successful!")
            return redirect('login') 
        return render(request, 'register.html', {"form": form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('product')  
        
        return render(request,'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class viewemp(View):
    def get(self, request):
        users = User.objects.all() 
        groups = Group.objects.all() 
        
        content = {
            "userall": users,  
            "groups": groups, 
        }
        return render(request, 'viewemp.html', content)
    
    
class addrole(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = "/login/"
    permission_required = ["auth.change_group"]
    def get(self, request,pk):
        users = get_object_or_404(User, pk=pk) 
        allgroup = Group.objects.all()  
        newgroups = users.groups.all()
        content = {
            "useruse": users,  
            "groups": newgroups,
            "allgroup": allgroup,
        }
        return render(request, 'addrole.html', content)
    
    def post(self, request, pk):
        group_id = request.POST.get('groupid')
        if group_id:  
            group = get_object_or_404(Group, pk=group_id)  
            user = get_object_or_404(User, pk=pk)  
            user.groups.add(group) 
            user.save()  
        return redirect('addrole', pk=pk)  

        
        

class Deletegroup(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = "/login/"
    permission_required = ["auth.delete_group"]
    def get(self, request, pk, gpk):
        users = get_object_or_404(User, pk=pk)
        group = get_object_or_404(Group, pk=gpk)

        
        if group in users.groups.all():
            users.groups.remove(group)  
        newgroups = users.groups.all()
        allgroup = Group.objects.all()
        content = {
            "useruse": users,  
            "groups": newgroups, 
            "allgroup" : allgroup,
        }
        
        return render(request, 'addrole.html', content)  

    