from django.contrib import admin
from django.urls import include, path
from . import views
from lot.views import View_Lot_Product,View_Lotform,Deletelot

urlpatterns = [
path("lot_product/<int:pk>", View_Lot_Product.as_view(), name="lot_product"),
path('Lotform/<int:product_id>/', View_Lotform.as_view(), name='Lotform'),  # แก้ไข URL pattern
path('deletelot/<int:pk>', Deletelot.as_view(), name='deletelot'),

]