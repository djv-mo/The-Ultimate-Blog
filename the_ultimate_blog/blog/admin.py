from django.contrib import admin
from .models import Category, Article, Comment

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
