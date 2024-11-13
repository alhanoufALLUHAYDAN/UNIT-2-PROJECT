from django.shortcuts import render, redirect, get_object_or_404
from .models import CommunityPost, CommunityComment
from .forms import CommunityPostForm, CommunityCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

def community_view(request):
    if request.user.is_authenticated and request.method == 'POST':
        post_form = CommunityPostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
            return redirect('community:community_view')
    else:
        post_form = CommunityPostForm()
    
    posts = CommunityPost.objects.all().order_by('-created_at')
    return render(request, 'community/community.html', {
        'post_form': post_form, 
        'posts': posts,
        'is_authenticated': request.user.is_authenticated
    })
@login_required
def add_post(request):
    if request.method == 'POST':
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
            return redirect('community:community_view')
    else:
        form = CommunityPostForm()
    return render(request, 'community/add_post.html', {'form': form})

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(CommunityPost, id=post_id)
    if request.method == 'POST':
        comment_form = CommunityCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.creator = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('community:community_view')
    else:
        comment_form = CommunityCommentForm()
    
    return render(request, 'community/add_comment.html', {'comment_form': comment_form, 'post': post})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('community:community_view')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'community/login.html')

def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('community:community_view')
        else:
            messages.error(request, "Registration failed. Please correct the errors and try again.")
    else:
        form = UserCreationForm()
    return render(request, 'community/register.html', {'form': form})
