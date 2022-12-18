from django.urls import path

from . import views
app_name = 'blog_url'
urlpatterns = [
    path('', views.index, name='home'),
    path('article/<slug:slug>', views.article_detail, name='article_detail'),

]
