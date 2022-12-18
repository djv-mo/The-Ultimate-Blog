from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
            .filter(published=True)


class Category(models.Model):
    name = models.CharField('Category name', max_length=100)
    slug = AutoSlugField("Category Address",
                         unique=True, always_update=False, populate_from="name")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('blog_url:category',
                       args=[self.slug])


class Article(TimeStampedModel):
    title = models.CharField("Article title", max_length=255)
    slug = AutoSlugField("Article Address",
                         unique=True, always_update=False, populate_from="title")
    description = models.TextField("Description")
    image = models.ImageField(upload_to='static/images')
    published = models.BooleanField('Published', default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    objects = models.Manager()  # The default manager.
    publish = PublishedManager()  # Our custom manager

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blog_url:article_detail',
                       args=[self.slug])


class Comment(models.Model):
    name = models.CharField("Comment Author", max_length=255)
    email = models.EmailField('Comment Email')
    comment = models.TextField('Comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} in {self.article}'
