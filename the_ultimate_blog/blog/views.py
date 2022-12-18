from django.shortcuts import render, get_object_or_404
from .models import Category, Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
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
    context = {'articles': posts, 'page': page}
    return render(request, 'base.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug,
                                published=True)
    article.views = article.views+1
    article.save()
    return render(request,
                  'pages/detail.html',
                  {'article': article})


def category(request, slug):
    articles = Article.publish.select_related('category').filter(category__slug=slug).order_by('-id')
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
                  {'articles': posts, 'page': page})


def search_product(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Article.publish.select_related('category').filter(title__icontains=query_name)
            return render(request, 'pages/product-search.html', {"articles": results})

    return render(request, 'pages/product-search.html')
