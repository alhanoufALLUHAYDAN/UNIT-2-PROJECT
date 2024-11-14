from django.shortcuts import render, redirect, get_object_or_404
from .models import CommunityPost, CommunityComment
from .forms import CommunityPostForm, CommunityCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LogoutView


def community_view(request):
    if request.method == 'POST' and 'post_comment' in request.POST:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(CommunityPost, id=post_id)
        comment_form = CommunityCommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.creator = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('community:community_view')

    
    post_form = CommunityPostForm()
    posts = CommunityPost.objects.all().order_by('-created_at')
    comment_form = CommunityCommentForm()

    return render(request, 'community/community.html', {
        'post_form': post_form,
        'posts': posts,
        'comment_form': comment_form,
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
        
        elif request.method == 'POST' and 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(CommunityComment, id=comment_id, post=post, creator=request.user)
            comment.delete()
            return redirect('community:community_view')
    return redirect('community:community_view')


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

class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
    
@login_required
@require_POST
def edit_post(request, post_id):

    if request.method == 'POST':
        post = get_object_or_404(CommunityPost, id=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('community:community_view')
    

    
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    if request.user != post.creator:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect('community:community_view')
    
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('community:community_view')


