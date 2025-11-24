from django.shortcuts import render,redirect,get_object_or_404
from django import views
from .models import *
from product.forms import *
from django.contrib import messages
from lot.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class Deletelot(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/login/"  
    permission_required = ['lot.delete_lot']
    
    def get(self, request,pk):
        lot = get_object_or_404(Lot, pk=pk)
        # การเก็บค่า id ของ product ก่อนลบ
        product_id = lot.product.id 
        lot.delete()
        
        return redirect(f"/lot_product/{product_id}") 
    
class View_Lot_Product(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/login/"  
    permission_required = ['lot.view_lot']
    
    def get(self, request, pk):
        lot_product_list = Lot.objects.filter(product_id=pk)
        product_id = pk  
        today = date.today() 
        context = {
            "lot_product": lot_product_list,
            "product_id": product_id,  
            "today" : today
        }
        return render(request, "lot_product.html", context)
        
        
        
class View_Lotform(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/login/"  
    permission_required = ['lot.add_lot']
    
    def get(self, request, product_id=None):  
        
        
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            # กำหนดค่า field product ใน form มีค่าเริ่มต้นเป็น product ที่มาจาก product_id
            form = Lotform()  
      
        context = {
            'form': form,
            'product_id': product_id,
            'product': product 
        }

        return render(request, "Lot_form.html", context)

    def post(self, request, product_id=None):  
        # print(product_id)
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            form = Lotform(request.POST)
            
        if form.is_valid():
            form.save()  
            return redirect('product')
            
        context = {
            'form': form,
            'product': product 
        }
        return render(request, "Lot_form.html", context)