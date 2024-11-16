from django.shortcuts import render , redirect
from main.forms import ContactForm
from django.contrib import messages


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


def contact(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to send a message.")
        return redirect('accounts:login')  

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect('main:home_view')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})

