from django.shortcuts import render, redirect, get_object_or_404
from .models import CommunityPost, CommunityComment , Notification
from .forms import CommunityPostForm, CommunityCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
import re
from django.http import HttpResponseRedirect 
from django.urls import reverse

def community_view(request):
    post_form = CommunityPostForm()
    posts = CommunityPost.objects.all().order_by('-created_at')
    comment_form = CommunityCommentForm()
    if request.method == 'POST' and 'post_comment' in request.POST:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(CommunityPost, id=post_id)
        comment_form = CommunityCommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.creator = request.user
            new_comment.post = post
            new_comment.save()
        
        mention_usernames = re.findall(r'@(\w+)', new_comment.content)
        for username in mention_usernames:
                try:
                    mentioned_user = User.objects.get(username=username)
                    if mentioned_user != request.user:
                        Notification.objects.create(
                            recipient=mentioned_user,
                            comment=new_comment
                        )
                except User.DoesNotExist:
                    continue  

        return redirect('community:community_view')

    search_query = request.GET.get('search', '')
    if search_query:
        posts = CommunityPost.objects.filter(
            title__icontains=search_query) 
    else:
        posts = CommunityPost.objects.all().order_by('-created_at')
    
    posts_with_comments = []
    for post in posts:
        comments = post.comments.filter(reply_to__isnull=True)
        posts_with_comments.append({'post': post, 'comments': comments})
        
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

'''@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    
    if request.method == 'POST':
        # Adding a new comment
        if 'post_comment' in request.POST:
            comment_form = CommunityCommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.creator = request.user
                new_comment.post = post
                new_comment.save()

                # Handling mentions
                mention_usernames = re.findall(r'@(\w+)', new_comment.content)
                for username in mention_usernames:
                    try:
                        mentioned_user = User.objects.get(username=username)
                        if mentioned_user != request.user:
                            Notification.objects.create(
                                recipient=mentioned_user,
                                comment=new_comment
                            )
                    except User.DoesNotExist:
                        continue

                messages.success(request, "Your comment was posted successfully.")
            return redirect('community:community_view')

    return redirect('community:community_view')'''

@require_POST
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

            mention_usernames = re.findall(r'@(\w+)', new_comment.content)
            for username in mention_usernames:
                try:
                    mentioned_user = User.objects.get(username=username)
                    if mentioned_user != request.user:
                        Notification.objects.create(
                            recipient=mentioned_user,
                            comment=new_comment
                        )
                except User.DoesNotExist:
                    continue

            messages.success(request, "Your comment was posted successfully.")
        else:
            print("Form is not valid")  
            print(comment_form.errors)  
        return redirect('community:community_view')
    else:
        print("Request method is not POST")  
    
    return redirect('community:community_view')


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(CommunityComment, id=comment_id)
    if request.user != comment.creator:
        messages.error(request, "You are not allowed to delete this comment.")
        return redirect('community:community_view')
    
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('community:community_view')

@login_required
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(CommunityComment, id=comment_id)
    post = parent_comment.post
    
    if request.method == 'POST':
        reply_content = request.POST.get('content')
        if reply_content:
            reply = CommunityComment.objects.create(
                post=post,
                content=reply_content,
                creator=request.user,
                reply_to=parent_comment
            )
            Notification.objects.create(
                recipient=parent_comment.creator,
                comment=reply
            )
            messages.success(request, "Your reply was posted successfully.")
        else:
            messages.error(request, "Reply cannot be empty.")
        return redirect('community:community_view')
    
    return redirect('community:community_view')

    
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


@login_required
def notifications_view(request):
    notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
    return render(request, 'community/notifications.html', {'notifications': notifications})


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    comment_id = notification.comment.reply_to.id if notification.comment.reply_to else notification.comment.id
    return HttpResponseRedirect(reverse('community:community_view') + f'#comment-{comment_id}')



