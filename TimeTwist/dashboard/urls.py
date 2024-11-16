from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entry/', views.manage_entry, name='add_entry'),
    path('entry/<int:entry_id>/', views.manage_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('reply/<int:message_id>/', views.reply_message, name='reply_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]
