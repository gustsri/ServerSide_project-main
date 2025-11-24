from django.urls import path,include
from .views import LoginView, LogoutView,RegisterView,addrole,viewemp,Deletegroup,UpdateProfileView,ChangePasswordView


urlpatterns = [
    
    path('login/', LoginView.as_view(), name="login"),
    
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('addrole/<int:pk>', addrole.as_view(), name="addrole"),
    path('viewemp/', viewemp.as_view(), name="viewemp"),
    path('Deletegroup/<int:pk>/<int:gpk>', Deletegroup.as_view(), name="Deletegroup"),
    path('profile/', UpdateProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]