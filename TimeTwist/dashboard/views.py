from django.shortcuts import render, get_object_or_404, redirect
from twist.models import TimeTwist
from dashboard.forms import TimeTwistForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


def admin_only(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_only)
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('main/home.html') 
    entries = TimeTwist.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        entries = entries.filter(title__icontains=search_query)
    entry_type_filter = request.GET.get('entry_type', '')
    if entry_type_filter:
        entries = entries.filter(entry_type=entry_type_filter)
    return render(request, 'dashboard/dashboard.html', {'entries': entries})

def manage_entry(request, entry_id=None):
    entry = get_object_or_404(TimeTwist, id=entry_id) if entry_id else None
    if request.method == 'POST':
        form = TimeTwistForm(request.POST, instance=entry)
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

def delete_entry(request, entry_id):
    if request.method == "POST":
        entry = get_object_or_404(TimeTwist, id=entry_id)
        entry.delete()
        messages.success(request, "Entry has been successfully deleted.")
    return redirect('dashboard:dashboard')
