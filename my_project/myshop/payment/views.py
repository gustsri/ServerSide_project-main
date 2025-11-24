from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views import View
from django import views
from payment.models import *
from lot.models import *
from django.db.models import Count,Sum
from payment.forms import *
from django.db import transaction
from decimal import Decimal 
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")

def sale_detail(request, sale_id):
    
    sale = get_object_or_404(Sale, pk=sale_id)
    sale_items = sale.items.all()  # ใช้ related_name "items"
        
    for item in sale_items:
        item.total_price = item.quantity * item.price_at_sale
        
    context = {
        'sale': sale,
        'sale_items': sale_items
    }
    return render(request, 'sale_detail.html', context)

    
    
class View_sales(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"
    permission_required = ["payment.view_sale", "payment.view_saleitem"]
    
    def get(self, request):
        
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # แปลง string เป็น datetime object
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
        #  
        sales = Sale.objects.all()
        if start_date:
            sales = sales.filter(date__gte=start_date) 
        if end_date:
            sales = sales.filter(date__lte=end_date) 
            
        # คำนวณยอดรวม {'total_sale': Decimal('724.50')}
        grand_total = sales.aggregate(total_sale=Sum('total_price')) ['total_sale'] or Decimal('0.00')
        
        context = {
            "sales": sales,
            "grand_total": grand_total,
            "start_date": start_date_str,  
            "end_date": end_date_str,  
        }
        return render(request, "view_sales.html", context)
    
    
class PaymentView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"
    permission_required = ["payment.view_sale", "payment.view_saleitem"]       
           
    def get(self, request):
        products_with_stock = []
        products_expired_only = []
        products = Product.objects.all().prefetch_related('lots') # lot จาก related_name 
        # for product in products:
        #     for lot in product.lots.all(): 
        #         print(lot)
                
        if 'cart' not in request.session:  # เช็คค่าใน session data ว่ามี key 'cart' ไหม
            request.session['cart'] = {}

        for product in products:
            # แยก lots ที่หมดอายุ กับ ไม่หมด
            valid_lots = product.lots.filter(expiry_date__gte=timezone.now())
            expired_lots = product.lots.filter(expiry_date__lt=timezone.now())
           
            total_quantity = sum(lot.quantity for lot in valid_lots)

            if total_quantity > 0:
                # กำหนด .total_quantity เราเพิ่ม attribute นี้เข้าไปเองแบบ dynamic เพื่อเก็บค่า total_quantity ไว้ชั่วคราว เพื่อนำไปใช้แสดงผลใน template
                product.total_quantity = total_quantity
                # ดึงข้อมูล product ที่มี ID ตรงกับ product.id  แปลง product.id เป็น string ก่อน เพราะ key ใน dictionary request.session['cart'] เป็น string ถ้าไม่มี ส่ง {} แทน
                #  จะ return จำนวนสินค้าในตะกร้าของ product นั้นๆ หรือ 0 ถ้าสินค้าไม่อยู่ในตะกร้า
                product.cart_quantity = request.session['cart'].get(str(product.id), {}).get('quantity', 0)
                products_with_stock.append(product)
            
            # มีแต่ lot ที่หมดอายุแล้วเท่านั้น
            #  return True หากมี object อย่างน้อย 1 object และ return False
            elif expired_lots.exists() and not valid_lots.exists():
                product.total_quantity = 0
                product.expired_quantity = sum(lot.quantity for lot in expired_lots) # เอาไวแสดงจำนวนที่หมดอายุ ทำไปทำไมนะ
                products_expired_only.append(product)

        context = {
            'products': products_with_stock,
            'products_expired_only': products_expired_only,
            'cart': request.session['cart'],
        }
        
        return render(request, 'payment.html', context)


class CartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"
    permission_required = ["payment.view_sale", "payment.view_saleitem"]
    
    def get(self, request):
        cart_items = [] 
        total_price = Decimal(0)  

        if 'cart' in request.session:
            #  จะเป็น dictionary ที่มี product ID เป็น key และรายละเอียดสินค้าเป็น value
            #  "1": {"product_id": 1, "quantity": 2, "price": "10.00"}, มันเป็น nested dic
            for product_id_str, item_data in request.session['cart'].items():
                # print(request.session['cart'])
                # print(product_id_str)
                # print(item_data)
                product = get_object_or_404(Product, pk=int(product_id_str))
                quantity = item_data['quantity'] # ดึง quantity จาก cart
                price = Decimal(item_data['price']) # ดึง price และแปลงเป็น Decimal
                total = quantity * price 
                cart_items.append({
                    'product': product, 
                    'quantity': quantity, 
                    'price': price,
                    'total': total }) 
                total_price += quantity * price 

        context = {
            'cart_items': cart_items, 
            'total_price': total_price} 
        return render(request, 'cart.html', context)


    def post(self, request):

        if 'cart' not in request.session:
             request.session['cart'] = {}
        #  ทำให้ cart กลายเป็นตัวแปรที่ชี้ไปยัง dictionary เดียวกัน
        cart = request.session['cart']
        # request.POST บรรจุข้อมูลที่ user submit ผ่าน form ใน payment.html. key คือชื่อของ input field ใน form, และ value คือค่าที่ user กรอก
        for key, value in request.POST.items():  # วนลูปข้อมูลจาก POST request
            # input fields ใน form ที่ส่งข้อมูล product ID จะมีชื่อในรูปแบบ product_id_<product_id>
            # print(key)
            # product_id_1
            # quantity_1
            # product_id_2
            # quantity_2
            if key.startswith('product_id_'): # ถ้า key เริ่มต้นด้วย 'product_id_'
                product_id = (value) 
                quantity_key = f"quantity_{product_id}"  # สร้าง key สำหรับ quantity
                quantity = int(request.POST.get(quantity_key, 0)) # ดึง quantity จาก POST request

                if quantity > 0:  # ถ้า quantity มากกว่า 0 แสดงว่าuser ต้องการเพิ่มสินค้าลงในตะกร้า
                    product = get_object_or_404(Product, pk=product_id) # ดึง product object
                    cart[str(product_id)] = {
                        'product_id': product.id, 
                        'quantity': quantity, 
                        'price': str(product.price_at_sale)}  # อัพเดตหรือเพิ่มสินค้าใน cart
                    
                elif quantity == 0 and str(product_id) in cart:
                    del cart[str(product_id)] # ลบสินค้าออกจาก cart


        request.session['cart'] = cart # อัพเดต cart ใน session
        request.session.modified = True # บอก Django ให้บันทึก session
        
        return redirect('cart')  


class ConfirmOrderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/login/"
    permission_required = ["payment.view_sale", "payment.view_saleitem"]
    
    def post (self, request):
        if 'cart' not in request.session or not request.session['cart']:
            return redirect('payment')

        try:
            with transaction.atomic():
                # print("Cart:", request.session['cart'])  # Print cart contents
                
                sale = Sale.objects.create(total_price=0)
                total_price = Decimal(0)
                # print("Sale:", sale)
                
                for product_id_str, item_data in request.session['cart'].items():
                    product = Product.objects.get(pk=int(product_id_str))
                    quantity = item_data['quantity']
                    price = Decimal(item_data['price'])
                    
                    sale_item = SaleItem.objects.create(
                        sale=sale, 
                        product=product,
                        quantity=quantity, 
                        price_at_sale=price
                    )  
                    # print("SaleItem:", sale_item)
                    
                    total_price += quantity * price
                    
                    
                    #สำคัญ! เริ่มจากการหา โดย Filter lots ที่ยังไม่หมดอายุ *ก่อน* แล้วค่อย เรียงลำดับวันหมดอายุ
                    lots = product.lots.filter(expiry_date__gte=timezone.now()).order_by('expiry_date')
                    # remaining_quantity = quantity: เก็บ quantity ที่เหลือต้องลดจาก stock
                    remaining_quantity = quantity

                    for lot in lots:
                        # lot จะถูกกำหนดเป็น instance ของ Lot model โดยอัตโนมัติ Django ORM จัดการเรื่องนี้ให้เบื้องหลังให้
                        # ถ้า quantity ใน lot มากกว่าหรือเท่ากับ remaining_quantity, ลด stock ใน lot นั้น และ set remaining_quantity เป็น 0
                        if lot.quantity >= remaining_quantity:
                            lot.quantity -= remaining_quantity
                            lot.save()
                            remaining_quantity = 0
                            break
                        # แต่ว่าาาา  ถ้า quantity ใน lot น้อยกว่า remaining_quantity, ลด stock ใน lot นั้นให้หมด และอัพเดต remaining_quantity
                        else:
                            remaining_quantity -= lot.quantity
                            lot.quantity = 0 
                            lot.save()
                            
                    #  ทำเผิ่อไว้ กันปัญหา  Concurrency Issues, Data Inconsistency
                    if remaining_quantity > 0:
                        raise ValueError(f"Not enough stock for {product.name}")

                sale.total_price = total_price
                sale.save()
                del request.session['cart']

                # return redirect(reverse('sale_detail', kwargs={'sale_id': sale.id})) # The redirect
                return redirect(f'/sale/{sale.id}/')
            
        except ValueError as e:
            print("ValueError:", e) 
            return HttpResponse(str(e), status=400)
        except Exception as e:
            print("Exception:", e)
            return HttpResponse("An error occurred during order processing.", status=500)
