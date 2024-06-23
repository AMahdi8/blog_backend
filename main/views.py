from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Post


def home(request):
    return HttpResponse("Hello, world!")


def last_posts(request):
    last_posts = Post.objects.order_by('-publish_date')[:5]
    output = ", \n".join([p.title for p in last_posts])
    return HttpResponse(output)


def categories(request):
    categories = Category.objects.all()
    output = ", ".join([c.title for c in categories])
    return HttpResponse(output)
