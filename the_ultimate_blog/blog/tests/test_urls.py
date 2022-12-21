import pytest
from django.urls import reverse, resolve
from .Faker import ArticleFaker, CategoryFaker
pytestmark = pytest.mark.django_db

# setup our test factories


def test_home_page_reverse():
    assert reverse('blog_url:home') == '/'


def test_home_page_resolve():
    assert resolve('/').view_name == 'blog_url:home'


def test_tag_list_reverse():
    article = ArticleFaker()
    url = reverse('blog_url:tag_list', kwargs={'tag_slug': article.tags})
    assert url == f'/tag/{article.tags}/'


def test_tag_list_resolve():
    article = ArticleFaker()
    url = f'/tag/{article.tags}/'
    assert resolve(url).view_name == 'blog_url:tag_list'


def test_article_detail_reverse():
    article = ArticleFaker()
    url = reverse('blog_url:article_detail', kwargs={'slug': article.slug})
    assert url == f'/article/{article.slug}/'


def test_article_detail_resolve():
    article = ArticleFaker()
    url = f'/article/{article.slug}/'
    assert resolve(url).view_name == 'blog_url:article_detail'


def test_category_list_reverse():
    category = CategoryFaker()
    url = reverse('blog_url:category_list', kwargs={'category_slug': category.slug})
    assert url == f'/category/{category.slug}/'


def test_category_list_resolve():
    category = CategoryFaker()
    url = f'/category/{category.slug}/'
    assert resolve(url).view_name == 'blog_url:category_list'
