import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from .Faker import ArticleFaker, CategoryFaker
from ..views import index, article_detail
pytestmark = pytest.mark.django_db


@pytest.fixture
def article():
    return ArticleFaker()


def test_index_list_view(rf, article):
    # article = ArticleFaker()
    # Get the request
    request = rf.get(reverse("blog_url:home"))
    # Use the request to get the response
    response = index(request)
    # Test that the response is valid
    assertContains(response, article.title)


def test_tag_list_view(rf, article):
    # article = ArticleFaker()
    # Get the request
    request = rf.get(reverse("blog_url:tag_list", kwargs={'tag_slug': article.tags}))
    # Use the request to get the response
    response = index(request)
    # Test that the response is valid
    assertContains(response, article.title)


def test_category_list_view(rf, article):
    # article = ArticleFaker()
    category = CategoryFaker()
    # Get the request
    request = rf.get(reverse("blog_url:category_list", kwargs={'category_slug': category.slug}))
    # Use the request to get the response
    response = index(request)
    # Test that the response is valid
    assertContains(response, article.title)
    assertContains(response, category.name)


def test_article_detail_view(rf, article):
    # article = ArticleFaker()
    url = reverse('blog_url:article_detail',
                  kwargs={'slug': article.slug}
                  )
    request = rf.get(url)
    callable_obj = article_detail
    response = callable_obj(request, slug=article.slug)

    assertContains(response, article.title)
    assertContains(response, article.description)
    assertContains(response, article.category)


def test_search(client, article):
    # article = ArticleFaker()
    form_data = {
        'name': article.title
    }
    url = reverse('blog_url:search')
    response = client.post(url, form_data)

    assert response.status_code == 200

    assertContains(response, article.title)
