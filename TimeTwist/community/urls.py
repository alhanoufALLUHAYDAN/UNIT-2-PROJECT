from django.urls import path
from . import views

app_name = 'community'  

urlpatterns = [
    path('', views.community_view, name='community_view'), 
    path('add_post/', views.add_post, name='add_post'), 
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('add_reply/<int:comment_id>/', views.add_reply, name='add_reply'), 
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]

