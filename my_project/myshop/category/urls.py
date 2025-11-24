from django.contrib import admin
from django.urls import include, path
from category.views import View_category,CategoryCreateView,CategoryDeleteView


urlpatterns = [
path('category',View_category.as_view(), name= "category"),
path('create_category/',CategoryCreateView.as_view(), name= "create_category"),
path('delete/<int:pk>', CategoryDeleteView.as_view(), name="delete_category"),
]