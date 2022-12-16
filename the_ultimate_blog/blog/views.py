from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category


def index(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, 'base.html', context)
