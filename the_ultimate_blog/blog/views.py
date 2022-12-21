from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Category
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count


def index(request, tag_slug=None, category_slug=None):
    articles = Article.publish.all()
    # view of tags pages
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags__in=[tag])
    # view of Category pages
    category_view = None
    if category_slug:
        category_view = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category__slug=category_slug)

    paginator = Paginator(articles, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'articles': posts,
               'page': page,
               'tag': tag, 'category_view': category_view}
    return render(request, 'pages/index.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug,
                                published=True)
    # increase views with each request
    article.views = article.views+1
    article.save()
    # adding comments
    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    # similar Articles
    article_tags_ids = Article.tags.values_list('id', flat=True)
    similar_articles = Article.publish.filter(tags__in=article_tags_ids)\
        .exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-views')[:3]

    return render(request,
                  'pages/detail.html',
                  {'article': article,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_articles': similar_articles})


# def category(request, slug):
#     articles = Article.publish.select_related('category').filter(category__slug=slug)
#     paginator = Paginator(articles, 10)  # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'pages/category.html',
#                   {'articles': posts, 'page': page})


def search_product(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Article.publish.filter(title__icontains=query_name)
            return render(request, 'pages/product-search.html', {"articles": results, 'search_title': query_name})

    return render(request, 'pages/product-search.html')
