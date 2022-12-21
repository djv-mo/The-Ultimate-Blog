from django.contrib import admin
from django.urls import reverse
from django.db.models import Count
from django.utils.html import format_html, urlencode
from . import models

# Article admin model


@admin.register(models.Article)
class AtricleAdminModel(admin.ModelAdmin):
    list_display = ['title', 'category', 'views', 'image_view', 'published', 'tag_list']
    list_editable = ['published']
    list_per_page = 20
    list_filter = ['category', 'published', 'created', 'tags']
    search_fields = ['title']
    readonly_fields = ['views']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def image_view(self, obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))

# Category admin model


@admin.register(models.Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['name', 'articles_count']
    search_fields = ['name']

    @admin.display(ordering='articles_count')
    def articles_count(self, category):
        url = reverse('admin:blog_article_changelist') + '?' + \
            urlencode({'category__id': str(category.id)})
        return format_html('<a href="{}">{}</a>', url, category.articles_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            articles_count=Count('article')
        )
# Comments admin model


@admin.register(models.Comment)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['name', 'article', 'active']
    list_editable = ['active']
    list_per_page = 20
    list_filter = ['article', 'active', 'created']
    search_fields = ['article__title']
