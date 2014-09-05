# -- coding:utf-8 --
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from huron.blog.models import Post, Category


def single(request, day, month, year, slug):
    queryset = Post.objects.get_published()
    post = get_object_or_404(queryset, slug=slug)
    #redirect if not correct url
    if (str(post.pub_date.month) != str(month)
            or str(post.pub_date.day) != str(day)
            or str(post.pub_date.year) != str(year)):
        return redirect(post)

    categories = Category.objects.order_by('title')

    other_posts = Post.objects.exclude(pk=post.pk).order_by('?')[:3]

    ctx = {'post': post, 'categories': categories, 'other_posts': other_posts}

    return render_to_response('blog/single.html',
                              context_instance=RequestContext(request, ctx))


def listing(request, page, category):
    if category is None:
        posts_list = Post.objects.get_published().order_by('-pub_date')
    else:
        posts_list = Post.objects.get_published()\
            .filter(categories__slug=category).order_by('-pub_date')
    paginator = Paginator(posts_list, 10)

    try:
        posts = paginator.page(page)
    except EmptyPage:
        if (category is None):
            return redirect('/blog/')
        else:
            return redirect('/blog/%s/' % category)

    categories = Category.objects.order_by('title')

    ctx = {"object_list": posts, "categories": categories}

    return render_to_response('blog/index.html',
                              context_instance=RequestContext(request, ctx))
