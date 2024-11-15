from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  

app_name = 'accounts'

urlpatterns = [
    path('register/', views.custom_register, name='register'),  
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='custom_register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home_view'), name='logout'),
]
