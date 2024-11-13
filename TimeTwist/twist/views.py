from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator
from .models import TimeTwist


# Create your views here.

def time_twist_view(request):
    entries = TimeTwist.objects.all()  
    paginator = Paginator(entries, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'twist/time_twist.html', {'page_obj': page_obj})




