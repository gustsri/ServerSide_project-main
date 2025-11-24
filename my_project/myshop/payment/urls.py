from django.contrib import admin
from django.urls import include, path
from . import views
from .views import sale_detail
from payment.views import PaymentView , View_sales , CartView, ConfirmOrderView

urlpatterns = [
path('payment/', views.PaymentView.as_view(), name='payment'),
# path('remove_lot_quantity/', views.remove_lot_quantity, name='remove_lot_quantity'),
path('sale/<int:sale_id>/', views.sale_detail, name='sale_detail'),
path('view_sales/',  View_sales.as_view(), name='view_sales'),
path('cart/', views.CartView.as_view(), name='cart'),
path('confirm_order/', views.ConfirmOrderView.as_view(), name='confirm_order'),
]