from ..models import Category, Article, Comment
import pytest
pytestmark = pytest.mark.django_db


def test___str__category():
    category = Category.objects.create(
        name="food",
        slug="food")
    assert category.__str__() == "food"
    assert str(category) == "food"


def test___str__article():
    category = Category.objects.create(
        name="food",
        slug="food")

    article = Article.objects.create(
        title="World Cup",
        slug="World_Cup",
        published=True,
        category=category)
    assert article.__str__() == "World Cup"
    assert str(article) == "World Cup"


def test___str__comment():
    category = Category.objects.create(
        name="food",
        slug="food")

    article = Article.objects.create(
        title="World Cup",
        slug="World_Cup",
        published=True,
        category=category)

    comment = Comment.objects.create(
        name='john',
        email='john@example.com',
        comment='text',
        article=article
    )
    assert comment.__str__() == 'john in World Cup'
    assert str(comment) == "john in World Cup"
