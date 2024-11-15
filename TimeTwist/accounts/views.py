from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home_view')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'accounts/login.html')

class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            subject = "Verify Your Email Address"
            message = f"Welcome! Please verify your email by clicking this link: http://yourdomain.com/verify/{user.id}/"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, "Registration successful. Check your email to verify your account.")
            return redirect('main:home_view')
        else:
            messages.error(request, "Registration failed. Please correct the errors and try again.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})