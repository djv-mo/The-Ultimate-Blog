from django.shortcuts import render, get_object_or_404
from .models import Comment, Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm


def index(request):
    articles = Article.publish.select_related('category')
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
    # List of active comments for this post
    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
        # Assign the current post to the comment
            new_comment.article = article
        # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'pages/detail.html',
                  {'article': article,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def category(request, slug):
    articles = Article.publish.select_related('category').filter(category__slug=slug)
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
            return render(request, 'pages/product-search.html', {"articles": results, 'search_title': query_name})

    return render(request, 'pages/product-search.html')
