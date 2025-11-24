from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views import View
from django import views
from .models import *
from django.db.models import Count,Sum
from product.forms import *
from category.models import Category
from lot.models import Lot
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class AddProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"
    permission_required = ["product.add_product"]
    
    def get(self, request):
        form = ProductInfo()
        categories = Category.objects.all() 
        context = {
            "form": form,
            "categories":categories,
        }
        return render(request, "product_form.html", context)

    def post(self, request):
        
            form = ProductInfo(request.POST)
            if form.is_valid():
                product = form.save()
                # ใช้ name='categories' ใน HTML ดึงค่า list
                selected_categories = request.POST.getlist('categories')
                # print(selected_categories)
                product.categories.set(selected_categories) 
                
                return redirect('product')
            categories = Category.objects.all() 
            context = {
            "form": form,
            "categories": categories,
        }
            return render(request,"product_form.html", context)

class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = "/login/"
    permission_required = ["product.view_product"]
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        context = {
            "product": product,
        }
        return render(request, "product_detail.html", context)   
        

class View_Product(LoginRequiredMixin,View):
    login_url = "/login/"
    
    def get(self, request):
        today = date.today()
        totalproduct = Product.objects.count()

        lot_list = Lot.objects.values('product_id').annotate(total_quantity=Sum('quantity'))
        productlist = Product.objects.all()
    
        product_lot_count = [] 
        for product in productlist:
            lot_count = Lot.objects.filter(product_id=product.id,expiry_date__lt=today).count()
            product_lot_count.append({'product_id': product.id, 'lot_count': lot_count})  
        #     print(lot_count)
        # print(product_lot_count)

        
        category_id = request.GET.get('categoryid')
        # print(request.GET)
        
        # print(f"Category ID: {category_id}") 
        product_list = Product.objects.all()
        categorie = Category.objects.all()
        
        if category_id == "":
            return redirect('product')
        
        if category_id:
            try:                
                product_list = product_list.filter(categories__in=[category_id]) 
                totalproduct = product_list.count()
            except ValueError:
                
                product_list = Product.objects.none()

        context = {
            "products": product_list,
            "totalproduct": totalproduct,
            "lot_list": lot_list,
            "categories": categorie,
            "today" : today,
            "product_lot_count" : product_lot_count
        }
        return render(request, "product.html", context)

    
class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin,views.View):
    login_url = "/login/"
    permission_required = ["product.delete_product"]
    def get(self, request,pk):
        products = get_object_or_404(Product, pk=pk)
        products.delete()
        totalproduct = Product.objects.count()
        lot_list = Lot.objects.values('product_id').annotate(total_quantity=Sum('quantity'))
        productnew = Product.objects.all()
        context = {
            "products": productnew,
            "totalproduct": totalproduct,
            "lot_list": lot_list
        }
        return render(request, "product.html",context)
    


class ProductEditView(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = "/login/"
    permission_required = ["product.change_product"]
    
    def get(self, request, pk):
        print(pk)
        product = get_object_or_404(Product, pk=pk)
        form = ProductInfo(instance=product) 
        categories = Category.objects.all() 
        context = {
            "form": form,
            "product": product,
            "categories": categories,
            'product_id':pk
        }
        return render(request, "product_edit.html", context)
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductInfo(request.POST, instance=product)
        
        if form.is_valid():
            form.save()
            
            selected_categories = request.POST.getlist('categories') 
            product.categories.set(selected_categories) 

            return redirect('product_detail', pk=product.id) 
        
        categories = Category.objects.all()
        context = {
            "form": form,
            "product": product,
            "categories": categories
            
        }
        return render(request, "product_edit.html", context)
    
    