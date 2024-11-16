from twist.models import TimeTwist
from dashboard.forms import TimeTwistForm 
from django.contrib import messages
from django.core.paginator import Paginator
from main.models import Message
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_only(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_only)
def dashboard(request):
    entries = TimeTwist.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        entries = entries.filter(title__icontains=search_query)
    entry_type_filter = request.GET.get('entry_type', '')
    if entry_type_filter:
        entries = entries.filter(entry_type=entry_type_filter)

    paginator = Paginator(entries, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    messages = Message.objects.all()
  
    
    return render(request,'dashboard/dashboard.html', {'page_obj': page_obj,'search_query': search_query,'entry_type_filter': entry_type_filter,'messages': messages})

@login_required
@user_passes_test(admin_only)
def manage_entry(request, entry_id=None):
    if entry_id:
        entry = get_object_or_404(TimeTwist, id=entry_id)
    else:
        entry = None
    
    if request.method == 'POST':
        form = TimeTwistForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            message = "Entry updated successfully." if entry else "Entry added successfully."
            messages.success(request, message)
            return redirect('dashboard:dashboard')
    else:
        form = TimeTwistForm(instance=entry)
    
    context = {
        'form': form,
        'is_edit': bool(entry),
    }
    return render(request, 'dashboard/manage_entry.html', context)

@login_required
@user_passes_test(admin_only)
def delete_entry(request, entry_id):
    if request.method == "POST":
        entry = get_object_or_404(TimeTwist, id=entry_id)
        entry.delete()
        messages.success(request, "Entry has been successfully deleted.")
    return redirect('dashboard:dashboard')

def reply_message(request, message_id):
    message = Message.objects.get(id=message_id)
    
    if request.method == 'POST':
        reply_content = request.POST.get('reply_content')
        
        if reply_content:
            message.reply_content = reply_content
            message.replied = True
            message.save()

            
            user = message.user  
            notifications = [
                {
                    'message': reply_content,
                    'sender': request.user.username,  
                    'date': message.created_at.strftime('%Y-%m-%d %H:%M')
                }
            ]

            return render(request, 'community/notifications.html', {'notifications': notifications})
    
    return render(request, 'dashboard/reply_message.html', {'message': message})

def delete_message(request, message_id):
   
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return redirect('dashboard:dashboard')