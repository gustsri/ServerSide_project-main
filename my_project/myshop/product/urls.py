from django.contrib import admin
from django.urls import include, path
from product.views import AddProduct,View_Product,ProductDetailView,ProductEditView,DeleteProduct

urlpatterns = [
path('productform/', AddProduct.as_view(),name ='productform'),
path("", View_Product.as_view(), name="product"),
path('productdetail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
path('productedit/<int:pk>', ProductEditView.as_view(), name='product_edit'),
path('deleteproduct/<int:pk>', DeleteProduct.as_view(), name='deleteproduct'),
]