from django.shortcuts import render, get_object_or_404
from django_ratelimit.decorators import ratelimit

from blog.models import Post
from blog.form import CommentForm
from portfolio.utils import handle_form


def blog(request):
    posts = Post.published.all()
    return render(request, 'blog/blog.html', {'posts': posts})


@ratelimit(key='ip', rate='2/10m', method='POST', block=False)
def detail_post(request, slug):
    is_limited: bool = getattr(request, 'limited', False)
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        handle_form(
            request,
            form,
            is_limited,
            text_message='Thank you for your comment!',
            is_comment_form=True
        )
        comment.save()
    comments = post.comments.filter(parent=None)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'is_limited': is_limited,
    }
    return render(request, 'blog/post.html', context)