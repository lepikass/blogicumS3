from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from django.http import Http404


def get_published_posts(category=None):
    posts = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    if category:
        posts = posts.filter(category=category)
    return posts.order_by('-pub_date')


def index(request):
    posts = get_published_posts()[:5]
    return render(request, 'blog/index.html', {'post_list': posts})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = get_published_posts(category=category)
    return render(
        request, 'blog/category.html',
        {
            'category': category,
            'post_list': post_list
        }
    )


def post_detail(request, pk):
    post = get_object_or_404(
        Post, pk=pk, is_published=True,
        pub_date__lte=timezone.now()
    )
    if not post.category.is_published:
        raise Http404
    return render(request, 'blog/detail.html', {'post': post})
