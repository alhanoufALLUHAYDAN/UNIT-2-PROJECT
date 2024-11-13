from django.urls import path
from . import views

app_name = 'twist'

urlpatterns = [
    path('time/',views.time_twist_view, name='time_twist_view'),
]
