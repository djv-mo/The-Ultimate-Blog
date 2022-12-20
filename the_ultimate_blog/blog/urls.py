from django.urls import path

from . import views
app_name = 'blog_url'
urlpatterns = [
    path('', views.index, name='home'),
    path('tag/<slug:tag_slug>/',
         views.index, name='tag_list'),
    path('category/<slug:category_slug>/',
         views.index, name='category_list'),
    path('search/', views.search_product, name='search'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    #     path('category/<slug:slug>/', views.category, name='category'),

]
