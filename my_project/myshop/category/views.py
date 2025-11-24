from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views import View
from django import views
from .models import *
from product.forms import *
from django.contrib import messages
from decimal import Decimal 
from category.models import Category
from category.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class View_category(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"
    permission_required = ["category.view_category"]
    def get(self, request):
        category_list = Category.objects.all()
        context = {
            "categorys": category_list,
        }
        return render(request, "category.html", context)

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"  # Redirect URL for login
    permission_required = ['category.add_category'] 
    def get(self, request):
        
        form = CategoryForm()
        return render(request, "create_category.html", {"form": form})
    
    def post(self, request):
        
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('category')
            
        return render(request,'category.html', {"form": form})
    
class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"  # Redirect URL for login
    permission_required = ['category.delete_category'] 
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category')
        
