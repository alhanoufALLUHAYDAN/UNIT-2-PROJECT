from django.shortcuts import render
from django.core.paginator import Paginator
from .models import TimeTwist


# Create your views here.

def time_twist_view(request):

    entries = TimeTwist.objects.all().order_by('-created_at')

    query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', '')

    if query:
        entries = entries.filter(title__icontains=query)
    if filter_type:
        entries = entries.filter(entry_type__iexact=filter_type)
    paginator = Paginator(entries, 2)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'twist/time_twist.html', {'page_obj': page_obj, 'query': query, 'filter_type': filter_type})




