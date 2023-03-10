from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
            .filter(published=True)\
            .select_related('category')\
            .prefetch_related('tags')


class Category(models.Model):
    name = models.CharField('Category name', max_length=100)
    slug = AutoSlugField("Category Address",
                         unique=True, always_update=False, populate_from="name")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('blog_url:category_list',
                       args=[self.slug])


class Article(TimeStampedModel):
    title = models.CharField("Article title", max_length=255)
    slug = AutoSlugField("Article Address",
                         unique=True, always_update=False, populate_from="title")
    description = RichTextField()
    image = models.ImageField(upload_to='static/images')
    published = models.BooleanField('Published', default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    views = models.IntegerField(default=0)
    tags = TaggableManager()
    objects = models.Manager()  # The default manager.
    publish = PublishedManager()  # Our custom manager

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('blog_url:article_detail',
                       args=[self.slug])


class Comment(TimeStampedModel):
    name = models.CharField("Name", max_length=255)
    email = models.EmailField('Email')
    comment = models.TextField('Comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('created',)
