from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'community'  

urlpatterns = [
    path('', views.community_view, name='community_view'), 
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
     path('add_post/', views.add_post, name='add_post'), 
]
