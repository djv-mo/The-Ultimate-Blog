import datetime
from django.template.defaultfilters import slugify
import factory
import factory.fuzzy
from ..models import Article, Category, Comment


class CategoryFaker(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))

    class Meta:
        model = Category


class ArticleFaker(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    created = factory.LazyFunction(datetime.datetime.now)
    description = factory.Faker("sentence")
    published = factory.fuzzy.FuzzyChoice(choices=[True, True, True, False])
    image = factory.Faker("image_url")
    views = factory.fuzzy.FuzzyInteger(0, 420)
    category = factory.SubFactory(CategoryFaker)
    tags = None

    class Meta:
        model = Article


class CommentFaker(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    email = factory.Faker('email')
    comment = factory.Faker("sentence")
    article = factory.SubFactory(ArticleFaker)
    active = factory.fuzzy.FuzzyChoice(choices=[True, True, True, False])
    created = factory.LazyFunction(datetime.datetime.now)

    class Meta:
        model = Comment
