from django.urls import path

from . import views
app_name = 'blog_url'
urlpatterns = [
    path('', views.index, name='home'),
]
