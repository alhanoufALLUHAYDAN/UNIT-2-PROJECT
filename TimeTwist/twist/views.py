from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator
from .models import TimeTwist


# Create your views here.

def time_twist_view(request):

    entries = TimeTwist.objects.all()  

    query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', '')

    if query:
        entries = entries.filter(title__icontains=query)
    if filter_type:
        entries = entries.filter(entry_type__iexact=filter_type)
    paginator = Paginator(entries, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'twist/time_twist.html', {'page_obj': page_obj, 'query': query, 'filter_type': filter_type})




