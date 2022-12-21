import pytest
from .Faker import ArticleFaker, CategoryFaker, CommentFaker

pytestmark = pytest.mark.django_db


def test___str__category():
    category = CategoryFaker()
    assert category.__str__() == category.name
    assert str(category) == category.name


def test___str__article():
    article = ArticleFaker()
    assert article.__str__() == article.title
    assert str(article) == article.title


def test___str__comment():
    comment = CommentFaker()
    assert comment.__str__() == comment.name
    assert str(comment) == comment.name


def test_get_absolute_url_article():
    article = ArticleFaker()
    url = article.get_absolute_url()
    assert url == f'/article/{article.slug}/'


def test_get_absolute_url_category():
    category = CategoryFaker()
    url = category.get_absolute_url()
    assert url == f'/category/{category.slug}/'
