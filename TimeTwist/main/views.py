from django.shortcuts import render 

# Create your views here.

def home_view(request):

    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
        has_notifications = notifications.exists() 
        return render(request, 'main/home.html', {'has_notifications': has_notifications})
    else:
        has_notifications = False  
    
    return render(request, 'main/home.html', {'has_notifications': has_notifications})

def about_view(request):
    
    return render(request, 'main/about.html')



