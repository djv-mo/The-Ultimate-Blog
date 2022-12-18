from django.shortcuts import render, get_object_or_404
from .models import Category, Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    categories = Category.objects.all()
    articles = Article.publish.select_related('category').order_by('-id')
    paginator = Paginator(articles, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context = {"categories": categories, 'articles': posts, 'page': page}
    return render(request, 'base.html', context)


def article_detail(request, slug):
    categories = Category.objects.all()
    article = get_object_or_404(Article, slug=slug,
                                published=True)
    return render(request,
                  'pages/detail.html',
                  {'article': article, "categories": categories})


def category(request, slug):
    categories = Category.objects.all()
    articles = Article.publish.filter(category__slug=slug)
    paginator = Paginator(articles, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'pages/category.html',
                  {'articles': posts, "categories": categories, 'page': page})
