from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pages/index.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.parent = parent_obj
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'pages/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            return JsonResponse({'status': 'ok', 'likes_count': post.total_likes()})
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(title__icontains=query)
    return render(request, 'pages/search_results.html', {'results': results, 'query': query})

# --- Static Pages Views ---
def curriculum_view(request):
    return render(request, 'pages/curriculum.html')

def smart_tools_view(request):
    return render(request, 'pages/smart_tools.html')

def phone_security_view(request):
    return render(request, 'pages/phone_security.html')
